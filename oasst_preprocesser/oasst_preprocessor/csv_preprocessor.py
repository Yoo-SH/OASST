import csv
import re


def clean_text(text):
    # 콤마, 탭, 엔터 제거
    text = re.sub(r'[,\t\n"]', '', text)  # ,\t\n" 를 제거
    # 2개 이상의 빈칸을 1개로 변환
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip()  # strip() 메소드는 문자열의 시작과 끝에 있는 모든 공백을 제거


def process_csv(input_file, output_file):
    # with open(...) as ...는 파일을 열고 자동으로 닫는 작업을 수행하는 구문
    # newline=''는 파일을 읽고 쓸 때 줄바꿈을 조정하는 데 사용. CSV 파일을 다룰 때는 보통 이 옵션을 빈 문자열로 설정하여 표준 동작을 유지
    # Python은 모든 줄바꿈 문자를 운영체제에 맞는 기본 줄바꿈 문자로 변환. 예를 들어, Windows에서는 모든 줄바꿈이 \r\n으로 변환하는데 이를 방지하기 위해 newline=''을 사용
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile, open(output_file, mode='w', newline='', encoding='utf-8') as outfile:

        # csv.reader는 열려 있는 입력 파일(infile)을 CSV 형식으로 읽기 위한 객체
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # reader 객체를 이용하여 CSV 파일의 각 행을 읽어오고, writer 객체를 이용하여 CSV 파일에 각 행을 쓰기
        for row in reader:
            # 각 셀을 clean_text 함수로 처리
            cleaned_row = [clean_text(cell) for cell in row]
            writer.writerow(cleaned_row)


# 사용 예시
input_csv = '../../data/sample_preprocessor/oasst_lawtalk_상담사례_20240807.csv'
output_csv = '../../data/sample_preprocessor/output.csv'
process_csv(input_csv, output_csv)
