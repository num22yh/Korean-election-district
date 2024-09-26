import pdfplumber
import pandas as pd

def pdf_to_df(pdf_file_path):
    """
    PDF 파일에서 데이터를 추출하여 Pandas DataFrame으로 변환하는 함수.
    :param pdf_file_path: PDF 파일 경로
    :return: 추출된 데이터로 구성된 DataFrame
    """
    with pdfplumber.open(pdf_file_path) as pdf:
        pages = pdf.pages
        table_data = []

        # 모든 페이지에서 테이블 데이터 추출
        for page in pages:
            table = page.extract_table()
            if table:
                table_data.extend(table)

    # 추출된 데이터를 DataFrame으로 변환
    df = pd.DataFrame(table_data)
    return df
