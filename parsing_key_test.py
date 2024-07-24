from bs4 import BeautifulSoup

# HTML 파일 경로
file_path = '성매매 기소유예 선처를 받기 위하여 _ 로톡.html'

# HTML 파일 읽기
with open(file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# BeautifulSoup 객체 생성
soup = BeautifulSoup(html_content, 'lxml')

# 클래스명이 'u_cbox_contents'인 모든 요소 찾기 (기존 방식)
description_elements = soup.find_all(class_='se-component se-text se-l-default')

# 텍스트 추출 및 출력 (기존 방식)
print("Using find_all with class name:")
for element in description_elements:
    print(element.get_text() + '\n')


""" 
# CSS 셀렉터를 사용하여 클래스명이 'u_cbox_contents'인 모든 요소 찾기
css_selector_elements = soup.select('.u_cbox_contents:not(.u_cbox_reply_area .u_cbox_contents)')

# 텍스트 추출 및 출력 (CSS 셀렉터 방식)
print("Using CSS selector:")
for element in css_selector_elements:
    print(element.get_text() + '\n') """
