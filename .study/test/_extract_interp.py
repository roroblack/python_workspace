import email, re, html, glob, os
from html.parser import HTMLParser

notes = r"C:\_proj\python_workspace\.study\notes"
candidates = glob.glob(os.path.join(notes, "*.mhtml"))
target = [p for p in candidates if "인터프리터" in p][0]
print("target:", target)

with open(target, "rb") as f:
    msg = email.message_from_bytes(f.read())

texts = []
for part in msg.walk():
    if part.get_content_type() == "text/html":
        payload = part.get_payload(decode=True)
        cs = part.get_content_charset() or "utf-8"
        texts.append(payload.decode(cs, errors="replace"))

big = max(texts, key=len)


class S(HTMLParser):
    def __init__(self):
        super().__init__()
        self.out = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip += 1
        if tag in ("p", "br", "div", "li", "h1", "h2", "h3", "h4", "tr"):
            self.out.append("\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip -= 1
        if tag in ("p", "div", "li", "h1", "h2", "h3", "h4", "tr"):
            self.out.append("\n")

    def handle_data(self, data):
        if self.skip <= 0:
            self.out.append(data)


p = S()
p.feed(big)
text = "".join(p.out)
text = re.sub(r"\n\s*\n+", "\n\n", text)
text = html.unescape(text)
out = os.path.join(notes, "_interp_extracted.txt")
with open(out, "w", encoding="utf-8") as f:
    f.write(text)
print("wrote", out, "len", len(text))
