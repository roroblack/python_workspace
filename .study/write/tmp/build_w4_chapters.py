# -*- coding: utf-8 -*-
"""Chapters 2-9 + footer for retrospective_w4.html, appended to build_w4.py at runtime."""
# This file is imported into build_w4.py via exec or by simple string concat below.

CH2 = """
<section id="ch2">
  <h2 class="chap"><span class="num">CH 02</span>처음 한 일: ERD부터 시작한 이유<a href="#ch2" class="anchor-link">#</a></h2>

  <h3 class="step">학습</h3>
  <p>16(토) 19:30 디스코드 회의에서 백엔드 팀원이 &ldquo;ERD부터 그리자&rdquo;고 제안했다. 첫 2일(15~16)은 그래서 ERD를 짜고 프로젝트 구조를 잡고 아이디어를 정형화하는 데 거의 다 썼다. 코드를 한 줄도 치지 않고 두 가지에만 집중한 셈이다 — <strong>(1) 어떤 데이터를 어떤 테이블로 둘 것인가</strong>, <strong>(2) 그 데이터를 어떤 화면에 어떤 형태로 흘릴 것인가</strong>.</p>

  <p>주제 좁히기에서 살아남은 페이지는 4개였다 — 홈 / 수소차 등록현황 / 수소차 충전소 / FAQ. 각 페이지에 필요한 컬럼을 적어 내려가니 자연스럽게 후보 테이블이 정리됐다.</p>
  <ul>
    <li><strong>regions</strong> — 시·도 단위 지역 (모든 통계의 분모)</li>
    <li><strong>car_registrations</strong> — 연도별 지역별 수소차 누적 등록 대수</li>
    <li><strong>hydrogen_charging_station</strong> — 충전소 위도·경도 포함</li>
    <li><strong>faq</strong> — 질문/답변 한 쌍</li>
    <li><strong>crawl_stat</strong> — 마지막 크롤 시각 (히스토리가 아닌 &ldquo;최신 1건&rdquo;)</li>
  </ul>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox"><span class="label">가설</span>
    크롤링 결과를 시계열로 모두 쌓을 필요는 없다. ① 화면이 보여주는 단위는 &ldquo;가장 최근 1회 수집&rdquo;이면 충분하고, ② 장기 백업/롤백 요구가 없으니 history 테이블 대신 <code>crawl_stat</code> 1행으로 <strong>"target_type × last_crawled_at"</strong> 만 유지하면 된다. 이 가설이 깨지지 않는다면 스키마가 한 단계 단순해진다.
  </div>

  <h3 class="step">시행</h3>
  <p>처음 그려본 ERD를 팀에 공유했다 — 디스코드 첨부 원본을 그대로 인라인으로 첨부한다(아래 이미지). 이 시점의 ERD에는 두 가지 미완 지점이 있었다.</p>
  <ol>
    <li><code>crawl_stat</code>을 처음엔 <strong>크롤링 히스토리</strong>로 모델링해, 외래키로 다른 테이블과 연결하려 했다.</li>
    <li><code>target_type</code> 컬럼 제약을 <code>UNIQUE</code>로만 두고 값 후보를 강제하지 않았다.</li>
  </ol>

  __IMG_ERD_INITIAL__

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint"><span class="label">PARTIAL OK — 1차 ERD</span>
    가설은 통과했다. 화면 4개에 필요한 컬럼은 모두 5개 테이블에 매핑됐고, history는 필요 없었다. 다만 <code>crawl_stat</code>의 모델링(독립 테이블화 + <code>CHECK</code> 제약)이 다음 챕터에서 한 차례 더 수정됐다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 1차 ERD의 두 미완 지점을 어떻게 정리하면 &ldquo;최신만 유지&rdquo;가 SQL로도 정확히 표현될까? 다음 챕터에서 <code>CHECK</code> 제약과 외래키 정규화로 닫는다.
  </div>
</section>
"""

