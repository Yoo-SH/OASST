import xml.etree.ElementTree as ET

# XML 파일 파싱
tree = ET.parse('xml/sample1.xml')
root = tree.getroot()

# 특정 범위의 요소 추출
def extract_range_texts_in_item(item, start_tag, end_tag):
    texts = []
    start_found = False

    def traverse(node):
        nonlocal start_found

        if node.tag == start_tag:
            start_found = True
        if start_found and node.text:
            texts.append(node.text.strip())
        if node.tag == end_tag:
            return True

        for child in node:
            if traverse(child):
                return True

    traverse(item)
    return texts

# 모든 <item> 요소에서 <title>부터 <detail_content>까지 텍스트 추출
for item in root.findall('item'):
    texts = extract_range_texts_in_item(item, 'title', 'comment_html')
    print("Extracted texts from <title> to <comment_html>:")
    for text in texts:
        print(text)
