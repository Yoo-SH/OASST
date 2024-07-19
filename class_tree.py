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
    4: 'create_date',  # string
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
    18: 'labels'  # sequence
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


# 각 파일에 대응되는 user_id 파싱 키 클래스
parsing_classkey_userid = {
    'naver_cafe': 'nick_name'
}

parsing_classkey_userid = {
    'naver_cafe': 'end_user_nick'
}

# 각 파일에 대응하는 secretComment 파싱 키 클래스
parsing_classKey_secretComment = {
    'naver_blog': 'u_cbox_delete_contents',
    'naver_cafe': uuid.uuid4(),
    'naver_kin': uuid.uuid4()


}

def extract_texts_from_html(html_content, html_selectors):
    """
    HTML 콘텐츠에서 특정 클래스 이름들을 만족하는 텍스트 추출

    Args:
        html_content (str): HTML 문자열
        html_selectors (list): CSS 셀렉터 문자열들의 리스트

    Returns:
        dict: 각 셀렉터별로 추출된 텍스트 리스트를 포함하는 딕셔너리
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    result = {}
    for selector in html_selectors:
        elements = soup.select(selector)
        if not elements:
            logging.debug(f"No elements found for selector: {selector}")
            result[selector] = ['None']
        else:
            texts = []
            for element in elements:
                # If the element has children, get text from the first child
                if element.findChild():
                    texts.append(element.findChild().get_text(strip=True))
                else:
                    texts.append(element.get_text(strip=True))
            result[selector] = texts
    return result



def extract_class_and_text_from_xml_tag(tag, tags_to_extract, html_selectors):
    """
    XML 태그에서 HTML 콘텐츠 추출 및 특정 클래스의 텍스트 추출

    Args:
        tag (_type_): XML 태그 요소
        tags_to_extract (list): 첫 번째 요소는 HTML 태그 이름, 나머지는 추출할 태그 이름들의 리스트
        html_selectors (list): CSS 셀렉터 문자열들의 리스트

    Returns:
        dict: 추출된 텍스트와 제목의 딕셔너리
    """
    html_tag = tags_to_extract[0]
    desired_tags = tags_to_extract[1:]

    texts = {}
    for desired_tag in desired_tags:
        texts[desired_tag] = tag.find(desired_tag).text if tag.find(desired_tag) is not None else 'No Content'

    html_content = tag.find(html_tag).text if tag.find(html_tag) is not None else ''
    if html_content:
        html_texts = extract_texts_from_html(html_content, html_selectors) 
        texts['html_texts'] = html_texts
    else:
        texts['html_texts'] = {'None': ['None']}
    
    return texts

def extract_texts_from_xml(root, tags_to_extract, html_selectors):
    """
    XML에서 HTML 콘텐츠 추출 및 특정 클래스의 텍스트 추출

    Args:
        root (_type_): XML 루트 요소
        tags_to_extract (list): 첫 번째 요소는 HTML 태그 이름, 나머지는 추출할 태그 이름들의 리스트
        html_selectors (list): CSS 셀렉터 문자열들의 리스트

    Returns:
        list: 추출된 텍스트와 제목의 딕셔너리 리스트
    """
    all_texts = []
    for tag in root.findall('.//item'):
        extracted_texts = extract_class_and_text_from_xml_tag(tag, tags_to_extract, html_selectors)
        all_texts.append(extracted_texts)
    return all_texts

def parse_xml_file(xml_file_path, tags_to_extract, html_selectors):
    """
    XML 파일을 파싱하고 특정 클래스의 텍스트를 추출

    Args:
        xml_file_path (str): XML 파일 경로
        tags_to_extract (list): 첫 번째 요소는 HTML 태그 이름, 나머지는 추출할 태그 이름들의 리스트
        html_selectors (list): CSS 셀렉터 문자열들의 리스트

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
    return extract_texts_from_xml(root, tags_to_extract, html_selectors)

 

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

    # 추출할 태그 및 클래스 지정
    tags_to_extract = ['comment_html', 'title', 'registered_date', 'detail_content']
    class_names_to_extract = [ None, 'comment_content', 'end_user_nick', 'nick_name']

    # 셀렉터 생성
    html_selectors = [f'.{cls}' for cls in class_names_to_extract]

    # 텍스트 추출
    extracted_texts = parse_xml_file(xml_file_path, tags_to_extract, html_selectors)

    # 추출된 태그와 클래스 텍스트 출력
    for item in extracted_texts:
        print("Title:", item.get('title'))
        print("Registered Date:", item.get('registered_date'))
        print("Detail Content:", item.get('detail_content'))
        
        print("HTML Texts:")
        html_texts = item.get('html_texts', {})
        for selector, texts in html_texts.items():
            print(f"  Selector: {selector}")
            if texts == ['None']:
                print("    No texts found")
            else:
                for text in texts:
                    print(f"    Text: {text}")
        
        print("-" * 40)
        
    

if __name__ == "__main__":
    main()
