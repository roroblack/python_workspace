"""retrospective_w1w2.html 본문(<main>...</main>)을 서사 사슬 구조로 교체."""
from pathlib import Path

HTML = Path(r"c:\_proj\python_workspace\.study\blog\retrospective_w1w2.html")

NEW_BODY = r"""<main>
<div class="page">

<!-- ============================================================ 도입 다리 -->
<div class="bridge" style="margin-top:18px">
  <strong>이 회고가 추적하는 한 줄 의문</strong> — "C 출신인 나에게 파이썬은 어디서부터 다른가?"
  1주차 첫 파일 <code>python_logic/allocation.py</code> 의 동적 할당 주석을 본 순간 떠오른 이 질문이,
  CH01 ~ CH06 의 6개 프로젝트를 거치며 어떻게 답을 얻어갔는지를 사슬로 따라간다.
  CH07 에서 출발 의문으로 회수한다.
</div>

<!-- ============================================================ CH01 -->
<section id="ch1">
  <h2 class="chap">
    <span class="num">CH 01</span>
    <span class="week-badge">1주차</span>python_logic — 변수를 선언하지 않는 언어, 그 첫 위화감<a href="#ch1" class="anchor-link">#</a>
  </h2>

  <h3 class="step">학습</h3>
  <p>
    1주차 첫 프로젝트 <code>python_logic/</code> 는
    <code>allocation.py</code>, <code>builtin_function.py</code>, <code>naming.py</code>,
    <code>test_str.py</code>, <code>input_mission1.py</code>, <code>input_mission2.py</code>,
    <code>make_function.py</code>, <code>using_input.py</code> 8개로 구성됐다.
    가장 강하게 기억에 남은 줄은 <code>allocation.py</code> 주석 하나 —
    <em>"파이썬에서의 변수 할당은 동적 할당임. 실행 시(Runtime) 메모리에 변수 공간을 만들고 값을 기록하는 것."</em>
    C 의 <code>int x;</code> 같은 자료형 선언을 단 한 번도 쓰지 않는다는 사실이 가장 먼저 부딪힌 벽이었다.
  </p>
  <blockquote class="cite">
    If the target list is a comma-separated list of targets: The object must be an iterable with the same number of items
    as there are targets in the target list, and the items are assigned, from left to right, to the corresponding targets.
    <span class="src">— <a href="https://docs.python.org/3/reference/simple_stmts.html#assignment-statements" target="_blank" rel="noopener">docs.python.org/3/reference § Assignment statements</a></span>
  </blockquote>
  <pre><code class="language-python"># allocation.py — 첫 위화감을 일으킨 패턴들
x, y, z = 10, 20, 30           # 한 줄 다중 할당
first, second = second, first  # swap — 임시 변수 없이 성립
value += 10                    # 복합 대입
</code></pre>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    <code>a, b = b, a</code> 가 임시 변수 없이 성립하려면 — ① 오른쪽이 먼저 튜플로 평가되고 ② 그 튜플이
    좌측 타깃 리스트에 언패킹되어야 한다. 공식 reference 의 "from left to right" 라는 문구가 이 동작을 보장한다면,
    가설은 통과한다.
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">KEY POINT — 가설 통과</span>
    파이썬은 변수를 "선언" 하지 않는다 — 대입 순간 런타임이 메모리를 동적으로 할당한다.
    swap 이 작동하는 이유도 이 동적성 위에 "오른쪽 튜플 평가 → 왼쪽 언패킹" 규칙이 얹혀 있기 때문이다.
    출발 의문 "C와 어디서부터 다른가" 의 첫 답: <strong>"선언이 없다"</strong>.
  </div>
  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 선언이 없다면, 자료를 담는 컬렉션도 타입 고정 없이 무엇이든 담을 수 있을 것이다.
    그렇다면 list 와 tuple 은 어떻게 다르고, 왜 list 의 메서드가 그렇게 많은가? CH02 에서 확인한다.
  </div>
</section>


<!-- ============================================================ CH02 -->
<section id="ch2">
  <h2 class="chap">
    <span class="num">CH 02</span>
    <span class="week-badge">1주차</span>python_collection — list 메서드가 왜 이렇게 많은가<a href="#ch2" class="anchor-link">#</a>
  </h2>

  <h3 class="step">학습</h3>
  <p>
    <code>python_collection/</code> 은 <code>main.py</code> 와
    <code>my_collections/test_list/</code> (list_sample.py, list_sample2.py, list_mission1.py, list_mission2.py),
    <code>my_collections/test_tuple/</code> (tuple_sample.py) 로 구성됐다.
    list 의 거의 모든 메서드 — append · remove · insert · pop · extend · reverse · sort · count · index — 를 직접 호출했다.
    그 다음 tuple_sample.py 에서 <code>t[0] = 99</code> 를 시도하다 <code>TypeError: 'tuple' object does not support item assignment</code>
    를 받았다. 가변(mutable) 과 불변(immutable) 의 차이를 처음으로 손으로 체감한 순간이었다.
  </p>
  <blockquote class="cite">
    The main difference between tuples and lists is that tuples are immutable. … Tuples are usually used for heterogeneous data,
    while lists are usually used for homogeneous sequences.
    <span class="src">— <a href="https://docs.python.org/3/tutorial/datastructures.html#tuples-and-sequences" target="_blank" rel="noopener">docs.python.org/3/tutorial § Tuples and Sequences</a></span>
  </blockquote>
  <p>
    그리고 <code>main.py</code> 의 import 3가지 형식이 두 번째 충격이었다. 같은 모듈을 부르는 데 왜 형식이 셋이나 있는가?
  </p>
  <pre><code class="language-python"># main.py — import 3 형식
import my_collections.test_list.list_sample as ls
from my_collections.test_list.list_sample import make_list1, make_list2
import my_collections.test_list.list_sample2 as ls2
</code></pre>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    list 메서드가 많은 이유는 "가변" 이라서 — 불변 타입에는 정의할 수 없는 in-place 변형 연산이 모두 들어가 있기 때문이다.
    tuple_sample.py 의 TypeError 가 그 증거다. 그리고 import 3가지 형식은 모두 동일하게
    <code>sys.modules</code> 에 모듈 전체를 캐시한 뒤, 현재 네임스페이스에 어떤 이름을 바인딩할지만 다를 것이다.
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">KEY POINT — 가설 통과</span>
    list 의 메서드 다수(append/insert/pop/sort/...) 는 in-place 변형이며, tuple 에는 그 자리가 비어 있다 — 가변/불변의 직접적 결과.
    import 3형식은 "모듈 전체 로드 + 어떤 이름을 노출하느냐" 의 차이일 뿐, 메모리에 올라가는 모듈은 한 번뿐이다.
  </div>
  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — list/tuple 같은 메모리 구조는 사라지면 끝이지만,
    파일 핸들·DB 커넥션 같은 외부 자원은 닫지 않으면 누수가 난다. 1주차 마지막 프로젝트 <code>python_fileio/</code> 가 바로 그 자원 안전 관리를 가르쳤다.
  </div>
</section>


<!-- ============================================================ CH03 -->
<section id="ch3">
  <h2 class="chap">
    <span class="num">CH 03</span>
    <span class="week-badge">1주차</span>python_fileio — 예외가 나도 파일이 닫히는 이유<a href="#ch3" class="anchor-link">#</a>
  </h2>

  <h3 class="step">학습</h3>
  <p>
    <code>python_fileio/</code> 는 1주차 마지막 프로젝트(0504)다.
    <code>main.py</code> 가 CLI 진입점이고, <code>match/case</code> 로 메뉴를 라우팅했다.
    하위에는 <code>fileio_sample/fileio_module.py</code>(텍스트 R/W), <code>fileio_sample/fileio_module2.py</code>(이진 R/W),
    <code>loop/while_sample.py</code>, <code>test_dict/dict_sample.py</code>, <code>fileio/fileio_mission.py</code> 가 있다.
    이 프로젝트에서 처음 <code>with open(...) as f:</code> 패턴을 만났다.
  </p>
  <blockquote class="cite">
    The with statement is used to wrap the execution of a block with methods defined by a context manager …
    The context manager's <code>__exit__()</code> method is invoked. If an exception caused the suite to be exited,
    its type, value, and traceback are passed as arguments to <code>__exit__()</code>.
    <span class="src">— <a href="https://docs.python.org/3/reference/compound_stmts.html#the-with-statement" target="_blank" rel="noopener">docs.python.org/3/reference § The with statement</a></span>
  </blockquote>
  <pre><code class="language-python"># main.py — match/case CLI 라우터 (Python 3.10+)
while loop_sw:
    key = str(input("select menu: "))
    match key:
        case '1': fm.test_fwrite()
        case '3': fm.test_fread()
        case '0': loop_sw = False
</code></pre>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    <code>with</code> 블록 안에서 예외가 발생해도 파일이 닫히는 이유는 — <code>__exit__</code> 이 예외 발생 경로로도 호출되기 때문이다.
    공식 reference 의 "If an exception caused the suite to be exited … passed as arguments to __exit__" 가 이 동작을 보장한다면,
    <code>f.close()</code> 직접 호출보다 더 안전한 자원 관리 방식이라는 결론이 따라온다.
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">KEY POINT — 가설 통과</span>
    <code>with</code> 는 정상 종료·예외 종료 모든 경로에서 <code>__exit__</code> 를 호출한다.
    파일 객체는 IOBase 의 context manager 프로토콜을 구현하므로 누수가 원천 차단된다.
    출발 의문에 대한 두 번째 답: <strong>"파이썬은 자원 관리도 객체 프로토콜로 표현한다"</strong> — C 의 free()/fclose() 를 잊을 위험이 사라지는 자리다.
  </div>
  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 자원을 객체 프로토콜로 다룬다면, 객체 자체의 설계는 어떻게 되는가?
    2주차의 첫날(0506) <code>python_oop/</code> 가 그 답을 본격적으로 가르쳤다 — 그리고 거기서 자습 글의 씨앗이 됐다.
  </div>
</section>


<!-- ============================================================ CH04 -->
<section id="ch4">
  <h2 class="chap">
    <span class="num">CH 04</span>
    <span class="week-badge">2주차</span>python_oop — class_oop4.py 한 줄의 TypeError<a href="#ch4" class="anchor-link">#</a>
  </h2>

  <h3 class="step">학습</h3>
  <p>
    2주차 첫날(0506) 은 OOP 전체를 6개 파일로 순차 실습했다.
  </p>
  <table>
    <thead>
      <tr><th>파일</th><th>주제</th><th>핵심 개념</th></tr>
    </thead>
    <tbody>
      <tr><td><code>class_sample.py</code></td><td>클래스 기초</td><td>동적 속성, <code>__dict__</code> 첫 인식</td></tr>
      <tr><td><code>class_oop.py</code></td><td>캡슐화</td><td>private(<code>__</code>), protected(<code>_</code>), 이름 맹글링</td></tr>
      <tr><td><code>class_oop2.py</code></td><td>연산자 오버로딩</td><td><code>__len__</code>·<code>__contains__</code>·<code>__getitem__</code> (MyBox·MyList·MyNumber)</td></tr>
      <tr><td><code>class_oop3.py</code></td><td>다형성</td><td>Animal/Dog/Cat — 타입 검사 없이 <code>speak()</code> 호출</td></tr>
      <tr><td><code>class_oop4.py</code></td><td>추상화(ABC)</td><td><code>Animal(ABC)</code> + <code>@abstractmethod</code></td></tr>
      <tr><td><code>exception/except_sample.py</code></td><td>예외</td><td>ZeroDivision/Index/Key/Value 직접 raise</td></tr>
    </tbody>
  </table>
  <p>
    가장 인상 깊었던 줄은 <code>class_sample.py</code> 의 주석 — <em>"dict 로 클래스가 생성되는 구조상 그렇게 됨"</em>.
    인스턴스마다 독립적인 <code>__dict__</code> 가 있어서 동적으로 속성을 추가할 수 있다는 사실이 여기서 시작됐다.
    그리고 <code>class_oop4.py</code> 마지막의 한 줄 — 주석 처리된 <code>Animal()</code> — 이 모든 의문의 폭발점이었다.
  </p>
  <blockquote class="cite">
    A class that has a metaclass derived from ABCMeta cannot be instantiated unless all of its abstract methods
    and properties are overridden.
    <span class="src">— <a href="https://docs.python.org/3/library/abc.html" target="_blank" rel="noopener">docs.python.org/3/library/abc</a></span>
  </blockquote>
  <pre><code class="language-python"># class_oop4.py — 줄 하나가 자습 글 한 편을 만들었다
from abc import ABC, abstractmethod
class Animal(ABC):
    @abstractmethod
    def speak(self): pass

class Dog(Animal):
    def speak(self): print("강아지가 멍멍 짖습니다.")

# Animal()  ← 이 한 줄이 TypeError 를 낸다. 왜?
</code></pre>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    <code>class_oop3.py</code> 에서는 ABC 없이도 다형성이 동작했다 (덕 타이핑). 그런데 <code>class_oop4.py</code> 의
    <code>Animal()</code> 은 호출 시점이 아니라 <strong>객체 생성 시점</strong> 에 막힌다.
    공식 문서가 말하는 "ABCMeta … cannot be instantiated unless all of its abstract methods … are overridden" 이 사실이라면,
    이 차단은 어떤 내부 자료구조 한 줄(예: 추상 메서드 집합) 의 검사로 구현되어 있을 것이다.
    이 가설을 따라 추상화 한 편을 자습 글로 정리했다 → <code>abstraction.html</code>.
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">KEY POINT — 가설 통과</span>
    덕 타이핑은 호출 시점에 missing 메서드를 발견하지만, ABC 는 객체 생성 시점에 차단한다.
    이 차이가 <strong>"인터페이스 키워드가 없는 언어가 어떻게 인터페이스를 강제하는가"</strong> 의 답이다.
    부트캠프의 한 줄 주석이 자습 노트 한 편의 출발점이 됐다 — 회고 차원에서 가장 큰 수확.
  </div>
  <div class="callout">
    <span class="label">발견</span>
    <code>class_oop2.py</code> 의 MyBox·MyList·MyNumber 가 자습 글 abstraction.html 의 예제로 그대로 재사용됐다.
    GUIDE.txt §16-C "workspace 기존 파일 우선" 원칙이 처음으로 작동한 사례.
  </div>
  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 클래스를 설계했으면 그 다음은 모듈로 묶고 패키지로 배포하는 단계다.
    그런데 그 전에 한 가지 의문이 떠올랐다 — 파이썬은 <code>import</code> 한 줄로 어떻게 그 모듈을 찾아오는가?
  </div>
</section>


<!-- ============================================================ CH05 -->
<section id="ch5">
  <h2 class="chap">
    <span class="num">CH 05</span>
    <span class="week-badge">2주차</span>python_module / python_package — 모듈은 어디서 찾아오는가<a href="#ch5" class="anchor-link">#</a>
  </h2>

  <h3 class="step">학습</h3>
  <p>
    0507 에 두 프로젝트를 함께 진행했다. <code>python_module/module/my_module.py</code> 는 가변 매개변수와 예외 발생을 함께 학습할 수 있는
    유틸 모음이다.
  </p>
  <pre><code class="language-python"># my_module.py — 가변 매개변수 + 예외 발생 + docstring
def div(a, b):
    '두 수를 전달 받아서 몫을 리턴'
    if b == 0:
        raise Exception("0으로 나눌 수 없습니다.")
    return a / b

def max(*args):              # 가변 매개변수
    '전달받은 값들 중 가장 큰 값을 리턴'
    ...
</code></pre>
  <p>
    <code>python_package/</code> 는 <code>pyproject.toml</code>·<code>setup.py</code> 를 갖춘 실제 배포 가능한 패키지 구조다.
    <code>pip install -e .</code> 로 로컬 개발 모드 설치를 직접 해본 첫 경험.
    <code>test_set/set_sample.py</code> 에서는 <code>frozenset</code> 과 집합 연산(교·합·차) 을 함께 실습했다.
  </p>
  <blockquote class="cite">
    When a regular package is imported, its <code>__init__.py</code> file is implicitly executed …
    During import, the import system first checks <code>sys.modules</code>; if the module name is found there, it is used.
    <span class="src">— <a href="https://docs.python.org/3/reference/import.html" target="_blank" rel="noopener">docs.python.org/3/reference § The import system</a></span>
  </blockquote>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    <code>import my_module</code> 한 줄로 모듈이 메모리에 올라가려면 — ① 먼저 <code>sys.modules</code> 캐시를 보고
    ② 없으면 built-in / frozen → <code>sys.path</code> 순서로 디렉터리를 뒤진다.
    그리고 <code>pip install -e .</code> 는 site-packages 안에 <code>.pth</code> 파일을 추가해 sys.path 에 프로젝트 루트를 끼워 넣을 것이다.
    이 가설이 맞다면, 소스 수정이 즉시 import 에 반영되는 동작이 자연스럽게 설명된다.
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">KEY POINT — 가설 통과</span>
    탐색 순서: <code>sys.modules</code> → built-in → frozen → <code>sys.path</code>.
    개발 모드 설치는 <code>.pth</code> 파일 한 줄로 sys.path 를 확장한다.
    출발 의문의 또 한 답: <strong>"모듈 시스템조차 런타임 자료구조로 표현되어 있다"</strong> — C 의 컴파일 타임 링킹과 정반대다.
  </div>
  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 모듈을 잘 묶었으니 이제 사용자가 보는 화면을 띄울 차례다. 0508 에는 GUI 도구로 넘어갔는데,
    여기서 또 한 번 위화감이 왔다 — Streamlit 은 입력이 들어올 때마다 스크립트를 처음부터 다시 돌린다.
  </div>
</section>


<!-- ============================================================ CH06 -->
<section id="ch6">
  <h2 class="chap">
    <span class="num">CH 06</span>
    <span class="week-badge">2주차</span>python_gui / streamlit — 매 입력마다 스크립트가 다시 돈다고?<a href="#ch6" class="anchor-link">#</a>
  </h2>

  <h3 class="step">학습</h3>
  <p>
    <code>python_gui/1.py</code> ~ <code>5.py</code> 에서 Streamlit 위젯을 단계적으로 익혔다 —
    <code>st.text_input</code>·<code>number_input</code>·<code>selectbox</code>·<code>checkbox</code>·<code>button</code>·<code>success/warning/error</code>.
  </p>
  <pre><code class="language-python"># python_gui/1.py — Streamlit 기본 위젯
import streamlit as st
st.title("제목"); st.header("헤더"); st.subheader("소제목")
name   = st.text_input("이름 입력")
age    = st.number_input("나이 입력", min_value=0, max_value=100)
gender = st.selectbox("성별 선택", ["남", "여"])
agree  = st.checkbox("동의합니다")
btn    = st.button("확인")
</code></pre>
  <p>
    이후 <code>streamlit_login_csv_project/app/main.py</code> 로 pandas + matplotlib + Streamlit 을 통합한 미니 프로젝트를 완성했다 —
    CSV 사용자 인증, 로그인 후 매출 차트 표시까지. 그러다 곧장 부딪힌 문제 — 로그인 성공 변수가 다음 입력마다 사라졌다.
  </p>
  <blockquote class="cite">
    Session State is a way to share variables between reruns, for each user session. … In addition to the ability to store
    and persist state, Streamlit also exposes the ability to manipulate state using Callbacks.
    <span class="src">— <a href="https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state" target="_blank" rel="noopener">docs.streamlit.io · st.session_state</a></span>
  </blockquote>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    Streamlit 이 매 위젯 변경마다 스크립트 전체를 처음부터 다시 돌린다면, 일반 변수에 담은 로그인 상태는 매번 초기화될 수밖에 없다.
    공식 문서의 "share variables between reruns, for each user session" 이 사실이라면 — <code>st.session_state</code> 는
    실제로는 <strong>스크립트 외부(서버 측)에 사용자 세션 단위로 살아있는 dict</strong> 일 것이다.
    그래야 재실행 사이에 상태가 유지된다.
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">KEY POINT — 가설 통과</span>
    <code>st.session_state</code> 는 사용자 세션에 연결된 서버 측 dict 다. 스크립트가 수십 번 재실행돼도 세션이 살아있는 동안 값이 유지된다.
    1주차 <code>python_fileio</code> 의 "with 로 자원 안전 관리" 정신이 여기서는 <code>pathlib.Path(__file__).resolve().parents[1]</code> 로
    CSV 경로를 안전하게 잡는 형태로 이어졌다.
  </div>
  <div class="bridge">
    <strong>마지막 챕터로 가는 다리</strong> — 6개 프로젝트를 모두 통과했다. 이제 출발 의문 — "C 출신인 나에게 파이썬은 어디서부터 다른가?" — 으로 돌아간다.
  </div>
</section>


<!-- ============================================================ CH07 -->
<section id="ch7">
  <h2 class="chap">
    <span class="num">CH 07</span>2주간의 답 — 출발 의문으로 돌아오기<a href="#ch7" class="anchor-link">#</a>
  </h2>

  <h3 class="step">학습</h3>
  <p>
    회고를 시작하며 던진 한 줄짜리 의문은 단순했다 — "C 출신인 나에게 파이썬은 어디서부터 다른가?"
    CH01 ~ CH06 이 각자 한 조각씩 답을 내놓았으니, 이제 그 조각들을 한 자리에 모은다.
  </p>

  <h3 class="step">의문 → 가설(최종)</h3>
  <div class="qbox">
    <span class="label">가설(최종)</span>
    각 챕터의 결론들을 합치면 한 문장으로 압축될 수 있을 것이다 — "파이썬은 C 가 컴파일 타임에 결정하는 것들(타입 선언, 메모리 레이아웃,
    링킹, 인터페이스 강제) 을 거의 전부 <strong>런타임 객체 모델</strong> 로 옮긴 언어다." 이 한 줄이 6개 프로젝트 모두를 설명한다면,
    회고는 닫힌다.
  </div>

  <h3 class="step">최종 결론</h3>
  <div class="keypoint">
    <span class="label">FINAL CONCLUSION</span>
    가설은 통과했다. 정리하면 —
    <ol>
      <li><strong>CH01 (python_logic)</strong> — 변수 선언 없음. 대입 순간 런타임이 메모리를 동적 할당.</li>
      <li><strong>CH02 (python_collection)</strong> — 가변/불변 구분이 메서드 집합을 결정. 컬렉션 자체가 객체.</li>
      <li><strong>CH03 (python_fileio)</strong> — 자원 관리도 <code>__enter__</code>/<code>__exit__</code> 객체 프로토콜.</li>
      <li><strong>CH04 (python_oop)</strong> — 인터페이스 키워드의 부재를 <code>ABCMeta</code> 와 <code>__abstractmethods__</code> 로 메움. 자습 글의 씨앗.</li>
      <li><strong>CH05 (python_module/package)</strong> — 모듈 시스템조차 <code>sys.modules</code>·<code>sys.path</code> 라는 런타임 자료구조.</li>
      <li><strong>CH06 (streamlit)</strong> — UI 상태조차 서버 측 dict(<code>session_state</code>)로 표현.</li>
    </ol>
    공통 패턴: <strong>"C 가 컴파일 타임/링커/OS 에 맡긴 모든 것을, 파이썬은 런타임에 살아있는 객체로 표현한다."</strong>
    이것이 1·2주차에서 얻은 답이다. 다음 단계(SQL → 웹 크롤링 → 데이터 분석) 에서도 이 관점이 지속해서 작동하는지가 3주차의 새 의문이 된다.
  </div>
</section>

</div>
</main>

"""

text = HTML.read_text(encoding="utf-8")
start_marker = "<main>\n<div class=\"page\">"
end_marker = "</div>\n</main>"

start = text.find(start_marker)
end = text.find(end_marker, start) + len(end_marker)
assert start != -1 and end > start, "markers not found"

new_text = text[:start] + NEW_BODY.strip() + "\n\n" + text[end:].lstrip()
HTML.write_text(new_text, encoding="utf-8")
print(f"replaced {end - start} chars with {len(NEW_BODY)} chars")
print(f"new file size: {len(new_text)}")
