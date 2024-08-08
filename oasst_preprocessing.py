import re
from kiwipiepy import Kiwi

# Kiwi 객체 생성
kiwi = Kiwi()

# 분석할 문장
text = "안녕하세요. 변호사 이희범입니다. 법무법인 XYZ도 있습니다. 자세한 사항은 https://example.com에서 확인하세요. 서울대 경영학 출신 변호사 홍대범입니다."

# URL 패턴 정의, \S+: 공백이 아닌 문자 하나 이상을 의미합니다. URL의 나머지 부분을 매칭합니다.
url_pattern = re.compile(r'https?://\S+|www\.\S+')
name_pattern =  re.compile(r'\S*변호사|변호사\S*')



# URL 제거
clean_text = url_pattern.sub('', text)

# 이름 관련 패턴 제거
clean_text = name_pattern.sub('', clean_text)


print("URL 제거 후 텍스트:")
print(clean_text)
