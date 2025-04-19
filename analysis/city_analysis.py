import pandas as pd

#데이터프레임 가져오기
sample_data=pd.read_json('data/cleaned_data.json')
df = pd.DataFrame(sample_data)

#지역별 채용공고수
city_counts = df['city'].value_counts()
print("===== 지역별 채용공고 수 =====")
print(city_counts)

#지역별 직군 분포
city_job_dist = pd.crosstab(df['city'],df['job_group'])
print("===== 지역별 직군분포 수 =====")
print(city_job_dist)

