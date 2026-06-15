"""블로그 자동 생성 파이프라인.

3단계:
  1) plan(): LLM 으로 블로그 기획 JSON 생성
  2) build_and_run_runner(): JSON → <주제>_runner.py 작성 후 실제 실행
  3) generate_html(): 실행 로그를 함께 LLM 에 전달, 최종 HTML 생성·저장
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from .llm import LLMClient

WORKSPACE = Path(r"c:\_proj\python_workspace")
GUIDE_PATH = WORKSPACE / ".study" / "GUIDE.txt"
BLOG_DIR = WORKSPACE / ".study" / "blog"
TEST_DIR = WORKSPACE / ".study" / "test"
VENV_PY = WORKSPACE / ".venv" / "Scripts" / "python.exe"


@dataclass
class Plan:
    slug: str
    title: str
    subtitle: str
    category: str
    tags: str
    starter_question: str
    chapters: list[dict] = field(default_factory=list)
    final_conclusion: str = ""
    references: list[dict] = field(default_factory=list)
    raw: dict = field(default_factory=dict)

    @classmethod
    def from_json(cls, data: dict) -> "Plan":
        return cls(
            slug=_slugify(data.get("slug") or data.get("title", "blog")),
            title=data.get("title", ""),
            subtitle=data.get("subtitle", ""),
            category=data.get("category", "자습 노트(Self-Study)"),
            tags=data.get("tags", "Python"),
            starter_question=data.get("starter_question", ""),
            chapters=data.get("chapters", []),
            final_conclusion=data.get("final_conclusion", ""),
            references=data.get("references", []),
            raw=data,
        )


@dataclass
class RunResult:
    runner_path: Path
    logs_dir: Path
    log_files: dict[str, str]
    stdout: str
    returncode: int


# ──────────────────────────────────────────────────────────
# helpers
# ──────────────────────────────────────────────────────────
def _slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9가-힣]+", "_", text)
    return text.strip("_") or "blog"


def _read_guide() -> str:
    return GUIDE_PATH.read_text(encoding="utf-8")


def _extract_json(text: str) -> dict:
    """LLM 출력에서 JSON 블록을 안전하게 추출."""
    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if m:
        return json.loads(m.group(1))
    m = re.search(r"(\{.*\})", text, re.DOTALL)
    if m:
        return json.loads(m.group(1))
    raise ValueError(f"JSON 을 찾을 수 없음:\n{text[:400]}")


def _extract_html(text: str) -> str:
    """LLM 출력에서 HTML 문서 추출."""
    m = re.search(r"```html\s*(.*?)```", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    m = re.search(r"(<!DOCTYPE html.*?</html>)", text, re.DOTALL | re.IGNORECASE)
    if m:
        return m.group(1).strip()
    return text.strip()


# ──────────────────────────────────────────────────────────
# Step 1 — plan
# ──────────────────────────────────────────────────────────
PLAN_SYSTEM = """당신은 파이썬 기술 블로그 작성 전문가다.
사용자가 제공하는 GUIDE.txt 규칙(서사 사슬 구조, Swiss Style, 인라인 인용,
검증 가능한 가설, 실제 실행 로그 삽입)을 엄격히 따라야 한다.
모든 출력은 한국어로 작성한다.
출력은 오직 JSON 한 덩어리. 마크다운 설명·서두 없이 JSON 만 출력한다."""


PLAN_USER_TMPL = """다음 GUIDE.txt 규칙을 준수하며 새 블로그 글의 '기획서'를 JSON 으로 작성하라.

[GUIDE.txt — 일부 발췌]
{guide}

[작성 대상]
주제(또는 자유 입력): {topic}

[참고 노트 (있을 경우)]
{notes}

[요구 출력 JSON 스키마]
{{
  "slug": "영문 소문자/숫자/언더스코어로 된 파일명 (예: abstraction)",
  "title": "검색 가능한 기술 용어가 포함된 제목 (GUIDE §10)",
  "subtitle": "독자 이득이 명확한 부제",
  "category": "Self-Study 또는 Bootcamp/주차",
  "tags": "콤마 구분 태그",
  "starter_question": "글 전체가 회수할 한 줄짜리 출발 의문 (workspace 코드 한 줄 권장)",
  "chapters": [
    {{
      "id": "ch1",
      "title": "독자의 궁금증을 자극하는 챕터 제목",
      "section_name": "01_topic_part",          // runner 로그 파일명 (snake_case)
      "learning": "학습 본문 핵심 주장(2~4문장)",
      "citations": [
        {{ "quote": "원문 그대로 인용", "url": "https://docs.python.org/...", "source": "출처명" }}
      ],
      "hypothesis": "통과하려면 ①②③ 이 모두 일어나야 한다 — 검증 가능한 진술",
      "test_code": "from __future__ import annotations\\nprint('...')\\n# 가설을 직접 검증하는 파이썬 코드. 외부 패키지 의존 금지(표준 라이브러리만). UTF-8 출력. 파일 입출력 시 임시 경로 사용.",
      "conclusion": "KEY POINT / PARTIAL OK / FAILURE→CLUE 중 적절한 라벨 + 결론",
      "bridge": "다음 챕터로 가는 다리 — 직전 결론에서 어떤 의문이 파생되는가"
    }}
  ],
  "final_conclusion": "출발 의문 회수 + 전체 사슬 통합 결론",
  "references": [
    {{ "type": "docs|cpython|workspace|run", "label": "표기", "url": "https://...", "note": "설명" }}
  ]
}}

