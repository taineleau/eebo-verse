from bs4 import BeautifulSoup
import re
# from markdownify import markdownify as md


def seg_page(path, result_path="result_seg2.md"):
    xml = BeautifulSoup(open(path).read(), 'lxml')

    # print(xml) # header is removed with hierarchy preserved

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

    def replace_tags(content):
        # print(content)
        # def replace_head_tag(match):
        #     tag = match.group(0)
        #     level = tag.count('n')
        #     print(level)
        #     content = match.group(1)
        #     return f'{"#" * level} {content}'

        # content = re.sub(r'<head>(.*?)</head>', replace_head_tag, content)
        content = re.sub(r'<hi>(.*?)</hi>', r'**\1**', content)
        content = re.sub(r'<g ref="char:EOLhyphen"/>',
                         r'- [EOLhyphen]', content)
        content = re.sub(r'<seg rend="decorInit">(.*?)</seg>',
                         r'[\1]', content)
        content = re.sub(r'<opener>(.*?)</opener>', r'```\1```', content)
        content = re.sub(r'<figure/>', r'figure', content)
        content = re.sub(r'<desc>〈◊〉</desc>', r'[unread]', content)
        content = re.sub(r'<desc>•…</desc>', r'[unread]', content)
        content = re.sub(r'<list>', '', content)
        content = re.sub(r'</list>', '', content)
        content = re.sub(r'<item>', '- ', content)
        content = re.sub(r'</item>', '', content)

        content = re.sub(r'<.*?>', '', content)
        return content

    with open(result_path, 'w', encoding='utf-8') as wf:
        for idx, p in enumerate(new_pages):
            wf.write(f"\n\n=====>> {idx}\n")
            markdown_content = replace_tags(p)
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

# input_directory = "/trunk/shared/tcp/all"
# output_directory = "/trunk3/shared/tracytian/forced_alignment/tcp_with_replacement/"
# process_all_xml_files(input_directory, output_directory)


# Usage example
# seg_page("/Users/tracyqwerty/Desktop/forced_alignment/A32403.xml")
seg_page("/Users/tracyqwerty/Desktop/forced_alignment/A19336.xml")
# seg_page("/Users/tracyqwerty/Desktop/forced_alignment/A19336.xml") # very very large. takes 3 mins+
# seg_page("/Users/tracyqwerty/Desktop/forced_alignment/N00260.xml")
