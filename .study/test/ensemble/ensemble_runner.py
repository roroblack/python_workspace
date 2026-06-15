# ensemble_runner.py
# 머신러닝 Day5 (0602) — 알고리즘과 앙상블(배깅·부스팅·랜덤포레스트) 섹션별 테스트 실행기
# 실행: c:\_proj\python_workspace\.venv\Scripts\python.exe ensemble_runner.py
# 결과: logs/{섹션명}.txt 저장 + 터미널 출력,  charts/*.png 생성
# 데이터: sklearn 내장 load_breast_cancer / load_wine — 외부 파일 의존 없이 재현 가능(고정 시드 42)
#   ※ 0602-s 노트북(German Credit + RandomForest/Bagging/AdaBoost/GradientBoosting)과 동일한
#     앙상블 구성을 따르되, 재현성을 위해 sklearn 내장 데이터로 새로 작성(§16-C 우선순위 2, 사유 명시).

import sys, io, pathlib
from contextlib import redirect_stdout

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
# 차트 한글 렌더링 (Windows 기본 한글 폰트)
matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False

from sklearn.datasets import load_breast_cancer, load_wine
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (BaggingClassifier, RandomForestClassifier,
                              AdaBoostClassifier, GradientBoostingClassifier)
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

HERE = pathlib.Path(__file__).parent
LOGS = HERE / "logs"; LOGS.mkdir(exist_ok=True)
CHARTS = HERE / "charts"; CHARTS.mkdir(exist_ok=True)
SEED = 42


def run_section(name, fn):
    sep = "=" * 60
    buf = io.StringIO()
    print(sep); print(f"# {name}"); print(sep)
    with redirect_stdout(buf):
        try:
            fn()
        except Exception as e:
            print(f"{type(e).__name__}: {e}")
    out = buf.getvalue()
    sys.stdout.write(out)
    (LOGS / f"{name}.txt").write_text(sep + "\n" + f"# {name}" + "\n" + sep + "\n" + out, encoding="utf-8")


def _split(loader=load_breast_cancer):
    """공통 데이터 분할 — train/test 고정(시드 42)."""
    d = loader()
    Xtr, Xte, ytr, yte = train_test_split(
        d.data, d.target, test_size=0.25, random_state=SEED, stratify=d.target)
    return d, Xtr, Xte, ytr, yte


# ── §00: 데이터 준비 + 단일 결정트리는 정말 불안정한가 ────────────────────
def s00_single_tree():
    """앙상블의 출발점 — 단일 결정트리. 깊이 제한이 없으면 train 을 거의 완벽히 외우지만(과대적합)
    test 는 떨어진다. 또 random_state 만 바꿔도 트리 구조가 흔들려 정확도가 출렁인다(분산이 크다)."""
    d, Xtr, Xte, ytr, yte = _split()
    print(f"[데이터] load_breast_cancer  X{d.data.shape}  클래스 {list(d.target_names)}")
    print(f"  train {Xtr.shape[0]}개 / test {Xte.shape[0]}개\n")

    # 깊이 제한 없는 단일 트리 — train 을 외운다
    full = DecisionTreeClassifier(random_state=SEED).fit(Xtr, ytr)
    tr = accuracy_score(ytr, full.predict(Xtr))
    te = accuracy_score(yte, full.predict(Xte))
    print(f"[단일 트리·깊이무제한] train acc={tr:.4f}  test acc={te:.4f}  과대적합 gap={tr-te:+.4f}")
    print(f"  트리 깊이={full.get_depth()}  리프(터미널 노드) 수={full.get_n_leaves()}\n")

    # seed 만 바꿔도 test 정확도가 출렁인다 → 분산이 크다(불안정)
    accs = []
    for s in range(10):
        t = DecisionTreeClassifier(random_state=s).fit(Xtr, ytr)
        accs.append(accuracy_score(yte, t.predict(Xte)))
    accs = np.array(accs)
    print(f"[단일 트리·seed 0~9] test acc 범위 {accs.min():.4f} ~ {accs.max():.4f}")
    print(f"  평균={accs.mean():.4f}  표준편차={accs.std():.4f}  (seed 만 바뀌어도 흔들림 = 높은 분산)")


