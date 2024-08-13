import duckdb
import pyarrow as pa
import pyarrow.compute as pc
import re
import logging
import pandas as pd

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 시작 로그
logging.info("프로그램 시작")

# Excel 파일 읽기
oasst_file_path = 'oasst_lawtalk_상담사례_20240807.xlsx'
filter_file_path = '지역명.xlsx'

logging.info("Excel 파일 읽기 시작")
# pandas로 읽기 대신 pyarrow로 읽기
oasst_file = pa.Table.from_pandas(pd.read_excel(oasst_file_path))
filter_file = pa.Table.from_pandas(pd.read_excel(filter_file_path))
logging.info("Excel 파일 읽기 완료")


# DuckDB 연결
logging.info("DuckDB 데이터베이스 연결 시작")
conn = duckdb.connect('my_database.duckdb')
logging.info("DuckDB 데이터베이스 연결 완료")


# 필터 리스트 생성
logging.info("필터 리스트 생성 시작")
filter_to_remove = [x.as_py() for x in filter_file.column('지역명') if x.as_py() is not None]  # NaN 제거
filter_pattern = f"\\s*({'|'.join(map(re.escape, filter_to_remove))})\\s*"
logging.info("필터 리스트 생성 완료")

# PyArrow를 사용하여 데이터 필터링 및 텍스트 수정
logging.info("텍스트 필터링 및 수정 시작")
oasst_file = oasst_file.append_column(
    'text',
    pc.replace_substring_regex(
        pc.replace_substring_regex(oasst_file.column('text'), filter_pattern, '', max_replacements=-1), 'http[s]?://\\S+|www\\.\\S+', '', max_replacements=-1
    ),
)
logging.info("텍스트 필터링 및 수정 완료")

# 필터링된 데이터를 DuckDB 테이블에 삽입
logging.info("DuckDB 테이블 생성 및 데이터 삽입 시작")
conn.execute("DROP TABLE IF EXISTS oasst_table")
conn.execute("CREATE TABLE oasst_table AS SELECT * FROM oasst_file")
logging.info("DuckDB 테이블 생성 및 데이터 삽입 완료")

# 결과를 가져오기
logging.info("결과 가져오기 시작")
oasst_table_query_result = conn.execute("SELECT * FROM oasst_table").fetch_df()
logging.info("결과 가져오기 완료")

# 결과를 Excel 파일로 저장
output_file_path = 'output_file.xlsx'
logging.info(f"결과를 Excel 파일({output_file_path})로 저장 시작")
oasst_table_query_result.to_excel(output_file_path, index=False)
logging.info(f"결과를 Excel 파일({output_file_path})로 저장 완료")

# 프로그램 종료 로그
logging.info("프로그램 종료")
