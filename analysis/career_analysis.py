import pandas as pd

#데이터프레임 가져오기
sample_data=pd.read_json('data/cleaned_data.json')
df = pd.DataFrame(sample_data)

#경력사항 분포 확인
print("===== 경력사항 분포 =====")
print(df['career'].value_counts())

#직군별 경력사항 분포 확인
job_career_dist = pd.crosstab(df['job_group'],df['career'])
print("===== 직군별 경력사항 분포 =====")
print(job_career_dist)

#직군별 평균 경력 요구 사항
career_to_year = {
    '1년 이상': 1,
    '2년 이상': 2,
    '3년 이상': 3,
    '4년 이상': 4,
    '5년 이상': 5,
    '무관': 0,
    '신입': 0
}

# 경력 연차 * 해당 count → 총합
numerator = job_career_dist.mul([career_to_year.get(c, 0) for c in job_career_dist.columns], axis=1).sum(axis=1)

# 전체 공고 수
denominator = job_career_dist.sum(axis=1)

# 평균 연차 = 총합 / 개수
job_group_avg_years = (numerator / denominator).round(2)
job_group_avg_years = job_group_avg_years.astype(str) + " 년"
print("===== 직군별 평균 경력 요구사항 =====")
print(job_group_avg_years)

#하위 직군별 경력사항 분포 확인
subjob_career_dist = pd.crosstab([df['job_group'],df['job_subgroup']],df['career'])
print("===== 하위 직군별 경력사항 분포 =====")
print(subjob_career_dist)

#하위 직군별 평균 경력 요구 사항
# 각 셀에 경력 연차 수치 곱하기
weighted = subjob_career_dist.mul([career_to_year.get(c, 0) for c in subjob_career_dist.columns], axis=1)

# 평균 = 총합 / 전체 공고 수
numerator = weighted.sum(axis=1)
denominator = subjob_career_dist.sum(axis=1)
subjob_avg_years = (numerator / denominator).round(2)

# 결과를 DataFrame으로 정리
df_subjob_avg = subjob_avg_years.reset_index()
df_subjob_avg.columns = ['job_group', 'job_subgroup', 'career_years']
df_subjob_avg['career_years']=df_subjob_avg['career_years'].astype(str) + " 년"
print("===== 하위 직군별 평균 경력 요구사항 =====")
print(df_subjob_avg)