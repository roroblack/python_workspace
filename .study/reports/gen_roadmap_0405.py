# gen_roadmap_0405.py — 04~05월 학습 로드맵 다이어그램 생성
# 실행: c:\_proj\python_workspace\.venv\Scripts\python.exe .study\reports\gen_roadmap_0405.py
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import pathlib

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

OUT = pathlib.Path(__file__).parent / "assets"
OUT.mkdir(exist_ok=True)

# (라벨, 시작주차idx, 길이, 색, 교과목)
C1 = "#5B9BD5"   # 교과목1 프로그래밍·데이터 기초
C2 = "#52A97E"   # 교과목2 데이터분석·머신러닝
ACC = "#E8875A"  # 프로젝트/마일스톤

# 행: 단원 트랙
rows = [
    ("교과목1 · 단원1 Python",      0.0, 2.0, C1, ["logic·collection·fileio", "oop·module·package·gui·streamlit"]),
    ("교과목1 · 단원2 DB(MySQL)",   2.0, 1.0, C1, ["intro·B+Tree·제약·SELECT·JOIN·서브쿼리"]),
    ("교과목1 · 단원3 Web Crawling",3.0, 1.0, C1, ["static·dynamic·selector·HTML 파싱"]),
    ("교과목1 단위 프로젝트(팀)",   3.4, 0.7, ACC, ["SKN32-1st-3Team · 수집·ERD·웹앱·발표"]),
    ("교과목2 · 단원1 데이터분석",   4.0, 1.0, C2, ["numpy·pandas·전처리·이상치·정규화·시각화"]),
    ("교과목2 · 단원2 머신러닝",     5.0, 1.2, C2, ["Day1 회귀·데이터관리 / Day2 분류·로지스틱 / Day3 SVM"]),
]

fig, ax = plt.subplots(figsize=(13, 6.2))
week_labels = ["1주차\n~04/30", "2주차\n05/04~08", "3주차\n05/11~15", "4주차\n05/16~19",
               "5주차\n05/20~26", "6주차\n05/27~"]
nW = len(week_labels)

for i, (name, x, w, color, items) in enumerate(rows):
    y = len(rows) - 1 - i
    box = FancyBboxPatch((x, y + 0.12), w, 0.76, boxstyle="round,pad=0.02,rounding_size=0.04",
                         linewidth=1.5, edgecolor=color, facecolor=color + "22")
    ax.add_patch(box)
    ax.text(x + 0.06, y + 0.66, name, fontsize=10.5, fontweight='bold', color="#1f2933", va='center')
    ax.text(x + 0.06, y + 0.31, " · ".join(items), fontsize=8.3, color="#374151", va='center')

# 세로 주차 격자 + 라벨
for k in range(nW + 1):
    ax.axvline(k, color="#d7dee8", lw=0.8, zorder=0)
for k, lab in enumerate(week_labels):
    ax.text(k + 0.5, len(rows) + 0.18, lab, ha='center', va='bottom', fontsize=9, color="#667085")

ax.set_xlim(0, nW); ax.set_ylim(0, len(rows) + 0.7)
ax.set_yticks([]); ax.set_xticks([])
for s in ax.spines.values(): s.set_visible(False)
ax.set_title("SK 네트웍스 AI Family 32기 — 04~05월 학습 로드맵 (교과목1 전 과정 + 교과목2 시작)",
             fontsize=13, fontweight='bold', pad=26, color="#1f2933")

# 범례
from matplotlib.patches import Patch
ax.legend(handles=[Patch(facecolor=C1 + "22", edgecolor=C1, label="교과목1 · 프로그래밍과 데이터 기초"),
                   Patch(facecolor=C2 + "22", edgecolor=C2, label="교과목2 · 데이터분석·머신러닝"),
                   Patch(facecolor=ACC + "22", edgecolor=ACC, label="단위 프로젝트")],
          loc='lower left', fontsize=8.5, framealpha=0.95)

fig.tight_layout()
p = OUT / "roadmap_0405.png"
fig.savefig(p, dpi=130, bbox_inches='tight'); plt.close(fig)
print("저장:", p)
