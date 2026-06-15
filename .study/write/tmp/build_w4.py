"""Build retrospective_w4.html with inline base64 images and full content from blog_w4.txt."""
from __future__ import annotations
import base64, json, re
from pathlib import Path

ROOT = Path(r"c:\_proj\python_workspace")
ASSETS = ROOT / ".study" / "write" / "tmp" / "w4_assets"
OUT = ROOT / ".blog" / "retrospective_w4.html"

imgs = json.loads((ASSETS / "images.json").read_text(encoding="utf-8"))

def img(key: str, alt: str, max_w: int = 820, cap: str | None = None) -> str:
    e = imgs[key]
    src = f"data:{e['mime']};base64,{e['b64']}"
    fig = f'<figure class="shot"><img src="{src}" alt="{alt}" '
    fig += f'style="display:block;width:100%;height:auto;max-width:{max_w}px;margin:0 auto;border:1px solid var(--line);" />'
    if cap:
        fig += f'<figcaption>{cap}</figcaption>'
    fig += '</figure>'
    return fig

CSS = r"""
@import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic+Coding:wght@400;700&display=swap');
:root {
  color-scheme: light;
  --ink:#1f2933; --muted:#667085; --line:#d7dee8;
  --paper:#ffffff; --surface:#ffffff;
  --accent:#52A97E; --accent-2:#E8875A; --accent-3:#5B9BD5; --accent-4:#9178C4;
  --accent-soft:#EBF7F1; --warn-soft:#FFF1E8;
  --code-bg:#1e1e1e; --code-ink:#e5e7eb; --shadow:none;
}
* { box-sizing:border-box; }
body { margin:0; background:var(--paper); color:var(--ink);
  font-family:"Nanum Gothic Coding","Segoe UI",Arial,sans-serif;
  line-height:1.78; font-size:16px; }
a { color:var(--accent-3); text-underline-offset:3px; }
.page { width:min(880px, calc(100% - 32px)); margin:0 auto; }
header.cover { padding:48px 0 24px; border-bottom:3px solid var(--ink); }
.eyebrow { font-size:0.9rem; color:var(--muted); letter-spacing:0.06em;
  text-transform:uppercase; margin:0 0 8px; }
h1 { font-size:2rem; line-height:1.32; margin:6px 0 12px; letter-spacing:-0.01em; }
.deck { font-size:1.05rem; color:#374151; margin:0 0 18px; }
.meta-row { display:flex; flex-wrap:wrap; gap:12px 18px;
  font-size:0.92rem; color:var(--muted); padding-top:10px;
  border-top:1px solid var(--line); }
.meta-row strong { color:var(--ink); margin-right:6px; }
main { padding:36px 0 60px; }
nav.toc { border-top:3px solid var(--ink); border-bottom:1px solid var(--line);
  padding:14px 0 18px; margin:0 0 30px; }
nav.toc h2 { font-size:0.95rem; letter-spacing:0.06em;
  text-transform:uppercase; color:var(--muted); margin:0 0 8px; }
nav.toc ol { list-style:none; padding:0; margin:0;
  display:grid; grid-template-columns:repeat(2,1fr); gap:4px 16px; font-size:0.95rem; }
nav.toc a { color:var(--ink); text-decoration:none; border-bottom:1px dashed transparent; }
nav.toc a:hover { border-bottom-color:var(--accent-3); }
section { margin:48px 0 0; }
h2.chap { font-size:1.45rem; margin:0 0 14px; padding:14px 0 8px;
  border-top:3px solid var(--ink); position:relative; }
h2.chap .num { display:inline-block; border:2px solid var(--accent);
  color:var(--accent); padding:1px 8px; font-size:0.8rem;
  margin-right:10px; vertical-align:middle; letter-spacing:0.04em; }
h2.chap .anchor-link { float:right; color:var(--muted); font-weight:400;
  text-decoration:none; opacity:0; transition:opacity .15s; }
h2.chap:hover .anchor-link { opacity:1; }
h3.step { margin:22px 0 10px; font-size:1.05rem; letter-spacing:0.04em;
  color:var(--accent-3); border-left:4px solid var(--accent-3); padding-left:10px; }
p { margin:10px 0; }
ul, ol { padding-left:1.4em; }
li { margin:4px 0; }
strong { color:var(--ink); }
.qbox { border-left:4px solid var(--accent-3); background:#EBF4FF;
  padding:12px 16px; margin:14px 0; }
.qbox .label { display:inline-block; background:var(--accent-3); color:#fff;
  padding:1px 8px; font-size:0.78rem; font-weight:700;
  margin-right:10px; letter-spacing:0.04em; }
.keypoint { border-left:4px solid var(--accent); background:var(--accent-soft);
  padding:12px 16px; margin:14px 0; }
.keypoint .label { display:inline-block; background:var(--accent); color:#fff;
  padding:1px 8px; font-size:0.78rem; font-weight:700;
  margin-right:10px; letter-spacing:0.04em; }
.callout { border-left:4px solid var(--accent-2); background:var(--warn-soft);
  padding:12px 16px; margin:14px 0; }
.callout .label { display:inline-block; background:var(--accent-2); color:#fff;
  padding:1px 8px; font-size:0.78rem; font-weight:700;
  margin-right:10px; letter-spacing:0.04em; }
.bridge { border-left:4px solid var(--muted); background:#F4F6F9;
  padding:10px 14px; margin:18px 0 4px; font-size:0.94rem; color:#374151; }
.bridge strong { color:var(--ink); }
blockquote.cite { border-left:4px solid var(--accent-4); background:#F7F5FD;
  padding:12px 16px; margin:14px 0; font-style:normal; }
blockquote.cite .src { display:block; color:var(--muted);
  font-size:0.9em; margin-top:6px; }
code { font-family:"Cascadia Code","Consolas","D2Coding",monospace;
  background:#EEF0F6; padding:1px 5px; font-size:0.92em; }
pre { background:var(--code-bg); color:var(--code-ink); padding:16px;
  overflow-x:auto; font-size:0.88rem; line-height:1.55; margin:14px 0;
  border:1px solid #2a2a2a; }
pre code { background:transparent; padding:0; color:inherit;
  font-family:"Cascadia Code","Consolas","D2Coding",monospace; }
.terminal { margin:14px 0; border:1px solid #2a2a2a; }
.terminal-header { background:#2d2d2d; color:#cbd5e1; padding:6px 12px;
  font-size:0.82rem; font-family:"Cascadia Code","Consolas",monospace; }
.terminal-header::before { content:'PS> '; color:var(--accent); font-weight:700; }
.terminal-body { background:#1e1e1e; color:#e5e7eb; padding:14px 16px;
  margin:0; overflow-x:auto; font-size:0.86rem; line-height:1.55;
  font-family:"Cascadia Code","Consolas","D2Coding",monospace; white-space:pre; }
table { border-collapse:collapse; width:100%; margin:14px 0; font-size:0.95rem; }
th, td { border:1px solid var(--line); padding:6px 10px; text-align:left;
  vertical-align:top; }
th { background:#EEF0F5; color:var(--ink); }
.figcaption, figure.shot figcaption { color:var(--muted); font-size:0.88rem;
  text-align:center; margin-top:6px; }
figure.shot { margin:14px 0; }
footer { padding:30px 0 60px; border-top:3px solid var(--ink); margin-top:50px;
  color:var(--muted); font-size:0.9rem; }
footer p { margin:6px 0; }
.ref-chain { border-left:4px solid var(--accent-4); background:#F7F5FD;
  padding:14px 18px; margin:24px 0; }
.ref-chain .ref-title { color:var(--accent-4); font-weight:700;
  margin:0 0 8px; letter-spacing:0.04em; }
.ref-chain ol { padding-left:1.4em; margin:0; }
.ref-chain li { margin:4px 0; font-size:0.93rem; }
"""

