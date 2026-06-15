from __future__ import annotations

import html
import re
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
KNOWLEDGE = ROOT / ".study" / "knowledge"


class HeadingParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._tag: str | None = None
        self._buf: list[str] = []
        self.title = ""
        self.h1 = ""
        self.h2: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag in {"title", "h1", "h2"}:
            self._tag = tag
            self._buf = []

    def handle_endtag(self, tag: str) -> None:
        if tag != self._tag:
            return
        text = clean_text("".join(self._buf))
        if tag == "title" and not self.title:
            self.title = text
        elif tag == "h1" and not self.h1:
            self.h1 = text
        elif tag == "h2" and text:
            self.h2.append(text)
        self._tag = None
        self._buf = []

    def handle_data(self, data: str) -> None:
        if self._tag:
            self._buf.append(data)


def read_text(path: Path) -> str:
    for enc in ("utf-8", "utf-8-sig", "cp949", "euc-kr"):
        try:
            return path.read_text(encoding=enc)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def clean_text(value: str) -> str:
    value = html.unescape(value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def collect_blog() -> list[dict[str, object]]:
    rows = []
    for path in sorted((ROOT / ".blog").glob("*.html")):
        if "_base64" in path.stem or ".backup_" in path.name or path.name.endswith(".old.html"):
            continue
        parser = HeadingParser()
        parser.feed(read_text(path))
        rows.append(
            {
                "path": rel(path),
                "title": parser.h1 or parser.title or path.stem,
                "h2": parser.h2[:12],
            }
        )
    return rows


def collect_pdfs() -> list[Path]:
    pdf_dir = ROOT / ".study" / "pdf"
    return sorted(pdf_dir.glob("*.pdf")) if pdf_dir.exists() else []


def classify_note(path: Path) -> str:
    name = path.name.lower()
    suffix = path.suffix.lower()
    if "_extracted" in name or path.parent.name == "_w4_extract":
        return "extracted text"
    if suffix == ".mhtml":
        return "raw web note"
    if suffix == ".txt":
        return "text note"
    if suffix in {".docx", ".pptx", ".xlsx"}:
        return "office artifact"
    return suffix.lstrip(".") or "file"


def preview_text(path: Path, limit: int = 120) -> str:
    if path.suffix.lower() != ".txt":
        return ""
    text = read_text(path)
    for line in text.splitlines():
        line = clean_text(line)
        if line:
            return line[:limit]
    return ""


def collect_notes() -> list[dict[str, object]]:
    notes_dir = ROOT / ".study" / "notes"
    rows = []
    if not notes_dir.exists():
        return rows
    for path in sorted(p for p in notes_dir.rglob("*") if p.is_file()):
        rows.append(
            {
                "path": rel(path),
                "group": path.relative_to(notes_dir).parts[0],
                "kind": classify_note(path),
                "size_mb": path.stat().st_size / 1024 / 1024,
                "modified": datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d"),
                "preview": preview_text(path),
            }
        )
    return rows


def collect_tests() -> list[dict[str, object]]:
    test_dir = ROOT / ".study" / "test"
    rows = []
    if not test_dir.exists():
        return rows
    for folder in sorted(p for p in test_dir.iterdir() if p.is_dir()):
        logs = sorted((folder / "logs").glob("*.txt")) if (folder / "logs").exists() else []
        charts = sorted((folder / "charts").glob("*.png")) if (folder / "charts").exists() else []
        runners = sorted(folder.glob("*runner.py")) + sorted(folder.glob("build_*.py"))
        if logs or charts or runners:
            rows.append(
                {
                    "path": rel(folder),
                    "logs": len(logs),
                    "charts": len(charts),
                    "runners": [rel(p) for p in runners[:4]],
                }
            )
    return rows


def collect_root_projects() -> list[dict[str, object]]:
    skip = {".blog", ".git", ".github", ".scripts", ".study", ".venv", ".vscode"}
    rows = []
    for folder in sorted(p for p in ROOT.iterdir() if p.is_dir() and p.name not in skip):
        files = [p for p in folder.rglob("*") if p.is_file()]
        rows.append({"path": rel(folder), "files": len(files)})
    return rows


def render() -> str:
    blog = collect_blog()
    notes = collect_notes()
    pdfs = collect_pdfs()
    tests = collect_tests()
    projects = collect_root_projects()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines: list[str] = []
    lines.append("# Knowledge Index")
    lines.append("")
    lines.append(f"Generated: {now}")
    lines.append("")
    lines.append("이 파일은 `.study/knowledge/scripts/build_index.py`로 생성한다.")
    lines.append("")

    lines.append("## Source Notes")
    lines.append("")
    lines.append("`.study/notes/`는 이 지식 시스템의 원천 자료다. 블로그는 결과물이고, notes는 사고 과정과 질문의 출처다.")
    lines.append("")
    current_group = ""
    for item in notes:
        if item["group"] != current_group:
            current_group = str(item["group"])
            lines.append(f"### {current_group}")
            lines.append("")
        lines.append(
            f"- `{item['path']}` ({item['kind']}, {item['size_mb']:.1f} MB, {item['modified']})"
        )
        if item["preview"]:
            lines.append(f"  - preview: {item['preview']}")
    lines.append("")

    lines.append("## Blog Outputs")
    lines.append("")
    for item in blog:
        lines.append(f"- `{item['path']}`")
        lines.append(f"  - title: {item['title']}")
        h2 = item["h2"]
        if h2:
            lines.append("  - chapters:")
            for heading in h2[:8]:
                lines.append(f"    - {heading}")
    lines.append("")

    lines.append("## Study Tests")
    lines.append("")
    for item in tests:
        lines.append(f"- `{item['path']}`: logs {item['logs']}, charts {item['charts']}")
        runners = item["runners"]
        if runners:
            lines.append(f"  - runners: {', '.join(f'`{r}`' for r in runners)}")
    lines.append("")

    lines.append("## PDFs")
    lines.append("")
    for path in pdfs:
        size_mb = path.stat().st_size / 1024 / 1024
        lines.append(f"- `{rel(path)}` ({size_mb:.1f} MB)")
    lines.append("")

    lines.append("## Root Project Folders")
    lines.append("")
    for item in projects:
        lines.append(f"- `{item['path']}`: {item['files']} files")
    lines.append("")

    lines.append("## Source Files")
    lines.append("")
    lines.append("- `about.txt`: 날짜별 학습/프로젝트 흐름")
    lines.append("- `.study/HISTORY.md`: 작업 이력")
    lines.append("- `.study/GUIDE.txt`: 블로그 작성 규칙")
    lines.append("- `.study/notes/`: 원천 노트")
    lines.append("")
    return "\n".join(lines)


def render_notes() -> str:
    notes = collect_notes()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines: list[str] = []
    lines.append("# Notes Index")
    lines.append("")
    lines.append(f"Generated: {now}")
    lines.append("")
    lines.append("이 파일은 `.study/notes/`만 따로 보기 위한 원천 노트 인덱스다.")
    lines.append("")
    lines.append("## 읽는 기준")
    lines.append("")
    lines.append("- `raw web note`: Gemini, 블로그, 웹에서 저장된 원본 mhtml")
    lines.append("- `extracted text`: 원본에서 텍스트만 뽑아낸 카드화 후보")
    lines.append("- `text note`: 직접 작성하거나 별도로 저장한 텍스트")
    lines.append("- `office artifact`: 프로젝트 문서, 발표, 표")
    lines.append("")

    by_group: dict[str, list[dict[str, object]]] = {}
    for item in notes:
        by_group.setdefault(str(item["group"]), []).append(item)

    for group, items in by_group.items():
        lines.append(f"## {group}")
        lines.append("")
        counts: dict[str, int] = {}
        for item in items:
            counts[str(item["kind"])] = counts.get(str(item["kind"]), 0) + 1
        summary = ", ".join(f"{kind}: {count}" for kind, count in sorted(counts.items()))
        lines.append(f"Summary: {summary}")
        lines.append("")
        for item in items:
            lines.append(
                f"- `{item['path']}` ({item['kind']}, {item['size_mb']:.1f} MB, modified {item['modified']})"
            )
            if item["preview"]:
                lines.append(f"  - preview: {item['preview']}")
        lines.append("")

    lines.append("## 카드화 우선순위")
    lines.append("")
    lines.append("1. `_extracted.txt` 파일에서 핵심 질문과 직접 검증한 내용을 먼저 뽑는다.")
    lines.append("2. 같은 주제의 `.mhtml`은 원문 맥락을 확인할 때만 연다.")
    lines.append("3. 프로젝트 문서 `.xlsx`, `.pptx`는 project card에 연결한다.")
    lines.append("4. 개념 카드에는 notes 경로를 반드시 관련 산출물로 남긴다.")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    KNOWLEDGE.mkdir(parents=True, exist_ok=True)
    (KNOWLEDGE / "INDEX.md").write_text(render(), encoding="utf-8")
    (KNOWLEDGE / "NOTES.md").write_text(render_notes(), encoding="utf-8")


if __name__ == "__main__":
    main()