# ── §01: 배깅(Bagging) — 여러 트리를 부트스트랩으로 모으면 분산이 줄까 ─────
def s01_bagging():
    """배깅 = 부트스트랩 표본으로 같은 약한 모델 여러 개를 독립 학습 후 다수결.
    한 트리의 출렁임(분산)을 평균으로 깎는다. 단일 트리 vs 배깅의 test 정확도·안정성을 비교한다."""
    d, Xtr, Xte, ytr, yte = _split()

    one = DecisionTreeClassifier(random_state=SEED).fit(Xtr, ytr)
    one_te = accuracy_score(yte, one.predict(Xte))
    print(f"[기준] 단일 트리 test acc = {one_te:.4f}\n")

    bag = BaggingClassifier(
        estimator=DecisionTreeClassifier(random_state=SEED),
        n_estimators=100, random_state=SEED).fit(Xtr, ytr)
    bag_tr = accuracy_score(ytr, bag.predict(Xtr))
    bag_te = accuracy_score(yte, bag.predict(Xte))
    print(f"[배깅·트리 100개] train acc={bag_tr:.4f}  test acc={bag_te:.4f}  gap={bag_tr-bag_te:+.4f}")
    print(f"  단일 트리 대비 test 변화: {bag_te-one_te:+.4f}\n")

    # 배깅도 seed 를 바꿔 안정성 비교 (단일 트리와 같은 실험)
    accs = []
    for s in range(10):
        b = BaggingClassifier(
            estimator=DecisionTreeClassifier(random_state=s),
            n_estimators=100, random_state=s).fit(Xtr, ytr)
        accs.append(accuracy_score(yte, b.predict(Xte)))
    accs = np.array(accs)
    print(f"[배깅·seed 0~9] test acc 범위 {accs.min():.4f} ~ {accs.max():.4f}")
    print(f"  표준편차={accs.std():.4f}  (단일 트리보다 출렁임이 작으면 → 분산 감소 확인)")


# ── §02: 랜덤포레스트 — 배깅에 특성 무작위까지, 그리고 n_estimators 효과 ───
def s02_random_forest():
    """랜덤포레스트 = 배깅 + 각 분기에서 특성도 무작위 일부만 본다 → 트리들이 더 서로 달라진다(상관↓).
    n_estimators(트리 수)를 늘리며 test 정확도가 어디서 수렴하는지 본다."""
    d, Xtr, Xte, ytr, yte = _split()

    counts = [1, 5, 10, 25, 50, 100, 200, 400]
    te_scores = []
    print(f"{'n_estimators':>13} | {'train acc':>9} | {'test acc':>9}")
    print("-" * 40)
    for n in counts:
        rf = RandomForestClassifier(n_estimators=n, random_state=SEED).fit(Xtr, ytr)
        tr = accuracy_score(ytr, rf.predict(Xtr))
        te = accuracy_score(yte, rf.predict(Xte))
        te_scores.append(te)
        print(f"{n:>13} | {tr:9.4f} | {te:9.4f}")
    print(f"\n트리 1개 → {te_scores[0]:.4f},  트리 400개 → {te_scores[-1]:.4f}  "
          f"(향상 {te_scores[-1]-te_scores[0]:+.4f})")

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(counts, te_scores, "o-", color="#52A97E", lw=2)
    ax.set_xscale("log")
    ax.set_xlabel("n_estimators (트리 개수, 로그축)"); ax.set_ylabel("test 정확도")
    ax.set_title("랜덤포레스트 — 트리 수↑ → 정확도 수렴")
    ax.grid(alpha=0.3); fig.tight_layout()
    fig.savefig(CHARTS / "ch_n_estimators.png", dpi=110); plt.close(fig)
    print("[chart] ch_n_estimators.png 저장")


