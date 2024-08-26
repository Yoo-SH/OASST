import streamlit as st
import pandas as pd
import requests
import os
import re
import zipfile
from io import BytesIO
import shutil
import csv


def safe_folder_name(name):
    """안전한 폴더 이름 생성 함수."""
    name = re.sub(r'[<>:"/\\|?*\s*\.\.{1,}「」]', '_', str(name))  # 문제 있는 문자와 패턴을 밑줄로 대체
    name = re.sub(r'^\.+|\.+$', '', str(name))  # 앞뒤의 점 제거
    return name[:50]  # 길이 제한


def clean_file_name(filename):
    """파일명에서 확장자만 추출하고 반환."""
    filename = str(filename)
    match = re.search(r'\.[a-zA-Z0-9]+', filename)
    if match:
        ext_pos = match.start() + len(match.group())
        return filename[:ext_pos]
    return filename


def safe_filename(file):
    """문제 있는 문자를 밑줄로 대체하고, 길이를 제한."""
    file = re.sub(r'[!@#$%^&*()_+\-=\[\]{}|\\:;"\'<>,/?\n「」]', '_', str(file))
    return file[:50]


def is_html(content):
    """HTML 콘텐츠 여부 확인."""
    return bool(re.search(r'<html', content.decode('utf-8', errors='ignore'), re.IGNORECASE))


def initialize_logging(base_folder):
    """로그 파일 및 CSV 초기화."""
    log_file_path = os.path.join(base_folder, 'log.log')
    log_csv_path = os.path.join(base_folder, 'log.csv')
    error_log_file_path = os.path.join(base_folder, 'error.log')
    error_csv_path = os.path.join(base_folder, 'error.csv')

    if not os.path.exists(base_folder):
        os.makedirs(base_folder)

    with open(log_file_path, 'w', encoding='utf-8') as log_file, open(error_log_file_path, 'w', encoding='utf-8') as error_log_file:
        log_file.write('Download Log\n')
        error_log_file.write('Error Log\n')

    with open(log_csv_path, 'w', newline='', encoding='utf-8-sig') as log_csv, open(error_csv_path, 'w', newline='', encoding='utf-8-sig') as error_csv:
        log_writer = csv.writer(log_csv)
        error_writer = csv.writer(error_csv)
        log_writer.writerow(['Index', 'Organization', 'Title', 'File Name', 'URL', 'Status', 'Message'])
        error_writer.writerow(['Index', 'Organization', 'Title', 'File Name', 'URL', 'Error Message'])

    return log_file_path, log_csv_path, error_log_file_path, error_csv_path


