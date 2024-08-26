import pandas as pd
import numpy as np
from math import ceil
import os
import chardet
import logging
import file_encoding_data


def detect_encoding(file_path):
    """
    파일의 인코딩을 감지하는 함수입니다.

    Parameters:
    - file_path (str): 파일의 경로

    Returns:
    - encoding (str): 감지된 인코딩
    """
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']


def under_sampling(input_file: str, ratio: float) -> None:
    """
    지정된 비율에 따라 분류열에 있는 데이터셋(형사, 민사, 이혼 등)을 토대로 샘플링하는 함수

    Parameters:
    - input_file (str): 샘플링할 파일의 경로 (xlsx, csv, json, parquet)
    - ratio (float): 샘플링 비율 (최소 클래스 샘플 수의 비율)
    """

    # 파일 확장자 확인
    file_extension = os.path.splitext(input_file)[1].lower()

    # 파일 확장자에 따라 파일 읽기
    if file_extension == '.xlsx':
        df = pd.read_excel(input_file)
    elif file_extension == '.csv':
        try:
            df = pd.read_csv(input_file, encoding=file_encoding_data.GLOBAL_ENCODING_UNIFICATION)
        except UnicodeDecodeError:
            raise ValueError(f"감지된 인코딩으로 파일을 디코딩할 수 없습니다: {file_encoding_data.GLOBAL_ENCODING_UNIFICATION}.")
    elif file_extension == '.json':
        df = pd.read_json(input_file)
    elif file_extension == '.parquet':
        df = pd.read_parquet(input_file)
    else:
        raise ValueError("지원되지 않는 파일 형식입니다. xlsx, csv, json, 또는 parquet 형식의 파일을 업로드하세요.")

    # 열 이름의 공백 제거
    df.columns = df.columns.str.strip()

    if file_extension != '.json':
        # 데이터셋에 필요한 열이 존재하는지 확인
        if '분류' not in df.columns or 'message_tree_id' not in df.columns:
            raise KeyError("필요한 열 '분류' 또는 'message_tree_id'가 데이터셋에 없습니다.")

        # 분류별로 데이터프레임 분리
        class_groups = {}
        for category in df['분류'].unique():
            class_groups[category] = df[df['분류'] == category]

        # 각 분류에서 고유한 message_tree_id의 수를 계산
        class_group_counts = {category: len(group['message_tree_id'].unique()) for category, group in class_groups.items()}

        # 가장 적은 그룹 수를 기준으로 최대 그룹 수 계산
        min_group_count = min(class_group_counts.values())
        max_groups = ceil(min_group_count * ratio)

        # 각 분류에서 그룹의 수를 제한하여 샘플링
        sampled_groups = []
        for category, group in class_groups.items():
            unique_tree_ids = group['message_tree_id'].unique()
            sampled_tree_ids = np.random.choice(unique_tree_ids, size=min(len(unique_tree_ids), max_groups), replace=False)
            sampled_group = group[group['message_tree_id'].isin(sampled_tree_ids)]
            sampled_groups.append(sampled_group)

        # 샘플링된 데이터프레임 생성
        df_resampled = pd.concat(sampled_groups)

    else:
        # JSON 파일의 경우, 그룹화 및 샘플링을 수행하지 않음
        original_class_counts = df['분류'].value_counts()
        min_class_count = original_class_counts.min()
        max_samples = ceil(min_class_count * ratio)
        df_resampled = df.groupby('분류').apply(lambda x: x.sample(min(len(x), max_samples))).reset_index(drop=True)

    # 샘플링된 데이터셋 저장 (파일 형식에 따라)
    if file_extension == '.xlsx':
        df_resampled.to_excel(input_file, index=False)
    elif file_extension == '.csv':
        df_resampled.to_csv(input_file, index=False, encoding='utf-8-sig')
    elif file_extension == '.json':
        df_resampled.to_json(input_file, orient='records', force_ascii=False, indent=4)
    elif file_extension == '.parquet':
        df_resampled.to_parquet(input_file, index=False)
    else:
        raise ValueError("저장할 수 없는 파일 형식입니다.")

    # 샘플링 결과에 대한 설명 출력
    logging.info("샘플링이 성공적으로 완료되었습니다.")
