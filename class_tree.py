import os
import logging
import uuid
from bs4 import BeautifulSoup
from lxml import etree
from collections import defaultdict
from datetime import datetime

# Set up logging
logging.basicConfig(filename='parsing_link_test.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def extract_texts_from_html(html_content, html_selectors):
    """
    주어진 HTML 컨텐츠와 선택자들을 사용하여 텍스트를 추출합니다.

    Args:
        html_content (str): HTML 컨텐츠를 포함하는 문자열입니다.
        html_selectors (list of str): HTML 내에서 요소를 찾기 위한 CSS 선택자들의 리스트입니다.

    Returns:
        dict: 선택자별로 텍스트 컨텐츠가 리스트로 저장된 딕셔너리입니다.
    """
    logging.info("HTML 컨텐츠에서 텍스트를 추출합니다.")
    soup = BeautifulSoup(html_content, 'html.parser')
    result = {}
    for selector in html_selectors:
        elements = soup.select(selector)
        if not elements:
            logging.debug(f"선택자 {selector}에 대해 찾은 요소가 없습니다.")
            result[selector] = ['None']
        else:
            texts = [element.get_text(strip=True) for element in elements]
            result[selector] = texts
    logging.info("텍스트 추출 완료")
    return result

def extract_class_and_text_from_xml_tag(tag, tags_to_extract, html_selectors):
    """
    XML 태그에서 지정된 태그와 텍스트를 추출하고, HTML 컨텐츠가 있을 경우 추가로 처리합니다.

    Args:
        tag (lxml.etree.Element): 데이터 추출을 위한 XML 태그입니다.
        tags_to_extract (list of str): 텍스트를 추출할 태그들의 리스트입니다. 첫 번째 태그는 HTML 컨텐츠를 포함합니다.
        html_selectors (list of str): HTML 컨텐츠에서 텍스트를 추출하기 위한 CSS 선택자들의 리스트입니다.

    Returns:
        dict: 지정된 태그에서 추출한 텍스트와 처리된 HTML 컨텐츠를 포함하는 딕셔너리입니다.
    """
    logging.info(f"XML 태그에서 클래스와 텍스트를 추출합니다: {tag.tag}")
    html_tag = tags_to_extract[0]
    desired_tags = tags_to_extract[1:]

    texts = {}
    for desired_tag in desired_tags:
        texts[desired_tag] = tag.find(desired_tag).text if tag.find(desired_tag) is not None else 'No Content'

    html_content = tag.find(html_tag).text if tag.find(html_tag) is not None else ''
    texts['html_texts'] = extract_texts_from_html(html_content, html_selectors) if html_content else {'None': ['None']}
    
    logging.info("XML 태그에서 데이터 추출 완료")
    return texts

def parse_and_extract_from_xml(xml_file_path, tags_to_extract, html_selectors):
    """
    XML 파일을 파싱하고, 제공된 태그와 HTML 선택자를 기반으로 정보를 추출합니다.

    Args:
        xml_file_path (str): XML 파일의 경로입니다.
        tags_to_extract (list of str): 텍스트를 추출할 태그들의 리스트입니다. 첫 번째 태그는 HTML 컨텐츠를 포함합니다.
        html_selectors (list of str): HTML 컨텐츠에서 텍스트를 추출하기 위한 CSS 선택자들의 리스트입니다.

    Returns:
        list of dict: 각 XML 항목에서 추출된 데이터가 포함된 딕셔너리들의 리스트입니다.
    """
    logging.info(f"XML 파일을 파싱합니다: {xml_file_path}")
    try:
        tree = etree.parse(xml_file_path)
        root = tree.getroot()
    except Exception as e:
        logging.error(f"XML 파일 파싱 오류: {e}")
        return []

    all_texts = [extract_class_and_text_from_xml_tag(tag, tags_to_extract, html_selectors) for tag in root.findall('.//item')]
    logging.info(f"추출 완료. 추출된 항목 수: {len(all_texts)}")
    return all_texts

def format_date(date_str):
    """
    날짜 문자열을 표준 ISO 8601 형식으로 포맷합니다. 날짜 문자열이 유효하지 않은 경우 현재 날짜와 시간을 반환합니다.

    Args:
        date_str (str): 포맷할 날짜 문자열입니다.

    Returns:
        str: ISO 8601 형식으로 포맷된 날짜 문자열입니다.
    """
    logging.debug(f"날짜 포맷팅: {date_str}")
    try:
        dt = datetime.strptime(date_str, "%Y.%m.%d. %H:%M")
        formatted_date = dt.strftime("%Y-%m-%dT%H:%M:%S.%f+09:00")  # 한국 표준시 UTC+09:00
        return formatted_date
    except ValueError:
        try:
            dt = datetime.strptime(date_str, "%y.%m.%d")  # 날짜만 포함된 경우(naver_cafe의 detal_content)
            formatted_date = dt.strftime("%Y-%m-%dT00:00:00.000000+09:00")  # 한국 표준시 UTC+09:00
            return formatted_date
        except ValueError:
            current_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f+09:00")  # 현재 시간을 반환(로톡)
            logging.warning(f"유효하지 않은 날짜 형식. 현재 날짜를 반환합니다: {current_date}")
            return current_date

def format_uuid():
    """
    새로운 UUID를 생성합니다.

    Returns:
        str: 생성된 UUID 문자열입니다.
    """
    uuid_value = str(uuid.uuid4())
    logging.debug(f"생성된 UUID: {uuid_value}")
    return uuid_value

def build_comment_tree(extracted_texts):
    """
    추출된 텍스트 데이터를 기반으로 댓글의 계층 구조를 구축합니다.

    Args:
        extracted_texts (list of dict): XML 항목에서 추출된 데이터의 리스트입니다.

    Returns:
        defaultdict: 댓글의 계층 구조를 나타내는 중첩된 딕셔너리입니다.
    """
    logging.info("댓글 트리 구축 중")
    # 트리 구조를 초기화합니다.
    tree = defaultdict(lambda: {
        'Level_2': defaultdict(dict),
        'Level_3': defaultdict(lambda: defaultdict(dict)),
        'registered_date': None,
        'uuid': None
    })

    for item in extracted_texts:
        # 제목이나 상세 내용이 누락된 경우 기본값을 빈 문자열로 설정합니다.
        title = item.get('title', '')
        detail_content = item.get('detail_content', '')
        registered_date = item.get('registered_date', 'No Date')
        root = str(title) + '\n' + str(detail_content)

        if not root.strip():
            logging.debug(f"빈 루트 노드 건너뜁니다")
            continue

        # 'ul[data-v-7db6cb9f].comment_list .comment_content'의 댓글을 추출합니다.
        all_comments = item['html_texts'].get("ul[data-v-7db6cb9f].comment_list .comment_content", [])

        # 레벨 2 댓글과 레벨 3 댓글을 추출합니다.
        level_2_comments = item['html_texts'].get("li[data-v-49558ed9][data-v-7db6cb9f]:not(.reply) .comment_content", [])
        level_3_comments = item['html_texts'].get("li[data-v-49558ed9][data-v-7db6cb9f].reply .comment_content", [])
        
        # 댓글들의 날짜를 추출합니다.
        comment_dates = item['html_texts'].get(".date", [])

        # 레벨 2 댓글과 레벨 3 댓글의 인덱스를 추적하기 위한 변수입니다.
        level_2_index = 0
        level_3_index = 0
        date_index = 0
        
        # 레벨 2 댓글을 추적할 변수입니다.
        current_level_2_comment = None

        # 루트 노드에 UUID를 추가합니다.
        tree[root]['uuid'] = format_uuid()
        tree[root]['registered_date'] = format_date(registered_date)
        
        # 'ul[data-v-7db6cb9f].comment_list .comment_content'의 댓글을 순회합니다.
        for comment in all_comments:
            comment_date = comment_dates[date_index] if date_index < len(comment_dates) else 'No Date'
            formatted_date = format_date(comment_date)
            date_index += 1
            
            if level_2_index < len(level_2_comments) and comment == level_2_comments[level_2_index]:
                # 현재 댓글이 레벨 2 댓글이면 UUID를 추가하고 현재 레벨 2 댓글을 설정합니다.
                comment_uuid = format_uuid()
                tree[root]['Level_2'][comment_uuid] = {
                    'comment': comment,
                    'date': formatted_date
                }
                current_level_2_comment = comment_uuid
                level_2_index += 1
            elif level_3_index < len(level_3_comments) and comment == level_3_comments[level_3_index]:
                # 현재 댓글이 레벨 3 댓글이면 현재 레벨 2 댓글에 UUID를 추가합니다.
                if current_level_2_comment:
                    comment_uuid = format_uuid()
                    tree[root]['Level_3'][current_level_2_comment][comment_uuid] = {
                        'comment': comment,
                        'date': formatted_date
                    }
                level_3_index += 1

    logging.info("댓글 트리 구축 완료")
    return tree

def print_comment_tree(tree):
    """
    댓글 트리 구조를 출력합니다.

    Args:
        tree (defaultdict): 댓글의 계층 구조를 나타내는 중첩된 딕셔너리입니다.
    """
    logging.info("댓글 트리 출력 중")
    for root, levels in tree.items():
        print(f"레벨 1 본글: {root} (UUID: {levels['uuid']}), 날짜 {levels['registered_date']}")
        for level_2_uuid, level_2_data in levels['Level_2'].items():
            print(f"  레벨 2 댓글: {level_2_data['comment']} (UUID: {level_2_uuid}, 날짜: {level_2_data['date']})")
            for level_3_uuid, level_3_data in levels['Level_3'][level_2_uuid].items():
                print(f"    레벨 3 댓글: {level_3_data['comment']} (UUID: {level_3_uuid}, 날짜: {level_3_data['date']})")


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
        'li[data-v-49558ed9][data-v-7db6cb9f].reply .comment_content',
        '.date'  # 날짜 선택자를 추가합니다.
    ]

    extracted_texts = parse_and_extract_from_xml(xml_file_path, tags_to_extract, html_selectors)
    logging.info(f"Extracted texts: {extracted_texts}")

    tree = build_comment_tree(extracted_texts)
    print_comment_tree(tree)

if __name__ == "__main__":
    main()
