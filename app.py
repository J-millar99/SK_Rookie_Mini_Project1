import streamlit as st
from datetime import datetime

# Page Config
st.set_page_config(
    page_title="잡파인드 - JobFind",
    page_icon="🎯",
    layout="wide"
)

# Custom Style (다크/라이트 모드 대응)
st.markdown("""
    <style>
    .big-title {
        font-size: 48px;
        font-weight: 900;
        color: var(--text-color);
        margin-bottom: 10px;
    }
    .subtitle {
        font-size: 20px;
        color: var(--text-color);
        margin-bottom: 30px;
    }
    .section-title {
        font-size: 24px;
        font-weight: bold;
        color: var(--text-color);
        margin-top: 40px;
        margin-bottom: 15px;
    }

    /* 기본 박스 스타일 */
    .feature-box {
        border: 1px solid var(--border-color);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        background-color: var(--box-bg);
        transition: all 0.3s ease;
    }

    .feature-box:hover {
        background-color: var(--box-hover);
        border-color: var(--primary-color);
    }

    /* 라이트 모드 변수 */
    body.streamlit-light {
        --text-color: #1F1F1F;
        --box-bg: #FAFAFA;
        --box-hover: #F0F8FF;
        --border-color: #E0E0E0;
        --primary-color: #3A5AFF;
    }

    /* 다크 모드 변수 */
    body.streamlit-dark {
        --text-color: #F0F0F0;
        --box-bg: #1E1E1E;
        --box-hover: #2A2A2A;
        --border-color: #444;
        --primary-color: #3A5AFF;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="big-title">🎯 잡파인드 JobFind 대시보드</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI 추천 기반 채용 탐색 플랫폼에 오신 것을 환영합니다.</div>', unsafe_allow_html=True)

st.markdown('<div class="subtitle">잡파인드는 여러분의 취업을 응원합니다 ૮꒰ྀི∩´ ꒳ `∩꒱ྀིა</div>', unsafe_allow_html=True)

st.markdown("---")

# Feature Section
st.markdown('<div class="section-title">📂 주요 메뉴</div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-box">
        <h4>🔍 find job</h4>
        <p>직군, 지역, 경력 조건 등으로 필터링된 채용공고를 확인하세요.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-box">
        <h4>📎 my scrap</h4>
        <p>스크랩한 공고를 한눈에 확인하고<br>
        지원 여부까지 표시할 수 있어요.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-box">
        <h4>🧠 recomand job</h4>
        <p>내가 입력한 관심 직무, 활동 경험을 바탕으로<br>
        인공지능이 최적의 공고를 추천합니다.</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption(f"© 2025 잡파인드 | Made with ❤️ by Team SK Rookies 조은지, 지재현, 황지영 | Last updated {datetime.now().strftime('%Y-%m-%d')}")
