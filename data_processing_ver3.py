import pandas as pd
from bs4 import BeautifulSoup
import logging
import uuid
import os
from class_tree import *
from class_parsing import *
import argparse
import platform
import requests
from lxml import etree
import logging


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


# 각 파일에 대응하는 comment 파싱 키 클래스, 전체 comment를 파싱하는 class key , level2, level3의 comment를 parsing함 (with css selector)
parsing_classKey_comment = {
    'naver_blog': 'u_cbox_contents',
    'naver_cafe': 'ul[data-v-7db6cb9f].comment_list .comment_content',
    'naver_kin': 'answerDetail'
}

# 각 파일에 대응하는 child comment 파싱 키 클래스 , 전체 comment 중, level2 계층의 comment를 parsing함 (with css selector)
parsing_classkey_comment_level_2 = {
    'naver_cafe': 'li[data-v-49558ed9][data-v-7db6cb9f]:not(.reply) .comment_content' 
}

# 각 파일에 대응하는 child comment 파싱 키 클래스 , 전체 comment 중, level3 계층의 comment를 parsing함 (with css selector)
parsing_classkey_comment_level_3 = {
    'naver_cafe': 'li[data-v-49558ed9][data-v-7db6cb9f].reply .comment_content'
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
    html_selectors = [
        'ul[data-v-7db6cb9f].comment_list .comment_content',
        'li[data-v-49558ed9][data-v-7db6cb9f]:not(.reply) .comment_content',
        'li[data-v-49558ed9][data-v-7db6cb9f].reply .comment_content',
        '.date'  # 날짜 선택자를 추가합니다.
    ]


    extracted_texts = parse_and_extract_from_xml(xml_file_path, tags_to_extract, html_selectors)
    logging.info(f"Extracted texts: {extracted_texts}")

    tree = build_comment_tree(extracted_texts)
    print_comment_tree(tree)

    


    """ # 엑셀 파일로 저장할 데이터 프레임 생성
    data = []
    for tag in extracted_texts:
        for class_name, texts in tag['html_texts'].items():
            for text in texts:
                row = {
                    'message_id': str(uuid.uuid4()) if class_name == '.comment_content' else '',
                    'user_id': str(uuid.uuid4() ) if class_name== '.nick_name' else '',
                    'text': text if class_name == '.comment_content' else '',
                    'title': tag['title'],
                    'registered_date': tag['registered_date']
                }
                data.append(row)
    
    df = pd.DataFrame(data, columns=[column_filed[i] for i in [1, 3, 5, 4, 2]])
    df.to_excel('extracted_texts.xlsx', index=False)
    print("Data has been written to extracted_texts.xlsx")
 """

if __name__ == "__main__":
    main()
