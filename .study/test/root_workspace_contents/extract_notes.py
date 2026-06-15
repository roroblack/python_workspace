import os, re, email, sys

# Set stdout to utf-8
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def extract_text(fpath, max_chars=30000):
    try:
        with open(fpath, 'rb') as f:
            raw = f.read()
    except Exception as e:
        return f"Error reading file: {e}"
        
    msg = email.message_from_bytes(raw)
    all_text = []
    for part in msg.walk():
        ct = part.get_content_type()
        if 'html' in ct or 'text/plain' in ct:
            payload = part.get_payload(decode=True)
            if payload:
                # Try multiple encodings
                text = ""
                for enc in ['utf-8', 'cp949', 'latin-1']:
                    try:
                        text = payload.decode(enc)
                        break
                    except:
                        continue
                if not text:
                    continue
                    
                # Clean up HTML
                text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL|re.IGNORECASE)
                text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL|re.IGNORECASE)
                text = re.sub(r'<[^>]+>', ' ', text)
                text = re.sub(r'&[a-zA-Z]+;', ' ', text)
                text = re.sub(r'&#[0-9]+;', ' ', text)
                text = re.sub(r'\s+', ' ', text).strip()
                if re.search(r'[\uac00-\ud7a3]', text) and len(text) > 100:
                    all_text.append(text)
    return '\n\n'.join(all_text)[:max_chars]

base = r"c:\_proj\python_workspace\.study\notes"
files = [
    "파이썬 데이터베이스 자동 증가 시퀀스 비교 - Google Gemini.mhtml",
    "0519 PK 문자열 처리 책임 분리 - Google Gemini.mhtml",
    "파이썬 사번 년월 데이터 날짜 처리 팁 - Google Gemini.mhtml",
    "파이썬 MySQL 연결 문제 해결 방법 - Google Gemini.mhtml",
]

for fname in files:
    fpath = os.path.join(base, fname)
    if not os.path.exists(fpath):
        print(f"\n[NOT FOUND] {fname}")
        continue
    print(f"\n{'='*70}")
    print(f"FILE: {fname}")
    print('='*70)
    text = extract_text(fpath)
    print(text)
    print("\n--- END ---")
