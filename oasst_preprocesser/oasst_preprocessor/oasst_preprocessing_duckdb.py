import duckdb
import pandas as pd
import re
from concurrent.futures import ThreadPoolExecutor
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Excel 파일을 Feather 파일로 변환 (첫 실행 시에만 필요)
def convert_excel_to_feather(excel_path, feather_path):
    df = pd.read_excel(excel_path)
    df.to_feather(feather_path)


# Feather 파일로 변환하는 함수 (존재하지 않는 경우에만)
def ensure_feather_file(excel_path, feather_path):
    if not os.path.exists(feather_path):
        logging.info(f"Excel 파일을 Feather 파일로 변환 중: {excel_path}")
        convert_excel_to_feather(excel_path, feather_path)
        logging.info(f"Feather 파일 변환 완료: {feather_path}")


# Feather 파일을 읽어 청크로 분할하는 함수
def load_and_split_data(feather_path, num_chunks):
    logging.info(f"Feather 파일 읽기 및 청크로 분할 중: {feather_path}")
    df = pd.read_feather(feather_path)
    chunk_size = len(df) // num_chunks
    chunks = [df[i : i + chunk_size] for i in range(0, len(df), chunk_size)]
    logging.info("데이터 청크 분할 완료")
    return chunks


# 필터 패턴 생성 함수
def create_filter_pattern(filter_feather_path):
    logging.info(f"필터 패턴 생성 중: {filter_feather_path}")
    filter_file = pd.read_feather(filter_feather_path)
    filter_to_remove = [x for x in filter_file['지역명'] if pd.notnull(x)]
    filter_pattern = f"\\s*({'|'.join(map(re.escape, filter_to_remove))})\\s*"
    logging.info("필터 패턴 생성 완료")
    return filter_pattern


# 데이터베이스 연결 생성 및 쿼리 실행 함수
def process_chunk(chunk, filter_pattern):
    logging.info("데이터베이스 연결 생성")
    chunk_conn = duckdb.connect()

    logging.info("청크 데이터를 임시 테이블로 로드")
    chunk_conn.execute("CREATE TEMPORARY TABLE chunk_table AS SELECT * FROM chunk")

    logging.info("텍스트 필터링 작업 수행")
    chunk_conn.execute(
        f"""
        UPDATE chunk_table
        SET text = regexp_replace(regexp_replace(text, '{filter_pattern}', ''), 'http[s]?://\\S+|www\\.\\S+', '')
        """
    )

    logging.info("결과를 DataFrame으로 반환")
    result_df = chunk_conn.execute("SELECT * FROM chunk_table").fetch_df()

    return result_df


# 병렬 처리 함수
def parallel_processing(chunks, filter_pattern, num_threads):
    results = []

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(process_chunk, chunk, filter_pattern) for chunk in chunks]

        for future in futures:
            result_df = future.result()
            results.append(result_df)

    final_df = pd.concat(results, ignore_index=True)
    return final_df


# 데이터 전처리 및 병렬 처리 실행 함수
def preprocess_data(oasst_file_path, filter_file_path, output_file_path, num_threads=4):
    oasst_feather_path = oasst_file_path.replace('.xlsx', '.feather')
    filter_feather_path = filter_file_path.replace('.xlsx', '.feather')

    # Feather 파일로 변환 (필요 시)
    ensure_feather_file(oasst_file_path, oasst_feather_path)
    ensure_feather_file(filter_file_path, filter_feather_path)

    # 데이터 읽기 및 청크로 분할
    chunks = load_and_split_data(oasst_feather_path, num_threads)

    # 필터 패턴 생성
    filter_pattern = create_filter_pattern(filter_feather_path)

    # 병렬 처리 실행
    logging.info("병렬 처리 실행")
    final_df = parallel_processing(chunks, filter_pattern, num_threads)

    # 결과를 Excel 파일로 저장
    final_df.to_excel(output_file_path, index=False)
    logging.info(f"결과 파일 저장 완료: {output_file_path}")
