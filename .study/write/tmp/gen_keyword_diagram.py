import base64
from pathlib import Path
import html


HTML = Path(r"c:\_proj\python_workspace\.blog\day0511_mysql_btree.html")
PREVIEW = Path(r"c:\_proj\python_workspace\.study\write\tmp\keyword_diagram_preview.svg")

CANVAS_W = 1020
CANVAS_H = 1180
FONT_STACK = "Segoe UI, Malgun Gothic, sans-serif"


def esc(value):
    return html.escape(str(value), quote=True)


def text_block(x, y, lines, size, weight, fill, anchor="start", line_gap=24, opacity=1.0):
    parts = [
        f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" '
        f'fill="{fill}" text-anchor="{anchor}" font-family="{FONT_STACK}" opacity="{opacity}">'
    ]
    for index, line in enumerate(lines):
        dy = "0" if index == 0 else str(line_gap)
        parts.append(f'<tspan x="{x}" dy="{dy}">{esc(line)}</tspan>')
    parts.append("</text>")
    return "".join(parts)


def label_pill(x, y, w, h, label, fill, stroke, text_fill="#0f172a"):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h // 2}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
        f'<text x="{x + w / 2}" y="{y + h / 2 + 5}" font-size="14" font-weight="800" '
        f'fill="{text_fill}" text-anchor="middle" letter-spacing="1.2" '
        f'font-family="{FONT_STACK}">{esc(label)}</text>'
    )


def panel(x, y, w, h, title, subtitle, stroke, fill, header_fill):
    return "".join(
        [
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="26" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="2.5" filter="url(#shadow)"/>',
            f'<path d="M {x} {y + 26} Q {x} {y} {x + 26} {y} L {x + w - 26} {y} '
            f'Q {x + w} {y} {x + w} {y + 26} L {x + w} {y + 72} L {x} {y + 72} Z" '
            f'fill="{header_fill}"/>',
            text_block(x + 26, y + 42, [title], 28, 800, "#ffffff"),
            text_block(x + 26, y + 64, [subtitle], 15, 600, "#e2e8f0"),
        ]
    )


def component_box(x, y, w, h, title, lines, stroke, accent, fill="#ffffff"):
    body = [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="{fill}" '
        f'stroke="{stroke}" stroke-width="2" filter="url(#shadow-soft)"/>',
        f'<rect x="{x}" y="{y}" width="8" height="{h}" rx="4" fill="{accent}"/>',
        text_block(x + 24, y + 38, [title], 24, 800, "#0f172a"),
        text_block(x + 24, y + 70, lines, 18, 600, "#334155", line_gap=24),
    ]
    return "".join(body)


def side_service_box(x, y, w, h, title, lines, stroke, fill):
    return "".join(
        [
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="2" filter="url(#shadow-soft)"/>',
            text_block(x + w / 2, y + 38, [title], 22, 800, "#0f172a", anchor="middle"),
            text_block(x + w / 2, y + 70, lines, 18, 600, "#334155", anchor="middle", line_gap=22),
        ]
    )


def storage_bar(x, y, w, h):
    return "".join(
        [
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="24" fill="#edf4f7" '
            f'stroke="#5b7083" stroke-width="2.5" filter="url(#shadow)"/>',
            text_block(x + w / 2, y + 40, ["Persistent Storage (Disk / SSD)",], 28, 800, "#0f172a", anchor="middle"),
            text_block(
                x + w / 2,
                y + 74,
                ["tablespaces, data/index pages, redo files, durable checkpoints"],
                18,
                600,
                "#334155",
                anchor="middle",
            ),
        ]
    )


