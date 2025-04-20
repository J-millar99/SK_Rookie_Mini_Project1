# 데이터 전처리
import json
import pandas as pd
import re
from pprint import pprint


# row 데이터 가져오기
def load_raw_data(path: str) -> list:
    with open(path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    result = []

    # ✅ 최상위가 dict이면 바로 순회
    for big_category, sub_dict in raw_data.items():
        for small_category, jobs in sub_dict.items():
            for job in jobs:
                job["직군"] = big_category
                job["하위직군"] = small_category
                result.append(job)

    # 변환 완료 후 저장
    with open("data/raw_data.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    return result


# 고용형태 정제 -> employment_type, probation
def clean_employment_type(raw_data: str) -> tuple:
    employment_type = raw_data.strip()
    work_period = ""

    # 괄호 안 정보 추출
    match = re.match(r"^([^\[\(\s]+).*[\[\(]([^\]\)]+)[\]\)]", employment_type)
    if match:
        employment_type = match.group(1).strip()
        raw_inside = match.group(2).strip()

        # 년 -> 개월로 변환
        year_match = re.search(r"(\d+)\s*년", raw_inside)
        if year_match:
            months = int(year_match.group(1)) * 12
            work_period = f"{months}개월"
        else:
            # 개월이나 주 단위가 있는 경우
            period_match = re.search(r"\d+\s*(개월|주)", raw_inside)
            if period_match:
                work_period = period_match.group().replace(" ", "")
            elif "협의" in raw_inside:
                work_period = "협의"
            else:
                work_period = ""  # fallback
    else:
        employment_type = re.split(r"[\s\[\(]", employment_type)[0]

    return employment_type, work_period


# 도시명만 추출 -> 새로운 컬럼으로
def split_location(raw_location: str) -> tuple:
    raw_location = raw_location.strip()

    if ">" in raw_location:
        parts = raw_location.split(">")
        main_region = parts[0].strip()
        sub_region = parts[1].strip()

        # '외' 제거 + 양끝 공백 제거
        sub_region = re.sub(r"\s*외.*", "", sub_region).strip()
        return main_region, sub_region
    else:
        return raw_location, ""  # fallback



# 경력조건 정제
def clean_career(raw_data: str) -> str:
    career = raw_data.replace("\xa0", " ").strip()  # 특수 공백 제거
    career = career.replace("경력무관", "무관").replace("경력 ", "경력").replace("경력", "").strip()

    if not career:
        return "무관"
    
    if "무관" in career:
        return "무관"
    elif "신입" in career:
        return "신입"

    # 경력 5년~10년 → 5년 이상
    match_range = re.search(r"(\d+)\s*[~\-]\s*(\d+)년", career)
    if match_range:
        return f"{match_range.group(1)}년 이상"

    # 경력 3년 이상 5년 이하 → 3년 이상
    match_over_under = re.search(r"(\d+)년 이상\s*\d+년 이하", career)
    if match_over_under:
        return f"{match_over_under.group(1)}년 이상"

    # 경력 5년↑ 또는 5년 이상 → 5년 이상
    match_over = re.search(r"(\d+)년\s*(↑|이상)", career)
    if match_over:
        return f"{match_over.group(1)}년 이상"

    # 단일 숫자 년도만 있을 경우
    match_single = re.search(r"(\d+)년", career)
    if match_single:
        return f"{match_single.group(1)}년 이상"

    return career  # fallback


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
        (
            고용형태,
            근무기간
        ) = clean_employment_type(item.get("고용형태", ""))
        item["고용형태"] = 고용형태
        if 고용형태 == "정규직":
            item["수습기간"] = 근무기간
        else:
            item["근무기간"] = 근무기간

        (지역,하위지역) = split_location(item.get("근무지역", ""))
        item["지역"] = 지역
        item['하위지역'] = 하위지역

        career = clean_career(item.get("경력", ""))
        item["경력"] = career

        education = clean_education(item.get("학력", ""))
        item["학력"] = education

    df = pd.DataFrame(raw_data)
    df.fillna("", inplace=True)  # NaN 제거
    print("\nAfter Cleaning:")
    pprint(df.head(1).to_dict(orient="records"))  # Display the first row after cleaning
    return df


# 클린 데이터 저장 (Json)
def save_cleaned_data(df: pd.DataFrame, path: str) -> None:
    df.to_json(
        path, orient="records", force_ascii=False, indent=4
    )  # JSON 저장, 한글 깨짐 방지


if __name__ == "__main__":
    raw_path = "data/incruit_jobs.json"
    save_path = "data/cleaned_data.json"
    raw_data = load_raw_data(raw_path)
    df_clean = clean_data(raw_data)

    save_cleaned_data(df_clean, save_path)
    print(f"✅ 전처리 완료! 저장 위치: {save_path}")
