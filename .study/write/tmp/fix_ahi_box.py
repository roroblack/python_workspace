from pathlib import Path


HTML = Path(r"c:\_proj\python_workspace\.blog\day0511_mysql_btree.html")


def vw(text: str) -> int:
    return sum(1 if ord(char) < 128 else 2 for char in text)

INDENT = "   "
N = 18
INNER = N * 2
BOX_LEFT = vw(INDENT)
BOX_RIGHT = BOX_LEFT + 2 + INNER
MAX_VISUAL_WIDTH = 56


def pad_to(text: str, target: int) -> str:
    width = vw(text)
    if width > target:
        raise ValueError(f"line exceeds target: {width} > {target}: {text!r}")
    return text + " " * (target - width)


def box(content: str) -> str:
    return "│" + pad_to(content, INNER) + "│"


def table_row(content: str) -> str:
    return INDENT + box(content)


def marker_positions(text: str, markers: set[str]) -> list[tuple[str, int]]:
    positions: list[tuple[str, int]] = []
    pos = 0
    for char in text:
        if char in markers:
            positions.append((char, pos))
        pos += 1 if ord(char) < 128 else 2
    return positions


def build_lines() -> list[str]:
    return [
        "   B+Tree",
        "   [ Root ]",
        "      │",
        "      ▼",
        "   [Internal]",
        "      │",
        "      ▼",
        "   [ Leaf  ] ◀── 일반 조회 (3회 I/O)",
        "      │",
        "      └── 자주 쓰이면 등록",
        "          │",
        "          ▼",
        "   AHI Hash Table (인메모리)",
        INDENT + "┌" + "─" * N + "┐",
        table_row(" hash(\"id=1\")  → page#4,r3 "),
        table_row(" hash(\"id=2\")  → page#4,r4 "),
        table_row(" hash(\"id=15\") → page#5,r1 "),
        table_row(" hash(\"id=20\") → page#5,r2 "),
        table_row("     ... "),
        INDENT + "└" + "─" * N + "┘",
        "          │",
        "          ▼",
        "   그 다음부터 1회 메모리 lookup 으로 즉답",
    ]


def verify_lines(lines: list[str]) -> None:
    box_left: list[int] = []
    box_right: list[int] = []
    max_width = 0

    for line in lines:
        width = vw(line)
        max_width = max(max_width, width)
        if width > MAX_VISUAL_WIDTH:
            raise AssertionError(f"line too wide: {width} > {MAX_VISUAL_WIDTH}: {line!r}")

        marks = marker_positions(line, {"│", "┌", "┐", "└", "┘"})
        if line.startswith(INDENT + "┌") or line.startswith(INDENT + "└" + "─"):
            box_left.append(marks[0][1])
            box_right.append(marks[1][1])
        elif "hash(" in line or "..." in line:
            box_left.append(marks[0][1])
            box_right.append(marks[1][1])

    assert set(box_left) == {BOX_LEFT}, box_left
    assert set(box_right) == {BOX_RIGHT}, box_right
    assert max_width <= MAX_VISUAL_WIDTH, max_width


def main() -> None:
    lines = build_lines()
    verify_lines(lines)

    marker = '<div class="ascii">[ AHI 글로벌 해시 테이블 — 자주 쓰는 키들의 지름길 ]'
    text = HTML.read_text(encoding="utf-8")
    start = text.index(marker)
    end = text.index("</div>", start) + len("</div>")
    replacement = marker + "\n\n" + "\n".join(lines) + "\n</div>"
    HTML.write_text(text[:start] + replacement + text[end:], encoding="utf-8")

    print(f"BOX_LEFT={BOX_LEFT}, BOX_RIGHT={BOX_RIGHT}, MAX_VISUAL_WIDTH={MAX_VISUAL_WIDTH}")
    for index, line in enumerate(lines, 1):
        print(f"{index:02d} vw={vw(line):3d} {marker_positions(line, {'│', '┌', '┐', '└', '┘'})} |{line}|")
    print(f"[saved] {HTML}")


if __name__ == "__main__":
    main()