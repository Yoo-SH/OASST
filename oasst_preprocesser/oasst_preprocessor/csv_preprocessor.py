import csv
import re


def clean_text(text):
    # 콤마, 탭, 엔터 제거
    text = re.sub(r'[,\t\n"]', '', text)  # ,\t\n" 를 제거
    # 2개 이상의 빈칸을 1개로 변환
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip()  # strip() 메소드는 문자열의 시작과 끝에 있는 모든 공백을 제거


def process_csv_comma(input_file):
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile, open(input_file, mode='w', newline='', encoding='utf-8') as outfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        rows = []  # 임시 리스트에 저장할 변수

        for row in reader:
            cleaned_row = [clean_text(cell) for cell in row]
            rows.append(cleaned_row)  # 리스트에 클린된 행 저장

        infile.seek(0)  # 파일 포인터를 처음으로 돌림
        writer.writerows(rows)  # 모든 클린된 행을 파일에 씀


# with open(...) as ...는 파일을 열고 자동으로 닫는 작업을 수행하는 구문
# newline=''는 파일을 읽고 쓸 때 줄바꿈을 조정하는 데 사용. CSV 파일을 다룰 때는 보통 이 옵션을 빈 문자열로 설정하여 표준 동작을 유지
# Python은 모든 줄바꿈 문자를 운영체제에 맞는 기본 줄바꿈 문자로 변환. 예를 들어, Windows에서는 모든 줄바꿈이 \r\n으로 변환하는데 이를 방지하기 위해 newline=''을 사용
def process_csv_tab(input_file):
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile, open(input_file, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile, delimiter='\t')
        writer = csv.writer(outfile, delimiter='\t')

        rows = []  # 임시 리스트에 저장할 변수

        for row in reader:
            cleaned_row = [clean_text(cell) for cell in row]
            rows.append(cleaned_row)  # 리스트에 클린된 행 저장

        infile.seek(0)  # 파일 포인터를 처음으로 돌림
        writer.writerows(rows)  # 모든 클린된 행을 파일에 씀


##테스트
""" input_csv_tab_file = '../../data/sample_preprocessor/test_tab_utf-8.csv'
input_csv_comma_file = '../../data/sample_preprocessor/test_comma_utf-8.csv'

process_csv_tab(input_csv_tab_file)
process_csv_comma(input_csv_comma_file)
"""
