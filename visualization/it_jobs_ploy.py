import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import platform
import os
import seaborn as sns

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
df = pd.read_excel("data/IT직군.xlsx", sheet_name="Sheet1")

# ✅ IT직군별 하위직군 개수 비교
# ✅ IT 직군을 많이 뽑는 회사명 상위 5개
top_companies = df['회사명'].value_counts().head(5).reset_index()
top_companies.columns = ['회사명', '공고수']

# ✅ 시각화 (상위 5개 회사)
plt.figure(figsize=(8, 5))
barplot = sns.barplot(data=top_companies, x='공고수', y='회사명', palette='Blues_d')

# 막대 위에 공고수 표시
for p in barplot.patches:
    barplot.annotate(format(int(p.get_width()), '.0f'), 
                     (p.get_width(), p.get_y() + p.get_height() / 2.), 
                     ha='center', va='center', 
                     xytext=(8, 0), 
                     textcoords='offset points')

# x축 눈금을 정수로 설정
barplot.set_xticks(range(0, int(top_companies['공고수'].max()) + 1, 1))

plt.title('IT 직군 채용 회사 상위 5개')
plt.xlabel('공고수')
plt.ylabel('회사명')
plt.tight_layout()


output_dir = "visualization/result"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "IT직군_회사_상위_5개.png")
plt.savefig(output_path, dpi=300)

plt.show()


# ✅ 상위 5개 회사의 하위직군 집계
top_companies_list = top_companies['회사명'].tolist()
filtered_df = df[df['회사명'].isin(top_companies_list)]
sub_roles_count = filtered_df.groupby(['회사명', '하위직군']).size().reset_index(name='공고수')


# 상위 5개 회사의 하위직군 분포

# 데이터 피벗: 하위직군을 인덱스로, 회사명을 컬럼으로, 공고수 값으로
pivot_df = sub_roles_count.pivot(index='하위직군', columns='회사명', values='공고수').fillna(0)
pivot_df['총합'] = pivot_df.sum(axis=1)
pivot_df = pivot_df.sort_values(by='총합', ascending=False).drop(columns='총합')

# 색상 설정
colors = sns.color_palette('Set2', n_colors=len(pivot_df.columns))

# 누적 바 차트
pivot_df.plot(kind='barh', stacked=True, figsize=(12, 8), color=colors)

# 총 공고수 표시 (각 막대 끝에)
totals = pivot_df.sum(axis=1)
for i, (value, name) in enumerate(zip(totals, pivot_df.index)):
    plt.text(value, i, f"{int(value)}건", va='center')

plt.title('상위 5개 회사의 하위직군 분포 (스택형)', fontsize=14)
plt.xlabel('공고수')
plt.ylabel('하위직군')
plt.legend(title='회사명', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

output_path_sub_roles = os.path.join(output_dir, "상위_5개_회사_하위직군_분포.png")
plt.savefig(output_path_sub_roles, dpi=300)
plt.show()