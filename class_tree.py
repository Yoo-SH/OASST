import os
import logging
import uuid
from bs4 import BeautifulSoup
from lxml import etree
from collections import defaultdict

# Set up logging
logging.basicConfig(filename='parsing_link_test.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

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


def build_comment_tree(extracted_texts):
    # 트리 구조를 초기화합니다.
    tree = defaultdict(lambda: {'Level_2': [], 'Level_3': defaultdict(list)})
    
    for item in extracted_texts:

        title = item.get('title', '')
        detail_content = item.get('detail_content', '')
        root = str(title) + str(detail_content)


        if not root:
            continue

        # 'ul[data-v-7db6cb9f].comment_list .comment_content'의 댓글을 추출합니다.
        all_comments = item['html_texts'].get("ul[data-v-7db6cb9f].comment_list .comment_content", [])
        
        # 레벨 2 댓글과 레벨 3 댓글을 추출합니다.
        level_2_comments = item['html_texts'].get("li[data-v-49558ed9][data-v-7db6cb9f]:not(.reply) .comment_content", [])
        level_3_comments = item['html_texts'].get("li[data-v-49558ed9][data-v-7db6cb9f].reply .comment_content", [])
        
        
        # 레벨 2 댓글과 레벨 3 댓글의 인덱스를 추적하기 위한 변수입니다.
        level_2_index = 0
        level_3_index = 0
        
        # 레벨 2 댓글을 추적할 변수입니다.
        current_level_2_comment = None
        
        # 'ul[data-v-7db6cb9f].comment_list .comment_content'의 댓글을 순회합니다.
        for comment in all_comments:
            if level_2_index < len(level_2_comments) and comment == level_2_comments[level_2_index]:
                # 현재 댓글이 레벨 2 댓글이면 현재 레벨 2 댓글을 설정합니다.
                current_level_2_comment = comment
                level_2_index += 1
            elif level_3_index < len(level_3_comments) and comment == level_3_comments[level_3_index]:
                # 현재 댓글이 레벨 3 댓글이면 현재 레벨 2 댓글에 추가합니다.
                if current_level_2_comment:
                    tree[root]['Level_3'][current_level_2_comment].append(comment)
                level_3_index += 1

        # 레벨 2 댓글을 트리에 추가합니다.
        for comment in level_2_comments:
            tree[root]['Level_2'].append(comment)

    return tree



def print_comment_tree(tree):
    for root, levels in tree.items():
        print(f"Root Node: {root}")
        for level_2_comment in levels['Level_2']:
            print(f"  Level 2: {level_2_comment}")
            if level_2_comment in levels['Level_3']:
                for level_3_comment in levels['Level_3'][level_2_comment]:
                    print(f"    Level 3: {level_3_comment}")


def main():
    xml_file_path = 'xml/sample.xml'
    
    if not os.path.isabs(xml_file_path):
        xml_file_path = os.path.abspath(xml_file_path)

    if not os.path.exists(xml_file_path):
        logging.error(f"File not found: {xml_file_path}")
        return

    tags_to_extract = ['comment_html', 'title', 'registered_date', 'detail_content']
    html_selectors = [
        'ul[data-v-7db6cb9f].comment_list .comment_content',
        'li[data-v-49558ed9][data-v-7db6cb9f]:not(.reply) .comment_content',
        'li[data-v-49558ed9][data-v-7db6cb9f].reply .comment_content'
    ] 

    extracted_texts = parse_and_extract_from_xml(xml_file_path, tags_to_extract, html_selectors)
    logging.info(f"Extracted texts: {extracted_texts}")

    tree = build_comment_tree(extracted_texts)
    print_comment_tree(tree)




if __name__ == "__main__":
    main()