CH3 = """
<section id="ch3">
  <h2 class="chap"><span class="num">CH 03</span>ERD 완성과 폴더·파일 명명 규칙<a href="#ch3" class="anchor-link">#</a></h2>

  <h3 class="step">학습</h3>
  <p>1차 ERD의 두 미완 지점은 17(일) 회의에서 정리됐다.</p>
  <ol>
    <li><code>crawl_stat</code>은 <strong>히스토리가 아닌 독립 테이블</strong>로 두고 N:1 외래키를 만들지 않는다. 행 자체가 &ldquo;가장 최근 1회 수집&rdquo;을 의미한다.</li>
    <li><code>target_type</code>은 <code>UNIQUE</code>가 아니라 <strong>값 후보를 강제</strong>해야 한다. 그래서 <code>CHECK (target_type IN ('car_registration', 'station', 'faq'))</code>로 바꿨다.</li>
    <li>수소충전소 테이블은 위도·경도(<code>lat</code>, <code>lon</code>)를 컬럼으로 가져 Folium 지도에서 바로 마커를 그릴 수 있게 했다.</li>
  </ol>

  <p>실제로 채택된 DB 스키마 SQL은 다음과 같다. <code>regions</code>를 가운데 두고 등록·충전소가 외래키로 묶이는 정규화 형태다.</p>

<pre><code class="language-sql">create database if not exists crawler_db
    default character set utf8mb4 collate utf8mb4_unicode_ci;
use crawler_db;

create table if not exists regions (
    region_id   smallint primary key auto_increment,
    region_name varchar(20) not null unique
);

create table if not exists car_registrations (
    id        bigint primary key auto_increment,
    region_id smallint not null,
    stat_year smallint not null,
    count     int default 0,
    foreign key (region_id) references regions (region_id),
    unique key uq_stat (region_id, stat_year)
);

create table if not exists hydrogen_charging_station (
    id           int primary key auto_increment,
    region_id    smallint not null,
    station_name varchar(100) not null,
    address      varchar(255),
    lat          decimal(10, 7),
    lon          decimal(10, 7),
    foreign key (region_id) references regions (region_id)
);

create table if not exists faq (
    faq_id   int primary key auto_increment,
    question text not null,
    answer   text
);

create table if not exists crawl_stat (
    crawl_id        int primary key auto_increment,
    target_type     varchar(30) not null,
    last_crawled_at datetime,
    check (target_type in ('car_registration', 'station', 'faq'))
);</code></pre>

  <p>완성된 ERD 다이어그램은 다음과 같다.</p>

  __IMG_ERD_FINAL__

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox"><span class="label">가설</span>
    팀 4명이 같은 컬럼 위에서 작업하려면 ERD만으로는 부족하다. <strong>폴더·파일 명명 규칙</strong>이 같이 굳어야, 각자 자기 브런치에서 작업해도 머지에서 충돌이 줄어든다. 가설: &ldquo;크롤러는 <code>crawler_*.py</code>, 데이터 계층은 <code>data/</code>, 화면은 <code>app.py</code> 하나&rdquo; 형태로 단순화하면 의존 그래프가 한 방향이 된다.
  </div>

  <h3 class="step">시행</h3>
  <p>아래 트리가 합의된 결과다. 화면(<code>app.py</code>) → 데이터 계층(<code>data/</code>) → 크롤러(<code>crawling/</code>) 한 방향 의존이 보장된다.</p>

<pre><code>SKN32-1st-3Team/
├─ app.py                        # Streamlit 대시보드 (4페이지)
├─ crawling/
│  ├─ crawler_molit.py           # 국토부 수소차 등록 현황 크롤러
│  ├─ crawler_station.py         # 공공데이터포털 수소충전소 크롤러
│  ├─ crawler_faq.py             # ev.or.kr FAQ 크롤러
│  └─ models.py                  # @dataclass: CarRegistrationItem / FaqItem / StationItem
├─ data/
│  ├─ db.py                      # 엔진/스키마/CRUD
│  ├─ repository.py              # Repository 패턴 (UPSERT)
│  └─ service.py                 # CrawlService / SchedulerService
├─ dbscript/dbscript_table.sql   # DB 스키마 SQL
├─ assets/                       # 스크린샷·ERD 이미지
└─ requirements.txt</code></pre>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint"><span class="label">KEY POINT — ERD + 폴더 규칙</span>
    ERD는 화면이 필요로 하는 컬럼에서 역으로 도출됐고(<code>regions</code> 정규화 + <code>crawl_stat</code> 독립 테이블 + <code>CHECK</code>), 폴더는 <code>app → data → crawling</code> 한 방향 의존으로 굳었다. 이제 누구든 자기 브런치에서 자기 파일만 만지면 된다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 스키마와 폴더가 굳었으니, 이제 모두가 같은 출발선에 서기 위한 <strong>프로토타입</strong>이 필요하다. 팀장인 내가 뼈대를 만들어 공유하기로 했다.
  </div>
</section>
"""

