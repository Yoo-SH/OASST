import pandas as pd
from bs4 import BeautifulSoup
import logging
import os
import argparse
import platform
from lxml import etree
import logging

from class_tree import *
from class_parsing_and_extract import *


# Set up logging
logging.basicConfig(filename='parsing_link.log', level=logging.INFO,
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
        'naver_kin' : '.se-main-container',
        'lawtalk_상담사례': '.case-card__answer',
        'lawtalk_성공사례': '.solution-card__content',
        'lawtalk_법률가이드': '.guide-card__content'
    },
    
    # 각 파일에 대응하는 child comment 파싱 키 클래스 , 전체 comment 중, level2 계층의 comment를 parsing함 (with css selector)
    'comment_child_level_2': {
        'naver_cafe': 'li[data-v-49558ed9][data-v-7db6cb9f]:not(.reply) .comment_content',
        'naver_blog': '.u_cbox_contents:not(.u_cbox_reply_area .u_cbox_contents)',
        'naver_kin' : '.se-main-container',
        'lawtalk_상담사례': '.case-card__answer',
        'lawtalk_성공사례': '.solution-card__content',
        'lawtalk_법률가이드': '.guide-card__content'
    },

    # 각 파일에 대응하는 child comment 파싱 키 클래스 , 전체 comment 중, level3 계층의 comment를 parsing함 (with css selector)
    'comment_child_level_3': {
        'naver_cafe': 'li[data-v-49558ed9][data-v-7db6cb9f].reply .comment_content',
        'naver_blog': '.u_cbox_reply_area .u_cbox_contents',
        'naver_kin' : 'No data',
        'lawtalk_상담사례' :'No data',
        'lawtalk_성공사례': 'No data',
        'lawtalk_법률가이드': 'No data'
    },

    #각 파일에 대응하는 child comment 등록일 파싱키 클래스
    'comment_child_date': {
        'naver_cafe': '.date',
        'naver_blog': '.u_cbox_date',
        'naver_kin' : '.se-main-container',
        'lawtalk_상담사례' :'.answerDate',
        'lawtalk_성공사례': 'No data',
        'lawtalk_법률가이드' :'No data'
    },

}







def save_to_excel(rows, output_file):
    """
    주어진 데이터를 Pandas DataFrame으로 변환하여 Excel 파일로 저장합니다.

    Args:
        rows (list): 데이터 행을 담고 있는 리스트.
        output_file (str): 출력할 Excel 파일의 경로와 이름.

    Returns:
        None
    """
    print("oasst 테이블로 변환 중입니다. 잠시만 기다려 주세요.")

    df = pd.DataFrame(rows)
    if df.empty:
        logging.warning("DataFrame is empty. No data to save.")
    else:
        df.to_excel(output_file, index=False)
        logging.info(f"Excel 파일로 저장 완료: {output_file}")




def direct_path_input_file_link(input_path):
    """
    입력 파일 경로를 확인하고, 필요 시 경로 형식을 조정합니다.

    Args:
        input_path (str): 입력 파일의 디렉토리 경로.

    Returns:
        str: 조정된 입력 파일 경로.
    """



    if  os.path.isabs(input_path) and platform.system() == "Windows":  #상대경로가 아니라면
        print("input_path가 절대경로 입니다. input_path: "  + str(input_path))
        input_path += '\\'
    else:
        input_path += '/'
    
    print("파일 입력 경로 확인:", input_path)
    return input_path

   



def direct_path_output_file_link(output_path):
    """
    출력 파일 경로를 확인하고, 필요 시 경로 형식을 조정합니다.

    Args:
        output_path (str): 출력 파일의 디렉토리 경로.

    Returns:
        str: 조정된 출력 파일 경로.
    """ 

    if  os.path.isabs(output_path) and  platform.system() == "Windows":  #상대경로가 아니라면
        print("output_path가 절대경로 입니다. output_path: "  + str(output_path))
        output_path += '\\'        
    else:
        output_path += '/' 

    print("파일 출력 경로 확인:", output_path)
    return output_path
    


