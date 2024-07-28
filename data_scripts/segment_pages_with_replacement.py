from bs4 import BeautifulSoup
import re
# from markdownify import markdownify as md

def seg_page(path, result_path="result_seg2.md"):
    # xml = BeautifulSoup(open(path).read(), 'lxml')
    with open(path, 'r', encoding='utf-8') as file:
        xml = file.read()

    pattern = r'<pb[^>]*>'
    full_text = str(xml)#.prettify()
    matches = list(re.finditer(pattern, full_text))

    new_pages = []
    last_end = 0
    span_name = []
        
    for i, match in enumerate(matches):
        left, right = match.span()
        span_name.append(full_text[left:right])
        new_pages.append(full_text[last_end:left])
        last_end = right
    new_pages.append(full_text[last_end:])
    new_pages = new_pages[1:]
    
    def replace_symbols(match):
        text = match.group()
        text = text.replace('•', '[L]')
        text = text.replace('〈◊〉', '[W]')
        text = text.replace('〈…〉', '[S]')
        return text
    
    def replace_headers(match):
        spaces = len(match.group(1))
        header_level = spaces // 3 - 3 
        if header_level < 0:
            print("Warning: header level is less than 0")
        return f"{'#' * header_level} "

    def replace_tags(content):
        # content = re.sub(r'<teiHeader>.*?</teiHeader>', '', content, flags=re.DOTALL)
        content = re.sub(r'<hi>(.*?)</hi>', r'**\1**', content)
        content = re.sub(r'<g(?!ap)([^>]*)>', r'[EOL]', content) # be careful with <gap> and <g>
        content = re.sub(r'(<desc>.*?<\/desc>)', replace_symbols, content)
        content = re.sub(r'<figure>(.*?)</figure>', r'fig:\1', content, flags=re.DOTALL)
        content = re.sub(r'<opener>(.*?)</opener>', r'```\1```', content, flags=re.DOTALL)
        content = re.sub(r'<seg[^>]*>', r'[DECI]', content) #decorInit
        
        # First, remove extra spaces inside the <head> tags
        content = re.sub(r'<head>(.*?)</head>', lambda m: "<head>" + re.sub(r'\s+', ' ', m.group(1).strip()) + "</head>", content, flags=re.DOTALL)
        # Then, replace spaces before <head> with appropriate number of #
        pattern = re.compile(r'^( *)(<head>)', re.MULTILINE)
        content = re.sub(pattern, replace_headers, content)
        
        
        
        # content = re.sub(r'<list>', '', content)
        # content = re.sub(r'</list>', '', content)
        # content = re.sub(r'<item>', '- ', content)
        # content = re.sub(r'</item>', '', content)
        
        content = re.sub(r'<.*?>', '', content)
        return content

    with open(result_path, 'w', encoding='utf-8') as wf:
        for idx, p in enumerate(new_pages):
            wf.write(f"\n\n=====>> {idx}\n")
            markdown_content = replace_tags(p)
            markdown_content = re.sub(r'\n+', '\n', markdown_content)
            markdown_content = re.sub(r'(\d)\\\.', r'\1.', markdown_content)
            wf.write(markdown_content)


# input_directory = "/trunk/shared/tcp/all"
# output_directory = "/trunk3/shared/tracytian/forced_alignment/tcp_with_replacement/"
# process_all_xml_files(input_directory, output_directory)

# Usage example
# seg_page("/Users/tracyqwerty/Desktop/forced_alignment/A32403.xml")
seg_page("/Users/tracyqwerty/Desktop/forced_alignment/A19336.xml")
# seg_page("/Users/tracyqwerty/Desktop/forced_alignment/A86849.xml")
# seg_page("/Users/tracyqwerty/Desktop/forced_alignment/N00260.xml")
