# 파일을 cp949로 읽어서 utf-8-sig로 재인코딩하여 저장
input_file_path = 'C:/Users/user/Desktop/Korean-election-district/data/대한민국 행정동.csv'
output_file_path = 'C:/Users/user/Desktop/Korean-election-district/data/대한민국_행정동_utf8.csv'

# cp949로 파일을 읽음
with open(input_file_path, 'r', encoding='cp949') as f:
    content = f.read()

# utf-8-sig로 파일을 저장
with open(output_file_path, 'w', encoding='utf-8-sig') as f:
    f.write(content)

print("파일이 성공적으로 utf-8-sig로 변환되었습니다.")