[제약]
- chapters 5~8 개. 마지막 챕터는 bridge 없이 final_conclusion 으로 연결.
- 각 test_code 는 단독 실행 가능해야 한다 (외부 입력·네트워크·GUI 금지).
- test_code 의 첫 줄에 반드시 `print('# {{section_name}}')` 형태 헤더 출력.
- 코드는 한 챕터당 60줄 이내."""


def make_plan(llm: LLMClient, topic: str, notes_text: str) -> Plan:
    guide = _read_guide()
    # GUIDE 전부 넣으면 길어지므로 핵심 섹션만 추출
    guide_short = _shorten_guide(guide)
    notes_short = notes_text[:8000] if notes_text else "(없음)"
    user = PLAN_USER_TMPL.format(guide=guide_short, topic=topic, notes=notes_short)
    out = llm.complete(PLAN_SYSTEM, user)
    data = _extract_json(out)
    return Plan.from_json(data)


def _shorten_guide(guide: str) -> str:
    """토큰 절약: 핵심 섹션만 추출."""
    keep = []
    for header in ["2. 글 구조", "5. 터미널", "6. 코드 블록", "7. 챕터", "8. 박스",
                   "9. 표지", "10. 제목", "13. 금지", "15. 디자인",
                   "17. 레퍼런스", "18. 자습 글"]:
        m = re.search(rf"={{6,}}\n\s*{re.escape(header)}.*?(?=\n={{6,}})",
                      guide, re.DOTALL)
        if m:
            keep.append(m.group(0))
    return "\n".join(keep)[:18000]


# ──────────────────────────────────────────────────────────
# Step 2 — runner.py 생성 + 실행
# ──────────────────────────────────────────────────────────
RUNNER_TEMPLATE = '''"""자동 생성된 섹션별 테스트 실행기 — {slug}."""
from __future__ import annotations

import io
import os
import sys
import traceback
from contextlib import redirect_stdout
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
LOGS = HERE / "logs"
LOGS.mkdir(exist_ok=True)
FULL = HERE / "full_output.txt"
FULL.write_text("", encoding="utf-8")


def run_section(name: str, fn):
    print(f"\\n============ {{name}} ============")
    buf = io.StringIO()
    try:
        with redirect_stdout(buf):
            fn()
    except Exception:
        traceback.print_exc(file=buf)
    text = buf.getvalue()
    print(text, end="")
    (LOGS / f"{{name}}.txt").write_text(text, encoding="utf-8")
    with FULL.open("a", encoding="utf-8") as f:
        f.write(f"\\n============ {{name}} ============\\n")
        f.write(text)


{section_defs}


if __name__ == "__main__":
{section_calls}
'''


def _indent(code: str, n: int = 4) -> str:
    pad = " " * n
    return "\n".join(pad + line if line.strip() else line for line in code.splitlines())


def build_runner(plan: Plan) -> Path:
    test_subdir = TEST_DIR / plan.slug
    test_subdir.mkdir(parents=True, exist_ok=True)

    section_defs: list[str] = []
    section_calls: list[str] = []
    for ch in plan.chapters:
        sec = ch.get("section_name") or ch["id"]
        sec = _slugify(sec)
        code = ch.get("test_code", "").strip()
        if not code:
            code = f"print('# {sec} — no code')"
        fn_name = f"section_{sec}"
        section_defs.append(
            f"def {fn_name}():\n{_indent(code, 4)}\n"
        )
        section_calls.append(f'    run_section("{sec}", {fn_name})')

    runner_src = RUNNER_TEMPLATE.format(
        slug=plan.slug,
        section_defs="\n\n".join(section_defs),
        section_calls="\n".join(section_calls) or "    pass",
    )
    runner_path = test_subdir / f"{plan.slug}_runner.py"
    runner_path.write_text(runner_src, encoding="utf-8")
    return runner_path


def run_runner(runner_path: Path, log_cb: Callable[[str], None] | None = None) -> RunResult:
    py = str(VENV_PY) if VENV_PY.exists() else sys.executable
    proc = subprocess.run(
        [py, str(runner_path)],
        cwd=str(runner_path.parent),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if log_cb:
        log_cb(proc.stdout)
        if proc.stderr:
            log_cb("[stderr]\n" + proc.stderr)
    logs_dir = runner_path.parent / "logs"
    files: dict[str, str] = {}
    if logs_dir.exists():
        for p in sorted(logs_dir.glob("*.txt")):
            files[p.stem] = p.read_text(encoding="utf-8", errors="replace")
    return RunResult(
        runner_path=runner_path,
        logs_dir=logs_dir,
        log_files=files,
        stdout=proc.stdout + ("\n" + proc.stderr if proc.stderr else ""),
        returncode=proc.returncode,
    )


# ──────────────────────────────────────────────────────────
# Step 3 — 최종 HTML
# ──────────────────────────────────────────────────────────
HTML_SYSTEM = """당신은 파이썬 기술 블로그 HTML 작성 전문가다.
반드시 GUIDE.txt 의 모든 규칙을 따른다:
- 서사 사슬 구조(도입 의문 → 챕터 사슬 → 회수)
- 각 챕터: h3.step "학습" → 인라인 blockquote.cite → "의문→가설" qbox →
  "테스트" 코드+터미널 → "결론(중간)" keypoint → bridge.
