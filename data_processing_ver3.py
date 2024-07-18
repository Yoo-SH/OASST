import pandas as pd
from bs4 import BeautifulSoup
import logging
import os
import argparse
import platform
import requests
from lxml import etree

# Set up logging
logging.basicConfig(filename='parsing_link_test.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')



def extract_range_texts_in_item(item, start_tag, end_tag):
    """ 특정 범위의 요소 추출

    
    Args:
        item (_type_): _description_
        start_tag (_type_): _description_
        end_tag (_type_): _description_

    Returns:
        _type_: _description_
    """
    texts = []
    stack = [item]  # tag node들을 명시적으로 관리하기 위해 stack과 반복문을 이용하여 추출.
    start_found = False

    while stack:
        node = stack.pop()
        if node.tag == start_tag:
            start_found = True
        if start_found and node.text:
            texts.append(node.text.strip())
        if node.tag == end_tag:
            break
        stack.extend(reversed(node))

    return texts


   
def extract_texts_from_items(root, tag):
    """특정 태그의 텍스트 추출

    Args:
        root (_type_): _description_
        tag (_type_): _description_

    Returns:
        _type_: _description_
    """
    texts = []
    
    for item in root.findall('.//item'):
        for elem in item.findall(tag):
            if elem.text:
                texts.append(elem.text.strip())
            else:
                texts.append('None')
    return texts




def main():

    # XML 파일 파싱
    tree = etree.parse('xml/sample1.xml')
    root = tree.getroot()

    
# 추출할 태그
tag_to_extract = 'comment_html'

# 텍스트 추출
extracted_texts = extract_texts_from_items(root, tag_to_extract)

# 결과 출력
print(f"Extracted texts from <{tag_to_extract}>:")
for text in extracted_texts:
    print('comment_html:',text)     



    
if __name__ == "__main__":
    main()