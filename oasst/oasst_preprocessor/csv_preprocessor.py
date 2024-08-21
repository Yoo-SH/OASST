import csv
import re
import os
import chardet  # 문자 인코딩을 감지하는 라이브러리
import logging


GLOBAL_ENCODING_CSV = None


def clean_text(text):
    # 콤마, 탭, 엔터 제거
    text = re.sub(r'[,\t\n"]', '', text)  # ,\t\n" 를 제거
    # 2개 이상의 빈칸을 1개로 변환
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip()  # strip() 메소드는 문자열의 시작과 끝에 있는 모든 공백을 제거


def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']


def process_csv_comma(input_file):
    # 임시 파일에 기록 후 원본 파일에 덮어쓰기
    temp_file = input_file + '.tmp'
    logging.info("CSV 파일의 인코딩 사항을 확인하는 중입니다.")
    global GLOBAL_ENCODING_CSV
    GLOBAL_ENCODING_CSV = detect_encoding(input_file)
    logging.info(f"CSV 파일의 인코딩: {GLOBAL_ENCODING_CSV}")

    # 파일 읽기 및 쓰기
    with (
        open(input_file, mode='r', newline='', encoding=GLOBAL_ENCODING_CSV) as infile,
        open(temp_file, mode='w', newline='', encoding=GLOBAL_ENCODING_CSV) as outfile,
    ):
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        for row in reader:
            cleaned_row = [clean_text(cell) for cell in row]
            writer.writerow(cleaned_row)  # 클린된 행을 임시 파일에 기록

    # 임시 파일을 원본 파일로 덮어쓰기
    os.replace(temp_file, input_file)


def process_csv_tab(input_file):
    # 임시 파일에 기록 후 원본 파일에 덮어쓰기
    temp_file = input_file + '.tmp'
    logging.info("CSV 파일의 인코딩 사항을 확인하는 중입니다.")
    global GLOBAL_ENCODING_CSV
    GLOBAL_ENCODING_CSV = detect_encoding(input_file)
    logging.info(f"CSV 파일의 인코딩: {GLOBAL_ENCODING_CSV}")

    with (
        open(input_file, mode='r', newline='', encoding=GLOBAL_ENCODING_CSV) as infile,
        open(temp_file, mode='w', newline='', encoding=GLOBAL_ENCODING_CSV) as outfile,
    ):
        reader = csv.reader(infile, delimiter='\t')
        writer = csv.writer(outfile, delimiter='\t')

        for row in reader:
            cleaned_row = [clean_text(cell) for cell in row]
            writer.writerow(cleaned_row)  # 클린된 행을 임시 파일에 기록

    # 임시 파일을 원본 파일로 덮어쓰기
    os.replace(temp_file, input_file)


""" # 테스트 코드
input_csv_comma_file = '../../data/sample_preprocessor/oasst_lawtalk_상담사례_20240807.csv'

process_csv_comma(input_csv_comma_file)
 """
