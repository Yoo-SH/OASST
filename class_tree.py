import os
import logging
import uuid
from bs4 import BeautifulSoup
from lxml import etree

# Set up logging
logging.basicConfig(filename='parsing_link_test.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# 각 column_filed 번호에 대응하는 값
column_filed = {
    1: 'message_id',
    2: 'parent_id',
    3: 'user_id',
    4: 'create_date',
    5: 'text',
    6: 'role',
    7: 'lang',
    8: 'review_count',
    9: 'review_result',
    10: 'deleted',
    11: 'rank',
    12: 'synthetic',
    13: 'model_name',
    14: 'detoxify',
    15: 'message_tree_id',
    16: 'tree_state',
    17: 'emojis',
    18: 'labels'
}

# 각 파일에 대응하는 comment 파싱 키 클래스
parsing_classKey_comment = {
    'naver_blog': 'u_cbox_contents',
    'naver_cafe': 'comment_content',
    'naver_kin': 'answerDetail'
}

# 각 파일에 대응되는 user_id 파싱 키 클래스
parsing_classkey_userid = {
    'naver_cafe': 'nick_name',
    'naver_cafe': 'end_user_nick'
}

# 각 파일에 대응하는 secretComment 파싱 키 클래스
parsing_classKey_secretComment = {
    'naver_blog': 'u_cbox_delete_contents',
    'naver_cafe': uuid.uuid4(),
    'naver_kin': uuid.uuid4()
}

def extract_texts_from_html(html_content, html_selectors):
    soup = BeautifulSoup(html_content, 'html.parser')
    result = {}
    for selector in html_selectors:
        elements = soup.select(selector)
        if not elements:
            logging.debug(f"No elements found for selector: {selector}")
            result[selector] = ['None']
        else:
            texts = [element.get_text(strip=True) for element in elements]
            result[selector] = texts
    return result

def extract_class_and_text_from_xml_tag(tag, tags_to_extract, html_selectors):
    html_tag = tags_to_extract[0]
    desired_tags = tags_to_extract[1:]

    texts = {}
    for desired_tag in desired_tags:
        texts[desired_tag] = tag.find(desired_tag).text if tag.find(desired_tag) is not None else 'No Content'

    html_content = tag.find(html_tag).text if tag.find(html_tag) is not None else ''
    texts['html_texts'] = extract_texts_from_html(html_content, html_selectors) if html_content else {'None': ['None']}
    
    return texts

def parse_and_extract_from_xml(xml_file_path, tags_to_extract, html_selectors):
    try:
        tree = etree.parse(xml_file_path)
        root = tree.getroot()
    except Exception as e:
        logging.error(f"Error parsing XML file: {e}")
        return []

    all_texts = [extract_class_and_text_from_xml_tag(tag, tags_to_extract, html_selectors) for tag in root.findall('.//item')]
    return all_texts

def main():
    xml_file_path = 'xml/sample.xml'
    
    if not os.path.isabs(xml_file_path):
        xml_file_path = os.path.abspath(xml_file_path)

    if not os.path.exists(xml_file_path):
        logging.error(f"File not found: {xml_file_path}")
        return

    tags_to_extract = ['comment_html']
    html_selectors = ['li[data-v-49558ed9][data-v-7db6cb9f]:not(.reply)', 
                      'li[data-v-49558ed9][data-v-7db6cb9f].reply', 
                      '.se-fs- se-ff-', 
                      '.comment_content', 
                      '.info_wrap', 
                      '.nick_name', 
                      '.date.font_l']

    extracted_texts = parse_and_extract_from_xml(xml_file_path, tags_to_extract, html_selectors)

    for item in extracted_texts:
        print("Detail Content:", item.get('comment_html'))
        
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
