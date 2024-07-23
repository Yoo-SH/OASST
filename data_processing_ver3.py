import pandas as pd
from bs4 import BeautifulSoup
import logging
import uuid
import os
import argparse
import platform
import requests
from lxml import etree
import logging

from class_tree import *
from class_parsing_and_extract import *


# Set up logging
logging.basicConfig(filename='parsing_link_test.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# 각 column_filed 번호에 대응하는 값
column_filed = {
    1: 'message_id',  # string
    2: 'parent_id',  # string 
    3: 'user_id',  # string
    4: 'creadte_date', #string
    5: 'title', #stirng
    6: 'text',  # string
    7: '사용여부',  # string
    8: 'role',  # string
    9: 'lang',  # string
    10: 'review_count',  # int 
    11: 'review_result',  # bool
    12: 'deleted',  # bool
    13: 'rank',  # int
    14: 'synthetic',  # bool
    15: 'model_name',  # string
    16: 'detoxify',  # dict
    17: 'message_tree_id',  # string
    18: 'tree_state',  # string
    19: 'emojis',  # sequence
    20: 'lavels'  # sequence
}


selectors_class = {
    # 각 파일에 대응하는 comment 파싱 키 클래스, 전체 comment를 파싱하는 class key , level2, level3의 comment를 parsing함 (with css selector)
    'comment_child_level_all': {
        'naver_cafe': 'ul[data-v-7db6cb9f].comment_list .comment_content',
        'naver_blog': '.u_cbox_contents',
        'lawtalk_상담사례': 'case-card__answer'
    },
    
    # 각 파일에 대응하는 child comment 파싱 키 클래스 , 전체 comment 중, level2 계층의 comment를 parsing함 (with css selector)
    'comment_child_level_2': {
        'naver_cafe': 'li[data-v-49558ed9][data-v-7db6cb9f]:not(.reply) .comment_content',
        'naver_blog': '.u_cbox_contents:not(.u_cbox_reply_area .u_cbox_contents)',
        'lawtalk_상담사례': 'No data',
        'naver_kin': 'answerDetail'
    },

    # 각 파일에 대응하는 child comment 파싱 키 클래스 , 전체 comment 중, level3 계층의 comment를 parsing함 (with css selector)
    'comment_child_level_3': {
        'naver_cafe': 'li[data-v-49558ed9][data-v-7db6cb9f].reply .comment_content',
        'naver_blog': '.u_cbox_reply_area .u_cbox_contents',
        'lawtalk_상담사례' :'No data'
    },

    #각 파일에 대응하는 child comment 등록일 파싱키 클래스
    'comment_child_date': {
        'naver_cafe': '.date',
        'naver_blog': '.u_cbox_date',
        'lawtalk_상담사례' :'No data'
    },

}







def save_to_excel(rows, output_file):
    df = pd.DataFrame(rows)
    if df.empty:
        logging.warning("DataFrame is empty. No data to save.")
    else:
        df.to_excel(output_file, index=False)
        logging.info(f"Excel 파일로 저장 완료: {output_file}")




def main():
    
    # XML 파일 경로 설정
    xml_file_path = 'xml/lawtalk_상담사례_20240723.xml'
    
    # XML 파일 경로가 절대 경로인지 확인하고, 절대 경로로 변환
    if not os.path.isabs(xml_file_path):
        xml_file_path = os.path.abspath(xml_file_path)


    # XML 파일 존재 여부 확인
    if not os.path.exists(xml_file_path):
        logging.error(f"File not found: {xml_file_path}")
        return



    # 추출할 태그 및 클래스 지정
    tags_to_extract = ['comment_html', 'title', 'registered_date', 'detail_content'] #comment_html은 0번 위치에 고정시켜야 합니다.
    html_selectors = [
        selectors_class['comment_child_level_all']['lawtalk_상담사례'],
        selectors_class['comment_child_level_2']['lawtalk_상담사례'],
        selectors_class['comment_child_level_3']['lawtalk_상담사례'],
        selectors_class['comment_child_date']['lawtalk_상담사례']  # 날짜 선택자를 추가합니다.
    ]



    extracted_texts = parse_and_extract_from_xml(xml_file_path, tags_to_extract, html_selectors)
    logging.info(f"Extracted texts: {extracted_texts}")

    tree = build_comment_tree(extracted_texts,selectors_class,'lawtalk_상담사례')
    print_comment_tree(tree)
    
    """ rows = get_rows_from_tree(tree,column_filed)
    
    # 데이터가 제대로 구성되었는지 확인
    if not rows:
        logging.error("No rows generated from the comment tree.")
        return

    save_to_excel(rows, "lawtalk_상담사례.xlsx")
   """

    
    

if __name__ == "__main__":
    main()
