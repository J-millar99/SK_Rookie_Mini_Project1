#지역별 채용공고
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm
import platform
import os


# ✅ OS별 폰트 설정
def set_korean_font():
    os_name = platform.system()
    if os_name == "Darwin":  # macOS
        mpl.rc('font', family='AppleGothic')
    elif os_name == "Windows":
        mpl.rc('font', family='Malgun Gothic')
    else:  # Linux or 기타
        mpl.rc('font', family='NanumGothic')
    plt.rcParams['axes.unicode_minus'] = False  # 음수 깨짐 방지

set_korean_font()

# 엑셀 불러오기
df = pd.read_excel("data/지역분석.xlsx", sheet_name="지역별 채용공고수")


# NaN 또는 빈 문자열 제거
df = df.dropna(subset=['지역'])
df = df[df['지역'].astype(str).str.strip() != ""]

# 상위 10개 지역 추출
top10 = df.nlargest(10, '채용공고수').copy()
top10_names = top10['지역'].tolist()

# 기타 지역 집계
df['지역'] = df['지역'].astype(str)
df['기타'] = df['지역'].apply(lambda x: '기타' if x not in top10_names else x)
grouped = df.groupby('기타')['채용공고수'].sum().reset_index()

# ✅ 원형 그래프 그리기
fig, ax = plt.subplots(figsize=(9, 9))

# 그룹 수에 맞춰 색상 생성
cmap = cm.get_cmap('tab10')  # 또는 'Set3', 'Pastel1', 'Accent' 등 가능
colors = [cmap(i / len(grouped)) for i in range(len(grouped))]

wedges, texts, autotexts = ax.pie(
    grouped['채용공고수'],
    labels=grouped['기타'],
    autopct='%1.1f%%',
    startangle=140,
    textprops={'fontsize': 12},  # 라벨 글씨 크기
    pctdistance=0.8,  # 퍼센트 위치 조절
    labeldistance=1.05,
    colors=colors
)

# ✅ 퍼센트 텍스트 크기 조절
for autotext in autotexts:
    autotext.set_fontsize(11)

# ✅ 제목
plt.title("지역별 채용공고 비율", fontsize=16, fontweight='bold')
plt.axis('equal')  # 동그란 비율 유지
plt.tight_layout()

output_dir = "visualization/result"
os.makedirs(output_dir, exist_ok=True)
fig.savefig(os.path.join(output_dir, "지역별_채용공고_비율.png"), dpi=300, bbox_inches='tight')

# ✅ 시각화 표시
plt.show()