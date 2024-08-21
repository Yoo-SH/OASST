import duckdb
import pandas as pd
import re
from concurrent.futures import ThreadPoolExecutor
import logging
import csv_preprocessor

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def read_file(file_path, file_format):
    """
    Read a file based on its format.

    Args:
        file_path (str): Path to the input file.
        file_format (str): Format of the input file.

    Returns:
        pd.DataFrame: Data read from the file.
    """
    if file_format == 'excel':
        return pd.read_excel(
            file_path + '.xlsx', na_values=[], keep_default_na=False
        )  # na_values, keep_default_na 추가하여 기본 누락된 값 처리 옵션을 비활성화 null 문자열 사라짐 방지
    elif file_format == 'csv_comma':
        return pd.read_csv(file_path + '.csv', na_values=[], keep_default_na=False, encoding=csv_preprocessor.GLOBAL_ENCODING_CSV)
    elif file_format == 'csv_tab':
        return pd.read_csv(file_path + '.csv', sep='\t', na_values=[], keep_default_na=False, encoding=csv_preprocessor.GLOBAL_ENCODING_CSV)
    elif file_format == 'json':
        return pd.read_json(file_path + '.json', na_values=[], keep_default_na=False)
    elif file_format == 'jsonl':
        return pd.read_json(file_path + '.json', lines=True, na_values=[], keep_default_na=False)
    elif file_format == 'parquet':
        return pd.read_parquet(file_path + '.parquet', na_values=[], keep_default_na=False)
    elif file_format == 'feather':
        return pd.read_feather(file_path + '.feather', na_values=[], keep_default_na=False)
    else:
        raise ValueError(f"Unsupported file format in reading file: {file_format}")


def save_file(final_df, output_file_path, output_format):

    if output_format == 'excel':
        return final_df.to_excel(output_file_path + '.xlsx', index=False)
    elif output_format == 'csv_comma':
        return final_df.to_csv(output_file_path + '.csv', index=False, encoding=csv_preprocessor.GLOBAL_ENCODING_CSV)  # encoding 추가
    elif output_format == 'csv_tab':
        return final_df.to_csv(output_file_path + '.csv', index=False, sep='\t', encoding=csv_preprocessor.GLOBAL_ENCODING_CSV)  # encoding 추가
    elif output_format == 'json':
        return final_df.to_json(output_file_path + '.json', index=False)
    elif output_format == 'jsonl':
        return final_df.to_json(output_file_path + '.json', lines=True)
    elif output_format == 'parquet':
        return final_df.to_parquet(output_file_path + '.parquet', index=False)
    elif output_format == 'feather':
        return final_df.to_feather(output_file_path + '.feather', index=False)
    else:
        raise ValueError(f"Unsupported file format in saving file: {output_format}")


# Feather 파일을 읽어 청크로 분할하는 함수
def load_and_split_data(input_file, inputformat, num_chunks):

    logging.info(f" 파일 읽기 및 청크로 분할 중: {input_file}")
    df = read_file(input_file, inputformat)
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
def preprocess_data(input_file, output_file, filter_file, format, num_threads):

    # 데이터 읽기 및 청크로 분할
    chunks = load_and_split_data(input_file, format, num_threads)

    # 필터 패턴 생성
    filter_pattern = create_filter_pattern(filter_file)

    # 병렬 처리 실행
    logging.info("병렬 처리 실행")
    final_df = parallel_processing(chunks, filter_pattern, num_threads)

    # 결과를 파일로 저장
    save_file(final_df, output_file, format)
    logging.info(f"결과 파일 저장 완료: {output_file}")