def connector(points, label=None, label_x=None, label_y=None, end=True, start=False):
    d = "M " + " L ".join(f"{x} {y}" for x, y in points)
    attrs = []
    if start:
        attrs.append('marker-start="url(#arrow)"')
    if end:
        attrs.append('marker-end="url(#arrow)"')
    path = (
        f'<path d="{d}" fill="none" stroke="#55708a" stroke-width="3" '
        f'stroke-linejoin="round" stroke-linecap="round" {' '.join(attrs)}/>'
    )
    if not label:
        return path
    chip_w = max(108, len(label) * 8 + 24)
    chip = (
        f'<rect x="{label_x - chip_w / 2}" y="{label_y - 14}" width="{chip_w}" height="28" rx="14" '
        f'fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>'
        f'<text x="{label_x}" y="{label_y + 5}" font-size="14" font-weight="700" fill="#334155" '
        f'text-anchor="middle" font-family="{FONT_STACK}">{esc(label)}</text>'
    )
    return path + chip


def build_svg():
    svg = []
    svg.append('<?xml version="1.0" encoding="UTF-8"?>')
    svg.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" '
        f'viewBox="0 0 {CANVAS_W} {CANVAS_H}">'
    )
    svg.append(
        f'''<defs>
        <pattern id="grid" width="34" height="34" patternUnits="userSpaceOnUse">
            <path d="M 34 0 L 0 0 0 34" fill="none" stroke="#dbe7ef" stroke-width="1" opacity="0.55"/>
        </pattern>
        <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
            <feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#8aa3b8" flood-opacity="0.16"/>
        </filter>
        <filter id="shadow-soft" x="-20%" y="-20%" width="140%" height="140%">
            <feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#8aa3b8" flood-opacity="0.12"/>
        </filter>
        <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="#55708a"/>
        </marker>
        </defs>'''
    )

    svg.append(f'<rect width="{CANVAS_W}" height="{CANVAS_H}" fill="#f7fbfd"/>')
    svg.append(f'<rect width="{CANVAS_W}" height="{CANVAS_H}" fill="url(#grid)" opacity="0.9"/>')
    svg.append(
        f'<rect x="18" y="18" width="{CANVAS_W - 36}" height="{CANVAS_H - 36}" rx="30" '
        f'fill="#ffffff" stroke="#d9e4ea" stroke-width="2" filter="url(#shadow)"/>'
    )

    svg.append(text_block(CANVAS_W / 2, 84, ["INNODB SYSTEM ARCHITECTURE OVERVIEW"], 42, 900, "#0f172a", anchor="middle"))
    svg.append(
        text_block(
            CANVAS_W / 2,
            122,
            ["요청 유입 -> 핵심 처리 -> 메모리 캐시 -> 로그 내구성 -> 영속 스토리지"],
            20,
            600,
            "#475569",
            anchor="middle",
        )
    )

    svg.append(label_pill(415, 156, 190, 30, "EXTERNAL INGRESS", "#e0f2fe", "#7dd3fc"))
    svg.append(
        component_box(
            220,
            196,
            580,
            118,
            "Client Applications / SQL Entry",
            [
                "client apps, admin sessions, ORM and JDBC connections",
                "SELECT, INSERT, UPDATE, COMMIT requests enter through the MySQL protocol",
            ],
            "#2563eb",
            "#38bdf8",
            fill="#f8fbff",
        )
    )

    svg.append(label_pill(362, 350, 296, 30, "CORE PROCESSING SERVICE", "#dbeafe", "#93c5fd"))
    svg.append(
        panel(
            220,
            388,
            580,
            448,
            "INNODB CORE STORAGE SERVICE",
            "request routing, page access, cache reuse, and durable commit orchestration",
            "#2563eb",
            "#edf5ff",
            "#1d4ed8",
        )
    )
    svg.append(
        component_box(
            250,
            480,
            520,
            90,
            "Request Handler / Access Path Router",
            ["parses SQL intent and selects clustered / secondary / covering access path"],
            "#3b82f6",
            "#60a5fa",
        )
    )
    svg.append(
        component_box(
            250,
            592,
            520,
            100,
            "Core Page & Index Manager",
            ["coordinates page access, B+Tree traversal, insert flow, and split decisions"],
            "#0f766e",
            "#34d399",
        )
    )
    svg.append(
        component_box(
            250,
            716,
            244,
            108,
            "Memory Buffer Pool / Cache",
            ["keeps hot pages in RAM", "cuts random disk I/O and repeat reads"],
            "#059669",
            "#6ee7b7",
        )
    )
    svg.append(
        component_box(
            526,
            716,
            244,
            108,
            "Transaction Log Manager",
            ["records redo and commit order", "preserves crash-safe durability"],
            "#0f766e",
            "#86efac",
        )
    )

    svg.append(
        side_service_box(
            110,
            892,
            320,
            112,
            "Concurrency Control",
            ["MVCC, latches, atomic counters,", "and partitioned hot paths"],
            "#64748b",
            "#f8fafc",
        )
    )
    svg.append(
        side_service_box(
            590,
            892,
            320,
            112,
            "Backup & Recovery",
            ["checkpoint, redo replay,", "snapshot and restore workflows"],
            "#64748b",
            "#f8fafc",
        )
    )

    svg.append(label_pill(382, 852, 256, 30, "PERIPHERAL SERVICES", "#f1f5f9", "#cbd5e1"))
    svg.append(label_pill(382, 1026, 256, 30, "PERSISTENT STORAGE", "#ecfeff", "#99f6e4"))
    svg.append(storage_bar(110, 1066, 800, 116))

    svg.append(connector([(510, 314), (510, 480)], "SQL request flow", 510, 346))
    svg.append(connector([(510, 570), (510, 592)], "parse / route", 510, 582))
    svg.append(connector([(510, 692), (510, 704), (372, 704), (372, 716)], "page access / cache lookup", 390, 704))
    svg.append(connector([(510, 692), (510, 704), (648, 704), (648, 716)], "redo / commit record", 630, 704))
    svg.append(connector([(270, 892), (270, 860), (360, 860), (360, 692)], "MVCC / latches", 320, 850))
    svg.append(connector([(372, 824), (372, 900), (372, 1066)], "page read / dirty flush", 372, 1018, end=True, start=True))
    svg.append(connector([(648, 824), (648, 900), (648, 1066)], "redo write / commit durability", 648, 1018))
    svg.append(connector([(750, 892), (750, 860), (750, 1066)], "snapshot / restore", 750, 1018, end=True, start=True))

    svg.append('</svg>')
    return "".join(svg)


