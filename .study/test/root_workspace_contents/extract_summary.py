import os, re, email

def extract_text(fpath):
    with open(fpath, 'rb') as f:
        raw = f.read()
    msg = email.message_from_bytes(raw)
    all_text = []
    for part in msg.walk():
        ct = part.get_content_type()
        if 'html' in ct or 'text/plain' in ct:
            payload = part.get_payload(decode=True)
            if payload:
                try:
                    text = payload.decode('utf-8', errors='ignore')
                except:
                    text = payload.decode('cp949', errors='ignore')
                text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
                text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
                text = re.sub(r'<[^>]+>', ' ', text)
                text = re.sub(r'&[a-z]+;', ' ', text)
                text = re.sub(r'\s+', ' ', text).strip()
                if re.search(r'[\uac00-\ud7a3]', text) and len(text) > 100:
                    all_text.append(text)
    return '\n\n'.join(all_text)

base = r"c:\_proj\python_workspace\.study\notes"
files = [
    "파이썬 인덱스 사용 시점과 주의사항 - Google Gemini.mhtml",
    "파이썬 데이터베이스 자동 증가 시퀀스 비교 - Google Gemini.mhtml",
    "0519 PK 문자열 처리 책임 분리 - Google Gemini.mhtml",
    "파이썬 MySQL 연결 문제 해결 방법 - Google Gemini.mhtml",
    "파이썬 사번 년월 데이터 날짜 처리 팁 - Google Gemini.mhtml",
    "test1-프로그래밍과 데이터 기초.mhtml",
]

for fname in files:
    fpath = os.path.join(base, fname)
    if not os.path.exists(fpath):
        continue
    print(f"\n### FILE: {fname}")
    text = extract_text(fpath)
    
    # Simple heuristic to find interesting sections
    lines = text.split('.')
    found_q = [l.strip() for l in lines if '?' in l or '어떻게' in l or '요청' in l or '설명해' in l]
    
    print(" [QUESTIONS/REQUESTS]")
    for q in found_q[:3]:
        print(f" - {q}")
    
    print("\n [KEY SUMMARY (First 500 chars)]")
    print(text[:500] + "...")