HEAD = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>0516-0519 회고: 카데이터 팀 "물로간다" — 수소차 등록 현황 · 충전소 · FAQ 통합 대시보드</title>
  <meta name="description" content="SKN32 1st 단위 프로젝트 4주차(2026/05/15~19) 회고. 팀 카데이터의 '물로간다' 프로젝트로 국토교통부·공공데이터포털·EV 통합누리집에서 수소차 등록 현황·충전소·FAQ를 수집해 MySQL에 저장하고 Streamlit으로 시각화. ERD 정규화, 프로토타입, 깃 브런치 전략, 11건의 디버깅 사례와 마스터 직푸시 사건까지 정리." />
  <meta property="og:title" content="0516-0519 회고: 카데이터 팀 '물로간다' 단위 프로젝트" />
  <meta property="og:description" content="ERD 설계 · Streamlit + MySQL + Playwright + Folium 대시보드 · 11건 디버깅 회고." />
  <meta property="og:type" content="article" />
  <meta name="twitter:card" content="summary" />
  <meta name="twitter:title" content="0516-0519 회고: 카데이터 팀 '물로간다' 단위 프로젝트" />
  <meta name="twitter:description" content="ERD 설계 · Streamlit + MySQL + Playwright + Folium 대시보드 · 11건 디버깅 회고." />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Nanum+Gothic+Coding:wght@400;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css" />
  <style>{CSS}</style>