- 터미널 블록은 div.terminal > div.terminal-header + pre.terminal-body 형식, PS> 만 표시 (맥 dot 금지).
- 터미널 출력은 사용자가 제공한 '실제 실행 로그' 를 한 글자도 바꾸지 말고 그대로 삽입.
- Swiss Style 4색 팔레트 (--accent #52A97E / --accent-2 #E8875A / --accent-3 #5B9BD5 / --accent-4 #9178C4).
- Nanum Gothic Coding 폰트 link + @import 둘 다 포함.
- Prism.js CDN 헤드 + body 끝 script.
- 한국어로 작성.
- 출력은 완전한 HTML 문서 하나. ```html 코드블록으로 감싸서 반환."""


HTML_USER_TMPL = """아래 기획서·실행 로그·GUIDE 발췌를 토대로 완전한 HTML 한 편을 작성하라.

[GUIDE 발췌]
{guide}

[기획서 JSON]
{plan}

[실제 실행 로그 — 그대로 삽입할 것]
{logs}

요구:
- 표지(header.cover) + main 챕터들 + footer.
- 각 챕터의 '테스트' 블록에서 코드는 ```language-python``` 으로 highlight,
  그 직후 div.terminal 에 위 실행 로그 중 해당 section_name 의 내용을 그대로 삽입.
- 마지막 챕터 뒤에는 "전체 근거 출처" div.ref-chain 부록.
- 출력 코드블록은 ```html 으로 감싼다."""


def generate_html(llm: LLMClient, plan: Plan, run: RunResult,
                  log_cb: Callable[[str], None] | None = None) -> Path:
    guide = _shorten_guide(_read_guide())
    logs_str_parts = []
    for name, content in run.log_files.items():
        logs_str_parts.append(f"--- {name} ---\n{content}")
    logs_str = "\n\n".join(logs_str_parts) or "(로그 없음)"

    user = HTML_USER_TMPL.format(
        guide=guide,
        plan=json.dumps(plan.raw, ensure_ascii=False, indent=2),
        logs=logs_str,
    )
    out = llm.complete(HTML_SYSTEM, user)
    html = _extract_html(out)

    BLOG_DIR.mkdir(parents=True, exist_ok=True)
    target = BLOG_DIR / f"{plan.slug}.html"
    target.write_text(html, encoding="utf-8")
    if log_cb:
        log_cb(f"[saved] {target}")
    return target


# ──────────────────────────────────────────────────────────
# 통합 진입점
# ──────────────────────────────────────────────────────────
@dataclass
class PipelineResult:
    plan: Plan
    runner_path: Path
    run_result: RunResult
    html_path: Path


def run_full_pipeline(llm: LLMClient, topic: str, notes_text: str,
                      log_cb: Callable[[str], None] | None = None) -> PipelineResult:
    log = log_cb or (lambda s: None)
    log("[1/3] 기획서 생성 중…")
    plan = make_plan(llm, topic, notes_text)
    log(f"[1/3] slug={plan.slug}, 챕터 {len(plan.chapters)}개")

    log("[2/3] runner.py 작성·실행 중…")
    runner_path = build_runner(plan)
    log(f"      runner: {runner_path}")
    run_result = run_runner(runner_path, log_cb=log)
    log(f"[2/3] returncode={run_result.returncode}, 로그 {len(run_result.log_files)}개")

    log("[3/3] 최종 HTML 생성 중…")
    html_path = generate_html(llm, plan, run_result, log_cb=log)
    log(f"[3/3] 저장 완료: {html_path}")

    return PipelineResult(plan, runner_path, run_result, html_path)
