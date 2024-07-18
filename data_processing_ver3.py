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

# 각 파일에 대응되는 parent comment 파싱 키 클래스
parsing_classkey_nickName_parent = {
    'naver_cafe': 'reply_to'
}

parsing_classkey_userid = {
    'naver_cafe': 'nick_name'
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
    return ', '.join([f'.{cls}' for cls in classes])

def extract_texts_from_html(html_content, selectors):
    """
    HTML 콘텐츠에서 특정 클래스 이름들을 만족하는 텍스트 추출

    Args:
        html_content (str): HTML 문자열
        selectors (list): CSS 셀렉터 문자열들의 리스트

    Returns:
        dict: 각 셀렉터별로 추출된 텍스트 리스트를 포함하는 딕셔너리
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    result = {}
    for selector in selectors:
        elements = soup.select(selector)
        result[selector] = [element.get_text(strip=True) for element in elements]
    return result

def extract_texts_from_xml_item(item, html_tag, selectors, title_tag):
    """
    XML 아이템에서 HTML 콘텐츠 추출 및 특정 클래스의 텍스트 추출

    Args:
        item (_type_): XML 아이템 요소
        html_tag (str): HTML 태그 이름
        selectors (list): CSS 셀렉터 문자열들의 리스트
        title_tag (str): 제목 태그 이름

    Returns:
        dict: 추출된 텍스트와 제목의 딕셔너리
    """
    title = item.find(title_tag).text if item.find(title_tag) is not None else 'No Title'
    html_content = item.find(html_tag).text if item.find(html_tag) is not None else ''
    if html_content:
        texts = extract_texts_from_html(html_content, selectors)
        return {'title': title, 'texts': texts}
    else:
        return {'title': title, 'texts': {'None': ['None']}}

def extract_texts_from_xml(root, html_tag, selectors, title_tag):
    """
    XML에서 HTML 콘텐츠 추출 및 특정 클래스의 텍스트 추출

    Args:
        root (_type_): XML 루트 요소
        html_tag (str): HTML 태그 이름
        selectors (list): CSS 셀렉터 문자열들의 리스트
        title_tag (str): 제목 태그 이름

    Returns:
        list: 추출된 텍스트와 제목의 딕셔너리 리스트
    """
    all_texts = []
    for item in root.findall('.//item'):
        extracted_texts = extract_texts_from_xml_item(item, html_tag, selectors, title_tag)
        all_texts.append(extracted_texts)
    return all_texts

def parse_xml_file(xml_file_path, html_tag, selectors, title_tag):
    """
    XML 파일을 파싱하고 특정 클래스의 텍스트를 추출

    Args:
        xml_file_path (str): XML 파일 경로
        html_tag (str): HTML 태그 이름
        selectors (list): CSS 셀렉터 문자열들의 리스트
        title_tag (str): 제목 태그 이름

    Returns:
        list: 추출된 텍스트와 제목의 딕셔너리 리스트
    """
    # XML 파일 파싱
    try:
        tree = etree.parse(xml_file_path)
        root = tree.getroot()
    except Exception as e:
        logging.error(f"Error parsing XML file: {e}")
        return []

    # 텍스트 추출
    return extract_texts_from_xml(root, html_tag, selectors, title_tag)

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

    # 추출할 태그 및 클래스 지정
    html_tag_to_extract = 'comment_html'
    title_tag_to_extract = 'title'
    class_names_to_extract = ['comment_content', 'nick_name', 'reply']

    # 셀렉터 생성
    selectors = [f'.{cls}' for cls in class_names_to_extract]

    # 텍스트 추출
    extracted_texts = parse_xml_file(xml_file_path, html_tag_to_extract, selectors, title_tag_to_extract)

    # 결과 출력
    print(f"Extracted texts from <{html_tag_to_extract}>:")
    for item in extracted_texts:
        print(f"Title: {item['title']}")
        for selector, texts in item['texts'].items():
            for text in texts:
                print(f"{selector}: {text}")

if __name__ == "__main__":
    main()
