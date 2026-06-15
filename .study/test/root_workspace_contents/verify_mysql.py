import re

html = open('.blog/mysql_commands.html', encoding='utf-8').read()

checks = {
  'og:title':              bool(re.search(r'og:title', html)),
  'og:description':        bool(re.search(r'og:description', html)),
  'og:type':               bool(re.search(r'og:type', html)),
  'tw:card':               bool(re.search(r'twitter:card', html)),
  'tw:title':              bool(re.search(r'twitter:title', html)),
  'tw:description':        bool(re.search(r'twitter:description', html)),
  'h2.chap count':         len(re.findall(r'class="chap"', html)),
  'blockquote.cite count': len(re.findall(r'class="cite"', html)),
  'div.bridge count':      len(re.findall(r'class="bridge"', html)),
  'div.keypoint count':    len(re.findall(r'class="keypoint"', html)),
  'div.qbox count':        len(re.findall(r'class="qbox"', html)),
  'terminal count':        len(re.findall(r'class="terminal"', html)),
  'base64 img src':        bool(re.search(r'data:image/png;base64,', html)),
  'external img (fail)':   bool(re.search(r'<img[^>]+src="http', html)),
  'FINAL CONCLUSION':      bool(re.search(r'FINAL CONCLUSION', html)),
  'border-radius:0':       bool(re.search(r'border-radius: 0', html)),
  'no box-shadow':         bool(re.search(r'box-shadow: none', html)),
}

for k, v in checks.items():
    if k == 'external img (fail)':
        status = 'PASS' if not v else 'FAIL (외부 img 있음)'
    elif isinstance(v, bool):
        status = 'PASS' if v else 'FAIL'
    else:
        status = str(v)
    print(f'  {k:35s}: {status}')
