import pandas as pd

#데이터프레임 가져오기
sample_data=pd.read_json('data/cleaned_data.json')
df = pd.DataFrame(sample_data)

#고용 형태 분포 확인
print("===== 고용형태 분포 =====")
print(df['employment_type'].value_counts())

#직군별 고용 형태 분포 확인
job_employment_dist = pd.crosstab(df['job_group'],df['employment_type'])
print("===== 직군별 고용형태 분포 =====")
print(job_employment_dist)

#하위직군별 고용 형태 분포 확인
subjob_employment_dist = pd.crosstab([df['job_group'],df['job_subgroup']],df['employment_type'])
print("===== 하위직군별 고용형태 분포 =====")
print(subjob_employment_dist)

