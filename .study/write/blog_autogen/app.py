"""Streamlit UI — 기술 블로그 자동 생성기."""
from __future__ import annotations

import sys
import traceback
from pathlib import Path

# 패키지 경로 보장 (streamlit run 실행 시 cwd 기준)
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st

from blog_autogen.llm import LLMClient, LLMConfig, PROVIDER_MODELS
from blog_autogen.notes_loader import load_notes
from blog_autogen.pipeline import (
    BLOG_DIR,
    WORKSPACE,
    make_plan,
    build_runner,
    run_runner,
    generate_html,
)

NOTES_DIR = WORKSPACE / ".study" / "notes"

st.set_page_config(page_title="기술 블로그 자동 생성기", layout="wide")
st.title("📝 기술 블로그 HTML 자동 생성기")
st.caption("GUIDE.txt 규칙에 따라 LLM 으로 챕터·코드·HTML 을 만들고 실제 실행 로그까지 자동 삽입합니다.")

# ─── 사이드바: AI 설정 ─────────────────────────────
with st.sidebar:
    st.header("🔑 AI 설정")
    provider = st.selectbox("Provider", list(PROVIDER_MODELS.keys()), index=0,
                            format_func=lambda x: {"openai": "OpenAI", "anthropic": "Anthropic", "gemini": "Google Gemini"}[x])
    model = st.selectbox("모델", PROVIDER_MODELS[provider])
    api_key = st.text_input("API Key", type="password",
                            help="브라우저 세션 메모리에만 유지되며 저장되지 않습니다.")
    temperature = st.slider("temperature", 0.0, 1.0, 0.3, 0.05)
    max_tokens = st.number_input("max_tokens", 1000, 64000, 16000, 1000)

    st.divider()
    st.header("📁 경로")
    st.code(f"GUIDE: {WORKSPACE}\\.study\\GUIDE.txt", language="text")
    st.code(f"출력 : {BLOG_DIR}", language="text")

# ─── 메인: 입력 ──────────────────────────────────
mode = st.radio("입력 방식", ["주제만 입력", "노트 파일 사용"], horizontal=True)

topic = ""
notes_text = ""

if mode == "주제만 입력":
    topic = st.text_input("주제 (한 줄)", placeholder="예: 파이썬 데코레이터 동작 원리")
else:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.write(f"노트 폴더: `{NOTES_DIR}`")
        if NOTES_DIR.exists():
            files = sorted(
                [p for p in NOTES_DIR.iterdir()
                 if p.suffix.lower() in (".mhtml", ".txt", ".docx")],
                key=lambda p: p.name,
            )
        else:
            files = []
        selected = st.selectbox("노트 파일", files, format_func=lambda p: p.name if p else "")
        topic_extra = st.text_input("추가 주제 지시 (선택)",
                                    placeholder="예: 모듈 실행 흐름 위주로")
    with col2:
        if selected:
            try:
                notes_text = load_notes(selected)
                st.text_area("노트 내용 미리보기 (앞 4000자)",
                             notes_text[:4000], height=320)
            except Exception as e:
                st.error(f"노트 로드 실패: {e}")
    topic = topic_extra or (selected.stem if selected else "")

st.divider()

# ─── 단계별 실행 ────────────────────────────────
if "plan" not in st.session_state:
    st.session_state.plan = None
    st.session_state.runner_path = None
    st.session_state.run_result = None
    st.session_state.html_path = None
    st.session_state.log_buffer = []


def log(msg: str):
    st.session_state.log_buffer.append(msg)


def _client() -> LLMClient:
    if not api_key:
        st.error("API Key 를 입력하세요.")
        st.stop()
    return LLMClient(LLMConfig(
        provider=provider, model=model, api_key=api_key,
        temperature=temperature, max_tokens=int(max_tokens),
    ))


c1, c2, c3, c4 = st.columns(4)

