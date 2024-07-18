import pandas as pd
from bs4 import BeautifulSoup
import logging
import uuid
import os
import argparse
import platform
import requests
from lxml import etree

# Set up logging
logging.basicConfig(filename='parsing_link_test.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# 상위 하위 계층을 구분하기 위한 클래스를 찾아야함.

# 각 column_filed 번호에 대응하는 값
column_filed = {
    1: 'message_id',  # string
    2: 'parent_id',  # string 
    3: 'user_id',  # string
    4: 'creadte_date',  # string
    5: 'text',  # string
    6: 'role',  # string
    7: 'lang',  # string
    8: 'review_count',  # int 
    9: 'review_result',  # bool
    10: 'deleted',  # bool
    11: 'rank',  # int
    12: 'synthetic',  # bool
    13: 'model_name',  # string
    14: 'detoxify',  # dict
    15: 'message_tree_id',  # string
    16: 'tree_state',  # string
    17: 'emojis',  # sequence
    18: 'lavels'  # sequence
}

# 각 파일에 대응하는 comment 파싱 키 클래스
parsing_classKey_comment = {
    'naver_blog': 'u_cbox_contents',
    'naver_cafe': 'comment_content',
    'naver_kin': 'answerDetail'
}

# 각 파일에 대응하는 secretComment 파싱 키 클래스
parsing_classKey_secretComment = {
    'naver_blog': 'u_cbox_delete_contents',
    'naver_cafe': uuid.uuid4(),
    'naver_kin': uuid.uuid4()
}

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
            
    return texts



# 특정 클래스의 텍스트 추출 함수
def extract_texts_from_html(html_content, class_name):
    soup = BeautifulSoup(html_content, 'html.parser')
    texts = [element.get_text(strip=True) for element in soup.find_all(class_=class_name)]
    return texts


# XML에서 HTML 콘텐츠 추출 및 특정 클래스의 텍스트 추출
def extract_texts_from_xml(root, html_tag, class_name, title_tag):
    all_texts = []
    
    for item in root.findall('.//item'):
        title = item.find(title_tag).text if item.find(title_tag) is not None else 'No Title'
        html_content = item.find(html_tag).text if item.find(html_tag) is not None else ''
        if html_content:
            texts = extract_texts_from_html(html_content, class_name)
            all_texts.append((title, texts))
        else:
            all_texts.append((title, ['None']))
    
    return all_texts




def main():
    # XML 파일 경로 설정
    xml_file_path = 'xml/sample.xml'
    
    # XML 파일 경로가 절대 경로인지 확인하고, 절대 경로로 변환
    if not os.path.isabs(xml_file_path):
        xml_file_path = os.path.abspath(xml_file_path)

    # XML 파일 존재 여부 확인
    if not os.path.exists(xml_file_path):
        logging.error(f"File not found: {xml_file_path}")
        return

    # XML 파일 파싱
    try:
        tree = etree.parse(xml_file_path)
        root = tree.getroot()
    except Exception as e:
        logging.error(f"Error parsing XML file: {e}")
        return

    # 추출할 태그 및 클래스 지정
    html_tag_to_extract = 'comment_html'
    class_to_extract = 'comment_content'
    title_tag_to_extract = 'title'

    # 텍스트 추출
    extracted_texts = extract_texts_from_xml(root, html_tag_to_extract, class_to_extract, title_tag_to_extract)

    # 결과 출력
    print(f"Extracted texts from <{html_tag_to_extract}>:")
    for title, texts in extracted_texts:
        print(f'Title: {title}')
        for text in texts:
            print('comment_html:', text)

if __name__ == "__main__":
    main()
