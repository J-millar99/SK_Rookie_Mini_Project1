import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import platform
import os

# ✅ 한글 폰트 설정
def set_korean_font():
    if platform.system() == 'Darwin':  # macOS
        mpl.rc('font', family='AppleGothic')
    elif platform.system() == 'Windows':
        mpl.rc('font', family='Malgun Gothic')
    else:  # Linux
        mpl.rc('font', family='NanumGothic')
    plt.rcParams['axes.unicode_minus'] = False

set_korean_font()

# ✅ 엑셀 파일 읽기
df = pd.read_excel("data/지역분석.xlsx", sheet_name="서울 직군분포")

# ✅ 정렬 (큰 순서)
df = df.sort_values(by="서울 직군분포", ascending=True)



# ✅ 바 플롯 그리기
plt.figure(figsize=(10, 8))
bars = plt.barh(df['직군'], df['서울 직군분포'])

plt.title("서울 지역 직군별 채용공고 수", fontsize=16, fontweight='bold')
plt.xlabel("공고 수", fontsize=12)
plt.tight_layout()

# ✅ 이미지 저장
output_dir = "visualization/result"
os.makedirs(output_dir, exist_ok=True)
plt.savefig(os.path.join(output_dir, "서울_직군별_채용공고_수.png"))

plt.show()