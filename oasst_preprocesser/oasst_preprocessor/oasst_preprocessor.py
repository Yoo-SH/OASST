import oasst_preprocesser.oasst_preprocessor.oasst_preprocessing_duckdb as duck
import oaast_qa_separator as qa
import argparse


def main():

    parser = argparse.ArgumentParser(description='Process Excel file.')
    parser.add_argument('-input', required=True, help='input 경로와 파일 이름 (예: ./inputexcelfile.xml)')
    parser.add_argument('-output', required=True, help='output 경로와 파일 이름 (예: ./outputexcelfile)')
    parser.add_argument('-outputformat', required=True, help='[xlsx, csv, feather]')

    # 데이터 준비 및 병렬 처리 실행
    oasst_file_path = 'data/sample_preprocessor/oasst_lawtalk_상담사례_20240807.xlsx'

    filter_file_path = 'data/지역명.xlsx'

    output_file_path = 'oasst_preprocesser/output/filtered_output.xlsx'

    ## 파일이름 받아서 알아서 타입 가져오게 하기.
    if type == "naver_cafe":  # 네이버 카페의 경우 QA 분리 전처리를 한번 더 함.
        separation_words = ['A.', '답변']  # 여기에 더 많은 단어를 추가할 수 있음
        output_file_path = 'output_QA_file.xlsx'
        qa.preprocess_excel_file(oasst_file_path, separation_words, output_file_path)

    duck.preprocess_data(oasst_file_path, filter_file_path, output_file_path)


if __name__ == "__main__":
    main()