CH4 = """
<section id="ch4">
  <h2 class="chap"><span class="num">CH 04</span>프로토타입: Streamlit + MySQL + Playwright 뼈대<a href="#ch4" class="anchor-link">#</a></h2>

  <h3 class="step">학습</h3>
  <p>프로토타입의 목표는 화려한 화면이 아니라 <strong>&ldquo;팀원이 PR을 올렸을 때 머지가 가능한 상태&rdquo;</strong> 였다. 그래서 4가지를 뼈대로 잡았다.</p>
  <ul>
    <li><strong>Streamlit GUI</strong> — 기본 템플릿. 좌측 사이드바에 필터(연도 슬라이더 · 지역 드롭다운).</li>
    <li><strong>크롤러</strong> — 국토부 통계누리는 <strong>BeautifulSoup4 정적 크롤링</strong>, 공공데이터포털 충전소·EV 누리집 FAQ처럼 JS 렌더링이 필요한 곳은 <strong>Playwright</strong>.</li>
    <li><strong>DB 계층</strong> — <code>regions</code> 외래키 기반 정규화 + SQLAlchemy.</li>
    <li><strong>FAQ 폴백 5건</strong> — 외부 사이트가 다운돼도 페이지가 비지 않도록 디폴트 FAQ를 코드에 박아 둠.</li>
  </ul>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox"><span class="label">가설</span>
    크롤러가 만드는 데이터 객체와 DB가 받는 컬럼 사이에 <strong>한 곳</strong>만 둬야 한다. <code>@dataclass</code> 한 개당 INSERT SQL 한 개를 <strong>Repository.MODEL_INSERT_SQL</strong> 매핑으로 묶으면, 새 크롤러를 추가해도 데이터 모델만 늘리면 된다.
  </div>

  <h3 class="step">시행</h3>
  <p>실제 <code>data/repository.py</code>의 핵심부 — <strong>모델별 INSERT SQL 매핑</strong>과 <strong>바인딩 파라미터 방식</strong>으로 SQL Injection 위험을 낮춘 구조다.</p>

<pre><code class="language-python"># SKN32-1st-3Team/data/repository.py (발췌)
class Repository:
    MODEL_INSERT_SQL = {
        CarRegistrationItem: '''
            INSERT INTO car_registrations (region_id, stat_year, count)
            VALUES (:region_id, :stat_year, :count)
        ''',
        FaqItem: '''
            INSERT INTO faq (question, answer)
            VALUES (:question, :answer)
        ''',
        StationItem: '''
            INSERT INTO hydrogen_charging_station
                (region_id, station_name, address, lat, lon)
            VALUES (:region_id, :station_name, :address, :lat, :lon)
        ''',
    }

    MODEL_TARGET_TYPE = {
        CarRegistrationItem: 'car_registration',
        FaqItem:             'faq',
        StationItem:         'station',
    }

    def save_items(self, items: list) -> int:
        if not items:
            return 0
        model_class = type(items[0])
        sql          = self.MODEL_INSERT_SQL[model_class]
        column_names = [c.name for c in fields(model_class)]
        params_list  = [self._item_to_params(it, column_names) for it in items]
        with self.engine.begin() as conn:
            result = conn.execute(text(sql), params_list)
            conn.execute(
                text('UPDATE crawl_stat SET last_crawled_at = :ts WHERE target_type = :t'),
                {'ts': datetime.now(), 't': self.MODEL_TARGET_TYPE[model_class]},
            )
        return result.rowcount</code></pre>

  <p>화면 쪽 결과물은 다음과 같았다. 연도·지역을 고르면 등록 현황 그래프와 충전소 지도가 같이 갱신되고, FAQ는 키워드 검색이 동작한다.</p>

  __IMG_DASHBOARD__
  __IMG_REG_TREND__
  __IMG_REGION_BAR__
  __IMG_REGION_PIE__
  __IMG_STATION_MAP__
  __IMG_STATION_DETAIL__
  __IMG_SIDEBAR__

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint"><span class="label">KEY POINT — 같은 출발선</span>
    프로토타입이 마스터에 올라간 순간부터 팀원 누구든 &ldquo;자기 파트의 함수 시그니처&rdquo;만 알면 작업할 수 있게 됐다. 이게 4일짜리 프로젝트의 진짜 가드레일이다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 같은 코드를 4명이 동시에 만지려면 &ldquo;작업 단위&rdquo;와 &ldquo;합치는 시점&rdquo;을 약속해야 한다. 스프레드시트와 깃 브런치 전략이 그 약속이 됐다.
  </div>
</section>
"""

