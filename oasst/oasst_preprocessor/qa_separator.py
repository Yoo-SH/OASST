import pandas as pd
import uuid


def preprocess_excel_file(excel_file_path, format, separation_words):
    """
    엑셀 파일을 처리하여 특정 단어(separation_words) 이후의 텍스트를 분리하고 새로운 행을 추가하는 함수.

    Parameters:
        excel_file_path (str): 엑셀 파일의 경로
        separation_words (list): 텍스트 분리에 사용할 단어 목록
        output_file_path (str): 처리된 데이터를 저장할 엑셀 파일 경로

    Returns:
        None
    """

    # 엑셀 파일 읽기
    df = pd.read_excel(excel_file_path)

    start_row = 0
    end_row = df.shape[0]  # 마지막 행 번호, 참고로 shape[0]은 행의 개수를 나타냄, shape[1]은 열의 개수를 나타냄

    # 범위 내의 각 행에 대해 처리
    for idx in range(start_row, end_row):
        if idx >= len(df):
            break  # 인덱스 범위를 벗어나면 루프 중지

        # 'role' 열 값 가져오기
        role_column_value = df.at[idx, 'role']
        # 'text' 열 값 가져오기
        text_column_value = df.at[idx, 'text']

        # 'role'이 "prompter"이고 'text'에 text가 존재하며 'separation_words' 목록 중 하나가 포함된 경우 처리
        if role_column_value == 'prompter' and isinstance(text_column_value, str):
            separation_word = None

            # separation_words 목록을 순회하며 첫 번째로 발견된 단어로 텍스트를 분리
            for word in separation_words:
                if word in text_column_value:
                    separation_word = word
                    break

            if separation_word:
                # separation_word의 인덱스를 기준으로 텍스트 분리
                split_text = text_column_value.split(separation_word, 1)

                if len(split_text) > 1:
                    # separation_word 이후의 텍스트 추출
                    response_text_to_move = separation_word + split_text[1].strip()

                    # 다음 행의 데이터 복사
                    if idx + 1 < len(df):
                        next_row_data = df.iloc[idx + 1].copy()  # 새로운 행을 생성하되, 이후 row를 복사하여 생성.
                        next_row_data['message_id'] = uuid.uuid4()  # message_id 값 변경
                        next_row_data['user_id'] = uuid.uuid4()  # user_id 값 변경
                        next_row_data['role'] = 'assistant'  # role 값 변경
                        next_row_data['text'] = response_text_to_move  # text 값 변경

                        # 새로운 행 삽입
                        df = pd.concat([df.iloc[: idx + 1], pd.DataFrame([next_row_data]), df.iloc[idx + 1 :]]).reset_index(
                            drop=True
                        )  # pd.concat() 함수는 리스트로 제공된 DataFrames를 연결.

                # 현재 행의 'text'에서 separation_word 이후 텍스트 제거
                updated_f_column_value = split_text[0].strip()
                df.at[idx, 'text'] = updated_f_column_value

    # 수정된 데이터프레임을 엑셀 파일로 저장
    df.to_excel(excel_file_path + '.' + format, index=False)
