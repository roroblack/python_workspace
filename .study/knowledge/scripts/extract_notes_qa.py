from __future__ import annotations

import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
NOTES = ROOT / ".study" / "notes"
OUT = ROOT / ".study" / "knowledge" / "NOTES_QA_INSIGHTS.md"

USER_MARK = "말씀하신 내용"
AI_MARK = "Gemini의 응답"

CONFIRM_PATTERNS = [
    "맞습니다",
    "정확합니다",
    "정확하게",
    "핵심을 정확",
    "정확히",
    "맞아요",
    "네, 맞",
    "네. 맞",
    "맞게 이해",
    "완벽합니다",
    "제대로 이해",
    "잘 짚",
]

QUESTION_HINTS = [
    "?",
    "뭐",
    "왜",
    "어떻게",
    "그러면",
    "그럼",
    "맞",
    "이해",
    "원리",
    "차이",
    "가능",
    "되는",
    "하면",
]


def read_text(path: Path) -> str:
    for enc in ("utf-8", "utf-8-sig", "cp949", "euc-kr"):
        try:
            return path.read_text(encoding=enc)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def clean(value: str, limit: int | None = None) -> str:
    value = re.sub(r"\s+", " ", value)
    value = value.replace("|", "\\|").strip()
    if limit and len(value) > limit:
        return value[: limit - 1].rstrip() + "…"
    return value


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def parse_pairs(text: str) -> list[dict[str, str]]:
    pairs: list[dict[str, str]] = []
    pos = 0
    while True:
        start = text.find(USER_MARK, pos)
        if start < 0:
            break
        q_start = start + len(USER_MARK)
        a_mark = text.find(AI_MARK, q_start)
        if a_mark < 0:
            break
        next_start = text.find(USER_MARK, a_mark + len(AI_MARK))
        question = text[q_start:a_mark]
        answer = text[a_mark + len(AI_MARK) : next_start if next_start >= 0 else len(text)]
        pairs.append({"question": clean(question), "answer": clean(answer)})
        pos = next_start if next_start >= 0 else len(text)
    return pairs


def is_confirmed(answer: str) -> bool:
    return any(pattern in answer[:1200] for pattern in CONFIRM_PATTERNS)


def is_user_question(question: str) -> bool:
    return any(hint in question for hint in QUESTION_HINTS)


def answer_takeaway(answer: str) -> str:
    answer = clean(answer)
    sentences = re.split(r"(?<=[.!?다요죠])\s+", answer)
    picked = []
    for sentence in sentences:
        if not sentence:
            continue
        picked.append(sentence)
        if len(" ".join(picked)) >= 180 or len(picked) >= 2:
            break
    return clean(" ".join(picked), 260)


def topic_from_path(path: Path) -> str:
    name = path.name
    stem = path.stem.replace("_extracted", "")
    return stem


def collect() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for path in sorted(NOTES.rglob("*.txt")):
        text = read_text(path)
        pairs = parse_pairs(text)
        for idx, pair in enumerate(pairs, 1):
            question = pair["question"]
            answer = pair["answer"]
            rows.append(
                {
                    "path": rel(path),
                    "topic": topic_from_path(path),
                    "idx": idx,
                    "question": question,
                    "answer": answer,
                    "confirmed": is_confirmed(answer),
                    "question_like": is_user_question(question),
                    "takeaway": answer_takeaway(answer),
                }
            )
    return rows


def render(rows: list[dict[str, object]]) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    by_path: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        by_path[str(row["path"])].append(row)

    confirmed = [row for row in rows if row["confirmed"]]
    question_like = [row for row in rows if row["question_like"]]

    lines: list[str] = []
    lines.append("# Notes Q&A Insights")
    lines.append("")
    lines.append(f"Generated: {now}")
    lines.append("")
    lines.append("이 파일은 `.study/notes/`의 텍스트 노트에서 사용자 질문과 Gemini 응답을 추출한 인덱스다.")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Parsed Q&A pairs: {len(rows)}")
    lines.append(f"- User-question-like entries: {len(question_like)}")
    lines.append(f"- AI-confirmed insight entries: {len(confirmed)}")
    lines.append("")
    lines.append("## Counts By Source")
    lines.append("")
    lines.append("| Source | Q&A | Confirmed |")
    lines.append("|---|---:|---:|")
    for path, items in by_path.items():
        lines.append(f"| `{path}` | {len(items)} | {sum(1 for item in items if item['confirmed'])} |")
    lines.append("")

    lines.append("## AI-Confirmed Insights")
    lines.append("")
    lines.append("사용자가 제시한 이해나 가설에 대해 AI가 맞다고 확인한 부분이다.")
    lines.append("")
    for row in confirmed:
        lines.append(f"### {row['topic']} #{row['idx']}")
        lines.append("")
        lines.append(f"- source: `{row['path']}`")
        lines.append(f"- user: {clean(str(row['question']), 360)}")
        lines.append(f"- AI takeaway: {row['takeaway']}")
        lines.append("")

    lines.append("## All User Questions And Doubts")
    lines.append("")
    lines.append("사용자가 제시한 의문, 확인 질문, 코드/결과 검증 요청 전체 목록이다.")
    lines.append("")
    for path, items in by_path.items():
        lines.append(f"### `{path}`")
        lines.append("")
        for row in items:
            marker = "confirmed" if row["confirmed"] else "checked"
            lines.append(f"- #{row['idx']} [{marker}] {clean(str(row['question']), 300)}")
        lines.append("")

    lines.append("## How To Use This")
    lines.append("")
    lines.append("1. `AI-Confirmed Insights`에서 내 언어로 세운 가설을 먼저 본다.")
    lines.append("2. `All User Questions And Doubts`에서 반복해서 나온 질문 패턴을 찾는다.")
    lines.append("3. 중요한 항목은 `concepts/`의 개념 카드로 승격한다.")
    lines.append("4. 답을 외우기보다, 질문을 다시 보고 직접 설명해본다.")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    rows = collect()
    OUT.write_text(render(rows), encoding="utf-8")


if __name__ == "__main__":
    main()