def img_block(svg_b64: str) -> str:
    return f'''  <figure class="diagram">
    <img src="data:image/svg+xml;base64,{svg_b64}"
         alt="MySQL InnoDB 시스템 아키텍처 개요 다이어그램"
         style="display:block;width:100%;height:auto;max-width:100%;margin:0 auto;border:0;background:#f7fbfd;" />
    <figcaption>MySQL InnoDB 시스템 아키텍처 개요 — 요청 유입, 핵심 처리, 캐시, 로그, 영속 스토리지 흐름을 한 장으로 정리</figcaption>
  </figure>'''


def rebuild_html(svg_b64: str) -> None:
    html_text = HTML.read_text(encoding="utf-8")
    section_start = html_text.find('<section id="ch14">')
    if section_start == -1:
        raise RuntimeError("CH14 section not found")

    next_section = html_text.find('<section id="', section_start + 1)
    section_end = len(html_text) if next_section == -1 else next_section
    ch14_html = html_text[section_start:section_end]

    figure_start = ch14_html.find('<figure class="diagram">')
    if figure_start == -1:
        raise RuntimeError("CH14 diagram figure not found")

    figure_end = ch14_html.find('</figure>', figure_start)
    if figure_end == -1:
        raise RuntimeError("CH14 diagram closing tag not found")

    figure_end += len('</figure>')
    updated_ch14 = ch14_html[:figure_start] + img_block(svg_b64) + ch14_html[figure_end:]
    new_html = html_text[:section_start] + updated_ch14 + html_text[section_end:]
    HTML.write_text(new_html, encoding="utf-8")


if __name__ == "__main__":
    svg_text = build_svg()
    PREVIEW.write_text(svg_text, encoding="utf-8")
    svg_b64 = base64.b64encode(svg_text.encode("utf-8")).decode("ascii")
    rebuild_html(svg_b64)
    print(f"SVG architecture diagram generated: {len(svg_b64):,} bytes")