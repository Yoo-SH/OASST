import pytest
import pandas as pd
import os
import sys
from math import ceil
from under_sampling import under_sampling  # 실제 경로에 맞게 임포트합니다


sys.path.insert(0, r'C:/workspace/oasst-preprocessor/oasst/oasst_preprocessor')

# import

## https://docs.pytest.org/en/stable/


def validate_age(age):
    if age < 0:
        raise ValueError("Age cannot be less than 0")


def test_validate_age_valid_age():
    validate_age(10)


def test_validate_age_invalid_age():
    with pytest.raises(ValueError, match="Age cannot be less than 0"):
        validate_age(-1)


# class undersample:
# def test_undersample_1_5():
# def test_undersample_1_5_binary():
# def test_undersample_1_5_multiclass3():
# def test_undersample_1_5_multiclass5():
def test_undersample():
    """
    분류기준 최소 데이터의 1.5
    데이터 삭제 기준: 각 라벨 데이터 별 가장 적은 라벨 값의 최대 n배 까지만 남기고, 전부 삭제(최소값 1배)
    —undersample 1.5 최소 데이터의 1.5배 까지만
    —undersample 1.0 최소 데이터의 1.0배 까지만
    100개 짜리 testdata 2 class | 100개 짜리 testdata 3 class | 100개 짜리 testdata 5 class

    —undersample 1.5 실행시 [true 15개, false 85개] 이진분류 case 작동검증 -> 작동시 [true 15개, false 23개]
    —undersample 1.0 실행시 [true 15개, false 85개] 이진분류 case 작동검증 -> 작동시 [true 15개, false 15개]
    [형사, 민사, 이혼] 같은 3개 이상의 라벨 case 작동검증 -> 5개도 넣어 봐야됨

    """
    with pytest.raises(ValueError, match="Age cannot be less than 0"):
        validate_age(-1)

    # assert calculator.add(1, 2) == 3
    # assert calculator.add(2, 2) == 4


# 테스트용 파일과 비율을 정의합니다.
TEST_CASES = {
    "binary": {"file": 'C:/workspace/oasst-preprocessor/oasst/tests/oasst_lawtalk_상담사례_2class_분류.xlsx', "ratios": [1.0, 1.5]},
    "multiclass3": {"file": 'C:/workspace/oasst-preprocessor/oasst/tests/oasst_lawtalk_상담사례_3class_분류.xlsx', "ratios": [1.0, 1.5]},
    "multiclass5": {"file": 'C:/workspace/oasst-preprocessor/oasst/tests/oasst_lawtalk_상담사례_5class_분류.xlsx', "ratios": [1.0, 1.5]},
    "json": {"file": 'C:/workspace/oasst-preprocessor/oasst/tests/oasst_lawtalk_상담사례_3class_분류.json', "ratios": [1.0, 1.5]},
    "csv": {"file": 'C:/workspace/oasst-preprocessor/oasst/tests/oasst_lawtalk_상담사례_3class_분류.csv', "ratios": [1.0, 1.5]},
    "parquet": {"file": 'C:/workspace/oasst-preprocessor/oasst/tests/oasst_lawtalk_상담사례_3class_분류.parquet', "ratios": [1.0, 1.5]},
}


def read_file(file_path):
    """파일 형식에 따라 적절한 판다스 데이터프레임을 읽어옵니다."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.xlsx':
        return pd.read_excel(file_path)
    elif ext == '.csv':
        return pd.read_csv(file_path)
    elif ext == '.json':
        return pd.read_json(file_path)
    elif ext == '.parquet':
        return pd.read_parquet(file_path)
    elif ext == '.feather':
        return pd.read_feather(file_path)
    else:
        raise ValueError(f"지원하지 않는 파일 형식: {ext}")


def write_file(df, file_path):
    """데이터프레임을 파일 형식에 맞게 저장합니다."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.xlsx':
        df.to_excel(file_path, index=False)
    elif ext == '.csv':
        df.to_csv(file_path, index=False)
    elif ext == '.json':
        df.to_json(file_path, orient='records', lines=True)
    elif ext == '.parquet':
        df.to_parquet(file_path, index=False)
    elif ext == '.feather':
        df.to_feather(file_path, index=False)
    else:
        raise ValueError(f"지원하지 않는 파일 형식: {ext}")


