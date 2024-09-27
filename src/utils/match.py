import pandas as pd

# 파일 경로
administrative_file_path = 'C:/Users/num22/Desktop/Korean-election-district/data/대한민국_행정동_utf8.csv'
election_file_path = 'C:/Users/num22/Desktop/Korean-election-district/data/result/제22대 국회 선거구.csv'
output_file_path = 'C:/Users/num22/Desktop/Korean-election-district/data/result/매칭결과.csv'
# jeonbuk_output_file_path = 'C:/Users/user/Desktop/Korean-election-district/data/result/전북특별자치도_매칭결과.csv'
# jeonbuk_output_file_path2 = 'C:/Users/user/Desktop/Korean-election-district/data/result/전북특별자치도_매칭결과2.csv'
# CSV 파일 읽기
admin_df = pd.read_csv(administrative_file_path, encoding='utf-8-sig')
election_df = pd.read_csv(election_file_path, encoding='utf-8-sig')

# 선거구명 및 체크필요 열 추가
admin_df['선거구'] = ''
admin_df['체크필요'] = ''  # 체크필요 열 추가

# 공백 제거를 통한 데이터 전처리
admin_df['읍면동명'] = admin_df['읍면동명'].str.strip()
admin_df['시군구명'] = admin_df['시군구명'].str.strip()
election_df['선거구역'] = election_df['선거구역'].str.strip()
election_df['선거구명'] = election_df['선거구명'].str.replace(r'\s+', '', regex=True)

# 데이터 타입 통일
admin_df = admin_df.astype(str)
election_df = election_df.astype(str)

# 시도명을 저장할 컬럼 추가
election_df['시도명'] = None

# Step 1: 시도명 추출
current_sido = None
for idx, row in election_df.iterrows():
    if "지역구" in row['선거구명']:
        current_sido = row['선거구명'].split('(')[0].strip()  # 시도명 추출
    else:
        election_df.at[idx, '시도명'] = current_sido

# Step 2: 시도명에 따른 매칭
for sido in election_df['시도명'].unique():
    print(f"현재 처리 중인 시도: {sido}")

    # 현재 시도명에 해당하는 행만 필터링
    admin_sido_df = admin_df[admin_df['시도명'] == sido]
    # if sido == '전북특별자치도':
    #     admin_sido_df.to_csv(jeonbuk_output_file_path, index=False, encoding='utf-8-sig')
    #     print(f"전북특별자치도 데이터가 {jeonbuk_output_file_path}로 저장되었습니다.")
    election_sido_df = election_df[election_df['시도명'] == sido]
    # if sido == '전북특별자치도':
    #     election_sido_df.to_csv(jeonbuk_output_file_path2, index=False, encoding='utf-8-sig')
    #     print(f"전북특별자치도 데이터가 {jeonbuk_output_file_path2}로 저장되었습니다.")

    # '읍면동명'과 '선거구역' 매칭
    for idx, row in admin_sido_df.iterrows():
        matches = election_sido_df[election_sido_df['선거구역'] == row['읍면동명']]
        
        if len(matches) > 1:
            admin_df.at[idx, '체크필요'] = '중복된 읍면동명'  # 같은 이름이 여러 번 있으면 체크
        if not matches.empty:
            admin_df.at[idx, '선거구'] = matches.iloc[0]['선거구명']

    # '선거구'가 비어있는 행에 대해 '시군구명'과 '선거구역' 매칭
    for idx, row in admin_sido_df[admin_sido_df['선거구'] == ''].iterrows():
        matches = election_sido_df[election_sido_df['선거구역'] == row['시군구명']]
        
        if len(matches) > 1:
            admin_df.at[idx, '체크필요'] = '중복된 시군구명'  # 같은 이름이 여러 번 있으면 체크
        if not matches.empty:
            admin_df.at[idx, '선거구'] = matches.iloc[0]['선거구명']

# Step 3: 선거구가 여전히 빈 값인 행 체크
admin_df.loc[admin_df['선거구'] == '', '체크필요'] = '선거구 매칭 실패'

# 결과를 CSV로 저장
admin_df.to_csv(output_file_path, index=False, encoding='utf-8-sig')

print("매칭이 완료되었으며, 결과가 CSV 파일로 저장되었습니다.")
