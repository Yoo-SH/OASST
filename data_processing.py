import xml.etree.ElementTree as ET

# XML 파일 파싱
tree = ET.parse('./xml/sample.xml')  # 파일 경로 지정
root = tree.getroot()

# 데이터 접근
detail_content = root.find('detail_content').text
title = root.find('title').text
registered_date = root.find('registered_date').text
link = root.find('link').text

print(f"detail_content: {detail_content}, title: {title}, registered_date: {registered_date}, link: {link}")
