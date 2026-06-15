# -*- coding: utf-8 -*-
"""
Notion 강의자료 PDF 동기화 (GUIDE.txt §30)
- about.txt 의 notion.so 단원 링크에서 page id 수집
- 각 단원 collection 의 "수업 자료 PDF" 속성 → (파일명, Google Drive 링크) 추출
- .study/pdf 와 비교 (접두 번호/대소문자 변형은 보유로 간주)
- 링크 있고 로컬에 없는 PDF만 다운로드 (%PDF 헤더 검증)

실행:
  c:\\_proj\\python_workspace\\.venv\\Scripts\\python.exe .study\\write\\tmp\\notion_pdf_sync.py
"""
import json, io, re, os, sys, urllib.request

ROOT = r'c:\_proj\python_workspace'
ABOUT = os.path.join(ROOT, 'about.txt')
PDFDIR = os.path.join(ROOT, '.study', 'pdf')
NOTION = 'https://www.notion.so/api/v3/'


def post(endpoint, payload):
    req = urllib.request.Request(
        NOTION + endpoint,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'})
    return json.loads(urllib.request.urlopen(req, timeout=30).read().decode('utf-8'))


def dash(h):
    return '%s-%s-%s-%s-%s' % (h[0:8], h[8:12], h[12:16], h[16:20], h[20:32])


def seg_name_url(prop):
    if not prop:
        return '', None
    name = ''.join(s[0] for s in prop)
    url = None
    for s in prop:
        if len(s) > 1 and s[1]:
            for ann in s[1]:
                if ann[0] == 'a':
                    url = ann[1]
    return name, url


def norm(fname):
    """접두 번호(1_, 02_) 제거 + 소문자 → 보유 비교 키."""
    base = fname.rsplit('.', 1)[0]
    base = re.sub(r'^\d+_', '', base)
    return base.lower()


def discover():
    txt = io.open(ABOUT, encoding='utf-8').read()
    ids = []
    for m in re.findall(r'notion\.so/([0-9a-f]{32})', txt):
        if m not in ids:
            ids.append(m)
    found = {}
    for h in ids:
        pid = dash(h)
        try:
            chunk = post('loadCachedPageChunk', {"page": {"id": pid}, "limit": 50,
                         "cursor": {"stack": []}, "chunkNumber": 0, "verticalColumns": False})
        except Exception as e:
            print('  page load err', h, e); continue
        bw = chunk['recordMap'].get('block', {}).get(pid, {})
        pv = bw.get('value', {})
        pv = pv.get('value', pv)
        cptr = (pv.get('format') or {}).get('collection_pointer') or {}
        space = bw.get('spaceId') or pv.get('spaceId') or pv.get('space_id') or cptr.get('spaceId')
        cid, views = pv.get('collection_id'), pv.get('view_ids') or []
        if not (cid and views):
            continue
        try:
            col = post('queryCollection', {
                "collection": {"id": cid, "spaceId": space},
                "collectionView": {"id": views[0], "spaceId": space},
                "loader": {"type": "reducer",
                           "reducers": {"collection_group_results": {"type": "results", "limit": 200}},
                           "searchQuery": "", "userTimeZone": "Asia/Seoul"}})
        except Exception as e:
            print('  coll query err', h, e); continue
        crm = col['recordMap']
        schema = {}
        for c in crm.get('collection', {}).values():
            sc = c.get('value', {}).get('value', {}).get('schema') or c.get('value', {}).get('schema')
            if sc:
                schema = sc
        pdfkeys = [k for k, v in schema.items() if 'PDF' in (v.get('name') or '')]
        for b in crm.get('block', {}).values():
            v = b.get('value', {}).get('value') or b.get('value', {})
            if v.get('type') == 'page' and v.get('parent_table') == 'collection':
                for pk in pdfkeys:
                    name, url = seg_name_url(v.get('properties', {}).get(pk))
                    if name.lower().endswith('.pdf') and (name not in found or (url and not found[name])):
                        found[name] = url
    return found


def fetch(fid):
    url = 'https://drive.google.com/uc?export=download&id=' + fid
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    return urllib.request.urlopen(req, timeout=60).read()


def main():
    found = discover()
    have = {norm(f) for f in os.listdir(PDFDIR)}
    dl = skip = nolink = 0
    for name in sorted(found):
        url = found[name]
        if norm(name) in have:
            continue
        if not url:
            print('NO-LINK (미업로드, 보류):', name); nolink += 1; continue
        m = re.search(r'/d/([A-Za-z0-9_-]+)', url)
        if not m:
            print('LINK-PARSE-FAIL:', name, url); continue
        try:
            data = fetch(m.group(1))
        except Exception as e:
            print('ERR', name, e); continue
        if data[:4] != b'%PDF':
            print('NOT-PDF (interstitial?):', name, len(data)); continue
        io.open(os.path.join(PDFDIR, name), 'wb').write(data)
        print('OK %.1f KB  %s' % (len(data) / 1024, name)); dl += 1
    print('\n다운로드 %d · 미업로드보류 %d · 이미보유 스킵' % (dl, nolink))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
