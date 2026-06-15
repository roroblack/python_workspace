# fix_duplicate_pre.py
# 버그: rebuild_terminals2.py 가 non-greedy 정규식으로 첫 번째 </div>에서 끊겨
#       이전 <pre class="terminal-body">...내용...</pre>\n  </div> 가 잔여로 남음
# 수정: "  </div>\n    <pre class="terminal-body">..잔여..</pre>\n  </div>" 패턴 제거

import re, pathlib, datetime

HTML = pathlib.Path(r"c:\_proj\python_workspace\.study\blog\dict.html")
TMP  = pathlib.Path(r"c:\_proj\python_workspace\.study\blog\tmp")

html = HTML.read_text(encoding="utf-8")

before_pre = html.count('<pre class="terminal-body">')
before_div = html.count('<div class="terminal">')
print(f"수정 전: div.terminal={before_div}  pre.terminal-body={before_pre}")

# 잔여 패턴:
#   "  </div>\n    <pre class="terminal-body">...(내용)...</pre>\n  </div>"
#  (2칸 들여쓰기 </div> 다음에 4칸 들여쓰기 <pre>)
# → "  </div>" 로 교체 (잔여 pre와 뒤의 닫는 div 제거)
ORPHAN = re.compile(
    r'  </div>\n    <pre class="terminal-body">.*?</pre>\n  </div>',
    re.DOTALL
)

removed = 0
def remove_orphan(m):
    global removed
    removed += 1
    return '  </div>'

html = ORPHAN.sub(remove_orphan, html)

after_pre = html.count('<pre class="terminal-body">')
after_div = html.count('<div class="terminal">')
print(f"잔여 pre 제거: {removed}개")
print(f"수정 후: div.terminal={after_div}  pre.terminal-body={after_pre}")

if after_div == after_pre == 11:
    print("✓ 정상 (div:11 = pre:11)")
else:
    print(f"✗ 불일치 — 추가 확인 필요")

HTML.write_text(html, encoding="utf-8")
print(f"저장 완료: {HTML}")

# 로그
log = (
    f"=== fix_duplicate_pre.py {datetime.datetime.now()} ===\n"
    f"잔여 pre 제거: {removed}개\n"
    f"수정 후 div.terminal={after_div}  pre.terminal-body={after_pre}\n"
)
(TMP / "fix_log.txt").write_text(log, encoding="utf-8")

# 이 스크립트 자체도 tmp 에 복사
import shutil
shutil.copy(__file__, TMP / "fix_duplicate_pre.py")
print(f"스크립트 → blog/tmp/fix_duplicate_pre.py 복사 완료")