def run_under_sampling_test(input_file, ratio):
    """
    under_sampling 함수의 샘플링 후 그룹 수 검증을 테스트합니다.
    """

    # 파일 확장자 확인
    ext = os.path.splitext(input_file)[1].lower()

    # 샘플링 실행
    under_sampling(input_file, ratio)

    # 결과 파일 경로 설정
    output_file = os.path.splitext(input_file)[0] + '_resampled' + os.path.splitext(input_file)[1]

    # 결과 파일이 생성되었는지 확인
    assert os.path.exists(output_file), "샘플링된 파일이 생성되지 않았습니다."

    # 결과 파일을 읽어 데이터가 올바르게 생성되었는지 검증
    df_resampled = read_file(output_file)

    # 원본 데이터셋 읽기
    df_original = read_file(input_file)

    # 원본 데이터셋에서 각 분류의 그룹 수를 계산
    if ext != 'json':
        original_class_group_counts = df_original.groupby('분류')['message_tree_id'].nunique()
    else:
        original_class_group_counts = df_original['분류'].value_counts()

    min_group_count = original_class_group_counts.min()

    # 비율에 따른 최대 그룹 수를 소수점 첫째 자리에서 반올림
    max_groups = ceil(min_group_count * ratio)

    # 샘플링 후 데이터셋에서 각 분류의 그룹 수를 계산
    if ext != 'json':
        resampled_class_group_counts = df_resampled.groupby('분류')['message_tree_id'].nunique()
    else:
        resampled_class_group_counts = df_resampled['분류'].value_counts()

    # 결과 출력
    print(f"\n원본 데이터셋의 각 분류별 그룹 수 (비율 {ratio}):")
    print(original_class_group_counts)
    print(f"\n샘플링 후 데이터셋의 각 분류별 그룹 수 (비율 {ratio}):")
    print(resampled_class_group_counts)
    print(f"\n비율에 따른 최대 그룹 수 (소수점 첫째 자리에서 반올림, 비율 {ratio}):")
    print(max_groups)

    # 샘플링 후 그룹 수가 최대 그룹 수보다 작거나 같은지 확인
    assert (resampled_class_group_counts <= max_groups).all(), "샘플링 후 클래스별 그룹 수가 최대 그룹 수를 초과했습니다."

    # 테스트 완료 후 결과 파일 삭제
    os.remove(output_file)


def test_undersample_1_0_binary():
    run_under_sampling_test(TEST_CASES["binary"]["file"], 1.0)


def test_undersample_1_5_binary():
    run_under_sampling_test(TEST_CASES["binary"]["file"], 1.5)


def test_undersample_1_0_multiclass3():
    run_under_sampling_test(TEST_CASES["multiclass3"]["file"], 1.0)


def test_undersample_1_5_multiclass3():
    run_under_sampling_test(TEST_CASES["multiclass3"]["file"], 1.5)


def test_undersample_1_0_multiclass5():
    run_under_sampling_test(TEST_CASES["multiclass5"]["file"], 1.0)


def test_undersample_1_5_multiclass5():
    run_under_sampling_test(TEST_CASES["multiclass5"]["file"], 1.5)


def test_undersample_1_5_multiclass5_csv():
    run_under_sampling_test(TEST_CASES["csv"]["file"], 1.5)


# def test_undersample_1_5_multiclass3_json():
#     run_under_sampling_test(TEST_CASES["json"]["file"], 1.5)


def test_undersample_1_5_multiclass5_parquet():
    run_under_sampling_test(TEST_CASES["parquet"]["file"], 1.5)


# def test_undersample_1_5_multiclass5_feather():
#     run_under_sampling_test(TEST_CASES["multiclass5"]["file"], 1.5)
