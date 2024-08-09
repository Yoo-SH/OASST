import pandas as pd

# 엑셀 파일 경로 및 시트 이름 설정
excel_file_path = 'path_to_your_excel_file.xlsx'
sheet_name = 'Sheet1'

# 엑셀 파일 읽기
df = pd.read_excel(excel_file_path, sheet_name=sheet_name)

# 시작 및 종료 행 설정
start_row = 1  # 파이썬에서는 인덱스가 0부터 시작하므로 1을 뺌
end_row = 10000
separation_word = "답변"  # 특정 단어 설정

# 범위 내의 각 행에 대해 처리
for idx in range(start_row, end_row + 1):
    if idx >= len(df):
        break  # 인덱스 범위를 벗어나면 루프 중지

    # H 열 값 가져오기
    h_column_value = df.at[idx, 'role']  
    # F 열 값 가져오기
    f_column_value = df.at[idx, 'text']  

    # H 열이 "prompter"이고 F 열에 "답변"이 독립적으로 존재하는 경우 처리
    if h_column_value == 'prompter' and isinstance(f_column_value, str):
        f_column_words = f_column_value.split()  # 공백으로 단어 분리
        if separation_word in f_column_words:
            index_of_answer = f_column_words.index(separation_word)
            
            # "답변" 단어 포함 이후 텍스트 추출
            response_text_to_move = ' '.join(f_column_words[index_of_answer:]).trim()
            
            # 다음 행에 삽입할 텍스트 설정
            if idx + 1 < len(df):
                df.at[idx + 1, 'text'] = response_text_to_move
            
            # 현재 행의 F 열에서 "답변" 이후 문자 제거
            updated_f_column_value = ' '.join(f_column_words[:index_of_answer]).strip()
            df.at[idx, 'text'] = updated_f_column_value

# 수정된 데이터프레임을 엑셀 파일로 저장
output_file_path = 'output_excel_file.xlsx'
df.to_excel(output_file_path, index=False)
