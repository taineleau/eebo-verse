from bs4 import BeautifulSoup
import json, re
from markdownify import markdownify as md
import os

def seg_page(path, result_path="result_seg.json"):
    xml = BeautifulSoup(open(path).read())

    for a in xml.find_all('teiheader'):
        a.decompose()

    pages = xml.find_all('pb')

    new_pages = []

    image_page_id = []
    for page in pages:
        image_page_id.append(page['ref'])
        
    pattern = r'<pb[^>]*>'
    full_text = str(xml)
    
    # Find all matches
    matches = list(re.finditer(pattern, full_text))

    new_pages = []
    last_end = 0
    span_name = []
        
    for match in matches:
        left, right = match.span()
        span_name.append(full_text[left:right])
        new_pages.append(full_text[last_end:left])
        last_end = right
        
    new_pages.append(full_text[last_end:])
    
    new_pages = new_pages[1:]
    
    clean_pages = []
    for p in new_pages:
        markdown_content = md(p)
        markdown_content = re.sub(r'\n+', '\n', markdown_content)
        markdown_content = re.sub(r'∣', "", markdown_content)
        markdown_content= re.sub(r'(?<=\d)\\\.', '.', markdown_content)
        markdown_content = markdown_content.strip("\n")
        clean_pages.append(markdown_content)

    json.dump((image_page_id, clean_pages), open(result_path, "w"))
    return clean_pages


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


new_pages = seg_page("/trunk/shared/tcp/all/A29574.xml")