</head>
<body>
<div class="page">
"""

COVER = """
<header class="cover">
  <p class="eyebrow">Python · 4주차 회고 · 부트캠프 · 단위 프로젝트</p>
  <h1>0516-0519 회고: 카데이터 팀 &ldquo;물로간다&rdquo; — 수소차 등록 현황 · 충전소 · FAQ 통합 대시보드</h1>
  <p class="deck">이 글은 SKN32 1차 교과목 단위 프로젝트(2026/05/15~19) 회고다. 한 주의 출발 목표 한 줄에서 시작해, ERD 정규화 → 프로토타입 → 살붙이기 → 11건의 디버깅 → 발표·시연 → 종합 회고까지 학습 사슬을 따라간다.</p>
  <div class="meta-row">
    <span><strong>작성일자</strong> 2026/05/25</span>
    <span><strong>기간</strong> 2026/05/15(금) ~ 05/19(화)</span>
    <span><strong>팀</strong> 카데이터 · 프로젝트 물로간다</span>
    <span><strong>HW</strong> Asrock x600 · Ryzen 8600G · 24GB · RTX 4070 Super</span>
    <span><strong>SW</strong> Win11 25H2 · Python 3.14.2 · PowerShell · Streamlit 1.57 · MySQL 8.0 · Playwright 1.59</span>
  </div>
</header>
"""

TOC = """
<nav class="toc">
  <h2>목차</h2>
  <ol>
    <li><a href="#ch1">CH01 — 팀 프로젝트 시작 &amp; 팀 구성</a></li>
    <li><a href="#ch2">CH02 — 처음 한 일: ERD부터 시작한 이유</a></li>
    <li><a href="#ch3">CH03 — ERD 완성과 폴더·파일 명명 규칙</a></li>
    <li><a href="#ch4">CH04 — 프로토타입: Streamlit + MySQL + Playwright 뼈대</a></li>
    <li><a href="#ch5">CH05 — 일정·회의·협업 도구 (스프레드시트 · 깃 브런치)</a></li>
    <li><a href="#ch6">CH06 — 디버깅 11건 + 마스터 직푸시 사건</a></li>
    <li><a href="#ch7">CH07 — 발표 준비와 마지막 날의 위태로움</a></li>
    <li><a href="#ch8">CH08 — 회고: 잘한 점 / 부족했던 점 / 다음 한 수</a></li>
    <li><a href="#ch9">CH09 — 총 정리</a></li>
  </ol>
</nav>
"""

INTRO = """
<div class="bridge">
  <strong>한 주의 출발 목표</strong> — &ldquo;4명이 4일 안에, 크롤링·DB·웹앱 한 흐름을 발표 가능한 형태로 완성한다.&rdquo; 이 문장이 가능하려면 ① 주제와 ERD를 첫 2일 안에 굳히고, ② 프로토타입으로 모든 팀원이 같은 코드 기반 위에 서고, ③ 협업 채널(스프레드시트·브런치)과 디버깅 노트가 끊기지 않아야 한다. 각 챕터는 이 세 조건이 어떻게 검증되고, 어디서 깨졌는지 따라간다.
