import duckdb

# 데이터베이스 연결
conn = duckdb.connect('my_database.duckdb')

# 테이블이 이미 존재할 경우 삭제
conn.execute("DROP TABLE IF EXISTS items")
conn.execute("DROP TABLE IF EXISTS section")


# SQL 쿼리 실행
conn.execute("CREATE TABLE items (id INTEGER, name STRING)")
conn.execute("CREATE TABLE section (id STRING, name STRING, gender CHAR(1))")
conn.execute("INSERT INTO items VALUES (1, 'Apple'), (2, 'Banana'), (3, 'Cherry')")
conn.execute("INSERT INTO section VALUES (' 이거 이렇게 쓰는거 맞냐', 'Apple', 'M'), ('이렇게?', 'Banana', 'W'), ('요렇게?', 'Cherry', 'M')")

# 쿼리 결과 가져오기
result = conn.execute("SELECT * FROM section").fetchall()
print(result)
