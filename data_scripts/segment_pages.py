from bs4 import BeautifulSoup
import re


path = "/trunk/shared/tcp/all/A50079.xml"

def seg_page(path="/trunk/shared/tcp/all/A50079.xml", result_path="result_seg.txt"):
    xml = BeautifulSoup(open(path).read())

    ### get rid of teiheader
    for a in xml.find_all('teiheader'):
        a.decompose()
    

    pattern = r'<pb[^>]*>'
    full_text = xml.prettify()
    # Find all matches
    matches = list(re.finditer(pattern, full_text))

    new_pages = []

    last_end = 0
    for match in matches:
        left, right = match.span()
        new_pages.append(full_text[last_end:left])
        last_end = right
    new_pages.append(full_text[last_end])

    with open(result_path, 'w') as wf:
        for idx, p in enumerate(new_pages):
            wf.write(f"\n\n=====>> {idx}\n")
            wf.write(p)
