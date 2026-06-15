"""dict.html 을 GUIDE.txt 의 새 서사 사슬 방식으로 재구성.

- CSS: blockquote.cite, .bridge 추가
- 표지 deck 갱신 (출발 의문 명시)
- main 도입에 .bridge 추가
- 챕터별: '의문' → '의문 → 가설', 'Q' → '가설',
  '결론' → '결론(중간)' (CH12는 '최종 결론'), 'KEY POINT' → 'KEY POINT — 가설 통과'
- 챕터간 .bridge 삽입 (CH01~CH11 끝)
"""
import re
from pathlib import Path

HTML = Path(r"c:\_proj\python_workspace\.study\blog\dict.html")
text = HTML.read_text(encoding="utf-8")

# ─── 1) CSS 추가 ────────────────────────────────────────────────
css_new = """
    /* ------------ 인라인 인용 (학습 본문 안) ------------ */
    blockquote.cite {
      border: 1px solid #d8d0f0;
      border-left: 4px solid var(--accent-4);
      background: #F7F5FD;
      padding: 12px 16px;
      margin: 12px 0;
      border-radius: 0;
      font-size: 0.95rem;
      line-height: 1.65;
    }
    blockquote.cite .src {
      display: block;
      color: var(--muted);
      font-size: 0.85em;
      margin-top: 8px;
    }

    /* ------------ 다음 챕터로 가는 다리 ------------ */
    .bridge {
      border-left: 4px solid var(--muted);
      background: #F4F6F8;
      padding: 12px 16px;
      margin: 18px 0 8px;
      font-size: 0.92rem;
      line-height: 1.65;
      color: #3a4250;
      border-radius: 0;
    }
    .bridge strong { color: var(--ink); }
"""
# style 블록 끝(  </style>) 직전에 끼워넣기
text = text.replace("  </style>\n</head>", css_new + "\n  </style>\n</head>")

# ─── 2) 표지 deck 갱신 ──────────────────────────────────────────
text = text.replace(
    '<p class="deck">학습 → 의문 → 테스트 → 결론. 한 챕터 안에서 한 주제를 끝까지 따라가는 방식으로, 부트캠프 실습 코드와 CPython 소스를 같은 흐름에 엮었다. 본문 인용·동작 검증은 모두 <strong>Python 3.14 기준</strong>이다.</p>',
    '<p class="deck">"<code>list</code> 까지 익혔는데 왜 또 새 자료형 <code>dict</code> 가 필요한가?" — 한 줄짜리 출발 의문에서 시작해, 12개 챕터를 학습 → (인라인 인용) → 가설 → 테스트 → 중간 결론 → 다음 챕터로 가는 다리 의 사슬로 이어 따라간다. CH12 에서 출발 의문에 한 문장으로 답하며 닫는다. 본문 인용·동작 검증은 모두 <strong>Python 3.14.2 · Windows 11 · PowerShell</strong> 기준.</p>',
)

# ─── 3) main 도입 .bridge 삽입 ─────────────────────────────────
intro_bridge = """<main class="page">

<!-- ============================================================ 도입 다리 -->
<div class="bridge" style="margin-top:18px">
  <strong>이 글이 추적하는 한 줄 의문</strong> — "list 까지 익혔는데 왜 또 새 자료형 dict 가 필요한가?"
  CH01 ~ CH11 이 표면 동작 → 내부 자료구조까지 사슬로 이어가며 답을 쌓고, CH12 에서 한 문장으로 압축한다.
</div>

"""
text = text.replace("<main class=\"page\">\n\n", intro_bridge, 1)

# ─── 4) 의문 → 가설 라벨 변경 ────────────────────────────────────
text = text.replace('<h3 class="step">의문</h3>', '<h3 class="step">의문 → 가설</h3>')
text = text.replace('<span class="label">Q</span>', '<span class="label">가설</span>')

# ─── 5) 결론 라벨 — CH12 만 '최종 결론' 처리 ─────────────────────
# CH12 는 마지막 한 곳. CH12 의 결론 h3 와 keypoint label 만 별도 토큰화 후 일괄 치환.
ch12_pos = text.find('<section id="ch12">')
assert ch12_pos != -1, "ch12 not found"
before, after = text[:ch12_pos], text[ch12_pos:]

# CH12 안의 결론 라벨을 임시 토큰으로
after = after.replace('<h3 class="step">결론</h3>', '<h3 class="step">최종 결론</h3>', 1)
after = after.replace('<span class="label">KEY POINT</span>', '<span class="label">FINAL CONCLUSION</span>', 1)

# CH01~CH11 의 결론 라벨 일괄 치환 (before 영역만)
before = before.replace('<h3 class="step">결론</h3>', '<h3 class="step">결론(중간)</h3>')
before = before.replace('<span class="label">KEY POINT</span>', '<span class="label">KEY POINT — 가설 통과</span>')

