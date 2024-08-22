import argparse
import pandas as pd
import parallel_processing as duck
import qa_separator
import logging
import os
import platform
import csv_preprocessor
import file_encoding_data
import re


def isContainsKeyword(path, keyword):
    """
    경로에서 특정 키워드가 포함되어 있는지 확인합니다.

    Args:
        path (str): 검색할 경로 문자열.
        keyword (str): 찾고자 하는 키워드.

    Returns:
        bool: 키워드가 경로에 포함되어 있으면 True, 그렇지 않으면 False.
    """
    # 정규 표현식 패턴을 정의합니다.
    pattern = rf'{keyword}'
    # 정규 표현식을 사용하여 경로에서 키워드를 찾습니다.
    return re.search(pattern, path) is not None


def convert_to_realformat(format):
    """
    주어진 형식을 실제 파일 확장자로 변환합니다.

    Args:
        format (str): 파일 형식 (예: 'excel', 'csv_comma', 'csv_tab', 'json', 'jsonl', 'parquet').

    Returns:
        str: 실제 파일 확장자 (예: 'xlsx', 'csv', 'json', 'jsonl', 'parquet').
    """
    if format == 'excel':
        return 'xlsx'
    elif (format == 'csv_comma') or (format == 'csv_tab'):
        return 'csv'
    elif format == 'json':
        return 'json'
    elif format == 'jsonl':
        return 'jsonl'
    elif format == 'parquet':
        return 'parquet'


# Excel 파일을 Feather 파일로 변환 (첫 실행 시에만 필요)
def convert_excel_to_feather(filter_file):
    """
    Excel 파일을 Feather 파일로 변환합니다.

    Args:
        filter_file (str): 변환할 Excel 파일의 경로.

    Raises:
        ValueError: Excel 파일이 비어 있을 때 예외를 발생시킵니다.
    """
    df = pd.read_excel(filter_file)
    if df.empty:
        logging.warning(f"Excel 파일에 데이터가 없습니다: {filter_file}")
        raise ValueError("Excel 파일이 비어 있어 Feather 파일로 변환할 수 없습니다.")
    df.to_feather(filter_file)


# Feather 파일로 변환하는 함수 (존재하지 않는 경우에만)
def ensure_feather_file(filter_file):
    """
    Feather 파일이 존재하지 않을 경우, Excel 파일을 Feather 파일로 변환합니다.

    Args:
        filter_file (str): Feather 파일로 변환할 원본 파일의 경로.
    """

    filter_type = filter_file.split('.')[1]

    if filter_type == 'xlsx' and filter_type != 'feather':
        logging.info(f"Excel 파일을 Feather 파일로 변환 중: {filter_file}")
        convert_excel_to_feather(filter_file)
        logging.info(f"Feather 파일 변환 완료: {filter_file}")


def direct_path_filter_file_link(filter_path):
    """
    입력 파일 경로를 확인하고, 필요 시 경로 형식을 조정합니다.

    Args:
        input_path (str): 입력 파일의 디렉토리 경로.

    Returns:
        str: 조정된 입력 파일 경로.
    """

    if os.path.isabs(filter_path) and platform.system() == "Windows":  # 상대경로가 아니라면
        print("filter_path가 절대경로 입니다. filter_path: " + str(filter_path))
        filter_path += '\\'
    else:
        filter_path += '/'

    print("필터 파일 입력 경로 확인:", filter_path)
    return filter_path


def direct_path_input_file_link(input_path):
    """
    입력 파일 경로를 확인하고, 필요 시 경로 형식을 조정합니다.

    Args:
        input_path (str): 입력 파일의 디렉토리 경로.

    Returns:
        str: 조정된 입력 파일 경로.
    """

    if os.path.isabs(input_path) and platform.system() == "Windows":  # 상대경로가 아니라면
        print("input_path가 절대경로 입니다. input_path: " + str(input_path))
        input_path += '\\'
    else:
        input_path += '/'

    print("인풋 파일 입력 경로 확인:", input_path)
    return input_path


def direct_path_output_file_link(output_path):
    """
    출력 파일 경로를 확인하고, 필요 시 경로 형식을 조정합니다.

    Args:
        output_path (str): 출력 파일의 디렉토리 경로.

    Returns:
        str: 조정된 출력 파일 경로.
    """

    if os.path.isabs(output_path) and platform.system() == "Windows":  # 상대경로가 아니라면
        print("output_path가 절대경로 입니다. output_path: " + str(output_path))
        output_path += '\\'
    else:
        output_path += '/'

    print("아웃풋 파일 출력 경로 확인:", output_path)
    return output_path


