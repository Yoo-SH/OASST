from bs4 import BeautifulSoup

# sample.html 파일을 읽습니다
with open('먼책신청 문의_ _ 네이버 카페.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# BeautifulSoup 객체를 생성합니다
soup = BeautifulSoup(html_content, 'html.parser')

# 특정 속성 값을 가진 <li> 요소를 찾습니다
general_items = soup.select('li[data-v-49558ed9][data-v-7db6cb9f]:not(.reply)')
reply_items = soup.select('li[data-v-49558ed9][data-v-7db6cb9f].reply')

# 일반 <li> 요소의 텍스트를 출력합니다
print("General Items:")
for item in general_items:
    print(item.get_text(strip=True))

# 클래스가 'reply'인 <li> 요소의 텍스트를 출력합니다
print("\nReply Items:")
for item in reply_items:
    print(item.get_text(strip=True))
