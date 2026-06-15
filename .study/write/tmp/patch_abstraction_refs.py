# patch_abstraction_refs.py
# abstraction.html 각 챕터에 ref-chain (근거 출처) 블록 추가 + CSS 삽입
# 실행: & "c:\_proj\python_workspace\.venv\Scripts\python.exe" "c:\_proj\python_workspace\.study\blog\tmp\patch_abstraction_refs.py"

import re, pathlib, sys

HTML = pathlib.Path(r"c:\_proj\python_workspace\.study\blog\abstraction.html")
html = HTML.read_text(encoding='utf-8')

# ── 중복 실행 방지 ──────────────────────────────────────────────────────────
if 'class="ref-chain"' in html:
    print("[SKIP] ref-chain 이 이미 삽입되어 있습니다. 중복 방지.")
    sys.exit(0)

# ══════════════════════════════════════════════════════════════════════════════
# 1. CSS 추가
# ══════════════════════════════════════════════════════════════════════════════
REF_CSS = """
    /* ------------ 근거 출처 체인 (ref-chain) ------------ */
    .ref-chain {
      border-left: 4px solid var(--accent-4);
      background: #F7F5FD;
      border: 1px solid #d8d0f0;
      padding: 14px 18px;
      margin: 14px 0 18px;
    }
    .ref-chain .ref-title {
      font-weight: 800;
      font-size: 0.82rem;
      color: var(--accent-4);
      letter-spacing: 0.08em;
      text-transform: uppercase;
      margin: 0 0 10px;
    }
    .ref-chain ol {
      margin: 0;
      padding-left: 20px;
    }
    .ref-chain ol li {
      margin-bottom: 7px;
      font-size: 0.9rem;
      line-height: 1.6;
    }
    .ref-chain ol li strong {
      display: inline-block;
      min-width: 110px;
      color: var(--accent-4);
      font-size: 0.78rem;
      letter-spacing: 0.05em;
      text-transform: uppercase;
    }
    .ref-chain a { color: var(--accent-3); }
    .ref-chain code { font-size: 0.88em; }
"""

MOBILE_MARKER = '    /* ------------ 모바일 ------------ */'
assert MOBILE_MARKER in html, "모바일 CSS 마커를 찾지 못함"
html = html.replace(MOBILE_MARKER, REF_CSS + MOBILE_MARKER, 1)
print("[OK] CSS 추가 완료")

# ══════════════════════════════════════════════════════════════════════════════
# 2. ref-chain 블록 정의 (섹션 ID → HTML)
#    출처: docs.python.org, peps.python.org, github.com/python/cpython
# ══════════════════════════════════════════════════════════════════════════════
def rc(title, items):
    """ref-chain HTML 생성 헬퍼"""
    lis = '\n'.join(
        f'      <li><strong>{k}</strong> {v}</li>'
        for k, v in items
    )
    return f'''<div class="ref-chain">
  <p class="ref-title">📚 근거 출처 — {title}</p>
  <ol>
{lis}
  </ol>
</div>
'''

DOCS = "https://docs.python.org/3"
CPYTHON = "https://github.com/python/cpython/blob/main"
PEPS = "https://peps.python.org"