def check_link_rule(input_path,input_file_name,output_file_name,args):
    """
    입력 및 출력 파일의 존재 여부와 유효성을 확인합니다.

    Args:
        input_path (str): 입력 파일의 디렉토리 경로.
        input_file_name (str): 입력 파일의 이름.
        output_file_name (str): 출력 파일의 이름 (선택 사항).
        args (argparse.Namespace): 명령줄 인수 파서 객체.

    Returns:
        None
    """



    if not input_file_name:
        print("Error: 파일 이름을 입력해야 합니다.")
        exit(0)

    
    # XML 파일 존재 여부 확인
    if not os.path.exists(input_path+input_file_name):
        print(f"파일이 존재하지 않습니다:{input_file_name}")
        exit(0)

    
    if not output_file_name: #output file명을 입력하지 않으면, _decompress이름이 붙은 파일이 생성.
        output_file_name = None


    if not args.type:
        print("Error: 파일 종류를 입력해야 합니다.")
        exit(0)

    print("입력 파일 확인", input_file_name)
    print("출력 파일 확인", output_file_name)
    print("파일 타입 확인:", args.type)




def main():
    """
    메인 함수로, 명령줄 인수를 처리하고 XML 파일에서 데이터를 추출하여 Excel 파일로 저장합니다.

    Steps:
        1. 명령줄 인수 파싱.
        2. 입력 및 출력 경로 설정.
        3. 파일 및 입력 인수 유효성 검사.
        4. XML 파일에서 데이터 추출.
        5. 추출한 데이터를 트리 구조로 변환.
        6. 트리 구조에서 데이터 행을 생성.
        7. 데이터 행을 Excel 파일로 저장.

    Returns:
        None
    """
    
    parser = argparse.ArgumentParser(description='Process Excel file.')
    parser.add_argument('-input', required=True, help='input 경로와 파일 이름 (예: ./inputexcelfile.xml)')
    parser.add_argument('-output', required=True, help='output 경로와 파일 이름 (예: ./outputexcelfile.xlsx)')
    parser.add_argument('-type', required=True, help='파일 종류 (예: naver_blog)')
    args = parser.parse_args()

    input_path, input_file_name = os.path.split(args.input) #경로와 파일이름을 분리함
    output_path, output_file_name = os.path.split(args.output) #경로와 파일이름을 분리함


    input_path = direct_path_input_file_link(input_path) 
    output_path = direct_path_output_file_link(output_path)
    check_link_rule(input_path,input_file_name,output_file_name,args)
    
    
     # XML 파일 존재 여부 확인
    if not os.path.exists(input_path+input_file_name):
        logging.error(f"File not found: {input_path+input_file_name}")
        return


    # 추출할 태그 및 클래스 지정
    tags_to_extract = ['comment_html', 'title', 'registered_date', 'detail_content'] #comment_html은 0번 위치에 고정시켜야 합니다.
    html_selectors = [
        selectors_class['comment_child_level_all'][args.type],
        selectors_class['comment_child_level_2'][args.type],
        selectors_class['comment_child_level_3'][args.type],
        selectors_class['comment_child_date'][args.type]  # 날짜 선택자를 추가합니다.
    ]

    
    extracted_texts = parse_and_extract_from_xml(input_path+input_file_name, tags_to_extract, html_selectors)
    logging.info(f"Extracted texts: {extracted_texts}")

    tree = build_comment_tree(extracted_texts,selectors_class,args.type)
    
    #print_comment_tree(tree)
    
    rows = get_rows_from_tree(tree,column_filed)
    
    # 데이터가 제대로 구성되었는지 확인
    if not rows:
        logging.error("No rows generated from the comment tree.")
        return
    
    save_to_excel(rows, output_path+output_file_name)
   
    
    

if __name__ == "__main__":
    main()
