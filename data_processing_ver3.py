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

# 각 파일에 대응하는 child comment 파싱 키 클래스
parsing_classkey_comment_child = {
    'naver_cafe': 'reply'
}

#각 파일에 대응되는 parent comment 파싱 키 클래스 , 클래스 상위 계층은 reply, comment, reply_to 순으로, reply_to는 부모 id만을 지정하는 text class임..
parsing_classkey_comment_parent = {
    'nvaer_cafe': 'reply_to'
}




# 각 파일에 대응하는 secretComment 파싱 키 클래스
parsing_classKey_secretComment = {
    'naver_blog': 'u_cbox_delete_contents',
    'naver_cafe': uuid.uuid4(),
    'naver_kin': uuid.uuid4()
}

def generate_css_selector(classes):
    """
    주어진 클래스 리스트를 만족하는 CSS 셀렉터를 생성합니다.

    Args:
        classes (list): 클래스 이름들의 리스트

    Returns:
        str: CSS 셀렉터 문자열
    """
    return ' '.join([f'.{cls}' for cls in classes])

def extract_range_texts_in_item(item, start_tag, end_tag):
    """
    특정 범위의 요소 추출

    Args:
        item (_type_): XML 요소
        start_tag (str): 시작 태그 이름
        end_tag (str): 종료 태그 이름

    Returns:
        list: 추출된 텍스트 리스트
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
    """
    특정 태그의 텍스트 추출

    Args:
        root (_type_): XML 루트 요소
        tag (str): 추출할 태그 이름

    Returns:
        list: 추출된 텍스트 리스트
    """
    texts = []
    
    for item in root.findall('.//item'):
        for elem in item.findall(tag):
            if elem.text:
                texts.append(elem.text.strip())
            
    return texts

def extract_texts_from_html(html_content, class_names):
    """
    HTML 콘텐츠에서 특정 클래스 이름들을 만족하는 텍스트 추출

    Args:
        html_content (str): HTML 문자열
        class_names (list): 클래스 이름들의 리스트

    Returns:
        list: 추출된 텍스트 리스트
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    selector = generate_css_selector(class_names)
    texts = [element.get_text(strip=True) for element in soup.select(selector)]
    return texts

def extract_texts_from_xml(root, html_tag, class_names, title_tag):
    """
    XML에서 HTML 콘텐츠 추출 및 특정 클래스의 텍스트 추출

    Args:
        root (_type_): XML 루트 요소
        html_tag (str): HTML 태그 이름
        class_names (list): 클래스 이름들의 리스트
        title_tag (str): 제목 태그 이름

    Returns:
        list: 추출된 텍스트와 제목의 튜플 리스트
    """
    all_texts = []
    
    for item in root.findall('.//item'):
        title = item.find(title_tag).text if item.find(title_tag) is not None else 'No Title'
        html_content = item.find(html_tag).text if item.find(html_tag) is not None else ''
        if html_content:
            texts = extract_texts_from_html(html_content, class_names)
            all_texts.append((title, texts))
        else:
            all_texts.append((title, ['None']))
    
    return all_texts

def main():
    """
    메인 함수로, XML 파일을 파싱하고 특정 클래스의 텍스트를 추출하여 출력합니다.
    """
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
    title_tag_to_extract = 'title'
    class_names_to_extract = ['reply', 'comment_content', 'reply_to' ]

    # 텍스트 추출
    extracted_texts = extract_texts_from_xml(root, html_tag_to_extract, class_names_to_extract, title_tag_to_extract)

    # 결과 출력
    print(f"Extracted texts from <{html_tag_to_extract}>:")
    for title, texts in extracted_texts:
        print(f'Title: {title}')
        for text in texts:
            print('comment_html:', text)

if __name__ == "__main__":
    main()
