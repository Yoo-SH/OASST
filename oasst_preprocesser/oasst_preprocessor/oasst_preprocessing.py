import duckdb
import pyarrow as pa
import pyarrow.compute as pc
import re
import logging
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 시작 로그
logging.info("프로그램 시작")

# Excel 파일 읽기
oasst_file_path = 'oasst_lawtalk_상담사례_20240807.xlsx'
filter_file_path = 'sample_지역명.xlsx'

logging.info("Excel 파일 읽기 시작")
oasst_file = pa.Table.from_pandas(pd.read_excel(oasst_file_path))
filter_file = pa.Table.from_pandas(pd.read_excel(filter_file_path))
logging.info("Excel 파일 읽기 완료")

# DuckDB 연결
logging.info("DuckDB 데이터베이스 연결 시작")
conn = duckdb.connect('my_database.duckdb')
logging.info("DuckDB 데이터베이스 연결 완료")

# 필터 리스트 생성
logging.info("필터 리스트 생성 시작")
filter_to_remove = [x.as_py() for x in filter_file.column('지역명') if x.as_py() is not None]
filter_pattern = f"\\s*({'|'.join(map(re.escape, filter_to_remove))})\\s*"
logging.info("필터 리스트 생성 완료")

# PyArrow를 사용하여 기존의 text 컬럼을 수정
logging.info("텍스트 필터링 및 수정 시작")

# 기존 text 컬럼을 수정하고, 덮어쓰는 방식
filtered_text_column = pc.replace_substring_regex(
    pc.replace_substring_regex(oasst_file.column('text'), filter_pattern, '', max_replacements=-1), 'http[s]?://\\S+|www\\.\\S+', '', max_replacements=-1
)

# 덮어쓰기 위해 기존 컬럼을 삭제한 후 추가
oasst_file = oasst_file.remove_column(oasst_file.column_names.index('text'))
oasst_file = oasst_file.append_column('text', filtered_text_column)

# 컬럼 순서 조정 (여기서 컬럼 순서를 명시적으로 설정할 수 있습니다)
column_order = [
    'message_id',
    'parent_id',
    'user_id',
    'creadte_date',
    'title',
    'text',
    '사용여부',
    'role',
    'lang',
    'review_count',
    'review_result',
    'deleted',
    'rank',
    'synthetic',
    'model_name',
    'detoxify',
    'message_tree_id',
    'tree_state',
    'emojis',
    'lavels',
    'link',
    '변호사명',
]

# PyArrow 테이블의 컬럼 순서를 조정
oasst_file = pa.Table.from_pandas(oasst_file.to_pandas()[column_order])

logging.info("텍스트 필터링 및 수정 완료")


def execute_query_with_cursor(query):
    """커서를 사용하여 쿼리를 실행하는 함수"""
    with conn.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetch_df()


# 멀티스레딩 환경에서 커서를 사용하는 함수 예제
def multi_threaded_processing():
    logging.info("DuckDB 테이블 생성 및 데이터 삽입 시작")

    # 커서를 사용하여 테이블 생성 및 데이터 삽입
    with ThreadPoolExecutor(max_workers=2) as executor:  # ThreadPoolExecutor를 생성하고 max_workers=2로 설정하여 두 개의 스레드를 사용
        # 테이블 삭제 및 생성
        executor.submit(execute_query_with_cursor, "DROP TABLE IF EXISTS oasst_table")
        executor.submit(execute_query_with_cursor, "CREATE TABLE oasst_table AS SELECT * FROM oasst_file")

    logging.info("DuckDB 테이블 생성 및 데이터 삽입 완료")

    # 결과를 가져오기
    logging.info("결과 가져오기 시작")
    query_result = execute_query_with_cursor("SELECT * FROM oasst_table")
    logging.info("결과 가져오기 완료")

    return query_result


# 멀티스레딩 처리를 실행하고 결과를 저장
output_file_path = 'output_file.xlsx'
query_result_df = multi_threaded_processing()

logging.info(f"결과를 Excel 파일({output_file_path})로 저장 시작")
query_result_df.to_excel(output_file_path, index=False)
logging.info(f"결과를 Excel 파일({output_file_path})로 저장 완료")

# 프로그램 종료 로그
logging.info("프로그램 종료")
