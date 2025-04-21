import streamlit as st
import pandas as pd
import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

SCRAPED_JOBS_PATH = "data/scraped_jobs.json"

# 🔸 스크랩 저장 함수
def save_scraped_jobs_to_file():
    with open(SCRAPED_JOBS_PATH, "w", encoding="utf-8") as f:
        json.dump(st.session_state["scraped_jobs"], f, ensure_ascii=False, indent=2)

# 🔹 스크랩 세션 초기화
if "scraped_jobs" not in st.session_state:
    if os.path.exists(SCRAPED_JOBS_PATH):
        with open(SCRAPED_JOBS_PATH, "r", encoding="utf-8") as f:
            st.session_state["scraped_jobs"] = json.load(f)
    else:
        st.session_state["scraped_jobs"] = []

# 🔹 추천 결과 상태 저장용
if "recommended_jobs" not in st.session_state:
    st.session_state["recommended_jobs"] = []

st.set_page_config(page_title="맞춤 채용 추천", layout="wide")
st.title("🎯 맞춤 채용 추천 시스템")
st.markdown("당신의 정보와 경험을 바탕으로 어울리는 채용공고를 추천해드립니다.")

# 데이터 불러오기
@st.cache_data
def load_data():
    path = os.path.join("data", "cleaned_data.json")
    return pd.read_json(path)

df = load_data()

# 사용자 입력
name = st.text_input("이름을 입력해주세요")
interest = st.text_input("관심 직군 또는 분야를 입력해주세요 (예: 데이터 분석, 백엔드, 마케팅)")
spec = st.text_area("관심 직무 관련 경험이나 활동을 입력해주세요 (예: 프로젝트, 인턴 경험 등)")

# 추천 버튼 눌렀을 때만 추천 결과 세션에 저장
if st.button("🔍 추천받기"):
    if not interest and not spec:
        st.warning("관심 직군이나 활동 경험 중 하나 이상은 입력해야 합니다.")
    else:
        user_input = interest + " " + spec
        vectorizer = TfidfVectorizer(stop_words='english')
        documents = df["채용공고"] + " " + df["직군"] + " " + df["회사명"]
        tfidf_matrix = vectorizer.fit_transform(documents)
        user_vector = vectorizer.transform([user_input])

        similarities = cosine_similarity(user_vector, tfidf_matrix).flatten()
        top_indices = similarities.argsort()[::-1][:5]
        st.session_state["recommended_jobs"] = df.iloc[top_indices].to_dict(orient="records")
        st.success("추천 결과는 다음과 같아요!")

# 추천 결과가 있다면 계속 보여주기
if st.session_state["recommended_jobs"]:
    st.subheader(f"📋 {name or '사용자'} 님을 위한 추천 채용공고 Top 5")
    for i, job in enumerate(st.session_state["recommended_jobs"]):
        with st.expander(f"✅ {job['채용공고']} ({job['회사명']})"):
            st.markdown(f"""
            - **지역:** {job['지역']}  
            - **직군:** {job['직군']}  
            - **고용형태:** {job['고용형태']}  
            - **경력:** {job['경력']}  
            - **[공고 링크 바로가기]({job['URL']})**
            """)
            # ⭐ 스크랩 버튼
            if st.button("⭐ 스크랩하기", key=f"scrap_{i}"):
                if job not in st.session_state["scraped_jobs"]:
                    job["공고링크"] = f"[{job['채용공고']}]({job['URL']})"  # ✅ 필수!
                    st.session_state["scraped_jobs"].append(job)
                    save_scraped_jobs_to_file()
                    st.success("✅ 저장 완료!")
                else:
                    st.warning("⚠️ 이미 저장된 공고입니다.")
