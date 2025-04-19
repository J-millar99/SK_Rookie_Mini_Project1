#데이터 전처리
import json
import pandas as pd 
import re
from pprint import pprint

# row 데이터 가져오기
def load_raw_data(path: str) -> list:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

# 고용형태 정제 -> employment_type, probation
def clean_employment_type(raw_data: str) -> tuple:
    employment_type = raw_data.strip()
    probation=""
    probation_years = ""
    probation_months = ""
    probation_weeks = ""
    
    # 괄호 안에 내용이 있는 경우
    match = re.match(r'^([^\[\(]+)[\[\(]([^\]\)]+)[\]\)]$', employment_type)
    if match:
        employment_type = match.group(1).strip()
        raw_probation = match.group(2).strip()

        # 기간 정규표현식 우선 순위별 추출
        if "개월" in raw_probation:
            found = re.search(r'\d', raw_probation)
            probation_months = int(found.group()) if found else raw_probation
        elif "년" in raw_probation:
            found = re.search(r'\d', raw_probation)
            probation_years = int(found.group()) if found else raw_probation
        elif "주" in raw_probation:
            found = re.search(r'\d', raw_probation)
            probation_weeks = int(found.group()) if found else raw_probation
        elif "협의" in raw_probation:
            probation = "협의"
        else:
            probation = raw_probation  # fallback
    else:
        employment_type = employment_type  # 괄호 없는 경우

    return employment_type, probation, probation_months, probation_weeks, probation_years

# 도시명만 추출 -> 새로운 컬럼으로
def extract_city(raw_data: str) -> tuple:
    location = raw_data.strip()

    if '>' in location:
        left, right = map(str.strip, location.split('>'))

        # 오른쪽이 ~구, ~군 → 왼쪽 기준 추출
        if right.endswith(('구', '군')):
            match = re.match(r'([\w가-힣]+)(특별시|광역시|시)?', left)
            city = match.group(1) if match else left
            if city.endswith('시'):
                city = city[:-1]  # '시' 제거
        else:
            # 오른쪽이 도시명 (ex: 수원시)
            match = re.match(r'([\w가-힣]+)(시|군)?', right)
            city = match.group(1) if match else right
            if city.endswith('시'):
                city = city[:-1]
    else:
        # 단일 지역 (ex: 세종시, 부산광역시)
        match = re.match(r'([\w가-힣]+)(특별시|광역시|시|군|구)?', location)
        city = match.group(1) if match else location
        if city.endswith('시'):
            city = city[:-1]

    return city
    
# 경력조건 정제 
def clean_career(raw_data: str) -> tuple:
    career = raw_data.replace('\xa0', ' ').strip()  # 특수 공백 제거
    career = raw_data.replace('경력무관', '무관').replace('경력 ', '경력')

    if '무관' in career:
        return '무관'
    elif '신입' in career:
        return '신입'
    else:
        # 경력 5년↑ → 5년 이상
        match_over = re.match(r'경력\s*(\d+)년[↑|이상]?', career)
        if match_over:
            return f"{match_over.group(1)}년 이상"
        else:
            # 경력 5년~10년 → 5년 이상 10년 이하
            match_range = re.match(r'경력\s*(\d+)\s*~\s*(\d+)년', career)
            if match_range:
                return f"{match_range.group(1)}년 이상 {match_range.group(2)}년 이하"
            else:
                # 경력만 있는 경우
                return career.strip()    

# 학력 정제
def clean_education(raw_data: str) -> tuple:
    education = raw_data.strip()
    if "대졸" in education:
        return "대졸 이상"
    elif "초대졸" in education:
        return "초대졸"
    elif "고졸" in education:
        return "고졸 이상"
    elif "무관" in education or "학력무관" in education:
        return "무관"
    else:
        return education  # fallback (기타 처리)
        
# 데이터 전처리 
def clean_data(raw_data: list) -> pd.DataFrame:

    for item in raw_data:
        employment_type, probation, probation_months, probation_weeks, probation_years = clean_employment_type(item.get("employment_type", ""))
        item['employment_type'] = employment_type
        item['probation'] = probation
        item['probation_months'] = probation_months
        item['probation_years'] = probation_years
        item['probation_weeks'] = probation_weeks
        
        city= extract_city(item.get("location", ""))
        item['city']= city
        
        career = clean_career(item.get("career", ""))
        item["career"] =career
        
        education =clean_education(item.get("education", ""))
        item["education"] = education
    
        
    df = pd.DataFrame(raw_data)
    df.fillna("", inplace=True) # NaN 제거
    print("\nAfter Cleaning:")
    pprint(df.head(1).to_dict(orient="records"))  # Display the first row after cleaning
    return df

# 클린 데이터 저장 (Json)
def save_cleaned_data(df: pd.DataFrame, path: str) -> None:
    df.to_json(path, orient='records', force_ascii=False, indent=4)  # JSON 저장, 한글 깨짐 방지 
    

if __name__ == "__main__":
    raw_path = "../data/sample_dummy.json"
    save_path = "../data/cleaned_data.json"
    raw_data = load_raw_data(raw_path)
    df_clean = clean_data(raw_data)
    
    save_cleaned_data(df_clean, save_path)
    print(f"✅ 전처리 완료! 저장 위치: {save_path}")
    
