from bs4 import BeautifulSoup
import re
from markdownify import markdownify as md


def seg_page(path, result_path="result_seg.md"):
    xml = BeautifulSoup(open(path).read())

    for a in xml.find_all('teiheader'):
        a.decompose()

    pages = xml.find_all('pb')

    new_pages = []
    last_idx = 0

    xml_str = str(xml)

    for page in pages:
        current_idx = xml_str.find(str(page))
        if current_idx == -1:
            continue
        new_pages.append(xml_str[last_idx:current_idx])
        last_idx = current_idx + len(str(page))

    new_pages.append(xml_str[last_idx:])

    with open(result_path, 'w', encoding='utf-8') as wf:
        for idx, p in enumerate(new_pages):
            wf.write(f"\n\n=====>> {idx}\n")
            markdown_content = md(p)
            markdown_content = re.sub(r'\n+', '\n', markdown_content)
            wf.write(markdown_content)


def process_all_xml_files(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for file_name in os.listdir(input_dir):
        if file_name.endswith(".xml"):
            input_file_path = os.path.join(input_dir, file_name)
            output_file_path = os.path.join(
                output_dir, file_name.replace('.xml', '.md'))
            print(f"Processing {input_file_path} -> {output_file_path}")
            seg_page(input_file_path, output_file_path)


input_directory = "/trunk/shared/tcp/all"
output_directory = "/trunk3/shared/tracytian/forced_alignment/tcp"
process_all_xml_files(input_directory, output_directory)

# seg_page("/Users/tracyqwerty/Desktop/forced_alignment/A32403.xml")
# seg_page("/Users/tracyqwerty/Desktop/forced_alignment/A19336.xml") # very very large. takes 3 mins+
# seg_page("/Users/tracyqwerty/Desktop/forced_alignment/N00260.xml")
