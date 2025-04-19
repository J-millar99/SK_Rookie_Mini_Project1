import pandas as pd
import re

#데이터프레임 가져오기
sample_data=pd.read_json('data/cleaned_data.json')
df = pd.DataFrame(sample_data)

#경력사항 분포 확인
print("===== 경력사항 분포 =====")
print(df['경력'].value_counts())

#직군별 경력사항 분포 확인
job_career_dist = pd.crosstab(df['직군'],df['경력'])
print("===== 직군별 경력사항 분포 =====")
print(job_career_dist)

# 1. 경력 레이블 → 숫자 변환 함수
def extract_year_only(career_label):
    match = re.match(r'(\d+)년 이상', career_label)
    return int(match.group(1)) if match else None  # 무관, 신입은 None 반환

# 2. 숫자 매핑 (무관/신입 제외한 컬럼만 사용)
valid_columns = [col for col in job_career_dist.columns if extract_year_only(col) is not None]

# 3. 분자: 경력 연차 * 해당 수
numerator = job_career_dist[valid_columns].mul(
    [extract_year_only(col) for col in valid_columns],
    axis=1
).sum(axis=1)

# 4. 분모: 무관/신입 제외한 총 공고 수
denominator = job_career_dist[valid_columns].sum(axis=1)

# 5. 평균 연차 계산 (무관/신입 제외)
job_group_avg_years = (numerator / denominator).round(2)
job_group_avg_years = job_group_avg_years.fillna(0).astype(str) + " 년"

print("===== 직군별 평균 경력 요구사항 (무관/신입 제외) =====")
print(job_group_avg_years)

#하위 직군별 경력사항 분포 확인
subjob_career_dist = pd.crosstab([df['직군'],df['하위직군']],df['경력'])
print("===== 하위 직군별 경력사항 분포 =====")
print(subjob_career_dist)

# 1. 유효한 경력 컬럼 (숫자 매핑 가능한 'n년 이상'만 필터링)
valid_columns = [col for col in job_career_dist.columns if re.match(r'(\d+)년 이상', col)]

# 2. 숫자 변환 함수
def extract_year_only(career_label):
    match = re.match(r'(\d+)년 이상', career_label)
    return int(match.group(1)) if match else None

# 3. 직군-하위직군별 계산용 피벗 테이블 만들기
subgroup_dist = df[df["경력"].isin(valid_columns)].pivot_table(
    index=["직군", "하위직군"],
    columns="경력",
    aggfunc="size",
    fill_value=0
)

# 4. 분자: 각 경력 × count
numerator = subgroup_dist.mul(
    [extract_year_only(col) for col in subgroup_dist.columns],
    axis=1
).sum(axis=1)

# 5. 분모: 전체 count
denominator = subgroup_dist.sum(axis=1)

# 6. 평균 계산
avg_years = (numerator / denominator).round(2).fillna(0).astype(str) + " 년"

# 7. 데이터프레임 정리
df_subgroup_avg_years = avg_years.reset_index()
df_subgroup_avg_years.columns = ['직군', '하위직군', '평균경력']


print("===== 직군-하위직군별 평균 경력 요구사항 (무관/신입 제외) =====")
print(df_subgroup_avg_years)

# 같은 엑셀 파일에 시트로 추가
with pd.ExcelWriter('data/경력분석.xlsx', engine='openpyxl') as writer:
    df['경력'].value_counts().to_excel(writer, sheet_name='경력사항_분포')
    job_career_dist.to_excel(writer, sheet_name='직군별_경력사항_분포')
    subjob_career_dist.to_excel(writer, sheet_name='하위직군별_경력사항_분포')
    job_group_avg_years.to_excel(writer, sheet_name='직군별_평균_경력_요구사항')
    df_subgroup_avg_years.to_excel(writer, sheet_name='하위직군별_평균_경력_요구사항', index=False)

