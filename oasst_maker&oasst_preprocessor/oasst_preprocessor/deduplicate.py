import pandas as pd
import os
import chardet
import json
import logging


def detect_encoding(file_type):
    """파일의 인코딩을 감지"""
    with open(file_type, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']


def remove_duplicate_prompters(file_path):
    """한 파일 내에서'text' 열을 기준으로 중복된 행을 제거하고 결과를 새 파일에 저장"""
    # 파일 확장자 확인
    file_extension = os.path.splitext(file_path)[1].lower()

    # 파일 인코딩 감지
    encoding = detect_encoding(file_path)

    # 파일 형식에 맞게 읽기
    if file_extension == '.xlsx':
        df = pd.read_excel(file_path)
    elif file_extension == '.csv':
        try:
            df = pd.read_csv(file_path, encoding=encoding)
        except UnicodeDecodeError:
            raise ValueError(f"파일 인코딩을 감지할 수 없습니다: {encoding}.")
    elif file_extension == '.parquet':
        df = pd.read_parquet(file_path)
    elif file_extension == '.json':
        with open(file_path, 'r', encoding=encoding) as f:
            data = json.load(f)
        df = pd.json_normalize(data)
    else:
        raise ValueError("지원하지 않는 파일 형식입니다. .xlsx, .csv, .parquet, 또는 .json 파일을 제공해 주세요.")

    # 중복 제거 전 행 개수
    before_count = len(df)

    if file_extension == '.json':
        # 'text' 열을 기준으로 중복된 행 제거
        filtered_df = df.drop_duplicates(subset='text', keep='first')

        filtered_df.to_json(file_path, orient='records', lines=True, force_ascii=False)
        logging.info(f'필터링된 데이터 저장: {file_path}')
    else:
        # 'text' 열을 기준으로 중복된 행 제거
        duplicate_texts = df[df.duplicated(subset='text', keep='first')]['text']
        filtered_df = df[~df['text'].isin(duplicate_texts)]

        if file_extension == '.xlsx':
            filtered_df.to_excel(file_path, index=False)
        elif file_extension == '.csv':
            filtered_df.to_csv(file_path, index=False, encoding='utf-8-sig')
        elif file_extension == '.parquet':
            filtered_df.to_parquet(file_path, index=False)

        logging.info(f'필터링된 데이터 저장: {file_path}')

    # 중복 제거 후 행 개수
    after_count = len(filtered_df)

    # 제거된 데이터 수 출력
    removed_count = before_count - after_count
    logging.info(f'총 {removed_count}개의 데이터가 제거되었습니다.')
