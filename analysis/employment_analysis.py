import pandas as pd

# 데이터프레임 가져오기
sample_data = pd.read_json('data/cleaned_data.json')
df = pd.DataFrame(sample_data)
VALID_EMPLOYMENT_TYPES = ['정규직', '계약직', '인턴', '위촉직', '프리랜서', '병역특례', '교육생']
df = df[df['고용형태'].isin(VALID_EMPLOYMENT_TYPES)]

# 고용 형태 분포 확인
print("===== 고용형태 분포 =====")
print(df['고용형태'].value_counts())

# 직군별 고용 형태 분포 확인
job_employment_dist = pd.crosstab(df['직군'], df['고용형태'])
print("===== 직군별 고용형태 분포 =====")
print(job_employment_dist)

# 하위직군별 고용 형태 분포 확인
subjob_employment_dist = pd.crosstab([df['직군'], df['하위직군']], df['고용형태'])
print("===== 하위직군별 고용형태 분포 =====")
print(subjob_employment_dist)

# 정규직 수습기간 분석
regular_employees = df[df['고용형태'] == '정규직']

if '수습기간' in regular_employees.columns:
    # 0개월 또는 빈 문자열을 "없음"으로 통일
    probation_dist = regular_employees['수습기간'].fillna("").replace(["", "0개월"], "없음")

    # 분포 정리 및 출력
    probation_analysis = (
        probation_dist.value_counts().sort_index().reset_index()
    )
    probation_analysis.columns = ['수습기간', '공고 수']

    print("===== 정규직 수습기간 분포 (개월 수) =====")
    print(probation_analysis)
else:
    print("수습기간 데이터가 없습니다.")

# 계약직, 인턴 근무기간 분석
contract_intern = df[df['고용형태'].isin(['계약직', '인턴'])]

if '근무기간' in contract_intern.columns:
    # 결측치 또는 빈값 처리
    work_period_dist = contract_intern['근무기간'].fillna("").replace("", "없음")

    # value_counts로 분포 정리
    work_period_analysis = (
        work_period_dist.value_counts().sort_index().reset_index()
    )
    work_period_analysis.columns = ['근무기간', '공고 수']

    print("===== 계약직/인턴 근무기간 분포 =====")
    print(work_period_analysis)
else:
    print("근무기간 데이터가 없습니다.")
    
    
# 엑셀로 저장
with pd.ExcelWriter('data/고용형태.xlsx') as writer:
    df['고용형태'].value_counts().to_frame('고용형태 분포').to_excel(writer, sheet_name='고용형태 분포')
    job_employment_dist.to_excel(writer, sheet_name='직군별 고용형태 분포')
    subjob_employment_dist.to_excel(writer, sheet_name='하위직군별 고용형태 분포')
    probation_analysis.to_excel(writer, sheet_name='정규직 수습기간 분포',index=False)
    work_period_analysis.to_excel(writer,sheet_name='계약직_인턴 근무기간 분포', index=False)