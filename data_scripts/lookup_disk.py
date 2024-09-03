### author: Ashwin Muralidharan

import glob
import string
import os
# List of XML files
xml_files = glob.glob("./metadata/disk_xml/*.xml")
from bs4 import BeautifulSoup

eebo_ids = ['13572026', '12387746', '13672099', '15692452', '12033795', '12076039', '13352779', '13677265', '12185298', '13352824', '18182490', '13400411']
# Read the XML file
ids = []
for xml_file in xml_files:
    with open(xml_file, 'r', encoding='ISO-8859-1') as file:
        xml_content = file.read()
        # Parse the XML content with BeautifulSoup
        soup = BeautifulSoup(xml_content, 'xml')
        # Iterate over each REC entry in the XML
        for rec in soup.find_all('REC'):
            citation_id = rec.find('CITATION_ID').text
            image_id = rec.find('IMAGE_ID').text
            title = rec.find('TITLE').text
            if citation_id in eebo_ids:
                print(f"CITATION_ID: {citation_id}, IMAGE_ID: {image_id}, TITLE: {title}")
                ids.append((os.path.basename(xml_file), image_id))
                
print("Image IDs: " + str(ids))