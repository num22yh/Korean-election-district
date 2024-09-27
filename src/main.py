import sys
import os

# 프로젝트 루트 디렉토리를 Python 경로에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.pdf_to_df import pdf_to_df
from src.utils.split_region import split_regions

# PDF 파일 경로 및 결과 CSV 파일 경로
pdf_file_path = 'C:/Users/num22/Desktop/Korean-election-district/data/제22대_국회의원선거_국회의원지역선거구구역표.pdf'
csv_file_path = 'C:/Users/num22/Desktop/Korean-election-district/data/result/제22대 국회 선거구.csv'

# PDF에서 데이터를 추출하여 DataFrame으로 변환
df = pdf_to_df(pdf_file_path)

# 첫 번째 행을 컬럼명으로 설정
df.columns = df.iloc[0]  # 첫 번째 행을 컬럼명으로 설정
df = df.drop(0, axis=0)  # 첫 번째 행을 삭제
df.columns = df.columns.str.replace(r'\s+', '', regex=True)  # 모든 공백 문자 제거


# '선거구역' 컬럼을 분리하여 각 지역을 개별 행으로 확장
df = split_regions(df, '선거구역')
df['선거구역'] = df['선거구역'].str.replace('일원', '', regex=False)  # '일원' 제거
df['선거구역'] = df['선거구역'].str.replace(r'\s+', '', regex=True)  # 모든 공백 문자 제거
df['선거구명'] = df['선거구명'].str.replace(r'\s+', '', regex=True)  # 모든 공백 문자 제거

# 결과를 CSV로 저장
df.to_csv(csv_file_path, index=False, encoding='utf-8-sig')

print("CSV 파일로 변환이 완료되었습니다.")