CH5 = """
<section id="ch5">
  <h2 class="chap"><span class="num">CH 05</span>일정·회의·협업 도구 (스프레드시트 · 깃 브런치)<a href="#ch5" class="anchor-link">#</a></h2>

  <h3 class="step">학습</h3>
  <p>회의·작업 단위·디버깅 모두 같은 시트 한 장에 모았다. &ldquo;팀 정보 · 역할 · 작업목록 · 회의내용 · 디버깅 노트&rdquo; 5개 탭으로 구성했고, 작업 흐름은 다음과 같다.</p>

  <table>
    <thead><tr><th>날짜</th><th>형태</th><th>시간</th><th>주요 결과</th></tr></thead>
    <tbody>
      <tr><td>05-15(금)</td><td>대면(강의)</td><td>당일</td><td>팀 결성 · 주제(수소차) · 페이지 4개 · 역할 1차 분담</td></tr>
      <tr><td>05-16(토)</td><td>디스코드</td><td>19:30 ~ 20:30</td><td>1차 ERD 공유 · 스프레드시트 구성</td></tr>
      <tr><td>05-17(일)</td><td>디스코드</td><td>18:00 ~ 19:00</td><td>ERD 확정 · 폴더/네이밍 합의 · 프로토타입 공유</td></tr>
      <tr><td>05-18(월)</td><td>강의 + 추가</td><td>09:00 ~ 18:00 / 18:00 ~ 21:00</td><td>브런치 작업 · 1차 디버깅 다수</td></tr>
      <tr><td>05-19(화)</td><td>강의 + 발표</td><td>09:00 ~ 15:00</td><td>최종 디버깅 · 발표 준비 · 시연</td></tr>
    </tbody>
  </table>

  <p>작업분담 시트(스프레드시트 gid=471644863)의 진행 요약은 다음과 같다 — 전체 14개 작업이 모두 Done으로 닫혔다.</p>

<pre class="terminal-body">전체 작업 수 : 14
Done         : 14
Doing        : 0
Todo         : 0
Blocked      : 0
완료율(%)    : 107.7  (※ 추가로 잡힌 작업까지 닫혀서 100%를 넘김)</pre>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox"><span class="label">가설</span>
    4명이 동시에 같은 저장소를 만지면 머지가 가장 비싼 비용이 된다. <strong>브런치 전략</strong>으로 (1) 자기 파트만 자기 브런치에 푸시하고, (2) 회의 때 모여 머지하는 방식이면 충돌이 1일 1회로 묶인다.
  </div>

  <h3 class="step">시행</h3>
  <p>브런치 구성은 다음과 같다. 두 명은 작명 규칙을 따르지 않았지만 4명 규모라 그대로 진행했다.</p>
  <ul>
    <li><code>main</code> — 마스터(검수 통과한 코드만)</li>
    <li><code>feature/gui</code> — Streamlit 화면</li>
    <li><code>db-service</code> — Python↔MySQL 연동</li>
    <li><code>sora</code> — DB 설계 (작명 규칙 불일치)</li>
    <li><code>jihye</code> — 크롤링 (작명 규칙 불일치)</li>
  </ul>

  <p>15~18일은 &ldquo;회의 때 모여 머지&rdquo; 였지만, 19일 발표 직전에는 시간이 더 부족해져서 <strong>팀장 직접 검수 후 마스터 직접 푸시</strong> 방식으로 바뀌었다 — 각자 마스터를 최신으로 풀 받고 자기 작업 파일만 들고 있다가, 완료되면 내가 받아 검수해 마스터에 직접 푸시.</p>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint"><span class="label">KEY POINT — 동기화 비용 최소화</span>
    스프레드시트가 의사결정의 한 곳이 됐고, 브런치 전략이 머지 비용을 하루 1회로 묶었다. 단, 19일의 &ldquo;직접 푸시&rdquo; 전환은 다음 챕터에서 한 차례 사고로 돌아온다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 사람 4명 × 도구 6종 × 4일이면 버그는 반드시 11건 이상 나온다. 시트에 쌓인 11건 + 시트에 못 적은 2건이 어떤 가설로 닫혔는지 챕터를 통째로 할애한다.
  </div>
</section>
"""

