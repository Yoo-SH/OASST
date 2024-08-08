import duckdb
import pandas as pd
import re

# Excel 파일 읽기
input_file_path = 'db_matching_test.xlsx'
db_file_path = '변호사_법무법인명.xlsm'

# Excel 파일 읽기
db_file_df = pd.read_excel(db_file_path)
input_file_df = pd.read_excel(input_file_path)

# DuckDB 연결
conn = duckdb.connect('my_database.duckdb')

# 이미 DB에 테이블이 존재하면 삭제
conn.execute("DROP TABLE IF EXISTS lawyer_data")
conn.execute("DROP TABLE IF EXISTS input_data")

# DataFrame을 테이블로 로드
conn.register('db_file_df', db_file_df)
conn.register('input_file_df', input_file_df)

conn.execute("CREATE TABLE lawyer_data AS SELECT * FROM db_file_df")
conn.execute("CREATE TABLE input_data AS SELECT * FROM input_file_df")

# 특정 쿼리 실행
db_file_query_result = conn.execute("SELECT lawyer_name, company_name FROM lawyer_data").fetchdf()
input_file_query_result = conn.execute("SELECT name, content FROM input_data").fetchdf()

# 데이터를 매칭하고 content에서 company_name 제거
def remove_company_name(content, company_name):
    if pd.isna(company_name):
        return content
    pattern = re.compile(re.escape(company_name))
    return pattern.sub('', content)

# 매칭된 데이터를 처리하여 새로운 content 생성
for i, row in input_file_query_result.iterrows():
    matched_rows = db_file_query_result[db_file_query_result['lawyer_name'] == row['name']]
    for _, match in matched_rows.iterrows():
        input_file_query_result.at[i, 'content'] = remove_company_name(input_file_query_result.at[i, 'content'], match['company_name'])

# 결과 확인
print(input_file_query_result.head())

# 결과를 Excel 파일로 저장 (선택사항)
input_file_query_result.to_excel('processed_input_file.xlsx', index=False)
