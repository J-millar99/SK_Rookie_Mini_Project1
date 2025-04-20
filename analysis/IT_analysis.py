import pandas as pd

#데이터프레임 가져오기
sample_data=pd.read_json('data/cleaned_data.json')
df = pd.DataFrame(sample_data)


# 인터넷·IT·통신·모바일·게임 직군 필터링
filtered_data = df[df['직군']=='인터넷·IT·통신·모바일·게임']

# 지역, 연봉, 근무형태 데이터 추출 및 합치기
analysis_data = filtered_data[['회사명','하위직군','지역', '고용형태', '급여조건']].copy()

print(analysis_data)

# 엑셀 파일로 저장
output_path = 'data/IT직군.xlsx'
analysis_data.to_excel(output_path, index=False)

print(f"분석 결과가 {output_path}에 저장되었습니다.")