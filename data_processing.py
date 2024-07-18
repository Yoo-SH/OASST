import xml.etree.ElementTree as ET

# XML 파일 파싱
tree = ET.parse('xml/sample2.xml')  # 'note.xml' 파일이 현재 작업 디렉토리에 있어야 합니다.
root = tree.getroot()

# 데이터 접근
note = root.find('note').text
from_ = root.find('from').text
heading = root.find('heading').text
body = root.find('body').text

print(f"Original XML:\Note: {note}, From: {from_}, Heading: {heading}, Body: {body}")

original_xml_data = ET.tostring(root, encoding='unicode')
print(f"\Original XML:\n{original_xml_data}")


# 데이터 수정
root.find('to').text = 'John'
new_body = ET.SubElement(root, 'body')
new_body.text = "Don't forget to buy milk!"

# 수정된 XML 출력
new_xml_data = ET.tostring(root, encoding='unicode')
print(f"\nModified XML:\n{new_xml_data}")

# 수정된 XML을 파일로 저장
tree.write('xml/sample_output.xml', encoding='utf-8', xml_declaration=True)