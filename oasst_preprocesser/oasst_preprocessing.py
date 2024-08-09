import duckdb
import pandas as pd
import re

# Excel 파일 읽기
oasst_file_path = 'oasst_lawtalk_상담사례_20240807.xlsx'
filter_file_path = 'dict.xlsx'



oasst_file = pd.read_excel(oasst_file_path)
filter_file = pd.read_excel(filter_file_path)

# DuckDB 연결
conn = duckdb.connect('my_database.duckdb')


# 제거할 지역명 목록 정의
# 이미 DB에 테이블이 존재하면 삭제
conn.execute("DROP TABLE IF EXISTS oasst_table") 
conn.execute("DROP TABLE IF EXISTS filter_table") 


# DataFrame을 테이블로 저장
conn.execute("CREATE TABLE oasst_table AS SELECT * FROM oasst_file")
conn.execute("CREATE TABLE filter_table AS SELECT * FROM filter_file")

filter_to_remove = filter_file['지역명'].dropna().tolist()  # NaN값 제거한 뒤에, 시리즈 반환 후, 파이썬 리스트로 변환
filter_pattern = f"\\s*({'|'.join(map(re.escape, filter_to_remove))})\\s*"


# SQL 쿼리로 매칭된 데이터를 처리하여 기존 text 열을 업데이트
update_query = f"""
    UPDATE oasst_table
    SET text = regexp_replace(
                   regexp_replace(oasst_table.text,                       
                    '{filter_pattern}', '', 'g'),
               'http[s]?://\\S+|www\\.\\S+', '', 'g')
    WHERE role = 'assistant'
"""



conn.execute(update_query)

# 결과 확인
oasst_table_query_result = conn.execute("SELECT * FROM oasst_table").fetchdf()
print(oasst_table_query_result.head())

# 결과를 Excel 파일로 저장
output_file_path = 'output_file.xlsx'
oasst_table_query_result.to_excel(output_file_path, index=False)