def check_link_rule(input_path, input_file_name, output_file_name, filter_path, filter_name, args):
    """
    입력 및 출력 파일의 존재 여부와 유효성을 확인합니다.

    Args:
        input_path (str): 입력 파일의 디렉토리 경로.
        input_file_name (str): 입력 파일의 이름.
        output_file_name (str): 출력 파일의 이름 (선택 사항).
        filter_path (str): 필터 파일의 디렉토리 경로.
        filter_name (str): 필터 파일의 이름.
        args (argparse.Namespace): 명령줄 인수 파서 객체.

    Raises:
        SystemExit: 파일이 존재하지 않거나 필수 파일 이름이 주어지지 않은 경우 프로그램을 종료합니다.
    """

    if not input_file_name:
        print("Error: 파일 이름을 입력해야 합니다.")
        exit(0)

    if not filter_name:
        print("Error: 필터 파일 이름을 입력해야 합니다.")
        exit(0)

    # XML 파일 존재 여부 확인
    if not os.path.exists(input_path + input_file_name + '.' + convert_to_realformat(args.format)):  # 입력 파일이 존재하지 않으면 프로그램 종료
        print(f"입력 파일이 존재하지 않습니다:{input_file_name}.{args.format}")
        exit(0)

    if not os.path.exists(filter_path + filter_name):  # 필터 파일이 존재하지 않으면 프로그램 종료
        print(f"필터 파일이 존재하지 않습니다:{filter_name}")
        exit(0)

    if not output_file_name:  # output file명을 입력하지 않으면, _decompress이름이 붙은 파일이 생성.
        output_file_name = input_file_name + '_decompress.'

    print("입력 파일 확인", input_file_name)
    print("출력 파일 확인", output_file_name)
    print("필터 파일 확인", filter_name)
    print("파일 타입 확인:", args.format)


def main():
    """
    메인 함수는 파일 형식에 따라 파일을 처리하고 출력 파일을 생성합니다.

    명령줄 인수를 통해 입력, 출력, 필터 파일의 경로와 파일 형식을 지정할 수 있습니다.
    """

    parser = argparse.ArgumentParser(description='Process files with various formats.')
    parser.add_argument('-input', required=True, help='input 경로와 파일 이름 (예: ./inputfile_name)')
    parser.add_argument('-output', required=True, help='output 경로와 파일 이름 (예: ./outputfile_name)')
    parser.add_argument('-filter', required=True, help='filter 경로와 파일 이름 (예: ./filterfile_name)')
    parser.add_argument(
        '-format',
        required=True,
        choices=['excel', 'csv_comma', 'csv_tab', 'json', 'jsonl', 'parquet', 'feather'],
        help='Input file format[xlsx, csv_comma, csv_tab, json, jsonl, parquet, feather]',
    )

    args = parser.parse_args()

    input_path, input_file_name = os.path.split(args.input)  # 경로와 파일이름을 분리함
    output_path, output_file_name = os.path.split(args.output)  # 경로와 파일이름을 분리함
    filter_path, filter_file_name = os.path.split(args.filter)  # 경로와 파일이름을 분리함

    input_path = direct_path_input_file_link(input_path)  # 경로 형식을 조정함  (상대경로나 절대경로인 경우에 따라 다름)
    output_path = direct_path_output_file_link(output_path)  # 경로 형식을 조정함  (상대경로나 절대경로인 경우에 따라 다름)
    filter_path = direct_path_filter_file_link(filter_path)  # 경로 형식을 조정함  (상대경로나 절대경로인 경우에 따라 다름)

    # 경로규칙 및 파일 존재 유무 확인
    check_link_rule(input_path, input_file_name, output_file_name, filter_path, filter_file_name, args)  # 경로와 파일이름을 확인함

    print(args.input.split('_')[1])

    # 파일 인코딩 확인
    file_encoding_data.get_encoding(args.input + '.' + convert_to_realformat(args.format))

    keyword = 'oasst_naver_cafe'
    # Perform QA separation if needed
    if isContainsKeyword(args.input, keyword) and args.format == 'excel':  # _로 구분된 파일명에서 두 번째 단어가 'cafe'인 경우 ex) ../naver_cafe_2021 => cafe
        separation_words = ['A.', '답변']
        qa_separator.preprocess_excel_file(args.input, convert_to_realformat(args.format), separation_words)
    elif args.input.split('_')[1] == 'cafe' and args.format != 'excel':
        print.info("cafe 파일을 QA분류 작업을 처리하기 위해서는 xlsx 파일 형식이 필요합니다. QA분류 작업을 건너 뜁니다.")

    # 필터 파일을 feather 파일로 변환
    ensure_feather_file(args.filter)

    # Preprocess CSV files
    if args.format == 'csv_comma':
        csv_preprocessor.process_csv_comma(args.input + '.' + convert_to_realformat(args.format))
    elif args.format == 'csv_tab':
        csv_preprocessor.process_csv_tab(args.input + '.' + convert_to_realformat(args.format))

    # Preprocess data
    duck.preprocess_data(args.input, args.output, args.filter, args.format, os.cpu_count())


if __name__ == "__main__":
    main()
