import pandas as pd
import uuid

# 엑셀 파일 경로 및 시트 이름 설정
excel_file_path = '../../oasst/oasst_naver_cafe_20240731_1.xlsx'
sheet_name = 'Sheet1'

# 엑셀 파일 읽기
df = pd.read_excel(excel_file_path, sheet_name=sheet_name)

# 시작 및 종료 행 설정
start_row = 0  # 첫 번째 행의 인덱스는 0
end_row = 1000000
separation_words = ['A.', '답변']  # 특정 단어 설정

# 범위 내의 각 행에 대해 처리
for idx in range(start_row, end_row + 1):
    if idx >= len(df):
        break  # 인덱스 범위를 벗어나면 루프 중지

    # 'role' 열 값 가져오기
    role_column_value = df.at[idx, 'role']
    # 'text' 열 값 가져오기
    text_column_value = df.at[idx, 'text']

    # 'role'이 "prompter"이고 'text'에 text가 존재하며 'separation_word'가 포함된 경우 처리
    if role_column_value == 'prompter' and isinstance(text_column_value, str) and (separation_words[0] or separation_words[1]) in text_column_value:

        separation_word = separation_words[0] if separation_words[0] in text_column_value else separation_words[1]

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
output_file_path = 'output_QA_file.xlsx'
df.to_excel(output_file_path, index=False)
