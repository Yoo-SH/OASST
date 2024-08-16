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


# 데이터베이스 연결 생성 및 쿼리 실행 함수
def process_chunk(chunk, filter_pattern):
    logging.info("데이터베이스 연결 생성")
    chunk_conn = duckdb.connect()

    logging.info("청크 데이터를 임시 테이블로 로드")
    chunk_conn.execute("CREATE TEMPORARY TABLE chunk_table AS SELECT * FROM chunk")  # chunk_table이라는 임시 테이블 생성하여, 병렬처리시 데이터간 충돌 방지

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
        # 청크 처리 작업 제출
        futures = [executor.submit(process_chunk, chunk, filter_pattern) for chunk in chunks]

        # 작업 결과 수집
        for future in futures:
            result_df = future.result()
            results.append(result_df)

    # 모든 결과를 하나의 DataFrame으로 병합
    final_df = pd.concat(results, ignore_index=True)

    return final_df


# 데이터 준비 및 병렬 처리 실행
def main():

    oasst_file_path = 'data/sample_preprocessor/oasst_lawtalk_상담사례_20240807.xlsx'
    oasst_feather_path = 'data/sample_preprocessor/oasst_lawtalk_상담사례_20240807.feather'

    filter_file_path = 'data/지역명.xlsx'
    filter_feather_path = 'data/지역명.feather'

    # Feather 파일이 존재하지 않으면 Excel 파일을 Feather 파일로 변환
    if not os.path.exists(oasst_feather_path):
        logging.info("Excel 파일을 Feather 파일로 변환 중...")
        convert_excel_to_feather(oasst_file_path, oasst_feather_path)
        logging.info("Feather 파일 변환 완료")

    if not os.path.exists(filter_feather_path):
        logging.info("필터 Excel 파일을 Feather 파일로 변환 중...")
        convert_excel_to_feather(filter_file_path, filter_feather_path)
        logging.info("필터 Feather 파일 변환 완료")

    # 데이터 읽기 및 청크 분할

    oasst_file_df = pd.read_feather(oasst_feather_path)
    # 전체 행 수 계산
    total_rows = oasst_file_df.shape[0]
    # 병렬 처리 스레드 수
    num_threads = 4
    # 청크 크기
    chunk_size = total_rows // num_threads
    chunks = [oasst_file_df[i : i + chunk_size] for i in range(0, oasst_file_df.shape[0], chunk_size)]

    # 필터 패턴 생성
    filter_file = pd.read_feather(filter_feather_path)
    filter_to_remove = [x for x in filter_file['지역명'] if pd.notnull(x)]
    filter_pattern = f"\\s*({'|'.join(map(re.escape, filter_to_remove))})\\s*"

    logging.info("병렬 처리 실행")
    final_df = parallel_processing(chunks, filter_pattern, num_threads)

    # 결과를 Excel 파일로 저장
    final_df.to_excel('oasst_preprocesser/output/filtered_output.xlsx', index=False)


if __name__ == "__main__":
    main()
