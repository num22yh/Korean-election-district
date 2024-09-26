def split_regions(df, column_name='선거구역'):
    """
    '선거구역' 컬럼의 값을 ','로 나누어 여러 행으로 확장하는 함수.
    :param df: 처리할 데이터프레임
    :param column_name: 분리할 컬럼명, 기본값은 '선거구역'
    :return: 확장된 데이터프레임
    """
    # ,를 기준으로 리스트로 분리
    df[column_name] = df[column_name].str.split(',')
    
    # 리스트로 된 항목을 행으로 확장
    df = df.explode(column_name)
    
    # 각 항목의 공백 제거
    df[column_name] = df[column_name].str.strip()
    
    return df
