"""노트 파일 → 평문 추출. .txt / .mhtml / .docx 지원."""
from __future__ import annotations

import email
import quopri
from pathlib import Path


def load_notes(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".txt":
        return path.read_text(encoding="utf-8", errors="replace")
    if suffix == ".mhtml":
        return _extract_mhtml(path)
    if suffix == ".docx":
        return _extract_docx(path)
    return path.read_text(encoding="utf-8", errors="replace")


def _extract_mhtml(path: Path) -> str:
    raw = path.read_bytes()
    msg = email.message_from_bytes(raw)
    htmls: list[str] = []
    for part in msg.walk():
        ctype = part.get_content_type()
        if ctype not in ("text/html", "text/plain"):
            continue
        payload = part.get_payload(decode=True)
        if payload is None:
            continue
        charset = part.get_content_charset() or "utf-8"
        try:
            text = payload.decode(charset, errors="replace")
        except LookupError:
            text = payload.decode("utf-8", errors="replace")
        if part.get("Content-Transfer-Encoding", "").lower() == "quoted-printable":
            text = quopri.decodestring(text).decode(charset, errors="replace")
        htmls.append(text)
    combined = "\n\n".join(htmls)
    return _html_to_text(combined)


def _html_to_text(html: str) -> str:
    try:
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html, "lxml")
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()
        text = soup.get_text("\n")
        lines = [ln.strip() for ln in text.splitlines()]
        return "\n".join(ln for ln in lines if ln)
    except Exception:
        import re

        return re.sub(r"<[^>]+>", "", html)


def _extract_docx(path: Path) -> str:
    import zipfile
    import xml.etree.ElementTree as ET

    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    with zipfile.ZipFile(path) as zf:
        with zf.open("word/document.xml") as f:
            tree = ET.parse(f)
    paras: list[str] = []
    for p in tree.iter(f"{{{ns['w']}}}p"):
        texts = [t.text for t in p.iter(f"{{{ns['w']}}}t") if t.text]
        if texts:
            paras.append("".join(texts))
    return "\n".join(paras)