# 섹션 ID → ref-chain HTML
REFS = {
    'ch0': rc(
        'CH00 · C/C++ vtable vs Python 동적 디스패치',
        [
            ('공식 문서 ①',
             f'<a href="{DOCS}/reference/datamodel.html#customizing-attribute-access" target="_blank" rel="noopener">'
             f'Python Data Model § Customizing attribute access</a> — '
             f'"The default behavior for attribute access is to get, set, or delete the attribute from an object\'s dictionary." '
             f'→ Python이 vtable 대신 __dict__ 탐색을 선택한 공식 근거'),

            ('공식 문서 ②',
             f'<a href="{DOCS}/reference/datamodel.html#method-resolution-order" target="_blank" rel="noopener">'
             f'Python Data Model § Method Resolution Order</a> — '
             f'C3 선형화 알고리즘으로 <code>__mro__</code> 튜플 결정. '
             f'<code>type.__mro__</code>에 직접 접근해 탐색 순서 확인 가능'),

            ('CPython 소스',
             f'<a href="{CPYTHON}/Objects/typeobject.c" target="_blank" rel="noopener">'
             f'Objects/typeobject.c → <code>_PyType_Lookup()</code></a> — '
             f'MRO 튜플(<code>mro</code>)을 순서대로 순회하며 각 클래스의 <code>tp_dict</code>에서 이름을 탐색하는 실제 C 구현체. '
             f'vtable과 달리 런타임마다 탐색이 발생하는 이유가 여기 있음'),

            ('공식 문서 ③',
             f'<a href="{DOCS}/library/types.html#types.MethodType" target="_blank" rel="noopener">'
             f'types.MethodType</a> — '
             f'런타임에 인스턴스에 메서드를 동적으로 바인딩하는 공식 방법. '
             f'C++ vtable은 컴파일 타임 포인터 고정이므로 동등한 연산이 언어 수준에서 불가능'),

            ('workspace 확인',
             f'<code>python_oop/class_oop3.py</code> — Animal/Dog/Cat의 덕 타이핑 동작이 '
             f'<code>__mro__</code> 탐색의 실제 예제'),

            ('실행 검증',
             f'<code>abstraction_runner.py §00</code> → <code>logs/00_vtable_vs_python.txt</code>'),
        ]
    ),

    'ch1': rc(
        'CH01 · 덕 타이핑',
        [
            ('공식 문서',
             f'<a href="{DOCS}/glossary.html#term-duck-typing" target="_blank" rel="noopener">'
             f'Python Glossary § duck-typing</a> — '
             f'"Pythonic programming style that determines an object\'s type by inspection of its method or attribute signature rather than by explicit relationship to some type object." '
             f'→ "구현 누락을 호출 시점에 알게 된다"는 결론의 공식 근거'),

            ('workspace 확인',
             f'<code>python_oop/class_oop3.py</code> — Animal/Dog/Cat 원본 + '
             f'다형성 루프 <code>for an in animals: an.speak()</code>가 덕 타이핑 동작의 실례'),

            ('실행 검증',
             f'<code>abstraction_runner.py §01</code> → <code>logs/01_duck_typing.txt</code>'),
        ]
    ),

    'ch2': rc(
        'CH02 · ABC로 인터페이스 강제하기',
        [
            ('공식 문서',
             f'<a href="{DOCS}/library/abc.html" target="_blank" rel="noopener">'
             f'docs.python.org/3/library/abc.html</a> — '
             f'"A class that has a metaclass derived from ABCMeta cannot be instantiated unless all of its abstract methods and abstract properties are overridden." '
             f'→ "객체 생성 시점 차단"의 공식 명세'),

            ('PEP 3119',
             f'<a href="{PEPS}/pep-3119/" target="_blank" rel="noopener">'
             f'PEP 3119 — Introducing Abstract Base Classes</a> — '
             f'도입 동기: "덕 타이핑의 구현 누락 감지 불가" 문제를 해결. '
             f'ABCMeta + @abstractmethod 조합을 통해 에러를 호출 시점 → 생성 시점으로 당김'),

            ('CPython 소스 ①',
             f'<a href="{CPYTHON}/Lib/abc.py" target="_blank" rel="noopener">'
             f'Lib/abc.py → <code>ABCMeta.__new__()</code></a> — '
             f'<code>_abc_init(cls)</code>를 호출해 <code>__abstractmethods__</code> frozenset을 초기화. '
             f'이 집합이 비어있지 않으면 클래스가 추상 클래스로 표시됨'),

            ('CPython 소스 ②',
             f'<a href="{CPYTHON}/Objects/typeobject.c" target="_blank" rel="noopener">'
             f'Objects/typeobject.c → <code>object_new()</code></a> — '
             f'<code>Py_TPFLAGS_IS_ABSTRACT</code> 플래그가 세트된 타입은 '
             f'인스턴스 생성 시 <code>TypeError</code>를 발생시키는 실제 C 구현체. '
             f'"어떤 메서드가 미구현인지" 메시지에 명시됨'),

            ('workspace 확인',
             f'<code>python_oop/class_oop4.py</code> — Animal(ABC) + Dog/Cat. '
             f'주석 처리된 <code>Animal()</code> 직접 인스턴스화 코드가 바로 이 TypeError 유발 예제'),

            ('실행 검증',
             f'<code>abstraction_runner.py §02</code> → <code>logs/02_abc_basic.txt</code>'),
        ]
    ),

    'ch3': rc(
        'CH03 · ABC로 컬렉션 인터페이스 강제하기',
        [
            ('공식 문서 ①',
             f'<a href="{DOCS}/library/abc.html#abc.abstractmethod" target="_blank" rel="noopener">'
             f'abc.abstractmethod</a> — '
             f'<code>__len__</code>, <code>__contains__</code>, <code>__getitem__</code> 같은 '
             f'매직 메서드에도 abstractmethod 적용 가능. 누락 시 동일하게 생성 시점 TypeError'),

            ('공식 문서 ②',
             f'<a href="{DOCS}/library/collections.abc.html" target="_blank" rel="noopener">'
             f'collections.abc — Abstract Base Classes for Containers</a> — '
             f'파이썬 표준 라이브러리가 실제로 ABC를 사용해 Sequence·Mapping·Container 등 '
             f'컬렉션 인터페이스를 정의하는 방식. AbstractCollection은 이 패턴을 직접 구현한 것'),

            ('workspace 확인',
             f'<code>python_oop/class_oop2.py</code> — MyBox/MyList/MyNumber가 각자 '
             f'<code>__len__</code>, <code>__contains__</code>를 구현. '
             f'ABC로 묶으면 <code>__getitem__</code>까지 강제 가능'),

            ('실행 검증',
             f'<code>abstraction_runner.py §03</code> → <code>logs/03_abc_decorators.txt</code>'),
        ]
    ),

    'ch4': rc(
        'CH04 · typing.Protocol — 구조적 서브타이핑',
        [
            ('공식 문서',
             f'<a href="{DOCS}/library/typing.html#typing.Protocol" target="_blank" rel="noopener">'
             f'typing.Protocol</a> — '
             f'"A class is protocol if it directly has Protocol as a base class. '
             f'Allows structural subtyping (static duck typing)." '
             f'→ 상속 없이 메서드 이름만 맞으면 호환 — 구조적 서브타이핑의 공식 명세'),

            ('PEP 544',
             f'<a href="{PEPS}/pep-0544/" target="_blank" rel="noopener">'
             f'PEP 544 — Protocols: Structural subtyping (static duck typing)</a> — '
             f'도입 동기: 기존 클래스를 수정하지 않고 타입 호환성을 구조적으로 판단. '
             f'"If it walks like a duck and quacks like a duck, it is a duck."'),

            ('CPython 소스',
             f'<a href="{CPYTHON}/Lib/typing.py" target="_blank" rel="noopener">'
             f'Lib/typing.py → <code>_ProtocolMeta.__instancecheck__()</code></a> — '
             f'<code>@runtime_checkable</code> 시 isinstance 판별 로직: '
             f'메서드 이름 존재 여부만 확인. 파라미터 시그니처까지는 검사하지 않음 '
             f'(PEP 544 § Runtime checkable protocols 참고)'),

            ('workspace 확인',
             f'<code>python_oop/class_oop3.py</code> — Animal/Dog/Cat 원본. '
             f'Robot(Animal 상속 없음)이 Speakable로 판별되는 구조적 서브타이핑 확인'),

            ('실행 검증',
             f'<code>abstraction_runner.py §04</code> → <code>logs/04_protocol.txt</code>'),
        ]
    ),

    'ch5': rc(
        'CH05 · ABC vs Protocol — 선택 기준',
        [
            ('공식 문서 ①',
             f'<a href="{DOCS}/library/abc.html" target="_blank" rel="noopener">'
             f'abc 모듈</a> — ABC는 공통 구현 포함 가능, 명시적 상속 필요'),

            ('공식 문서 ②',
             f'<a href="{DOCS}/library/typing.html#typing.Protocol" target="_blank" rel="noopener">'
             f'typing.Protocol</a> — 기존 클래스를 수정하지 않고 구조적 서브타이핑 적용 가능. '
             f'"@runtime_checkable 없이는 isinstance 검사 불가" — 공식 제약 사항'),

            ('실행 검증',
             f'<code>abstraction_runner.py §05</code> → <code>logs/05_abc_vs_protocol.txt</code>'),
        ]
    ),

    'ch6': rc(
        'CH06 · __abstractmethods__ 와 ABCMeta 내부',
        [
            ('공식 문서',
             f'<a href="{DOCS}/library/abc.html#abc.ABCMeta" target="_blank" rel="noopener">'
             f'abc.ABCMeta</a> — '
             f'"Metaclass for defining Abstract Base Classes. '
             f'Use this metaclass to create an ABC." '
             f'→ <code>class ABC(metaclass=ABCMeta): pass</code> 와 동일함을 공식 명시'),

            ('CPython 소스 ①',
             f'<a href="{CPYTHON}/Lib/abc.py" target="_blank" rel="noopener">'
             f'Lib/abc.py → <code>ABCMeta.__new__()</code></a> — '
             f'클래스 생성 시 @abstractmethod 가 붙은 메서드 이름을 '
             f'<code>__abstractmethods__</code> frozenset에 기록. '
             f'서브클래스가 모두 구현하면 frozenset() (공집합)이 됨'),

            ('CPython 소스 ②',
             f'<a href="{CPYTHON}/Objects/typeobject.c" target="_blank" rel="noopener">'
             f'Objects/typeobject.c → <code>object_new()</code></a> — '
             f'<code>__abstractmethods__</code>가 비어있지 않으면 <code>Py_TPFLAGS_IS_ABSTRACT</code> 세트 → '
             f'인스턴스 생성 시 TypeError. '
             f'이 플래그는 <code>type.__new__()</code>에서 계산됨'),

            ('실행 검증',
             f'<code>abstraction_runner.py §06</code> → <code>logs/06_internals.txt</code>'),
        ]
    ),

    'ch7': rc(
        'CH07 · 결제 시스템 — Template Method 패턴',
        [
            ('공식 문서',
             f'<a href="{DOCS}/library/abc.html" target="_blank" rel="noopener">'
             f'abc 모듈</a> — "Abstract methods can be called by concrete methods or not at all." '
             f'→ ABC가 공통 로직(process())을 포함하고 서브클래스가 세부 구현을 담당하는 '
             f'Template Method 패턴의 공식 근거'),

            ('PEP 3119',
             f'<a href="{PEPS}/pep-3119/#rationale" target="_blank" rel="noopener">'
             f'PEP 3119 § Rationale</a> — '
             f'"ABCs are a form of interface checking more powerful than hasattr(). '
             f'They allow frameworks to require specific APIs while deferring implementation." '
             f'→ 결제 시스템처럼 프레임워크가 구현 계약을 강제하는 실전 사용 패턴'),

            ('CPython 소스',
             f'<a href="{CPYTHON}/Objects/typeobject.c" target="_blank" rel="noopener">'
             f'Objects/typeobject.c → <code>object_new()</code></a> — '
             f'BrokenGateway() 생성 시점에 TypeError가 발생하는 것이 바로 이 함수의 '
             f'<code>Py_TPFLAGS_IS_ABSTRACT</code> 검사 결과'),

            ('실행 검증',
             f'<code>abstraction_runner.py §07</code> → <code>logs/07_payment_system.txt</code>'),
        ]
    ),

    'ch8': rc(
        'CH08 · 부트캠프 실습 코드와의 연결',
        [
            ('공식 문서',
             f'<a href="{DOCS}/library/functions.html#isinstance" target="_blank" rel="noopener">'
             f'isinstance()</a> / '
             f'<a href="{DOCS}/library/functions.html#issubclass" target="_blank" rel="noopener">'
             f'issubclass()</a> — '
             f'ABC 계층 내 isinstance/issubclass는 MRO 기반으로 동작. '
             f'"Return True if the object argument is an instance of the classinfo argument"'),

            ('workspace 확인',
             f'<code>python_oop/class_oop4.py</code> — '
             f'수업 실습 코드 원본. isinstance/issubclass + 직접 인스턴스화 금지의 실례'),

            ('실행 검증',
             f'<code>abstraction_runner.py §08</code> → <code>logs/08_bootcamp_link.txt</code>'),
        ]
    ),
}