</div>
"""

CH1 = """
<section id="ch1">
  <h2 class="chap"><span class="num">CH 01</span>팀 프로젝트 시작 &amp; 팀 구성<a href="#ch1" class="anchor-link">#</a></h2>

  <h3 class="step">학습</h3>
  <p>2026-05-15(금) 강의 시간에 팀이 발표되었다. 같은 날 안에 팀명·프로젝트명·주제·역할 분담까지 끝내야 했다. 스프레드시트로 정리한 최종 팀 정보는 다음과 같다.</p>

  <table>
    <thead><tr><th>항목</th><th>내용</th></tr></thead>
    <tbody>
      <tr><td>팀명</td><td>카데이터</td></tr>
      <tr><td>프로젝트명</td><td>물로간다</td></tr>
      <tr><td>주제</td><td>한국 자동차 등록 현황 및 기업 FAQ 조회 시스템 (수소차로 좁힘)</td></tr>
      <tr><td>발표일</td><td>2026-05-19 (팀당 발표 10분 + Q&amp;A 10분)</td></tr>
      <tr><td>저장소</td><td><a href="https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN32-1st-3Team" target="_blank" rel="noopener">SKNETWORKS-FAMILY-AICAMP/SKN32-1st-3Team</a></td></tr>
    </tbody>
  </table>

  <p>팀장은 내가 맡기로 했고, 팀원들이 각자 역할을 정했다. 4명이라는 작은 규모라 한 사람이 두세 가지를 겸하는 것을 전제로 분담했다.</p>

  <table>
    <thead><tr><th>역할</th><th>이름</th><th>담당</th></tr></thead>
    <tbody>
      <tr><td>👑 팀장</td><td>최연우</td><td>Streamlit GUI · 수소차 충전소 맵 파트(DB · 크롤링 포함) · 발표 · 시연 · Q&amp;A</td></tr>
      <tr><td>🗄️ 팀원</td><td>권소라</td><td>MySQL DB 설계 · 저장 · PPT</td></tr>
      <tr><td>🕷️ 팀원</td><td>김지혜</td><td>크롤링 (bs4, Playwright) · 발표(개요)</td></tr>
      <tr><td>🔗 팀원</td><td>박회종</td><td>Python ↔ MySQL 연동 조회 시스템 · 시연 HW</td></tr>
    </tbody>
  </table>

  <p>팀장인 나는 <strong>GUI</strong> 와 수소차 충전소 맵 파트(해당 DB 및 크롤링 포함)를 전담하게 되었다. &ldquo;팀장이 가장 많이 한다&rdquo;가 아니라 &ldquo;발표·시연·Q&amp;A 같이 흐름 전체를 알아야 하는 자리&rdquo;를 같이 가져간 셈이다.</p>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox"><span class="label">가설</span>
    4일이라는 시간 안에 4명이 한 프로덕트를 완성하려면 첫날의 결정 셋 — <strong>(1) 주제 좁히기 · (2) 역할의 1차 분담 · (3) 다음 회의 시점</strong> — 이 그 자리에서 끝나야 한다. 어느 하나라도 다음 회의로 밀리면 4일이 3일로 줄어든다.
  </div>

  <h3 class="step">시행</h3>
  <p>주제 후보로 (가) 전기차와 충전소, (나) 연료별 자동차 등록 현황, (다) 수소차와 그 현황이 올라왔다. 등록 대수 규모가 가장 작아 시각화 사례로 다루기 용이하고 충전 인프라까지 묶을 수 있다는 점에서 <strong>수소차</strong>로 좁혔다. 같은 자리에서 페이지 구성 아이디어도 정했다.</p>
  <ul>
    <li>수소차 충전소 지도(Folium) 페이지</li>
    <li>수소차 등록 현황 그래프 페이지(연도·지역)</li>
    <li>차종별 / 사용목적별 분석은 표본이 작아 통계적 유의미성이 부족 → <strong>기각</strong></li>
    <li>FAQ 페이지(키워드 검색 포함)</li>
    <li>크롤링은 가능한 범위는 BeautifulSoup4 정적 크롤링, 막히는 부분만 Playwright 자동 크롤링</li>
    <li>robots.txt 확인하여 허용된 사이트만 수집</li>
    <li>발표는 자원자가 없어 내가 맡기로 함 (CH07 발표 라인업 참조)</li>
  </ul>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint"><span class="label">KEY POINT — 가설 통과</span>
    첫날에 주제·페이지 구성·1차 역할 분담이 모두 한 자리에서 닫혔다. 다음 회의는 16(토) 19:30 디스코드로 잡혔고, 그 사이 백엔드 팀원이 &ldquo;ERD부터 그리자&rdquo;고 제안하면서 다음 챕터의 의문이 만들어졌다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — &ldquo;첫 코드보다 ERD가 먼저&rdquo;라는 백엔드 팀원의 말은 4일짜리 프로젝트에서도 옳을까? 가설은 &ldquo;ERD가 굳어야 크롤러·앱이 같은 컬럼 위에서 돌 수 있다&rdquo;.
  </div>
</section>
"""
