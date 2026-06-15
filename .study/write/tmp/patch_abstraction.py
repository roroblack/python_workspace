# patch_abstraction.py
# abstraction.html 에 CH00(C vtable vs Python) 삽입 + h3.step 의문/결론 레이블 추가
# 실행: & "c:\_proj\python_workspace\.venv\Scripts\python.exe" "c:\_proj\python_workspace\.study\blog\tmp\patch_abstraction.py"

import re, pathlib

HTML = pathlib.Path(r"c:\_proj\python_workspace\.study\blog\abstraction.html")
html = HTML.read_text(encoding="utf-8")

# ══════════════════════════════════════════════════════════════════════
# 1. TOC 에 CH00 추가
# ══════════════════════════════════════════════════════════════════════
OLD_TOC = '        <li><a href="#ch1">덕 타이핑 — 추상화 없이 쓰면 어떻게 되나</a></li>'
NEW_TOC = ('        <li><a href="#ch0">C/C++ vtable vs Python — 왜 파이썬은 다른 방식을 선택했나</a></li>\n'
           '        <li><a href="#ch1">덕 타이핑 — 추상화 없이 쓰면 어떻게 되나</a></li>')

assert OLD_TOC in html, "TOC 치환 대상을 찾지 못했습니다"
html = html.replace(OLD_TOC, NEW_TOC, 1)
print("[OK] TOC CH00 추가")

