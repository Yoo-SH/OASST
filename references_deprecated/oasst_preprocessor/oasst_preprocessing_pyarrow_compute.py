import duckdb
import pyarrow as pa
import re
import logging
import pandas as pd
import os

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 시작 로그
logging.info("프로그램 시작")

oasst_file_path = 'data/sample_preprocessor/oasst_lawtalk_상담사례_20240807.xlsx'
filter_file_path = 'data/지역명.xlsx'

oasst_feather_path = 'data/sample_preprocessor/oasst_lawtalk_상담사례_20240807.feather'
filter_feather_path = 'data/지역명.feather'


# Excel 파일을 Feather 파일로 변환 (첫 실행 시에만 필요)
def convert_excel_to_feather(excel_path, feather_path):
    df = pd.read_excel(excel_path)
    df.to_feather(feather_path)


# Feather 파일이 존재하지 않으면 Excel 파일을 Feather 파일로 변환
if not os.path.exists(oasst_feather_path):
    logging.info("Excel 파일을 Feather 파일로 변환 중...")
    convert_excel_to_feather(oasst_file_path, oasst_feather_path)
    logging.info("Feather 파일 변환 완료")

if not os.path.exists(filter_feather_path):
    logging.info("필터 Excel 파일을 Feather 파일로 변환 중...")
    convert_excel_to_feather(filter_file_path, filter_feather_path)
    logging.info("필터 Feather 파일 변환 완료")

# Feather 파일 읽기
logging.info("Feather 파일 읽기 시작")
oasst_file = pa.Table.from_pandas(pd.read_feather(oasst_feather_path))
filter_file = pa.Table.from_pandas(pd.read_feather(filter_feather_path))
logging.info("Feather 파일 읽기 완료")

# DuckDB 연결
logging.info("DuckDB 데이터베이스 연결 시작")
conn = duckdb.connect('my_database.duckdb')
conn.execute("CREATE TEMPORARY TABLE oasst_file AS SELECT * FROM oasst_file")
logging.info("DuckDB 데이터베이스 연결 완료")

# 필터 리스트 생성
logging.info("필터 리스트 생성 시작")
filter_to_remove = [x.as_py() for x in filter_file.column('지역명') if x.as_py() is not None]
filter_pattern = f"\\s*({'|'.join(map(re.escape, filter_to_remove))})\\s*"
logging.info("필터 리스트 생성 완료")

# 텍스트 필터링 및 수정 (병렬 처리)
logging.info("텍스트 필터링 및 수정 시작")

conn.execute(
    f"""
    UPDATE oasst_file
    SET text = regexp_replace(regexp_replace(text, '{filter_pattern}', '', 'g'), 'http[s]?://\\S+|www\\.\\S+', '', 'g')
    """
)


logging.info("텍스트 필터링 및 수정 완료")


# 결과를 Excel 파일로 저장
logging.info("결과물을 Excel 파일로 저장 중...")
result_df = conn.execute("SELECT * FROM oasst_file").fetch_df()
result_df.to_excel('data/sample_preprocessor/oasst_lawtalk_filtered.xlsx', index=False)
logging.info("Excel 파일 저장 완료")

logging.info("프로그램 종료")