CH6 = """
<section id="ch6">
  <h2 class="chap"><span class="num">CH 06</span>디버깅 11건 + 마스터 직푸시 사건<a href="#ch6" class="anchor-link">#</a></h2>

  <h3 class="step">학습</h3>
  <p>디버깅 노트 시트(gid=1542101365)에는 18~19일 동안 닫힌 11건이 기록돼 있다. 모두 <strong>Closed</strong>다. 표는 시트 원본 그대로다.</p>

  <table>
    <thead><tr><th>#</th><th>일자</th><th>현상</th><th>담당</th><th>해결</th></tr></thead>
    <tbody>
      <tr><td>1</td><td>05-18</td>
        <td><code>save</code> 도중 <code>region_id</code> 바인딩 불일치. <code>CarRegistrationItem.region</code>은 문자열인데 <code>MODEL_INSERT_SQL</code>은 <code>:region_id</code>를 기대해 <code>_item_to_params()</code>가 키를 못 찾아 SQL 오류.</td>
        <td>박회종</td>
        <td><code>MODEL_INSERT_SQL</code>의 인터페이스를 <strong>문자열 region 기반</strong>으로 받도록 정리. 영속성 레이어(Repository/DAO) 안에서만 문자열 → PK 변환을 책임지게 해서 도메인 객체에는 PK 누설을 막음.</td></tr>
      <tr><td>2</td><td>05-18</td>
        <td>크롤링 누계 로직 오류 — <strong>분류별 수소차 등록 소계를 전부 합산</strong>하던 버그. 도메인의 모든 값을 더하면서 카운트가 부풀어 오름.</td>
        <td>김지혜</td>
        <td>수소에서 다음 분류로 넘어가는 <strong>행 번호</strong>와 <code>계</code> 문자가 있는 <strong>열 번호</strong>를 찾고, 그 다음 열 값들의 시트상 합으로 <code>count</code>를 다시 계산.</td></tr>
      <tr><td>3</td><td>05-18</td>
        <td>수소충전소 테이블 외래키 없음 에러.</td>
        <td>권소라</td>
        <td><code>FOREIGN KEY (region_id) REFERENCES regions(region_id)</code> 를 SQL에 추가.</td></tr>
      <tr><td>4</td><td>05-18</td>
        <td>슬라이더 최대값이 선형 그래프에 반영되지 않음.</td>
        <td>최연우</td>
        <td>기간 라벨과 레인지 값을 같이 사용. <code>f"기간: **{year_label(year_range[0])} ~ {year_label(year_range[1])}**"</code> 로 표기까지 맞춤.</td></tr>
      <tr><td>5</td><td>05-18</td>
        <td>월 데이터 연동 오류 — 크롤링에서 가져온 최신 월이 <code>app.py</code> 필터와 그래프에 반영되지 않음.</td>
        <td>최연우</td>
        <td><code>crawler_molit.py</code>에서 <code>last_stat_month</code>를 외부로 노출 → <code>st.session_state["stat_month"]</code>에 보관해 페이지 갱신/리런에도 초기화되지 않도록 처리.</td></tr>
      <tr><td>6</td><td>05-18</td>
        <td>필터의 키 값이 다른 탭 갔다 오면 초기화됨.</td>
        <td>최연우</td>
        <td>쉐도우키 사용. <code>st.session_state["year_range_saved"] = year_range</code> 로 저장하고 다시 진입 시 <code>get</code>으로 복원.</td></tr>
      <tr><td>7</td><td>05-18</td>
        <td>인서트 중첩 — 앱 재시작/리런마다 같은 크롤링이 다시 INSERT 되어 중복.</td>
        <td>박회종</td>
        <td><strong>UPSERT</strong>로 전환 — <code>ON DUPLICATE KEY UPDATE count = VALUES(count)</code> 를 <code>car_registrations</code> INSERT 에 부착. <code>(region_id, stat_year)</code> 유니크 키와 결합해 &ldquo;있으면 갱신, 없으면 삽입&rdquo;.</td></tr>
      <tr><td>8</td><td>05-19</td>
        <td>충전소 차트 선택 연동 오류 — 인덱스의 행 번호로 저장해서 지역을 바꾸면 같은 번호가 다른 충전소를 가리킴.</td>
        <td>최연우</td>
        <td><code>region_name + station_name + address + lat + lon</code> 으로 <code>_station_key</code>를 만들어 선택값을 안전하게 저장. 지도의 마커키와 비교해서 매칭.</td></tr>
      <tr><td>9</td><td>05-19</td>
        <td><code>python -m crawling.crawler_faq</code> 실행 시 동작하지 않음.</td>
        <td>최연우</td>
        <td>코드는 정상이고, 실제로는 EV 누리집(<a href="https://ev.or.kr/nportal/partcptn/initFaqAction.do" target="_blank" rel="noopener">ev.or.kr</a>) 사이트가 다운된 게 원인. 가능한 FAQ 링크만 사용하고 <strong>디폴트 FAQ 폴백</strong>을 추가해 페이지가 비지 않게 처리.</td></tr>
      <tr><td>10</td><td>05-19</td>
        <td>FAQ 본문의 <code>~</code> 가 마크다운 취소선으로 해석되는 문제.</td>
        <td>최연우</td>
        <td>출력 시 <code>~</code> → <code>&amp;#126;</code> HTML 엔티티로 치환.</td></tr>
      <tr><td>11</td><td>05-19</td>
        <td>저장/불러오기(ZIP) 한 뒤 선택 가능한 오브젝트들이 동작 안 함.</td>
        <td>최연우</td>
        <td>중복 업로드 방지 토큰(<code>hashlib.sha256</code>), 홈 지표 기준 수정, 차트 라디오 <code>key</code> 보강.</td></tr>
    </tbody>
  </table>

  <p>핵심 두 건은 코드까지 함께 본다.</p>

  <h4>#1 — 영속성 레이어가 PK 변환을 책임진다</h4>
<pre><code class="language-python"># crawling/models.py — region 은 "문자열" (서울 / 부산 / ...)
@dataclass
class CarRegistrationItem:
    stat_year: int
    region:    str   # ← 문자열. PK 가 아님
    count:     int

# data/repository.py — :region_id 바인딩을 만족시키는 책임은 Repository 가 진다
def _item_to_params(self, item, column_names):
    params = asdict(item)                          # {'stat_year':..,'region':'서울','count':..}
    if 'region' in params:
        params['region_id'] = self._region_to_id(params.pop('region'))
    return params                                  # {'stat_year':..,'region_id':3,'count':..}</code></pre>

  <h4>#2 — 분류 소계를 전부 더하던 합산 버그</h4>
<pre><code class="language-python"># crawling/crawler_molit.py — 잘못된 합산 (개념적 표현)
# ❌ "수소" 분류 아래 모든 행을 그냥 합산 → 분류별 소계까지 같이 더해져 두 배~수 배로 부풀어 오름
# ✅ "수소" 분류 시작 행을 찾고, 머리에서 '계' 가 적힌 열을 찾아
#     그 열 값들만 시트상 합으로 count 산출
for row_idx, row in enumerate(rows):
    if row[0] == '수소':
        start = row_idx
    if start and row[0] in ('전기', 'LPG'):       # 다음 분류 만나면 종료
        end = row_idx
        break
gye_col = header_row.index('계')
count   = sum(int(rows[r][gye_col].replace(',', '') or 0) for r in range(start, end))</code></pre>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox"><span class="label">가설</span>
    11건의 절반 이상은 <strong>경계</strong>(객체 ↔ DB · 페이지 전환 · 외부 사이트 다운)에서 발생한다. 이 경계마다 <strong>(a) 책임지는 한 레이어</strong>와 <strong>(b) 폴백/유니크 키</strong>를 명시하면 같은 버그가 재발하지 않는다.
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint"><span class="label">KEY POINT — 가설 통과 (11건 모두 Closed)</span>
    PK 변환은 Repository, 페이지 상태는 <code>st.session_state</code>, 중복은 <code>ON DUPLICATE KEY UPDATE</code>, 외부 사이트 다운은 폴백 FAQ — 책임이 분명해진 자리는 다시 부서지지 않았다.
  </div>

  <div class="callout"><span class="label">시트에 기록 안 된 2건</span>
    <strong>(가) 첫 머지에서 함수/변수 타입 불일치</strong> — 프로토타입 기반으로 작업한 내 코드와, 프로젝트 진행자가 따로 작업한 <code>repository.py</code> 의 함수/변수/타입이 어긋났다. 해결: 자료형과 파라미터를 한쪽 기준으로 통일.<br>
    <strong>(나) 5-18 마스터 직푸시 사건</strong> — 한 팀원이 마스터에 직접 푸시해 해당 경로 파일들이 전부 날아갔다. 해결: 내가 미리 백업해둔 로컬 파일로 즉시 복구 → CH05의 &ldquo;직접 푸시는 팀장 검수 뒤&rdquo; 정책 강화로 이어졌다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 코드가 다 닫힌 뒤에도 가장 어려운 시간은 <strong>발표 직전 24시간</strong>이다. 라인업과 그 24시간에 일어난 일을 정리한다.
  </div>
</section>
"""

