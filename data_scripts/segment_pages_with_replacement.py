import os
from bs4 import BeautifulSoup
import re
from markdownify import markdownify as md

def seg_page(path, result_path=None):
    with open(path, 'r', encoding='utf-8') as file:
        xml = BeautifulSoup(file, "lxml")

    for a in xml.find_all('teiheader'):
        a.decompose()


    pattern = r'<pb[^>]*>'
    full_text = str(xml)#.prettify()
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
        
    new_pages.append(full_text[last_end])
    
    new_pages = new_pages[1:]
    
    if result_path:
        with open(result_path, 'w', encoding='utf-8') as wf:
            for idx, (name, p) in enumerate(zip(span_name, new_pages)):
                wf.write(f"\n\n=====>> {idx} {name}\n")
                markdown_content = md(p)
                markdown_content = re.sub(r'\n+', '\n', markdown_content)
                markdown_content = re.sub(r'(\d)\\\.', r'\1.', markdown_content)

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