text = before + after

# ─── 6) 챕터간 .bridge 삽입 ─────────────────────────────────────
bridges = {
    "ch1":  "<code>list</code> 와는 다른 새 자료형이 왜 필요한지 알았으니, 다음 의문은 — 그런데 dict 의 키로는 무엇이든 다 쓸 수 있나? CH02 가 키의 자격을 본다.",
    "ch2":  "키의 자격을 알았다면, 그 키로 값을 꺼내는 방법이 두 가지라는 사실이 다음 의문이 된다 — 엄격한 <code>d[k]</code> 와 안전한 <code>d.get()</code>. 둘은 언제 어느 쪽을 써야 하는가?",
    "ch3":  "조회를 익혔으면 다음은 변경이다. dict 는 한 자리(<code>d[k] = v</code>)에서 갱신·삭제까지 끝낼 수 있는데, 그 비결은 무엇인가?",
    "ch4":  "값을 바꿨더니 <code>keys()</code>/<code>values()</code> 의 결과가 따라 바뀐다 — 그렇다면 뷰는 스냅샷이 아니라는 뜻인가? CH05 에서 확인한다.",
    "ch5":  "뷰가 살아있는 창이라는 사실을 확인했으니, 그 창이 보여주는 키의 <strong>순서</strong> 는 어떻게 결정되는가? 삽입 순서인가, 정렬인가?",
    "ch6":  "순서가 보존된다는 사실은 알았다. 그렇다면 dict 를 <code>copy()</code> 로 복사할 때, 그 안에 들어 있는 list/dict 까지 같이 복사되는가?",
    "ch7":  "얕은 복사의 함정이 dict 안에서 명확해졌다. 그러면 두 dict 를 <strong>합칠</strong> 때는 어떻게 되는가? Python 3.9 의 <code>|</code> 연산자와 컴프리헨션이 답한다.",
    "ch8":  "구문이 충분히 풍부해졌으니 이제 실전 적용. CH09 에서 <code>dict</code> + <code>pickle</code> 로 직원 관리 미니 프로젝트를 만들고, 디스크 직렬화까지 묶어 본다.",
    "ch9":  "실전에서 가장 자주 만나는 함정 한 가지가 남았다 — 반복(<code>for k in d</code>) 중에 dict 의 크기를 바꾸면 어떻게 되는가?",
    "ch10": "표면 동작은 거의 다 봤다. 이제 마지막 의문 — 왜 dict 의 조회·삽입은 평균 <code>O(1)</code> 인가? CPython <code>Objects/dictobject.c</code> 안으로 들어간다.",
    "ch11": "내부까지 모두 확인했다. CH12 에서 출발 의문 — \"list 까지 익혔는데 왜 또 새 자료형 dict 가 필요한가?\" — 으로 돌아가 한 문장으로 압축한다.",
}

# 각 section 의 닫는 </section> 직후에 bridge div 삽입
# 정규식: <section id="chN">...</section> 뒤에 우리가 매칭한 ID 별로 추가
def insert_bridges(html: str) -> str:
    out = html
    for chid, msg in bridges.items():
        # 해당 section 의 시작 위치
        sec_start = out.find(f'<section id="{chid}">')
        if sec_start == -1:
            continue
        # 그 뒤로 처음 만나는 </section>
        end = out.find("</section>", sec_start)
        if end == -1:
            continue
        end_close = end + len("</section>")
        bridge_html = (
            f'\n\n<div class="bridge">\n'
            f'  <strong>다음 챕터로 가는 다리</strong> — {msg}\n'
            f'</div>'
        )
        out = out[:end_close] + bridge_html + out[end_close:]
    return out

text = insert_bridges(text)

HTML.write_text(text, encoding="utf-8")
print(f"new size: {len(text)} bytes")

# 검증
checks = {
    "blockquote.cite css": "blockquote.cite {" in text,
    ".bridge css":        ".bridge {" in text,
    "intro bridge":       "이 글이 추적하는 한 줄 의문" in text,
    "가설 라벨":           '<span class="label">가설</span>' in text,
    "결론(중간)":          '<h3 class="step">결론(중간)</h3>' in text,
    "최종 결론":           '<h3 class="step">최종 결론</h3>' in text,
    "FINAL CONCLUSION":   'FINAL CONCLUSION' in text,
    "KEY POINT 가설 통과": 'KEY POINT — 가설 통과' in text,
    "ch11 bridge":        "출발 의문" in text and "list 까지 익혔는데" in text,
}
for k, v in checks.items():
    print(f"  [{'OK' if v else 'FAIL'}] {k}")

# 다리 개수
bridge_count = text.count('<strong>다음 챕터로 가는 다리</strong>')
print(f"  bridges inserted: {bridge_count} (expected 11)")
