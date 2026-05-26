import os
import re
import email
import quopri

notes_dir = r"c:\_proj\python_workspace\.study\notes"
files = [f for f in os.listdir(notes_dir) if f.endswith('.mhtml')]

for fname in sorted(files):
    fpath = os.path.join(notes_dir, fname)
    print(f"\n{'='*60}")
    print(f"FILE: {fname}")
    print('='*60)
    try:
        with open(fpath, 'rb') as f:
            raw = f.read()
        # Parse as email/MIME
        msg = email.message_from_bytes(raw)
        text_parts = []
        for part in msg.walk():
            ct = part.get_content_type()
            if 'html' in ct or 'text' in ct:
                payload = part.get_payload(decode=True)
                if payload:
                    try:
                        text = payload.decode('utf-8', errors='ignore')
                    except:
                        text = payload.decode('cp949', errors='ignore')
                    # Remove HTML tags
                    text = re.sub(r'<[^>]+>', ' ', text)
                    # Remove excessive whitespace
                    text = re.sub(r'\s+', ' ', text)
                    # Only print if contains Korean
                    if re.search(r'[\uac00-\ud7a3]', text):
                        text_parts.append(text[:3000])
        if text_parts:
            print('\n'.join(text_parts[:2]))
        else:
            print("(no Korean text found)")
    except Exception as e:
        print(f"Error: {e}")