CH7 = """
<section id="ch7">
  <h2 class="chap"><span class="num">CH 07</span>발표 준비와 마지막 날의 위태로움<a href="#ch7" class="anchor-link">#</a></h2>

  <h3 class="step">학습</h3>
  <p>발표 라인업은 다음과 같이 정해졌다.</p>
  <table>
    <thead><tr><th>구간</th><th>담당</th></tr></thead>
    <tbody>
      <tr><td>개요 발표</td><td>김지혜 (크롤링 담당)</td></tr>
      <tr><td>PPT 준비</td><td>권소라 (DB 담당)</td></tr>
      <tr><td>시연 HW</td><td>박회종 (백엔드 담당)</td></tr>
      <tr><td>발표 · 시연 · Q&amp;A</td><td>최연우 (팀장 · GUI 담당)</td></tr>
    </tbody>
  </table>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox"><span class="label">가설</span>
    발표 직전 24시간에 새로 추가되는 기능은 <strong>반드시</strong> 다른 곳을 깬다. &ldquo;오토 스케줄러&rdquo;나 &ldquo;테스트용 자료 제거&rdquo;처럼 코드 흐름을 건드리는 변경은 마지막 날에는 위험 부담이 크다.
  </div>

  <h3 class="step">시행 — 마지막 날 실제로 일어난 일</h3>
  <ul>
    <li>19일 당일까지 구현 목표였던 <strong>오토 스케줄러</strong>(APScheduler)가 말썽을 일으켰다.</li>
    <li>잘 동작하던 GUI 가 테스트용 테이블 구조체 자료를 제거하니 문제가 생겨, 의존 경로를 다시 좁혀야 했다.</li>
    <li>Q&amp;A 예상 질의 정리가 부족했다. 마지막 질문에는 완벽히 답하지 못했다.</li>
  </ul>

  <p>그래도 다행이었던 점 — DB 단(=ERD 정규화 + UPSERT)이 흔들리지 않았다. CH02~CH03 에서 굳혀둔 스키마가 마지막 날의 안전 마진이 된 셈이다.</p>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint"><span class="label">PARTIAL OK — 발표는 완수, Q&amp;A는 미흡</span>
    대본 없이 시연·Q&amp;A에 들어갔지만 프로젝트 전체를 꾸준히 점검/수정해 왔기에 시연 자체는 막힘이 없었다. Q&amp;A의 미흡은 다음 회고에서 가장 큰 개선 포인트가 된다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 잘된 점과 부족한 점을 같은 무게로 꺼내야 다음 프로젝트에서 같은 함정에 다시 빠지지 않는다.
  </div>
</section>
"""

