import argparse
import pandas as pd
import parallel_processing as duck
import qa_separator as qa
import logging
import os
import platform


# Excel 파일을 Feather 파일로 변환 (첫 실행 시에만 필요)
def convert_excel_to_feather(excel_path, feather_path):
    df = pd.read_excel(excel_path)
    if df.empty:
        logging.warning(f"Excel 파일에 데이터가 없습니다: {excel_path}")
        raise ValueError("Excel 파일이 비어 있어 Feather 파일로 변환할 수 없습니다.")
    df.to_feather(feather_path)


# Feather 파일로 변환하는 함수 (존재하지 않는 경우에만)
def ensure_feather_file(excel_path, feather_path):
    if not os.path.exists(feather_path) or os.path.getsize(feather_path) == 0:
        logging.info(f"Excel 파일을 Feather 파일로 변환 중: {excel_path}")
        convert_excel_to_feather(excel_path, feather_path)
        logging.info(f"Feather 파일 변환 완료: {feather_path}")
    else:
        logging.info(f"Feather 파일이 이미 존재하며 유효합니다: {feather_path}")


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

    print("파일 입력 경로 확인:", input_path)
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

    print("파일 출력 경로 확인:", output_path)
    return output_path


def check_link_rule(input_path, input_file_name, output_file_name, filter_path, filter_name, args):
    """
    입력 및 출력 파일의 존재 여부와 유효성을 확인합니다.

    Args:
        input_path (str): 입력 파일의 디렉토리 경로.
        input_file_name (str): 입력 파일의 이름.
        output_file_name (str): 출력 파일의 이름 (선택 사항).
        args (argparse.Namespace): 명령줄 인수 파서 객체.

    Returns:
        None
    """

    if not input_file_name:
        print("Error: 파일 이름을 입력해야 합니다.")
        exit(0)

    if not filter_name:
        print("Error: 필터 파일 이름을 입력해야 합니다.")
        exit(0)

    # XML 파일 존재 여부 확인

    if not os.path.exists(input_path + input_file_name + '.' + args.format):  # 입력 파일이 존재하지 않으면 프로그램 종료
        print(f"파일이 존재하지 않습니다:{input_file_name}")
        exit(0)

    if not os.path.exists(filter_path + filter_name + '.xlsx'):  # 필터 파일이 존재하지 않으면 프로그램 종료
        print(f"파일이 존재하지 않습니다:{filter_name}")
        exit(0)

    if not output_file_name:  # output file명을 입력하지 않으면, _decompress이름이 붙은 파일이 생성.
        output_file_name = input_file_name + '_decompress.'

    print("입력 파일 확인", input_file_name)
    print("출력 파일 확인", output_file_name)
    print("파일 타입 확인:", args.format)


def main():

    parser = argparse.ArgumentParser(description='Process files with various formats.')
    parser.add_argument('-input', required=True, help='input 경로와 파일 이름 (예: ./inputfile_name)')
    parser.add_argument('-output', required=True, help='output 경로와 파일 이름 (예: ./outputfile_name)')
    parser.add_argument('-filter', required=True, help='filter 경로와 파일 이름 (예: ./filterfile_name)')
    parser.add_argument(
        '-format',
        required=True,
        choices=['xlsx', 'csv(comma)', 'csv(tab)', 'json', 'jsonl', 'parquet', 'feather'],
        help='Input file format[xlsx, csv(comma), csv(tab), json, jsonl, parquet, feather]',
    )

    args = parser.parse_args()

    input_path, input_file_name = os.path.split(args.input)  # 경로와 파일이름을 분리함
    output_path, output_file_name = os.path.split(args.output)  # 경로와 파일이름을 분리함
    filter_path, filter_file_name = os.path.split(args.filter)  # 경로와 파일이름을 분리함

    input_path = direct_path_input_file_link(input_path)  # 경로 형식을 조정함  (상대경로나 절대경로인 경우에 따라 다름)
    output_path = direct_path_output_file_link(output_path)  # 경로 형식을 조정함  (상대경로나 절대경로인 경우에 따라 다름)
    filter_path = direct_path_input_file_link(filter_path)  # 경로 형식을 조정함  (상대경로나 절대경로인 경우에 따라 다름)

    check_link_rule(input_path, input_file_name, output_file_name, filter_path, filter_file_name, args)  # 경로와 파일이름을 확인함

    # Perform QA separation if needed
    if args.input.split('_')[1] == 'cafe' and args.format == 'xlsx':  # _로 구분된 파일명에서 두 번째 단어가 'cafe'인 경우 ex) ../naver_cafe_2021 => cafe
        separation_words = ['A.', '답변']
        temp_output_path = 'temp_QA_file.xlsx'
        qa.preprocess_excel_file(args.input, separation_words, temp_output_path)
    elif args.input.split('_')[1] == 'cafe' and args.format != 'xlsx':
        print.info("cafe 파일을 QA분류 작업을 처리하기 위해서는 xlsx 파일 형식이 필요합니다. QA분류 작업을 건너 뜁니다.")

    ensure_feather_file(args.filter + '.xlsx', args.filter + '.feather')  # 필터 파일을 feather 파일로 변환

    # Preprocess data
    duck.preprocess_data(args.input, args.format, args.output, args.format, args.filter + '.feather', 8)


if __name__ == "__main__":
    main()