# ── §03: 부스팅 — 이전 오차에 집중하는 순차 학습(AdaBoost·GBM) ───────────
def s03_boosting():
    """부스팅 = 약한 학습기를 순차로 쌓되, 이전 모델이 틀린 샘플에 가중치를 더 준다 → 편향을 줄인다.
    얕은 트리(깊이 1~3)로도 깊은 단일 트리를 능가하는지, AdaBoost·GradientBoosting 으로 확인한다."""
    d, Xtr, Xte, ytr, yte = _split()

    stump = DecisionTreeClassifier(max_depth=1, random_state=SEED).fit(Xtr, ytr)
    print(f"[약한 학습기 1개] 깊이1 그루터기(stump) test acc = {accuracy_score(yte, stump.predict(Xte)):.4f}\n")

    ada = AdaBoostClassifier(
        estimator=DecisionTreeClassifier(max_depth=1, random_state=SEED),
        n_estimators=200, random_state=SEED).fit(Xtr, ytr)
    ada_tr = accuracy_score(ytr, ada.predict(Xtr))
    ada_te = accuracy_score(yte, ada.predict(Xte))
    print(f"[AdaBoost·그루터기 200개] train acc={ada_tr:.4f}  test acc={ada_te:.4f}  gap={ada_tr-ada_te:+.4f}")
    print("  → 약한 학습기(깊이1) 하나는 시원찮지만, 순차로 모으니 강해진다\n")

    gbm = GradientBoostingClassifier(
        n_estimators=200, max_depth=3, learning_rate=0.1, random_state=SEED).fit(Xtr, ytr)
    gbm_tr = accuracy_score(ytr, gbm.predict(Xtr))
    gbm_te = accuracy_score(yte, gbm.predict(Xte))
    print(f"[GradientBoosting·깊이3·200개] train acc={gbm_tr:.4f}  test acc={gbm_te:.4f}  gap={gbm_tr-gbm_te:+.4f}")
    print("  → GBM 은 이전 단계의 '잔차'를 다음 트리가 예측하도록 순차 보강")


