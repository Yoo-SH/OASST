import duckdb
import pandas as pd
import re
from concurrent.futures import ThreadPoolExecutor
import logging
import file_encoding_data

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def read_file(file_path, file_format):
    """
    파일 형식에 따라 파일을 읽어 데이터프레임으로 반환합니다.

    Args:
        file_path (str): 입력 파일의 경로 (확장자 제외).
        file_format (str): 입력 파일의 형식. 지원되는 형식: 'excel', 'csv_comma', 'csv_tab', 'json', 'jsonl', 'parquet', 'feather'.

    Returns:
        pd.DataFrame: 파일에서 읽은 데이터를 포함한 데이터프레임.

    Raises:
        ValueError: 지원되지 않는 파일 형식이 제공된 경우 발생.
    """
    if file_format == 'excel':
        return pd.read_excel(file_path + '.xlsx', na_values=[], keep_default_na=False)
    elif file_format == 'csv_comma':
        return pd.read_csv(file_path + '.csv', na_values=[], keep_default_na=False, encoding=file_encoding_data.GLOBAL_ENCODING_UNIFICATION)
    elif file_format == 'csv_tab':
        return pd.read_csv(file_path + '.csv', sep='\t', na_values=[], keep_default_na=False, encoding=file_encoding_data.GLOBAL_ENCODING_UNIFICATION)
    elif file_format == 'json':
        return pd.read_json(file_path + '.json', orient='records')
    elif file_format == 'jsonl':
        return pd.read_json(file_path + '.jsonl', lines=True)
    elif file_format == 'parquet':
        return pd.read_parquet(file_path + '.parquet')
    elif file_format == 'feather':
        return pd.read_feather(file_path + '.feather', na_values=[], keep_default_na=False, encoding=file_encoding_data)
    else:
        raise ValueError(f"Unsupported file format in reading file: {file_format}")


def save_file(final_df, output_file_path, output_format):
    """
    데이터프레임을 지정된 파일 형식으로 저장합니다.

    Args:
        final_df (pd.DataFrame): 저장할 데이터프레임.
        output_file_path (str): 파일이 저장될 경로 (확장자 제외).
        output_format (str): 파일을 저장할 형식. 지원되는 형식: 'excel', 'csv_comma', 'csv_tab', 'json', 'jsonl', 'parquet', 'feather'.

    Returns:
        None

    Raises:
        ValueError: 지원되지 않는 파일 형식이 제공된 경우 발생.
    """
    if output_format == 'excel':
        return final_df.to_excel(output_file_path + '.xlsx', index=False)
    elif output_format == 'csv_comma':
        return final_df.to_csv(output_file_path + '.csv', index=False, encoding=file_encoding_data.GLOBAL_ENCODING_UNIFICATION)
    elif output_format == 'csv_tab':
        return final_df.to_csv(output_file_path + '.csv', index=False, sep='\t', encoding=file_encoding_data.GLOBAL_ENCODING_UNIFICATION)
    elif output_format == 'json':
        return final_df.to_json(output_file_path + '.json', orient='records', force_ascii=False, indent=4)
    elif output_format == 'jsonl':
        return final_df.to_json(output_file_path + '.jsonl', orient='records', force_ascii=False, indent=4)
    elif output_format == 'parquet':
        return final_df.to_parquet(output_file_path + '.parquet', index=False)
    elif output_format == 'feather':
        return final_df.to_feather(output_file_path + '.feather', index=False, encoding=file_encoding_data.GLOBAL_ENCODING_UNIFICATION)
    else:
        raise ValueError(f"Unsupported file format in saving file: {output_format}")


# Feather 파일을 읽어 청크로 분할하는 함수
def load_and_split_data(input_file, inputformat, num_chunks):
    """
    파일에서 데이터를 읽고, 병렬 처리를 위해 청크로 분할합니다.

    Args:
        input_file (str): 입력 파일의 경로 (확장자 제외).
        inputformat (str): 입력 파일의 형식.
        num_chunks (int): 데이터를 분할할 청크 수.

    Returns:
        list of pd.DataFrame: 분할된 데이터프레임 청크들의 리스트.
    """

    logging.info(f" 파일 읽기 및 청크로 분할 중: {input_file}")
    df = read_file(input_file, inputformat)
    if df.empty:
        logging.warning("데이터프레임이 비어 있습니다.")
        return

    chunk_size = max(len(df) // num_chunks, 1)  # 청크 크기를 최소 1로 설정 (데이터 크기가 코어 갯수보다 작을 떄, 1로 설정)
    chunks = [df[i : i + chunk_size] for i in range(0, len(df), chunk_size)]
    logging.info("데이터 청크 분할 완료")
    return chunks


# 필터 패턴 생성 함수
def create_filter_pattern(filter_feather_path):
    """
    필터링 조건이 포함된 feather 파일을 기반으로 필터 패턴을 생성합니다.

    Args:
        filter_feather_path (str): 필터 데이터가 포함된 feather 파일의 경로.

    Returns:
        str: 텍스트 필터링에 사용될 정규식 패턴.
    """
    logging.info(f"필터 패턴 생성 중: {filter_feather_path}")
    filter_file = pd.read_feather(filter_feather_path)
    filter_to_remove = [x for x in filter_file['지역명'] if pd.notnull(x)]
    filter_pattern = f"\\s*({'|'.join(map(re.escape, filter_to_remove))})\\s*"
    logging.info("필터 패턴 생성 완료")
    return filter_pattern


# 데이터베이스 연결 생성 및 쿼리 실행 함수
def process_chunk(chunk, filter_pattern):
    """
    청크 데이터를 데이터베이스에 임시 테이블로 로드하고, 필터 패턴을 적용하여 텍스트 필터링을 수행합니다.

    Args:
        chunk (pd.DataFrame): 처리할 데이터프레임 청크.
        filter_pattern (str): 적용할 정규식 필터 패턴.

    Returns:
        pd.DataFrame: 필터링이 적용된 데이터프레임 청크.
    """

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
    """
    데이터를 병렬로 처리하여 각 청크에 필터링을 적용한 후 결합합니다.

    Args:
        chunks (list of pd.DataFrame): 병렬로 처리할 데이터프레임 청크들의 리스트.
        filter_pattern (str): 적용할 정규식 필터 패턴.
        num_threads (int): 사용할 스레드 수.

    Returns:
        pd.DataFrame: 모든 청크가 병렬로 처리된 후 결합된 데이터프레임.
    """
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
    """
    데이터 전처리 작업을 병렬로 수행하고, 결과를 파일로 저장합니다.

    Args:
        input_file (str): 입력 파일의 경로 (확장자 제외).
        output_file (str): 출력 파일의 경로 (확장자 제외).
        filter_file (str): 필터 데이터가 포함된 feather 파일의 경로.
        format (str): 파일의 형식.
        num_threads (int): 사용할 스레드 수.

    Returns:
        None
    """
    logging.info("데이터전처리 병렬작업 시작")

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
