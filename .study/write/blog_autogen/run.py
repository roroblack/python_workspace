"""Blog AutoGen GUI launcher."""
import subprocess, sys
from pathlib import Path

HERE   = Path(__file__).resolve().parent
VENV   = Path(r"c:\_proj\python_workspace\.venv\Scripts")
PY     = VENV / "python.exe"
if not PY.exists():
    PY = Path(sys.executable)

req = HERE / "requirements.txt"
if req.exists():
    subprocess.run([str(PY), "-m", "pip", "install", "-q", "-r", str(req)], check=False)

subprocess.run([str(PY), str(HERE / "gui.py")])