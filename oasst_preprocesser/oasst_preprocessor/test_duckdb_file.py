import duckdb
import pandas as pd

# Excel 파일 읽기
file_path = '변호사_법무법인명.xlsm'
df = pd.read_excel(file_path)

# 데이터 확인
print(df.head())


# DuckDB 연결
conn = duckdb.connect('my_database.duckdb')

# 이미 DB에 테이블이 존재하면 삭제
conn.execute("DROP TABLE IF EXISTS lawyer_data")

# DataFrame을 테이블로 로드
conn.execute("CREATE TABLE lawyer_data AS SELECT * FROM df")


"""
# 데이터 확인
result = conn.execute("SELECT * FROM lawyer_data").fetchall()
print(result)
"""

# 특정 쿼리 실행
query_result = conn.execute("SELECT lawyer_name, company_name FROM lawyer_data").fetchall()
print(query_result)