# ══════════════════════════════════════════════════════════════════════════════
# 3. 섹션별 ref-chain 삽입
#    전략: HTML을 <h2 class="chap" id="chN"> 단위로 분리 후
#          각 조각의 첫 번째 <h3 class="step">테스트 앞에 ref-chain 삽입
# ══════════════════════════════════════════════════════════════════════════════
# 전체 요약 h2(style= 포함) 앞에서 잘라서 '본문'과 '요약+푸터' 분리
SUMMARY_MARKER = '<h2 class="chap" style='
split_idx = html.index(SUMMARY_MARKER)
body   = html[:split_idx]
suffix = html[split_idx:]

# h2 chap 경계로 분리 (id="chN" 를 가진 것만)
parts = re.split(r'(?=<h2 class="chap" id="ch)', body)
# parts[0] = CSS/header 영역, parts[1]~ = 각 챕터

processed_parts = [parts[0]]
inserted_count  = 0

for part in parts[1:]:
    # 현재 파트의 섹션 ID 추출 (ch0, ch1, ... ch8)
    m = re.match(r'<h2 class="chap" id="(ch\d+)"', part)
    if not m:
        processed_parts.append(part)
        continue

    sec_id = m.group(1)
    ref_html = REFS.get(sec_id)

    if ref_html is None:
        processed_parts.append(part)
        continue

    # 이 섹션 안에서 첫 번째 <h3 class="step">테스트 위치를 찾아 ref-chain 삽입
    test_pat = re.compile(r'<h3 class="step">테스트')
    tm = test_pat.search(part)
    if tm:
        insert_pos = tm.start()
        new_part = part[:insert_pos] + ref_html + part[insert_pos:]
        processed_parts.append(new_part)
        inserted_count += 1
        print(f"[OK] {sec_id} ref-chain 삽입")
    else:
        processed_parts.append(part)
        print(f"[WARN] {sec_id}: 테스트 스텝을 찾지 못함 — 삽입 건너뜀")

html = ''.join(processed_parts) + suffix

# ══════════════════════════════════════════════════════════════════════════════
# 4. 저장
# ══════════════════════════════════════════════════════════════════════════════
HTML.write_text(html, encoding='utf-8')
print(f"\n[SAVED] {HTML}")

# ══════════════════════════════════════════════════════════════════════════════
# 5. 검증
# ══════════════════════════════════════════════════════════════════════════════
rc_count    = html.count('class="ref-chain"')
term_count  = html.count('class="terminal"')
body_count  = html.count('class="terminal-body"')

print(f"\n=== 검증 결과 ===")
print(f"삽입된 ref-chain 수  : {inserted_count}")
print(f"div.ref-chain 수     : {rc_count}")
print(f"div.terminal 수      : {term_count}")
print(f"pre.terminal-body 수 : {body_count}  {'[PASS]' if term_count == body_count else '[FAIL]'}")
