import streamlit as st
import pandas as pd
import json
import os

# 경로 정의
SCRAPED_JOBS_PATH = "data/scraped_jobs.json"
APPLIED_JOBS_PATH = "data/applied_jobs.json"

# 파일 저장 함수
def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 파일 불러오기 함수
def load_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# 페이지 설정
st.set_page_config(page_title="나의 스크랩", layout="wide")
st.title("💾 나의 스크랩한 채용공고")

# 세션 상태 초기화
if "scraped_jobs" not in st.session_state:
    st.session_state["scraped_jobs"] = load_json(SCRAPED_JOBS_PATH)
if "applied_jobs" not in st.session_state:
    st.session_state["applied_jobs"] = load_json(APPLIED_JOBS_PATH)

saved_df = pd.DataFrame(st.session_state["scraped_jobs"])

# --------------------
# 📄 본문 표시
# --------------------
if saved_df.empty:
    st.info("아직 저장한 공고가 없습니다. '채용공고 찾기'에서 관심 공고를 저장해보세요!")
else:
    # 🔹 정렬 기준
    sort_option = st.selectbox("정렬 기준", ["회사명", "지역"])

    # 🔹 지원 상태 필터링
    status_filter = st.selectbox(
        "필터링 조건",
        ["전체 보기", "지원한 것만 보기", "지원하지 않은 것만 보기"]
    )

    # 정렬 적용
    saved_df = saved_df.sort_values(by=sort_option)

    # 지원 여부 필터링
    def is_applied(row):
        return row["채용공고"] in st.session_state["applied_jobs"]

    if status_filter == "지원한 것만 보기":
        saved_df = saved_df[saved_df.apply(is_applied, axis=1)]
    elif status_filter == "지원하지 않은 것만 보기":
        saved_df = saved_df[~saved_df.apply(is_applied, axis=1)]

    # 공고 출력
    for i, row in saved_df.iterrows():
        col1, col2 = st.columns([6, 1])
        with col1:
            st.markdown(f"""
            ### 📌 [{row['채용공고']}]({row['URL']})
            - **회사명:** {row['회사명']}
            - **지역:** {row['지역']} / **직군:** {row['직군']}
            - **고용형태:** {row['고용형태']} / **경력:** {row['경력']}
            """)

        with col2:
            # ✅ 지원 완료
            applied = is_applied(row)
            if st.checkbox("✅ 지원 완료", value=applied, key=f"applied_{i}"):
                if not applied:
                    st.session_state["applied_jobs"].append(row["채용공고"])
                    save_json(APPLIED_JOBS_PATH, st.session_state["applied_jobs"])
            else:
                if applied:
                    st.session_state["applied_jobs"].remove(row["채용공고"])
                    save_json(APPLIED_JOBS_PATH, st.session_state["applied_jobs"])

            # ❌ 삭제
            if st.button("🗑 삭제", key=f"delete_{i}"):
                st.session_state["scraped_jobs"].remove(row.to_dict())
                save_json(SCRAPED_JOBS_PATH, st.session_state["scraped_jobs"])
                st.rerun()

    st.markdown("---")
