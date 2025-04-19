import pandas as pd
import re

#데이터프레임 가져오기
sample_data=pd.read_json('data/cleaned_data.json')
df = pd.DataFrame(sample_data)


# 단위 -> 연봉으로 통일
def parse_salary(salary):
    salary = salary.replace(',', '')
    
    # 연봉
    match_year = re.search(r'(\d+)만원', salary)
    if match_year:
        return int(match_year.group(1))
    
    # 월급
    match_month = re.search(r'월\s*(\d+)만원', salary)
    if match_month:
        return int(match_month.group(1)) * 12
    
    return None  # '협의' 등 처리 불가 항목

df['salary_num'] = df['salary'].apply(parse_salary)
df_clean = df.dropna(subset=['salary_num'])

#직군별 평균 연봉
df_jobgroup_avg = df_clean.groupby('job_group')['salary_num'].mean().round(1).reset_index()
df_jobgroup_avg.columns = ['job_group', 'avg_salary']
#하위 직군별 평균 연봉
df_subgroup_avg = df_clean.groupby(['job_group', 'job_subgroup'])['salary_num'].mean().round(1).reset_index()
df_subgroup_avg.columns = ['job_group', 'job_subgroup', 'avg_salary']

print("===== 직군별 평균 연봉 =====")
df_jobgroup_avg['avg_salary'] = df_jobgroup_avg['avg_salary'].astype(int).astype(str) + " 만원"
print(df_jobgroup_avg)

print("===== 하위 직군별 평균 연봉 =====")
df_subgroup_avg['avg_salary'] = df_subgroup_avg['avg_salary'].astype(int).astype(str) + " 만원"
print(df_subgroup_avg)


