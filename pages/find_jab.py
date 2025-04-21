import streamlit as st
import pandas as pd
import os
import math
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import json

def save_scraped_jobs_to_file():
    with open("data/scraped_jobs.json", "w", encoding="utf-8") as f:
        json.dump(st.session_state["scraped_jobs"], f, ensure_ascii=False, indent=2)



# Load Data
# --------------------
@st.cache_data
def load_data():
    path = os.path.join("data", "cleaned_data.json")
    return pd.read_json(path)

df = load_data()
df["공고링크"] = df.apply(lambda row: f"[{row['채용공고']}]({row['URL']})", axis=1)

# --------------------
# Sidebar - Filters
# --------------------
with st.sidebar:
    st.title("🔍 필터")

    col1, col2 = st.columns(2)
    with col1:
        region = st.selectbox("지역", ["전체"] + sorted(df["지역"].dropna().unique().tolist()))
    with col2:
        job_type = st.selectbox("직군", ["전체"] + sorted(df["직군"].dropna().unique().tolist()))

    keyword = st.text_input("회사명 또는 공고명 키워드")
    employment = st.selectbox("고용형태", ["전체"] + sorted(df["고용형태"].dropna().unique().tolist()))
    experience = st.selectbox("경력", ["전체"] + sorted(df["경력"].dropna().unique().tolist()))

    st.markdown("---")
    st.markdown("**정렬 옵션**")
    sort_company = st.checkbox("회사명 가나다순 정렬", value=False)
    sort_region = st.checkbox("지역 가나다순 정렬", value=False)

    st.markdown("---")
    st.markdown("**페이지네이션 설정**")
    rows_per_page = st.selectbox("페이지 당 행 수", [10, 20, 50], index=0)

# --------------------
# Filter Logic
# --------------------
filtered = df.copy()

# 필터 적용
if region != "전체":
    filtered = filtered[filtered["지역"] == region]
if job_type != "전체":
    filtered = filtered[filtered["직군"] == job_type]
if keyword:
    filtered = filtered[
        filtered["회사명"].str.contains(keyword, case=False, na=False) |
        filtered["채용공고"].str.contains(keyword, case=False, na=False)
    ]
if employment != "전체":
    filtered = filtered[filtered["고용형태"] == employment]
if experience != "전체":
    filtered = filtered[filtered["경력"] == experience]

if sort_company:
    filtered = filtered.sort_values(by="회사명")
if sort_region:
    filtered = filtered.sort_values(by="지역")

# --------------------
# Main Layout
# --------------------
st.title(":dart: 잡파인드 채용공고 대시보드")
st.markdown("인크루트 기반 채용공고 데이터를 활용한 시각화 대시보드입니다.")
st.markdown("---")

# --------------------
# 📊 공고 분포 요약 (항상 보여줌)
# --------------------
st.subheader(":bar_chart: 공고 분포 요약")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("회사 수", f"{filtered['회사명'].nunique()}개")
with col2:
    st.metric("경력 필요 공고 수", f"{(filtered['경력'] != '무관').sum()}건")
with col3:
    st.metric("직군 수", f"{filtered['직군'].nunique()}개")

st.markdown("---")

# --------------------
# 📁 채용공고 목록 (항상 표시)
# --------------------
st.subheader("📁 채용공고 목록")
st.markdown("- 공고 제목을 클릭하면 해당 채용 사이트로 이동합니다.")
st.markdown("- 관심 공고는 스랩하여 저장할 수 있습니다.")

if "scraped_jobs" not in st.session_state:
    st.session_state["scraped_jobs"] = []

total_rows = filtered.shape[0]
total_pages = math.ceil(total_rows / rows_per_page)

# ✅ 페이지 선택 바: - / + 버튼 유지하며 좌우 간결하게
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    page_num = st.number_input("페이지 선택", min_value=1, max_value=max(1, total_pages), value=1, step=1)

start_idx = (page_num - 1) * rows_per_page
end_idx = start_idx + rows_per_page
paged_data = filtered.iloc[start_idx:end_idx]

# 채용공고 목록 출력 + 스크랩 버튼
for idx, row in paged_data.iterrows():
    with st.expander(f"📌 {row['채용공고']} ({row['회사명']})"):
        st.markdown(f"""
        **지역:** {row['지역']}  
        **직군:** {row['직군']}  
        **고용형태:** {row['고용형태']}  
        **경력:** {row['경력']}  
        **[공고 링크 바로가기]({row['URL']})**
        """)
        if st.button("⭐ 스크랩하기", key=f"scrap_{idx}"):
            job_dict = row.to_dict()
            if job_dict not in st.session_state["scraped_jobs"]:
                st.session_state["scraped_jobs"].append(job_dict)
                save_scraped_jobs_to_file()  # 파일 저장!
                st.success("✅ 저장 완료!")
            else:
                st.warning("⚠️ 이미 저장된 공고입니다.")


st.caption(f"총 {total_rows}건 중 {start_idx + 1} ~ {min(end_idx, total_rows)}건 표시 중")

st.markdown("---")

# --------------------
# 지도 & 그래프: 초기 상태일 때만 출력
# --------------------
is_initial_state = (
    region == "전체" and
    job_type == "전체" and
    not keyword and
    employment == "전체" and
    experience == "전체"
)

if is_initial_state:
    # 📍 지도
    st.subheader(":round_pushpin: 지역별 채용공고 분포 지도")
    region_counts = df["지역"].value_counts().reset_index()
    region_counts.columns = ["지역", "공고수"]

    region_coords = pd.read_csv("data/region_coords.csv")
    map_data = region_counts.merge(region_coords, left_on="지역", right_on="지역명", how="left").dropna(subset=["위도", "경도"])

    m = folium.Map(location=[36.5, 127.8], zoom_start=7)
    marker_cluster = MarkerCluster().add_to(m)

    for _, row in map_data.iterrows():
        folium.Marker(
            location=[row["위도"], row["경도"]],
            popup=f"{row['지역']} ({row['공고수']}건)",
            tooltip=row["지역"]
        ).add_to(marker_cluster)

    st_folium(m, width=1000, height=500)
    st.markdown("---")

    # 📊 막대 그래프
    st.subheader(":bar_chart: 지역별 공고 수 시각화")

    # 한글 폰트 설정 (macOS는 AppleGothic)
    mpl.rc('font', family='AppleGothic')
    plt.rcParams['axes.unicode_minus'] = False

    plt.style.use("ggplot")  # 또는 'seaborn', 'fivethirtyeight', 'bmh'


    fig, ax = plt.subplots(figsize=(10, 5))

    region_counts_sorted = region_counts.sort_values("공고수", ascending=False)

    bars = ax.bar(region_counts_sorted["지역"], region_counts_sorted["공고수"],
                  color='skyblue', edgecolor='black')

    #ax.bar(region_counts_sorted["지역"], region_counts_sorted["공고수"], color='skyblue')

    ax.set_xlabel("지역")
    ax.set_ylabel("공고 수")
    ax.set_title("지역별 채용공고 수")

    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, yval + 2, int(yval),
                ha='center', va='bottom', fontsize=9)
    # 바 위에 값 표시 이후에 바로 추가!
    ax.set_xticklabels(region_counts_sorted["지역"], rotation=45, ha='right')

    st.pyplot(fig)
    st.markdown("---")

# --------------------
# Footer
# --------------------
st.caption("© 2025 잡파인드 | Created by Team SK Rookies")
