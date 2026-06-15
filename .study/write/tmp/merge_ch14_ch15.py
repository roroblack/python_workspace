from pathlib import Path
import re

html_path = Path(r"C:\_proj\python_workspace\.blog\day0511_mysql_btree.html")
html = html_path.read_text(encoding="utf-8")

# figure 태그 바로 앞 위치 찾기 (qbox 닫는 </div> 다음의 figure)
# qbox 이후 ~ </section> x2 + CH15 section 전체를 새 내용으로 대체
# 새 내용: 표 + FINAL CONCLUSION + 부록 그림 + ref-chain + </section>

# 교체할 시작: '  </div>\n\n        <figure class="diagram">'
# 교체할 끝: CH15 </section> 까지

START_MARKER = '  </div>\n\n        <figure class="diagram">'
# END: 두 번째 </section> 이후 (CH14 닫힘 + CH15 전체)
# 실제로는 CH15 </section> 다음 줄까지

# 원본에서 START_MARKER 위치 찾기
start_idx = html.find(START_MARKER)
if start_idx == -1:
    # 공백 차이 대응
    START_MARKER = '  </div>\n\n        <figure'
    start_idx = html.find(START_MARKER)

print(f"start_idx: {start_idx}")

# CH15 </section> 끝 위치 찾기
ch15_section_end = html.find('<section id="ch15">')
ch15_close = html.find('</section>', ch15_section_end) + len('</section>')

print(f"ch15_section_start: {ch15_section_end}, ch15_close: {ch15_close}")

# 이미지 src 추출 (base64 그대로 재사용)
img_match = re.search(r'<img\s[^>]*src="(data:image/[^"]+)"[^>]*/>', html[start_idx:ch15_close], re.DOTALL)
img_src = img_match.group(1) if img_match else ""
print(f"img_src length: {len(img_src)}")