CH8 = """
<section id="ch8">
  <h2 class="chap"><span class="num">CH 08</span>회고: 잘한 점 / 부족했던 점 / 다음 한 수<a href="#ch8" class="anchor-link">#</a></h2>

  <h3 class="step">학습 — 배운 점</h3>
  <ul>
    <li><strong>ERD 의 중요성</strong> — 화면 4개에서 역으로 도출한 5개 테이블이 4일을 지탱했다.</li>
    <li><strong>초기 프로젝트 구조도</strong> — <code>app → data → crawling</code> 한 방향 의존이 머지 비용을 낮췄다.</li>
    <li><strong>Jira 역할의 스프레드시트</strong> — 의사결정/작업/디버깅을 한 곳에 모은 게 4명짜리 팀에선 충분했다.</li>
    <li><strong>깃 브런치 분할 작업</strong> — 하루 1회 머지 정책이 충돌 비용을 압축했다.</li>
    <li><strong>경계의 비용</strong> — 객체 ↔ DB ↔ 화면 사이에서 자료형/파라미터가 미세히 어긋나면 한순간에 SQL 오류로 폭발한다.</li>
    <li><strong>혼자 다 못한다</strong> — 시연·Q&amp;A 직전에 다른 팀의 호흡을 보며, 부족함을 혼자 끌어안기보다 팀과 공유해 해결하는 길이 있다는 걸 체감했다.</li>
  </ul>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox"><span class="label">가설</span>
    다음 단위 프로젝트에서는 <strong>같은 실수의 재발 방지</strong>가 가장 큰 가치다. 이번에 잘된 3가지(① 작업현황 공유 시스템, ② ERD &amp; 프로젝트 구성 사전 설계, ③ 중요 사안의 팀 회의 결정)를 그대로 가져가고, 잘 안 된 4가지를 명시적으로 개선하면 4일이 5일치로 늘어난다.
  </div>

  <h3 class="step">개선 항목</h3>
  <ol>
    <li>팀원과의 <strong>초기 아이스브레이킹</strong> — 첫날 30분만이라도 작업이 아닌 자기소개에 쓰기.</li>
    <li><strong>함수/파라미터/반환값/자료형 사전 설계</strong> — 머지 후 어긋남을 막기 위해 인터페이스를 글로 먼저 합의.</li>
    <li><strong>깃 브런치 관리</strong> — 작명 규칙 어김 없이, 그리고 마지막 날 &ldquo;직접 푸시&rdquo;는 반드시 팀장 검수 뒤로.</li>
    <li><strong>부족함 공유</strong> — 막히면 빠르게 말로 꺼내기. 그래야 내 파트도 여유 있게 닫힌다.</li>
  </ol>

  <h3 class="step">감사</h3>
  <p>주말에도 회의에 모이고 같이 코드를 짜며 끝까지 달려와 준 팀원들에게 고맙다. 부족한 부분을 알려준 시간이기도 했다. 다음에는 팀원과 더 많이 성장하는 걸 목표로, 더 단단히 준비해서 들어가야겠다.</p>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 마지막으로, 출발 의문 한 줄을 회수하고 4일의 사슬을 한 장에 닫는다.
  </div>
</section>
"""