# ══════════════════════════════════════════════════════════════════════
# 2. §1 앞에 CH00 섹션 삽입
# ══════════════════════════════════════════════════════════════════════
CH00_HTML = '''
<!-- ────────────────────────────────────────────────────────
     §0  C/C++ vtable vs Python 추상화 방식 비교
──────────────────────────────────────────────────────────── -->
<h2 class="chap" id="ch0">
  <span class="num">CH 00</span>C/C++ vtable vs Python — 왜 파이썬은 다른 방식을 선택했나
  <a class="anchor-link" href="#ch0">#</a>
</h2>

<h3 class="step">학습</h3>
<p>
  C++에서 가상 함수(<code>virtual</code>)를 선언하면 컴파일러가 <strong>vtable(가상 함수 테이블)</strong>을 만든다.
  각 클래스마다 함수 포인터 배열이 <strong>컴파일 타임에 고정</strong>되고, 런타임에는 포인터를 역참조해 메서드를 호출한다.
  이 덕분에 속도가 빠르지만, "이 클래스에 <code>speak()</code>가 있으면 동물로 취급한다"는 유연한 처리는 어렵다.
  순수 가상 함수(<code>pure virtual</code>)를 구현하지 않으면 <strong>컴파일 오류</strong>가 발생한다.
</p>
<p>
  파이썬은 다르다. 메서드 호출은 <strong>런타임에 동적으로</strong> 이루어진다.
  <code>obj.method()</code>를 호출하면 파이썬은 <code>__mro__</code>(Method Resolution Order) 순서로
  각 클래스의 <code>__dict__</code>를 탐색해 해당 이름의 함수를 찾는다.
  덕분에 상속 계층 없이도 다형성을 구현할 수 있고(<strong>덕 타이핑</strong>),
  런타임에 메서드를 교체하는 것도 가능하다.
  단, 구현 누락을 컴파일 타임에 잡지 못한다는 단점이 있어 <strong>ABC · Protocol</strong>로 보완한다.
</p>

<div class="ascii">  [C++ vtable — 컴파일 타임 고정]       [Python — 런타임 __mro__ 탐색]
  ───────────────────────────────────   ──────────────────────────────────────
  클래스 정의 시 vtable 생성            메서드 호출마다 __mro__ 순서 탐색
  ┌─────────────┐                       obj.speak() 호출 시:
  │   vtable    │                         1. obj.__dict__ 탐색
  │ ─────────── │                         2. type(obj).__dict__ 탐색
  │ speak → fn1 │                         3. 상위 클래스 순서대로 탐색
  │ move  → fn2 │                         4. 찾지 못하면 AttributeError
  └─────────────┘
  런타임 교체 불가 (포인터 고정)         런타임 교체 가능 (dict 교체)
  미구현 → 컴파일 오류                   미구현 → 런타임 AttributeError</div>

<table>
  <thead>
    <tr>
      <th>항목</th>
      <th>C++ vtable</th>
      <th>Python 동적 디스패치</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>바인딩 시점</td>
      <td>컴파일 타임 고정</td>
      <td>런타임 <code>__mro__</code> 탐색</td>
    </tr>
    <tr>
      <td>속도</td>
      <td>포인터 역참조 1회 → 빠름</td>
      <td><code>__dict__</code> 탐색 → 상대적으로 느림</td>
    </tr>
    <tr>
      <td>유연성</td>
      <td>낮음 (컴파일 후 고정)</td>
      <td>높음 (런타임 메서드 교체 가능)</td>
    </tr>
    <tr>
      <td>타입 검사</td>
      <td>컴파일 타임 강제</td>
      <td>없음(덕 타이핑) → ABC·Protocol로 보완</td>
    </tr>
    <tr>
      <td>다형성 구현</td>
      <td>상속 + <code>virtual</code> 필요</td>
      <td>메서드 이름만 맞으면 OK</td>
    </tr>
    <tr>
      <td>추상 클래스</td>
      <td>pure virtual → 컴파일 오류</td>
      <td>ABC → 객체 생성 시점 <code>TypeError</code></td>
    </tr>
  </tbody>
</table>

<h3 class="step">의문</h3>
<div class="qbox">
  <span class="label">Q</span>
  파이썬의 <code>__mro__</code>는 어떤 순서로 클래스를 탐색하나?
  런타임 교체(몽키 패칭)란 무엇이고, 어떻게 동작하나?
  덕 타이핑의 장점은 유연성, 단점은 구현 누락 감지 불가 — 이것을 어떻게 확인할 수 있나?
</div>

<h3 class="step">테스트 — MRO 탐색·덕 타이핑·런타임 메서드 교체</h3>
<pre><code class="language-python">import types

# 1. Python MRO(__mro__)와 __dict__ 탐색 순서
#    C++ vtable: 컴파일 타임에 함수 포인터 고정
#    Python: 런타임에 __mro__ 순서로 __dict__ 탐색
class Base:
    def method(self): print("Base.method() 호출")

class Child(Base):
    def method(self): print("Child.method() 호출")

print(f"Child.__mro__ : {[c.__name__ for c in Child.__mro__]}")
print(f"'method' in Child.__dict__: {'method' in Child.__dict__}")
print(f"'method' in Base.__dict__ : {'method' in Base.__dict__}")
c = Child()
c.method()   # Child.__dict__ 에서 먼저 발견 → Base 탐색 불필요

# 2. 덕 타이핑 — 타입 검사 없이 메서드 존재 여부만으로 동작
class Duck:
    def quack(self): print("꽥꽥! (Duck)")

class Person:
    def quack(self): print("꽥꽥 흉내냄 (Person) — Duck 상속 없음")

class Stone: pass  # quack 없음

def make_it_quack(thing):
    thing.quack()  # 타입 검사 없음 — AttributeError 면 실행 시 터짐

for obj in [Duck(), Person()]:
    make_it_quack(obj)   # 둘 다 동작 — 덕 타이핑

try:
    make_it_quack(Stone())
except AttributeError as e:
    print(f"AttributeError: {e}")

# 3. Python 동적 디스패치 — 런타임에 인스턴스 메서드 교체 가능 (C++ vtable 불가)
class Robot:
    def speak(self): print("로봇: 삐-뽀!")

r = Robot()
r.speak()   # 기본 구현

# 런타임에 이 인스턴스만 메서드 교체 (클래스 전체 영향 없음)
r.speak = types.MethodType(lambda self: print("로봇: 업그레이드됨!"), r)
r.speak()   # 동일 객체인데 다른 메서드 — C++ vtable에서는 불가능

r2 = Robot()
r2.speak()  # 새 인스턴스는 원래 메서드 유지

# 4. 덕 타이핑 장단점 요약
print("\n[덕 타이핑 장단점]")
print("장점: 상속 계층 없이도 다형성 — 유연하고 재사용성 높음")
print("단점: 구현 누락을 컴파일 타임에 잡지 못함 — 런타임 AttributeError")
print("해결: ABC(명시적 강제) 또는 Protocol(구조적 타입 힌트)으로 보완")</code></pre>

<div class="terminal">
  <div class="terminal-header"><span class="t-label">00_vtable_vs_python</span></div>
  <pre class="terminal-body">placeholder_00</pre>
</div>

<h3 class="step">결론</h3>
<div class="keypoint">
  <span class="label">CONCLUSION</span>
  파이썬은 <strong>유연성과 생산성</strong>을 위해 vtable 대신 런타임 <code>__mro__</code> 탐색을 선택했다.
  덕 타이핑은 상속 계층 없이도 다형성을 만들 수 있는 강력한 도구이지만,
  구현 누락을 <strong>실행 전에 잡지 못한다</strong>는 단점이 있다.
  이를 보완하기 위해 파이썬은 <strong>ABC(명시적 강제)</strong>와
  <strong>Protocol(구조적 타입 힌트)</strong>을 제공한다 — 이것이 이 글 전체의 주제다.
</div>

'''