def download_files(df, base_download_folder):
    """파일 다운로드 및 로그 기록."""
    log_file_path, log_csv_path, error_log_file_path, error_csv_path = initialize_logging(base_download_folder)

    download_count = 0
    total_files = len(df)
    progress_bar = st.progress(0)
    status_text = st.empty()

    for index, row in df.iterrows():
        url = row['file_download_link']
        organization = row['organization']
        title = row['title']
        file_name = row['file_name']

        if pd.isna(url) or not url.strip():
            continue  # URL이 없거나 유효하지 않으면 건너뛰기

        organization_folder = safe_folder_name(organization)
        title_folder = f"{index + 1:05d}_{safe_folder_name(title)}"

        safe_file = clean_file_name(file_name)
        safe_file = safe_filename(safe_file)

        organization_folder_path = os.path.join(base_download_folder, organization_folder)
        title_folder_path = os.path.join(organization_folder_path, title_folder)

        if not os.path.exists(title_folder_path):
            os.makedirs(title_folder_path)

        file_path = os.path.join(title_folder_path, safe_file)

        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            if is_html(response.content):
                raise ValueError("다운로드한 콘텐츠가 HTML입니다. 유효한 파일이 아닙니다.")

            with open(file_path, 'wb') as file:
                file.write(response.content)

            download_count += 1  # 다운로드 성공 시 카운트 증가

            # 성공 로그 기록
            with open(log_file_path, 'a', encoding='utf-8') as log_file, open(log_csv_path, 'a', newline='', encoding='utf-8-sig') as log_csv:
                log_file.write(f"파일 다운로드 성공: {url}\n")
                log_writer = csv.writer(log_csv)
                log_writer.writerow([index + 1, organization, title, safe_file, url, '성공', ''])

        except (requests.RequestException, ValueError) as e:
            error_message = f"{url} 다운로드 오류: {e}\n"
            # 에러 로그 기록
            with (
                open(error_log_file_path, 'a', encoding='utf-8') as error_log_file,
                open(error_csv_path, 'a', newline='', encoding='utf-8-sig') as error_csv,
                open(log_file_path, 'a', encoding='utf-8') as log_file,
                open(log_csv_path, 'a', newline='', encoding='utf-8-sig') as log_csv,
            ):
                error_log_file.write(error_message)
                error_writer = csv.writer(error_csv)
                error_writer.writerow([index + 1, organization, title, safe_file, url, str(e)])
                log_file.write(error_message)
                log_writer = csv.writer(log_csv)
                log_writer.writerow([index + 1, organization, title, safe_file, url, '실패', str(e)])
            continue

        except FileNotFoundError as e:
            error_message = f"{file_path} 파일 저장 오류: {e}\n"
            # 파일 저장 오류 로그 기록
            with (
                open(error_log_file_path, 'a', encoding='utf-8') as error_log_file,
                open(error_csv_path, 'a', newline='', encoding='utf-8-sig') as error_csv,
                open(log_file_path, 'a', encoding='utf-8') as log_file,
                open(log_csv_path, 'a', newline='', encoding='utf-8-sig') as log_csv,
            ):
                error_log_file.write(error_message)
                error_writer = csv.writer(error_csv)
                error_writer.writerow([index + 1, organization, title, safe_file, url, str(e)])
                log_file.write(error_message)
                log_writer = csv.writer(log_csv)
                log_writer.writerow([index + 1, organization, title, safe_file, url, '실패', str(e)])
            continue

        # 진행 상황 표시 바 업데이트
        progress_bar.progress((index + 1) / total_files)
        status_text.text(f"진행 중: {index + 1}/{total_files} 파일 다운로드 중")

    # ZIP 파일 생성
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, _, files in os.walk(base_download_folder):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, base_download_folder)
                try:
                    zip_file.write(file_path, relative_path)
                except FileNotFoundError as e:
                    # ZIP 파일 생성 중 오류 로그 기록
                    error_message = f"ZIP 파일 생성 중 오류: {e}\n"
                    with (
                        open(error_log_file_path, 'a', encoding='utf-8') as error_log_file,
                        open(log_file_path, 'a', encoding='utf-8') as log_file,
                        open(log_csv_path, 'a', newline='', encoding='utf-8-sig') as log_csv,
                    ):
                        error_log_file.write(error_message)
                        log_file.write(error_message)
                        log_writer = csv.writer(log_csv)
                        log_writer.writerow(['N/A', 'N/A', 'N/A', 'N/A', 'N/A', '실패', str(e)])
                    continue

    zip_buffer.seek(0)

    return zip_buffer


def main():
    st.title("파일 다운로드기")

    if "downloaded" not in st.session_state:
        st.session_state.downloaded = False
        st.session_state.df = None
        st.session_state.zip_buffer = None

    uploaded_file = st.file_uploader("Excel 또는 CSV 파일을 선택하세요", type=["xlsx", "csv"])

    if uploaded_file is not None:
        if uploaded_file.name.endswith('.xlsx'):
            st.session_state.df = pd.read_excel(uploaded_file)
        elif uploaded_file.name.endswith('.csv'):
            st.session_state.df = pd.read_csv(uploaded_file)

        st.session_state.downloaded = False

    if st.session_state.df is not None and not st.session_state.downloaded:
        base_download_folder = os.path.join(os.getcwd(), "downloads")

        if os.path.exists(base_download_folder):
            shutil.rmtree(base_download_folder)  # 기존 다운로드 폴더 삭제

        zip_buffer = download_files(st.session_state.df, base_download_folder)
        st.session_state.zip_buffer = zip_buffer
        st.session_state.downloaded = True
        original_file_name = os.path.splitext(uploaded_file.name)[0]
        st.write(f"다운로드 완료! {len(st.session_state.df)} 개의 파일 처리됨.")
        st.download_button(
            label="모든 파일을 ZIP으로 다운로드",
            data=st.session_state.zip_buffer,
            file_name=f"{original_file_name}.zip",
            mime="application/zip",
            key="download_button",
        )


if __name__ == "__main__":
    main()