CH9 = """
<section id="ch9">
  <h2 class="chap"><span class="num">CH 09</span>총 정리<a href="#ch9" class="anchor-link">#</a></h2>

  <h3 class="step">출발 의문 회수</h3>
  <p>출발의 한 줄은 &ldquo;4명이 4일 안에, 크롤링·DB·웹앱 한 흐름을 발표 가능한 형태로 완성한다&rdquo; 였다. 결과는 다음과 같다.</p>

  <table>
    <thead><tr><th>조건</th><th>설계</th><th>결과</th></tr></thead>
    <tbody>
      <tr><td>① 주제·ERD가 첫 2일 안에 굳는다</td><td>CH01~CH03 — 수소차로 좁히고 <code>regions</code> FK 정규화 + <code>crawl_stat</code> 독립 테이블</td><td>✅ 통과 — 19일까지 스키마 변경 없음</td></tr>
      <tr><td>② 모두가 같은 코드 기반 위에 선다</td><td>CH04 — 프로토타입 + <code>MODEL_INSERT_SQL</code> 매핑</td><td>✅ 통과 — 새 크롤러 추가는 모델 한 줄 + 매핑 한 줄</td></tr>
      <tr><td>③ 협업·디버깅 채널이 끊기지 않는다</td><td>CH05~CH06 — 스프레드시트 1장 + 브런치 5개</td><td>✅ 통과 — 11건 디버깅 모두 Closed, 직푸시 사건 1회 복구</td></tr>
    </tbody>
  </table>

  <h3 class="step">최종 결론</h3>
  <div class="keypoint"><span class="label">FINAL CONCLUSION</span>
    4일짜리 팀 프로젝트는 &ldquo;많이 하는 사람&rdquo; 보다 <strong>&ldquo;경계마다 책임을 분명히 한 사람&rdquo;</strong> 이 굴린다. 이번 프로젝트의 모든 통과 지점(ERD 정규화 · MODEL_INSERT_SQL 매핑 · UPSERT · session_state 쉐도우키 · 폴백 FAQ)은 모두 &ldquo;<strong>이 일은 누가 책임지는가</strong>&rdquo; 라는 한 줄 질문의 답이었다.
  </div>

  <div class="ref-chain">
    <p class="ref-title">📚 전체 근거 출처</p>
    <ol>
      <li><strong>저장소</strong> <a href="https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN32-1st-3Team" target="_blank" rel="noopener">SKNETWORKS-FAMILY-AICAMP/SKN32-1st-3Team</a> — README · <code>app.py</code> · <code>data/repository.py</code> · <code>crawling/models.py</code> · <code>dbscript/dbscript_table.sql</code></li>
      <li><strong>팀 작업현황 시트</strong> <code>물로간다_팀작업현황</code> (스프레드시트 ID <code>10QCpgSJE9i5_fRU6IW2nIoNO0pWymVEwm7qnRn2TKaQ</code>) — 작업분담 탭(gid=471644863), 디버깅 노트 탭(gid=1542101365)</li>
      <li><strong>출처 데이터</strong> 국토교통부 통계누리, 공공데이터포털 수소충전소, EV 무공해차 통합누리집(<code>ev.or.kr</code>)</li>
      <li><strong>도구 문서</strong>
        <a href="https://docs.streamlit.io/" target="_blank" rel="noopener">Streamlit</a> ·
        <a href="https://playwright.dev/python/" target="_blank" rel="noopener">Playwright(Python)</a> ·
        <a href="https://docs.sqlalchemy.org/" target="_blank" rel="noopener">SQLAlchemy</a> ·
        <a href="https://dev.mysql.com/doc/refman/8.0/en/insert-on-duplicate.html" target="_blank" rel="noopener">MySQL INSERT ... ON DUPLICATE KEY UPDATE</a> ·
        <a href="https://python-visualization.github.io/folium/" target="_blank" rel="noopener">Folium</a> ·
        <a href="https://altair-viz.github.io/" target="_blank" rel="noopener">Altair</a>
      </li>
    </ol>
  </div>
</section>
"""

FOOTER = """
<footer>
  <p>© 2026 devroro · SKN32 1차 단위 프로젝트 회고 · 카데이터 팀 &ldquo;물로간다&rdquo;</p>
  <p>작성: 2026-05-25 / 기간: 2026-05-15(금) ~ 2026-05-19(화)</p>
</footer>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-core.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/autoloader/prism-autoloader.min.js"></script>
</body>
</html>
"""
