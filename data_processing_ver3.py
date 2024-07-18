from lxml import etree

# XML 파일 파싱
tree = etree.parse('xml/sample1.xml')
root = tree.getroot()

# 특정 범위의 요소 추출
def extract_range_texts_in_item(item, start_tag, end_tag):
    texts = []
    stack = [item]  # tag node들을 명시적으로 관리하기 위해 stack과 반복문을 이용하여 추출.
    start_found = False

    while stack:
        node = stack.pop()
        if node.tag == start_tag:
            start_found = True
        if start_found and node.text:
            texts.append(node.text.strip())
        if node.tag == end_tag:
            break
        stack.extend(reversed(node))

    return texts

# 특정 태그의 텍스트 추출
def extract_texts_in_item(item, tag):
    texts = []
    #item.iter(tag): item.iter(tag): 이 메서드는 item 요소 내에서 주어진 tag를 가진 모든 자식 요소를 깊이 우선 순회(DFS) 방식으로 찾습니다.
    for node in item.iter(tag):
        if node.text:
            texts.append(node.text.strip())
        else:
            texts.append('None')
    return texts

""" # 모든 <item> 요소에서 <title>부터 <comment_html>까지 텍스트 추출
for item in root.findall('.//item'):
    texts = extract_range_texts_in_item(item, 'title', 'comment_html')
    print("Extracted texts from <title> to <comment_html>:")
    for text in texts:
        print(text) """

# 예시: <item> 요소에서 모든 <link> 태그의 텍스트 추출
for item in root.findall('.//item'):
    link_texts = extract_texts_in_item(item, 'comment_html')
    print("Extracted texts from <link>:")
    for text in link_texts:
        print(text)
