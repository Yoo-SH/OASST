import duckdb
import pandas as pd

# 데이터프레임 생성
df = pd.DataFrame({'id': [1, 2, 3], 'name': ['Apple', 'Banana', 'Cherry'], 'gender': ['M', 'W', 'M']})

# 데이터프레임을 테이블로 저장
conn = duckdb.connect()
conn.execute("CREATE TABLE items AS SELECT * FROM df")

# 쿼리 결과를 데이터프레임으로 변환
df_result = conn.execute("SELECT * FROM items").fetchdf()
print(df_result)