# ── §04: 한 자리 비교 — 단일 트리 vs 배깅 vs RF vs AdaBoost vs GBM ────────
def s04_compare():
    """같은 train/test 위에서 다섯 모델의 test 정확도와 과대적합 gap(train-test)을 한 번에 비교한다.
    '여러 모델을 모으면 단일 트리보다 나은가, 과대적합도 줄어드는가'에 대한 최종 표."""
    d, Xtr, Xte, ytr, yte = _split()

    models = {
        "단일 결정트리": DecisionTreeClassifier(random_state=SEED),
        "배깅(트리100)": BaggingClassifier(
            estimator=DecisionTreeClassifier(random_state=SEED),
            n_estimators=100, random_state=SEED),
        "랜덤포레스트(트리200)": RandomForestClassifier(n_estimators=200, random_state=SEED),
        "AdaBoost(그루터기200)": AdaBoostClassifier(
            estimator=DecisionTreeClassifier(max_depth=1, random_state=SEED),
            n_estimators=200, random_state=SEED),
        "GradientBoosting(200)": GradientBoostingClassifier(
            n_estimators=200, max_depth=3, learning_rate=0.1, random_state=SEED),
    }
    names, te_list, gap_list = [], [], []
    print(f"{'모델':<24} | {'train':>7} | {'test':>7} | {'gap(과대적합)':>12}")
    print("-" * 62)
    for name, m in models.items():
        m.fit(Xtr, ytr)
        tr = accuracy_score(ytr, m.predict(Xtr))
        te = accuracy_score(yte, m.predict(Xte))
        names.append(name); te_list.append(te); gap_list.append(tr - te)
        print(f"{name:<24} | {tr:7.4f} | {te:7.4f} | {tr-te:>+12.4f}")

    best = names[int(np.argmax(te_list))]
    print(f"\n최고 test 정확도: {best} ({max(te_list):.4f})")
    print(f"단일 트리 gap {gap_list[0]:+.4f} → 앙상블들의 gap 이 더 작으면 과대적합 완화 확인")

    # 차트 1 — 모델별 test 정확도
    short = ["단일\n트리", "배깅", "랜덤\n포레스트", "Ada\nBoost", "Gradient\nBoosting"]
    colors = ["#E8875A", "#5B9BD5", "#52A97E", "#9178C4", "#52A97E"]
    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.bar(short, te_list, color=colors, alpha=0.9)
    for b, v in zip(bars, te_list):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.001, f"{v:.3f}", ha="center", fontsize=9)
    ax.set_ylim(min(te_list) - 0.02, 1.0)
    ax.set_ylabel("test 정확도"); ax.set_title("모델별 test 정확도 비교 (breast_cancer)")
    fig.tight_layout(); fig.savefig(CHARTS / "ch_model_compare.png", dpi=110); plt.close(fig)
    print("[chart] ch_model_compare.png 저장")

    # 차트 2 — 과대적합 gap
    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.bar(short, gap_list, color=colors, alpha=0.9)
    for b, v in zip(bars, gap_list):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.0005, f"{v:.3f}", ha="center", fontsize=9)
    ax.set_ylim(0, max(gap_list) * 1.25)
    ax.set_ylabel("train - test (과대적합 gap)")
    ax.set_title("과대적합 gap — 작을수록 일반화가 좋다")
    fig.tight_layout(); fig.savefig(CHARTS / "ch_overfit_gap.png", dpi=110); plt.close(fig)
    print("[chart] ch_overfit_gap.png 저장")


# ── §05: 특성 중요도 — 랜덤포레스트가 본 '어떤 특성이 중요했나' ──────────
def s05_feature_importance():
    """랜덤포레스트는 부산물로 feature_importances_ 를 준다(분기에서 불순도를 얼마나 줄였나의 합).
    breast_cancer 30개 특성 중 상위 10개를 뽑아 무엇이 진단에 크게 기여했는지 본다."""
    d, Xtr, Xte, ytr, yte = _split()
    rf = RandomForestClassifier(n_estimators=300, random_state=SEED).fit(Xtr, ytr)
    imp = rf.feature_importances_
    order = np.argsort(imp)[::-1]
    print(f"중요도 합계 = {imp.sum():.4f}  (전체 특성 중요도의 합은 1)\n")
    print(f"{'순위':>3} | {'특성':<24} | {'중요도':>8}")
    print("-" * 44)
    for rank, i in enumerate(order[:10], 1):
        print(f"{rank:>3} | {d.feature_names[i]:<24} | {imp[i]:8.4f}")

    top = order[:10][::-1]
    fig, ax = plt.subplots(figsize=(7, 4.6))
    ax.barh([d.feature_names[i] for i in top], imp[top], color="#9178C4", alpha=0.9)
    ax.set_xlabel("특성 중요도 (불순도 감소 기여)")
    ax.set_title("랜덤포레스트 특성 중요도 상위 10")
    fig.tight_layout(); fig.savefig(CHARTS / "ch_feature_importance.png", dpi=110); plt.close(fig)
    print("[chart] ch_feature_importance.png 저장")


if __name__ == "__main__":
    run_section("00_single_tree", s00_single_tree)
    run_section("01_bagging", s01_bagging)
    run_section("02_random_forest", s02_random_forest)
    run_section("03_boosting", s03_boosting)
    run_section("04_compare", s04_compare)
    run_section("05_feature_importance", s05_feature_importance)
    print("\n완료: logs/*.txt, charts/*.png 생성")
