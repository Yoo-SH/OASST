import pandas as pd

# 기존 DataFrame
df = pd.DataFrame({
    'A': ['a1', 'a2'],
    'B': ['b1', 'b2']
})

# 새 행을 삽입할 인덱스와 내용
rows_to_insert = [(1, 'new_row1'), (3, 'new_row2')]

# 원본 DataFrame에서 빈 행을 삽입할 위치를 정렬하여 처리
rows_to_insert.sort()

# 빈 행 추가
for idx, _ in reversed(rows_to_insert):
    df = pd.concat([df.iloc[:idx], pd.DataFrame(columns=df.columns, index=[idx]), df.iloc[idx:]]).reset_index(drop=True)

# 빈 행에 내용 추가
for idx, content in rows_to_insert:
    df.loc[idx, 'A'] = content  # 예: 'A' 열에 내용 추가

# 결과 출력
print(df)