with c1:
    if st.button("1️⃣ 기획서 생성", use_container_width=True, type="primary"):
        if not topic:
            st.error("주제 또는 노트를 입력하세요.")
        else:
            try:
                with st.spinner("LLM 호출 중…"):
                    plan = make_plan(_client(), topic, notes_text)
                st.session_state.plan = plan
                log(f"[plan] slug={plan.slug}, 챕터 {len(plan.chapters)}개")
                st.success("기획서 생성 완료")
            except Exception as e:
                st.error(f"기획서 생성 실패: {e}")
                st.code(traceback.format_exc())

with c2:
    if st.button("2️⃣ Runner 작성·실행", use_container_width=True,
                 disabled=st.session_state.plan is None):
        try:
            plan = st.session_state.plan
            runner_path = build_runner(plan)
            st.session_state.runner_path = runner_path
            log(f"[runner] {runner_path}")
            with st.spinner("runner.py 실행 중…"):
                result = run_runner(runner_path, log_cb=log)
            st.session_state.run_result = result
            log(f"[run] returncode={result.returncode}, 로그 {len(result.log_files)}개")
            st.success(f"runner 실행 완료 (rc={result.returncode})")
        except Exception as e:
            st.error(f"runner 실행 실패: {e}")
            st.code(traceback.format_exc())

with c3:
    if st.button("3️⃣ HTML 생성", use_container_width=True,
                 disabled=st.session_state.run_result is None):
        try:
            with st.spinner("최종 HTML 생성 중…"):
                html_path = generate_html(
                    _client(),
                    st.session_state.plan,
                    st.session_state.run_result,
                    log_cb=log,
                )
            st.session_state.html_path = html_path
            log(f"[html] {html_path}")
            st.success(f"저장 완료: {html_path}")
        except Exception as e:
            st.error(f"HTML 생성 실패: {e}")
            st.code(traceback.format_exc())

with c4:
    if st.button("🔄 전체 초기화", use_container_width=True):
        for k in ("plan", "runner_path", "run_result", "html_path"):
            st.session_state[k] = None
        st.session_state.log_buffer = []
        st.rerun()

st.divider()

# ─── 결과 패널 ───────────────────────────────────
tabs = st.tabs(["📋 기획서", "🧪 실행 로그", "🌐 HTML 결과", "🪵 콘솔"])

with tabs[0]:
    if st.session_state.plan:
        plan = st.session_state.plan
        st.subheader(plan.title or plan.slug)
        st.caption(plan.subtitle)
        st.write(f"**slug**: `{plan.slug}` · **챕터**: {len(plan.chapters)}개")
        st.json(plan.raw)
    else:
        st.info("아직 기획서가 없습니다. 1단계를 실행하세요.")

with tabs[1]:
    rr = st.session_state.run_result
    if rr:
        st.write(f"**returncode**: {rr.returncode}")
        st.write(f"**runner**: `{rr.runner_path}`")
        for name, content in rr.log_files.items():
            with st.expander(f"📄 {name}.txt"):
                st.code(content or "(empty)", language="text")
        with st.expander("🖥 stdout 전체"):
            st.code(rr.stdout, language="text")
    else:
        st.info("아직 실행 결과가 없습니다.")

with tabs[2]:
    hp = st.session_state.html_path
    if hp and Path(hp).exists():
        html = Path(hp).read_text(encoding="utf-8")
        st.write(f"**파일**: `{hp}` ({len(html):,} bytes)")
        st.download_button("HTML 다운로드", data=html, file_name=Path(hp).name,
                           mime="text/html")
        with st.expander("HTML 소스 미리보기 (앞 8000자)"):
            st.code(html[:8000], language="html")
        with st.expander("🖼 렌더링 미리보기"):
            st.components.v1.html(html, height=900, scrolling=True)
    else:
        st.info("아직 HTML 이 없습니다.")

with tabs[3]:
    st.code("\n".join(st.session_state.log_buffer) or "(비어 있음)", language="text")
