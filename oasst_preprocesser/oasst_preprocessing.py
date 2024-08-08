import duckdb
import pandas as pd
import re

# 데이터를 매칭하고 text에서 삭제 텍스트 제거
def remove_text(text, delete_text, delete_hi): 
    if pd.isna(delete_text): # NaN 값이라면 
        delete_text = ''
    if pd.isna(delete_hi): # NaN 값이라면 
        delete_hi = ''
           # URL 정규 표현식 패턴
           
    url_pattern = re.compile(r'http[s]?://\S+|www\.\S+')
    pattern_text = re.compile(re.escape(delete_text)) # 정규표현식 문자 이스케이프 처리 후, 정규표현식 패턴 생성
    pattern_hi = re.compile(re.escape(delete_hi)) # 정규표현식 문자 이스케이프 처리 후, 정규표현식 패턴 생성

    text = url_pattern.sub('', text) # text에서 URL을 빈 문자열로 대체
    text = pattern_text.sub('', text) # text에서 delete_text를 빈 문자열로 대체
    text = pattern_hi.sub('', text) # text에서 delete_hi를 빈 문자열로 대체
    return text

# Excel 파일 읽기
oasst_file_path = 'oasst_lawtalk_상담사례_20240807.xlsx'
filter_file_path = '로톡_변호사_delete_dictionary.xlsx'

# Excel 파일 읽기
oasst_file = pd.read_excel(oasst_file_path)
filter_file = pd.read_excel(filter_file_path)

# DuckDB 연결
conn = duckdb.connect('my_database.duckdb')

# 이미 DB에 테이블이 존재하면 삭제
conn.execute("DROP TABLE IF EXISTS oasst_table")
conn.execute("DROP TABLE IF EXISTS filter_table")

# DataFrame을 테이블로 로드
conn.register('oasst_table', oasst_file)
conn.register('filter_table', filter_file)

# 특정 쿼리 실행
filter_file_query_result = conn.execute("SELECT lawyer_name, delete_text, delete_hi FROM filter_table").fetchdf()
oasst_table_query_result = conn.execute("SELECT * FROM oasst_table").fetchdf()

# 매칭된 데이터를 처리하여 새로운 content 생성
for i, row in oasst_table_query_result.iterrows():   # iterrows는 (인덱스, Series) 쌍을 반환, Series는 각 행의 데이터를 포함.
    matched_rows = filter_file_query_result[filter_file_query_result['lawyer_name'] == row['변호사명']]
    for _, match in matched_rows.iterrows(): # 매칭된 각 행을 다시 iterrows()로 순회. 행의 인덱스는 사용하지 않음.
        oasst_table_query_result.at[i, 'text'] = remove_text(oasst_table_query_result.at[i, 'text'], match['delete_text'], match['delete_hi']) # oasst_table_query_result.at[i, 'text']에 이 새로운 문자열을 할당하여 text를 업데이트

# 결과 확인
print(oasst_table_query_result.head())

# 결과를 Excel 파일로 저장
output_file_path = 'output_file.xlsx'
oasst_table_query_result.to_excel(output_file_path, index=False)
