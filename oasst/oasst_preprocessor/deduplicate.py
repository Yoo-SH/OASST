import pandas as pd
import os
import chardet


def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']


def remove_duplicate_prompters(file_path):
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
            raise ValueError(f"Unable to decode the file with detected encoding: {encoding}.")
    elif file_extension == '.parquet':
        df = pd.read_parquet(file_path)
    else:
        raise ValueError("Unsupported file format. Please provide a .xlsx, .csv, or .parquet file.")

    # 'role' 열이 'prompter'인 행을 선택합니다.
    prompters = df[df['role'] == 'prompter']

    # 중복된 'text'를 가진 'prompter' 중 첫 번째를 제외하고 나머지의 'message_tree_id'를 추출합니다.
    duplicate_message_tree_ids = prompters[prompters.duplicated(subset='text', keep='first')]['message_tree_id']

    # 중복된 'message_tree_id' 출력
    print("Duplicate message_tree_id values:")
    print(duplicate_message_tree_ids.tolist())

    # 원본 데이터에서 'message_tree_id'가 중복된 값에 해당하는 모든 행을 삭제합니다.
    filtered_df = df[~df['message_tree_id'].isin(duplicate_message_tree_ids)]

    # 파일 확장자에 따라 결과 파일 저장
    directory = os.path.dirname(file_path)
    base_name = os.path.basename(file_path)
    file_name, _ = os.path.splitext(base_name)

    if file_extension == '.xlsx':
        output_file_path = os.path.join(directory, f"{file_name}_filtered.xlsx")
        filtered_df.to_excel(output_file_path, index=False)
    elif file_extension == '.csv':
        output_file_path = os.path.join(directory, f"{file_name}_filtered.csv")
        filtered_df.to_csv(output_file_path, index=False, encoding='utf-8-sig')  # 저장 시 인코딩을 utf-8-sig로 지정
    elif file_extension == '.parquet':
        output_file_path = os.path.join(directory, f"{file_name}_filtered.parquet")
        filtered_df.to_parquet(output_file_path, index=False)

    print(f'Filtered data saved to {output_file_path}')
