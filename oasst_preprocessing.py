import pandas as pd
import spacy


# 엑셀 파일 로드
df = pd.read_excel('oasst_lawtalk_상담사례_20240807.xlsx')

# G열 데이터 가져오기
g_column_data = df['text'].astype(str)  # G열의 모든 데이터를 문자열로 변환하여 가져옴


# Spacy 모델 로드 (한국어 모델 사용)
nlp = spacy.blank("ko")

# 키워드 정의
keywords = ["변호사", "법무법인"]

# 전처리 함수 정의
def preprocess_text(text):
    doc = nlp(text)
    new_tokens = []
    i = 0
    while i < len(doc):
        token = doc[i]
        if token.text in keywords:
            # 키워드 좌우 단어 검사
            start = max(0, i - 3)  # 키워드 좌측 3단어
            end = min(len(doc), i + 4)  # 키워드 우측 3단어
            surrounding_tokens = doc[start:i] + doc[i+1:end]
            
            # 고유명사(NNP) 검사
            if any(t.pos_ == "PROPN" for t in surrounding_tokens):
                i += 4  # 키워드와 주변 단어를 건너뜀
                continue
        new_tokens.append(token.text)
        i += 1
    return " ".join(new_tokens)

# 전처리 적용
df['G_processed'] = g_column_data.apply(preprocess_text)

df.to_excel('processed_file.xlsx', index=False)