ANCHOR_BEFORE_CH1 = '<!-- ────────────────────────────────────────────────────────\n     §1  덕 타이핑'
assert ANCHOR_BEFORE_CH1 in html, "§1 앵커를 찾지 못했습니다"
html = html.replace(ANCHOR_BEFORE_CH1, CH00_HTML + ANCHOR_BEFORE_CH1, 1)
print("[OK] CH00 섹션 삽입")

# ══════════════════════════════════════════════════════════════════════
# 3. 기존 챕터(CH01~CH08)의 qbox 앞에 h3.step "의문" 추가
#    keypoint 앞에 h3.step "결론" 추가
#    CH00은 이미 위에서 삽입할 때 포함시켰으므로 제외
# ══════════════════════════════════════════════════════════════════════

# CH00 섹션 이후부터만 치환 (CH00 내부는 이미 레이블 있음)
# → CH00 부분과 나머지를 분리해서 처리
split_marker = ANCHOR_BEFORE_CH1
idx = html.index(split_marker)
ch00_part = html[:idx]  # CH00 포함 header 영역
rest_part  = html[idx:]  # CH01 이후

# qbox 앞에 h3.step "의문" 추가 (h3.step 이미 있으면 건너뜀)
# 패턴: 앞에 step "의문" 이 없는 qbox
def add_step_before(text, step_label, div_class):
    """h3.step {step_label} 이 없는 div.{div_class} 앞에 추가"""
    pattern = r'(?<!<h3 class="step">' + re.escape(step_label) + r'</h3>\n)(<div class="' + div_class + r'")'
    # 더 안전하게: 앞에 </h3>\n 가 없는 경우만 추가
    lines = text.split('\n')
    result = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if f'<div class="{div_class}">' in line:
            # 바로 앞 비어있지 않은 줄 확인
            prev_nonempty = ''
            for j in range(len(result) - 1, -1, -1):
                if result[j].strip():
                    prev_nonempty = result[j].strip()
                    break
            if f'>{step_label}</h3>' not in prev_nonempty:
                result.append(f'<h3 class="step">{step_label}</h3>')
        result.append(line)
        i += 1
    return '\n'.join(result)

rest_part = add_step_before(rest_part, '의문', 'qbox')
rest_part = add_step_before(rest_part, '결론', 'keypoint')

html = ch00_part + rest_part
print("[OK] h3.step 의문/결론 레이블 추가")

# ══════════════════════════════════════════════════════════════════════
# 4. 저장
# ══════════════════════════════════════════════════════════════════════
HTML.write_text(html, encoding="utf-8")
print(f"[SAVED] {HTML}")

# ══════════════════════════════════════════════════════════════════════
# 5. 검증
# ══════════════════════════════════════════════════════════════════════
qbox_count  = html.count('<div class="qbox">')
key_count   = html.count('<div class="keypoint">')
step_q      = html.count('<h3 class="step">의문</h3>')
step_c      = html.count('<h3 class="step">결론</h3>')
ch00_ok     = 'id="ch0"' in html
toc_ok      = 'href="#ch0"' in html

print(f"\n=== 검증 결과 ===")
print(f"ch0 섹션 삽입    : {'OK' if ch00_ok else 'FAIL'}")
print(f"TOC ch0 링크     : {'OK' if toc_ok else 'FAIL'}")
print(f"div.qbox 수      : {qbox_count}")
print(f"h3.step 의문 수  : {step_q}  (일치: {'OK' if step_q == qbox_count else f'FAIL (qbox={qbox_count})'})")
print(f"div.keypoint 수  : {key_count}")
print(f"h3.step 결론 수  : {step_c}  (일치: {'OK' if step_c == key_count else f'FAIL (key={key_count})'})")
