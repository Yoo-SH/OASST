import duckdb
import pandas as pd
import re

# Excel 파일 읽기
oasst_file_path = 'oasst_lawtalk_상담사례_20240807.xlsx'
filter_file_path = '로톡_변호사_delete_dictionary.xlsx'
local_file_path = 'dict.xlsx'


oasst_file = pd.read_excel(oasst_file_path)
filter_file = pd.read_excel(filter_file_path)
locations_file = pd.read_excel(local_file_path)

# DuckDB 연결
conn = duckdb.connect('my_database.duckdb')


#문자를 이스케이프 처리하여, 쿼리에서 글을 제대로 인식하도록 처리함.
filter_file['delete_header'] = filter_file['delete_header'].apply(lambda x: re.escape(x) if pd.notna(x) else '')
filter_file['delete_footer'] = filter_file['delete_footer'].apply(lambda x: re.escape(x) if pd.notna(x) else '')


# 제거할 지역명 목록 정의
# 이미 DB에 테이블이 존재하면 삭제
conn.execute("DROP TABLE IF EXISTS oasst_table") 
conn.execute("DROP TABLE IF EXISTS filter_table")

# DataFrame을 테이블로 저장
conn.execute("CREATE TABLE oasst_table AS SELECT * FROM oasst_file")
conn.execute("CREATE TABLE filter_table AS SELECT * FROM filter_file")

locations_to_remove = locations_file['지역명'].dropna().tolist()  # NaN값 제거한 뒤에, 시리즈 반환 후, 파이썬 리스트로 변환
location_pattern = f"\\s*({'|'.join(map(re.escape, locations_to_remove))})\\s*"


# SQL 쿼리로 매칭된 데이터를 처리하여 기존 text 열을 업데이트
update_query = f"""
    UPDATE oasst_table
    SET text = (
        SELECT regexp_replace(
                   regexp_replace(
                       regexp_replace(
                           regexp_replace(oasst_table.text, COALESCE(filter_table.delete_header, ''), '', 'g'),
                           COALESCE(filter_table.delete_footer, ''), '', 'g'),
                       '{location_pattern}', '', 'g'),
                   'http[s]?://\\S+|www\\.\\S+', '', 'g')
        FROM filter_table
        WHERE oasst_table.변호사명 = filter_table.lawyer_name
        LIMIT 1
    )
"""


conn.execute(update_query)

# 결과 확인
oasst_table_query_result = conn.execute("SELECT * FROM oasst_table").fetchdf()
print(oasst_table_query_result.head())

# 결과를 Excel 파일로 저장
output_file_path = 'output_file.xlsx'
oasst_table_query_result.to_excel(output_file_path, index=False)
