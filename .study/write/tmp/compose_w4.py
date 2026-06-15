"""Run: python compose_w4.py  → writes .blog/retrospective_w4.html"""
from __future__ import annotations
import sys, io, importlib.util
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HERE = Path(__file__).parent
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

b = load("build_w4", HERE / "build_w4.py")
c = load("build_w4_chapters", HERE / "build_w4_chapters.py")

# Build chapter 4 image insertions
img = b.img
ch2 = c.CH2.replace("__IMG_ERD_INITIAL__", img("erd_initial", "1차 ERD (디스코드 공유 원본)", 820, "1차 ERD — crawl_stat을 히스토리로 모델링하고 target_type 제약이 약했던 시점"))
ch3 = c.CH3.replace("__IMG_ERD_FINAL__", img("erd_final", "최종 ERD (README 게재본)", 820, "최종 ERD — regions FK 정규화 + crawl_stat 독립 + CHECK 제약"))
ch4 = (c.CH4
       .replace("__IMG_DASHBOARD__", img("dashboard_home", "Streamlit 대시보드 홈", 820, "대시보드 홈 — 좌측 사이드바 필터, 본문에 등록 현황·충전소·FAQ 4페이지 진입"))
       .replace("__IMG_SIDEBAR__",   img("sidebar", "사이드바 필터", 360, "사이드바 — 연도 슬라이더 · 지역 드롭다운 · 페이지 전환"))
       .replace("__IMG_REG_TREND__", img("registration_trend", "수소차 등록 추이 (연도별)", 820, "수소차 누적 등록 대수 추이 — Altair 선형 그래프"))
       .replace("__IMG_REGION_BAR__",img("region_bar", "지역별 등록 현황 (막대)", 820, "지역별 등록 현황 — 막대 차트"))
       .replace("__IMG_REGION_PIE__",img("region_pie", "지역별 비중 (파이)", 820, "지역별 비중 — 파이 차트"))
       .replace("__IMG_STATION_MAP__",img("station_map", "수소충전소 지도 (Folium)", 820, "수소충전소 지도 — Folium 마커 (lat/lon 컬럼 기반)"))
       .replace("__IMG_STATION_DETAIL__",img("station_detail", "충전소 선택 상세", 820, "충전소 선택 상세 — _station_key 매칭으로 안전하게 연동")))

html = (b.HEAD + b.COVER + "<main>" + b.TOC + b.INTRO
        + c.__dict__.get("CH1_OVERRIDE", b.CH1)
        + ch2 + ch3 + ch4
        + c.CH5 + c.CH6 + c.CH7 + c.CH8 + c.CH9
        + "</main>" + c.FOOTER)

out = b.OUT
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(html, encoding="utf-8")
print(f"written: {out}  size={out.stat().st_size:,} bytes")

# Quick checks
import re
http_imgs = len(re.findall(r'<img[^>]+src="https?://', html))
file_imgs = len(re.findall(r'<img[^>]+src="(?!data:)[^"]+(?<!\.html)"', html))
b64_imgs  = len(re.findall(r'<img[^>]+src="data:image/', html))
term_box  = len(re.findall(r'class="terminal"', html))
term_body = len(re.findall(r'class="terminal-body"', html))
print(f"img src=http*://  : {http_imgs}  (must be 0)")
print(f"img src=non-data  : {file_imgs}  (must be 0)")
print(f"img src=data:image: {b64_imgs}")
print(f"terminal box / body: {term_box} / {term_body}")
