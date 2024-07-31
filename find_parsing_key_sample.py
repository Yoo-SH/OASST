from bs4 import BeautifulSoup

# HTML 파일 경로
file_path = '울산 미납 3.99 입니다 _ 네이버 카페.html'

# HTML 파일 읽기
with open(file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# BeautifulSoup 객체 생성
soup = BeautifulSoup(html_content, 'lxml')

"""
# 클래스명이 ' '인 모든 요소 찾기 (기존 방식)
description_elements = soup.find_all(class_='reply_to')

# 텍스트 추출 및 출력 (기존 방식)
print("Using find_all with class name:")
for element in description_elements:
    print(element.get_text() + '\n') """



""" # 특정 태그 선택
spans_to_clear = soup.find_all('span', class_='reply_to')

# 텍스트 지우기 (각 요소에 대해 반복)
for span in spans_to_clear:
    span.string = ''  # 텍스트를 빈 문자열로 설정
    # 또는 span.clear()로 자식 요소와 텍스트 모두 제거 가능
     """

# CSS 셀렉터를 사용하여 클래스명이 ''인 모든 요소 찾기
css_selector_elements = soup.select('li[data-v-49558ed9][data-v-7db6cb9f].reply .comment_content')  


# 텍스트 추출 및 출력 (CSS 셀렉터 방식)
print("Using CSS selector:")
for element in css_selector_elements:
    print(element.get_text() + '\n') 
