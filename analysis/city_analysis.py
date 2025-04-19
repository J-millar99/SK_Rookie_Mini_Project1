import pandas as pd

#데이터프레임 가져오기
sample_data=pd.read_json('data/cleaned_data.json')
df = pd.DataFrame(sample_data)

# 지역별 채용공고수
city_counts = df['지역'].value_counts()
print("===== 지역별 채용공고 수 =====")
print(city_counts)

# 지역별 직군 분포
city_job_dist = pd.crosstab(df['지역'], df['직군'])
print("===== 지역별 직군분포 수 =====")
print(city_job_dist)

# 서울시 채용 직군 분포
seoul_job_dist = df[df['지역'] == '서울']['직군'].value_counts()
print("===== 서울시 채용 직군 분포 =====")
print(seoul_job_dist)

# 경기 지역 채용 직군 분포
gyeonggi_job_dist = df[df['지역'] == '경기']['직군'].value_counts()
print("===== 경기 지역 채용 직군 분포 =====")
print(gyeonggi_job_dist)

# 엑셀 파일로 저장
with pd.ExcelWriter('data/지역분석.xlsx') as writer:
    city_counts.to_frame('채용공고수').to_excel(writer, sheet_name='지역별 채용공고수')
    city_job_dist.to_excel(writer, sheet_name='지역별 직군분포')
    seoul_job_dist.to_frame('서울 직군분포').to_excel(writer, sheet_name='서울 직군분포')
    gyeonggi_job_dist.to_frame('경기 직군분포').to_excel(writer, sheet_name='경기 직군분포')