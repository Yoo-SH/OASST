import logging
from bs4 import BeautifulSoup
from lxml import etree


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
    #logging.info("encoding method : ",soup.original_encoding)
    result = {}

    logging.info("추출된 컨텐츠에서 특정 텍스트를 제거하고 선택자를 통해 텍스트를 가져옵니다.")
    
    
    # 특정 태그 선택, 네이버 카페의 경우 3계층 지움.(css선택자로 네이버카페HTML구조상 지우기가 어려움.)
    if html_selectors == ['ul[data-v-7db6cb9f].comment_list .comment_content', 'li[data-v-49558ed9][data-v-7db6cb9f]:not(.reply) .comment_content', 'li[data-v-49558ed9][data-v-7db6cb9f].reply .comment_content', '.date']: #네이버 카페 css 셀렉터
        spans_to_clear = soup.find_all('span', class_='reply_to')


    # 텍스트 지우기 (각 요소에 대해 반복, )
    for span in spans_to_clear:
        span.string = ''  # 텍스트를 빈 문자열로 설정
        # 또는 span.clear()로 자식 요소와 텍스트 모두 제거 가능



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
        texts[desired_tag] = tag.find(desired_tag).text if tag.find(desired_tag) is not None else ' '

    html_content = tag.find(html_tag).text if tag.find(html_tag) is not None else ' ' #로톡의 경우 title만 존재하기 떄문에 content는 공백 하나로 처리.
    texts['html_texts'] = extract_texts_from_html(html_content, html_selectors) if html_content else {'None': [' ']}
    
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
    print("xml에서 데이터를 추출하는 중입니다..")
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

    

    