NEW_BLOCK = '''
  <h3 class="step">챕터별 핵심 한 줄 요약표</h3>

  <table>
    <thead>
      <tr><th style="width:8%">CH</th><th style="width:28%">주제</th><th>핵심 한 줄</th></tr>
    </thead>
    <tbody>
      <tr><td>CH01</td><td>B+Tree 자료구조</td><td>InnoDB 의 모든 인덱스는 B+Tree(lv0=leaf). <code>SHOW INDEX</code> → BTREE 확인</td></tr>
      <tr><td>CH02</td><td>왜 B+Tree 인가</td><td>분기계수 $B\\approx1{,}000$ → 10억 행도 3단계. 디스크 I/O 횟수가 전부다</td></tr>
      <tr><td>CH03</td><td>$O(1)$에 가까운 성능</td><td>클러스터드 인덱스+AHI+Buffer Pool 3중 합산 → 97% hash 즉답</td></tr>
      <tr><td>CH04</td><td>세 기술 개관</td><td>각 기술은 직렬이 아니라 병렬. 캐시 미스 수준에 따라 단계적 fallback</td></tr>
      <tr><td>CH05</td><td>클러스터드 인덱스</td><td>리프 페이지 == 데이터 페이지. second lookup 0회</td></tr>
      <tr><td>CH06</td><td>B+Tree 내 위치</td><td>내부 배열 3곳: 중간 노드 라우팅 배열 / Page Directory 슬롯 / 레코드</td></tr>
      <tr><td>CH07</td><td>내부 알고리즘 3가지</td><td>Page Dir 이진탐색 + FIL_PAGE_NEXT 수평이동 + right-only split</td></tr>
      <tr><td>CH08</td><td>AHI</td><td>내부 카운터가 임계 초과 시 글로벌 해시 빌드 → B+Tree 수직하강 생략</td></tr>
      <tr><td>CH09</td><td>Buffer Pool</td><td>LRU/Flush/Free 3-list multi-linking. OS 캐시 우회(O_DIRECT)</td></tr>
      <tr><td>CH10</td><td>INSERT 전체 흐름</td><td>Redo→Buffer Pool→Page Dir→Multi-Link→AHI→디스크 WAL 순서</td></tr>
      <tr><td>CH11</td><td>AUTO_INCREMENT</td><td><code>dict_table_t::autoinc</code> 단조증가 → right-only split → 단편화≈0</td></tr>
      <tr><td>CH12</td><td>동시성 경합</td><td>mutex → <code>std::atomic</code>(인터락) + 파티셔닝 → 멀티코어 락 경합 제거</td></tr>
      <tr><td>CH13</td><td>최적화 포인트</td><td>커버링 인덱스: secondary만으로 완결 → clustered 재조회 0회</td></tr>
    </tbody>
  </table>

  <div class="keypoint">
    <span class="label">FINAL CONCLUSION — 출발 의문 회수 : "왜 B+Tree 여야만 했는가"</span>
    B+Tree 자체가 빠른 게 아니다.
    B+Tree 위에 <strong>클러스터드 인덱스 / AHI / Buffer Pool</strong> 이라는 가속 장치를 얹기에
    가장 적합한 구조이기 때문이다.
    <br><br>
    분기계수가 커서 높이가 3단계에 수렴하고,
    리프끼리 이중 연결 리스트로 이어져 범위 검색이 수평이동만으로 끝나며,
    right-only split 이 AUTO_INCREMENT 와 맞물려 단편화를 0으로 유지한다.
    이 세 가지 구조적 특성이 AHI와 Buffer Pool이 제 역할을 할 수 있는 토대를 만든다.
    <br><br>
    결론: $O(\\log_B n)$ 이지만 $B\\approx1{,}000$, 루트/중간 노드는 버퍼풀에 상주,
    자주 쓰는 키는 AHI가 $O(1)$으로 단락 →
    운영 환경에서 <strong>사실상 $O(1)$</strong>.
  </div>

  <h3 class="step">부록 — InnoDB B+Tree &amp; Buffer Pool 아키텍처 구조도</h3>

  <figure class="diagram">
    <img src="''' + img_src + '''"
         alt="MySQL InnoDB B+Tree &amp; Buffer Pool Engine 고수준 아키텍처 다이어그램"
         style="display:block;width:100%;height:auto;max-width:100%;margin:0 auto;border:0;background:#f7fbfd;" />
    <figcaption>InnoDB 고수준 아키텍처 — B+Tree Index Manager · AHI · Buffer Pool · Transaction Log · Persistent Storage 구성요소 흐름 (mysql-server 소스코드 분석 기반)</figcaption>
  </figure>

  <h3 class="step">전체 근거 출처 — 부록 ref-chain</h3>

  <div class="ref-chain">
    <p class="ref-title">📚 전체 근거 출처 — 공식 문서 · mysql-server 소스 · 운영 사례</p>
    <ol>
      <li><strong>공식 문서</strong>
          <a href="https://dev.mysql.com/doc/refman/8.0/en/index-btree-hash.html" target="_blank" rel="noopener">8.3.9 Comparison of B-Tree and Hash Indexes</a>
          — "Most MySQL indexes … are stored in B-trees."</li>
      <li><strong>공식 문서</strong>
          <a href="https://dev.mysql.com/doc/refman/8.0/en/innodb-index-types.html" target="_blank" rel="noopener">17.6.2.1 Clustered and Secondary Indexes</a>
          — "the leaf page contains the row data."</li>
      <li><strong>공식 문서</strong>
          <a href="https://dev.mysql.com/doc/refman/8.0/en/innodb-adaptive-hash.html" target="_blank" rel="noopener">17.5.3 Adaptive Hash Index</a>
          — "InnoDB to perform more like an in-memory database."</li>
      <li><strong>공식 문서</strong>
          <a href="https://dev.mysql.com/doc/refman/8.0/en/innodb-buffer-pool.html" target="_blank" rel="noopener">17.5.1 Buffer Pool</a>
          — "implemented as a linked list of pages, using a variation of the LRU algorithm."</li>
      <li><strong>공식 문서</strong>
          <a href="https://dev.mysql.com/doc/refman/8.0/en/innodb-auto-increment-handling.html" target="_blank" rel="noopener">17.6.1.6 AUTO_INCREMENT Handling</a>
          — autoinc lock mode 1/2 의 의미.</li>
      <li><strong>공식 문서</strong>
          <a href="https://dev.mysql.com/doc/refman/8.0/en/innodb-file-space.html" target="_blank" rel="noopener">17.11.1 InnoDB Disk I/O &amp; Page Size</a>
          — 16KB 페이지 + 4/8/16/32/64KB 옵션.</li>
      <li><strong>mysql 소스</strong>
          <a href="https://github.com/mysql/mysql-server/blob/8.0/storage/innobase/btr/btr0cur.cc" target="_blank" rel="noopener">storage/innobase/btr/btr0cur.cc → btr_cur_search_to_nth_level()</a>
          : B+Tree 수직 하강.</li>
      <li><strong>mysql 소스</strong>
          <a href="https://github.com/mysql/mysql-server/blob/8.0/storage/innobase/btr/btr0btr.cc" target="_blank" rel="noopener">storage/innobase/btr/btr0btr.cc → btr_page_split_and_insert() · btr_compress()</a>
          : 페이지 분할/병합.</li>
      <li><strong>mysql 소스</strong>
          <a href="https://github.com/mysql/mysql-server/blob/8.0/storage/innobase/page/page0cur.cc" target="_blank" rel="noopener">storage/innobase/page/page0cur.cc → page_cur_search_with_match()</a>
          : Page Directory 이진 탐색.</li>
      <li><strong>mysql 소스</strong>
          <a href="https://github.com/mysql/mysql-server/blob/8.0/storage/innobase/btr/btr0sea.cc" target="_blank" rel="noopener">storage/innobase/btr/btr0sea.cc → btr_search_build_page_hash_index()</a>
          : AHI 빌드.</li>
      <li><strong>mysql 소스</strong>
          <a href="https://github.com/mysql/mysql-server/blob/8.0/storage/innobase/buf/buf0buf.cc" target="_blank" rel="noopener">storage/innobase/buf/buf0buf.cc → buf_LRU_get_free_block()</a>
          : Buffer Pool 슬롯 획득.</li>
      <li><strong>mysql 소스</strong>
          <a href="https://github.com/mysql/mysql-server/blob/8.0/storage/innobase/buf/buf0lru.cc" target="_blank" rel="noopener">storage/innobase/buf/buf0lru.cc</a>
          : LRU Young/Old sublist 알고리즘.</li>
      <li><strong>mysql 소스</strong>
          <a href="https://github.com/mysql/mysql-server/blob/8.0/storage/innobase/include/btr0types.h" target="_blank" rel="noopener">storage/innobase/include/btr0types.h</a>
          : 트리 레벨 정의 (level 0 = leaf).</li>
      <li><strong>운영 사례</strong>
          <a href="https://planetscale.com/blog/the-mysql-adaptive-hash-index" target="_blank" rel="noopener">PlanetScale · The MySQL Adaptive Hash Index</a>
          : AHI 가 쓰기 워크로드에서 오히려 독이 되는 사례.</li>
      <li><strong>도식</strong>
          <a href="https://dev.mysql.com/doc/refman/8.4/en/innodb-architecture.html" target="_blank" rel="noopener">MySQL Developer Zone · InnoDB Architecture Diagram</a></li>
    </ol>
  </div>
</section>
'''

new_html = html[:start_idx] + NEW_BLOCK + html[ch15_close:]
html_path.write_text(new_html, encoding="utf-8")
print(f"완료. 새 파일 길이: {len(new_html)}")

# 검증
verify = html_path.read_text(encoding="utf-8")
print(f"ch14 found: {'section id=\"ch14\"' in verify}")
print(f"ch15 found: {'section id=\"ch15\"' in verify}")
print(f"table found: {'챕터별 핵심' in verify}")
print(f"img found: {'data:image/jpeg' in verify}")
