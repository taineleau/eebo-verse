# %%
import os
import json
import difflib
import re
import statistics
from PIL import Image, ImageDraw

# Read the original text data
with open("/trunk/shared/data/eebo_data_train.jsonl", "r") as f:
    lines = f.readlines()

print("finished loading")

current_line = None
image_url_to_find = None
usable = 0

for line in lines:
    data = json.loads(line)
    image_url_to_find = data["image_url"]
    current_line = data

    # print(f"current file:{image_url_to_find}\n")
    ori_text = current_line["sentence"]
    base_image_url = os.path.splitext(current_line["image_url"])[
        0]  # Removes the file extension
    side = base_image_url.split('.')[:][-1]
    # Removes the last segment after the last dot
    base_image_url = '.'.join(base_image_url.split('.')[:-1])
    ocr_text_path = f"/trunk/shared/pair_data/{base_image_url}_t_text.json"
    ocr_text_with_box_path = f"/trunk/shared/pair_data/{base_image_url}_t_text_with_box.json"

    if os.path.exists(ocr_text_path):
        with open(ocr_text_path, "r") as f:
            data = json.load(f)
            # the structure is like: [left_words, right_words]
            if side == 'left':
                if len(data) >= 1:
                    ocr_text = data[0]
                else:
                    # print("invalid ocr_text")
                    continue
            else:
                if len(data) == 2:
                    ocr_text = data[1]
                else:
                    # print("invalid ocr_text")
                    continue
    else:
        # print("no ocr_text!")
        continue

    if os.path.exists(ocr_text_with_box_path):
        with open(ocr_text_with_box_path, "r") as f:
            data = json.load(f)
            # the sturcture is like: [[left_words], [left_boxes], [right_words], [right_boxes]]
            if side == 'left':
                if len(data) >= 2 and all(isinstance(sublist, list) for sublist in data):
                    ocr_text_with_box = data[0]
                else:
                    # print("invalid ocr_text_with_box")
                    continue
            else:
                if len(data) >= 4 and all(isinstance(sublist, list) for sublist in data):
                    ocr_text_with_box = data[2]
                else:
                    # print("invalid ocr_text_with_box")
                    continue
    else:
        # print("no ocr_text_with_box!")
        continue

    ori_words = ori_text.split()
    ocr_words = ocr_text_with_box[0]
    ocr_boxes = ocr_text_with_box[1]

    matcher = difflib.SequenceMatcher(None, ori_words, ocr_words)

    similarity_threshold = 0.5
    matched_segments = []
    for match in matcher.get_opcodes():
        tag, i1, i2, j1, j2 = match
        # print("Matched Original Text: ", ori_words[i1:i2])
        # print("Matched OCR Text: ", ocr_words[j1:j2])
        if tag == 'equal':
            matched_segments.extend([(ori_words[i], ocr_boxes[j])
                                    for i, j in zip(range(i1, i2), range(j1, j2))])
            # print("Equal Original Text: ", ori_words[i1:i2])
            # print("Equal OCR Text: ", ocr_words[j1:j2])
        elif tag == 'replace' or tag == 'delete':
            ori_text = ' '.join(ori_words[i1:i2])
            ocr_text = ' '.join(ocr_words[j1:j2])
            similarity = difflib.SequenceMatcher(
                None, ori_text, ocr_text).ratio()
            if similarity < similarity_threshold:
                # print(f"Dropped segment due to low similarity ({similarity:.2f}):")
                # print("Original Text: ", ori_text)
                # print("OCR Text: ", ocr_text)
                continue
            # Handle cases where ori_words or ocr_words are missing words
            if tag == 'replace':
                for i, j in zip(range(i1, i2), range(j1, j2)):
                    matched_segments.append((ori_words[i], ocr_boxes[j]))
                # print("Replace Original Text: ", ori_words[i1:i2])
                # print("Replace OCR Text: ", ocr_words[j1:j2])
            elif tag == 'delete':
                for i in range(i1, i2):
                    # If ori_words lack word, skip it, or append the word-box to the previous word
                    if matched_segments:
                        matched_segments[-1] = (matched_segments[-1][0] +
                                                ' ' + ori_words[i], matched_segments[-1][1])
                # print("Delete Original Text: ", ori_words[i1:i2])
                # print("Delete OCR Text: ", ocr_words[j1:j2])
            elif tag == 'insert':
                # scenario impossible
                # print("Insert Original Text: ", ori_words[i1:i2])
                # print("Insert OCR Text: ", ocr_words[j1:j2])
                for j in range(j1, j2):
                    # If ocr_words lack word, skip the word.
                    continue

    lines_with_boxes = []
    current_line = []
    current_boxes = []
    current_left, current_top, current_right, current_bottom = None, None, None, None

    for word, bbox in matched_segments:
        left, top, right, bottom = bbox
        if current_top is None:
            current_top = top
            current_bottom = bottom
            current_left = left
            current_right = right
        if top > current_bottom + 10 or left < current_right - 300:
            if len(current_line) > 0:
                lines_with_boxes.append((current_line, current_boxes))
            current_line = [word]
            current_boxes = [bbox]
            current_top, current_bottom = top, bottom
            current_left, current_right = left, right
        else:
            current_line.append(word)
            current_boxes.append(bbox)
            current_top = min(current_top, top)
            current_bottom = max(current_bottom, bottom)
            current_left = min(current_left, left)
            current_right = max(current_right, right)

    if current_line:
        lines_with_boxes.append((current_line, current_boxes))

    # record the boxes[0][0]s' medium and boxes[last][2]s' medium. left_mid, right_mid
    all_lefts = [line[1][0][0] for line in lines_with_boxes if line[1]]
    all_rights = [line[1][-1][2] for line in lines_with_boxes if line[1]]
    # Calculate the median for left and right bounds
    left_mid = statistics.median(all_lefts) if all_lefts else 0
    right_mid = statistics.median(all_rights) if all_rights else 0

    lines_with_boundaries = []
    for line, boxes in lines_with_boxes:
        # Adjust the left boundary of the first box
        if boxes[0][0] < left_mid - 30:
            boxes[0][0] = left_mid
        # Adjust the right boundary of the last box
        if boxes[-1][2] > right_mid + 30:
            boxes[-1][2] = right_mid

        # Compute the bounding box of the whole line
        # left = min(box[0] for box in boxes)
        left = boxes[0][0]
        right = boxes[-1][2]
        top = min(box[1] for box in boxes)
        bottom = max(box[3] for box in boxes)

        if (bottom - top > 100):
            # discard them
            continue

        lines_with_boundaries.append((line, (left, top, right, bottom)))
        # print("Original Text Line:", ' '.join(line))
        # print("Line Bounding Box:", (left, top, right, bottom))

    # print(f"to draw:{image_url_to_find}\n")
    image_path = f"/trunk/shared/pair_data/{base_image_url}.tif"
    image = Image.open(image_path)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    draw = ImageDraw.Draw(image)

    json_lines = []
    for line, boundary in lines_with_boundaries:
        left, top, right, bottom = boundary
        if right < left or bottom < top:
            continue
        json_obj = {"line": line, "boundary": boundary}
        json_lines.append(json_obj)
        draw.rectangle([left, top, right, bottom], outline="red", width=2)

    output_directory = os.path.join(
        "/trunk3/shared/tracytian/forced_alignment/data/", base_image_url.split('/')[0])
    os.makedirs(output_directory, exist_ok=True)

    output_image_path = f"/trunk3/shared/tracytian/forced_alignment/data/{base_image_url}_{side}_with_boxes.jpg"
    original_width, original_height = image.size
    image = image.resize(
        (int(original_width/8), int(original_height/8)), Image.Resampling.LANCZOS)
    image.save(output_image_path)
    usable += 1
    print(f"Image saved to {output_image_path}")

    # folder = base_image_url.split('/')[0]
    with open(f'/trunk3/shared/tracytian/forced_alignment/data/{base_image_url}_{side}_lines_with_boundaries.jsonl', 'w') as file:
        for json_obj in json_lines:
            file.write(json.dumps(json_obj) + '\n')


print(f"usable files:{usable}\n")
