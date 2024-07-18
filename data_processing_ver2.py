import xml.etree.ElementTree as ET

# XML 파일 파싱
tree = ET.parse('xml/sample1.xml')  # 'sample2.xml' 파일이 현재 작업 디렉토리에 있어야 합니다.
root = tree.getroot()

# 특정 범위의 요소 추출
def extract_range_texts(start_tag, end_tag):
    texts = []
    start_found = False
    for elem in root:
        if elem.tag == start_tag:
            start_found = True
        if start_found:
            texts.append(elem.text.strip() if elem.text else '')
        if elem.tag == end_tag:
            break
    return texts

# from 태그부터 heading 태그까지 텍스트 추출
texts = extract_range_texts('item', 'link')


# 결과 출력
print("Extracted texts from <to> to <heading>:")
for text in texts:
    print(text)
