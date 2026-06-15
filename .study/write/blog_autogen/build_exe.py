"""PyInstaller 로 단일 실행 파일(.exe) 빌드 스크립트.

사용:
    & "c:\\_proj\\python_workspace\\.venv\\Scripts\\python.exe" build_exe.py

결과:
    dist/BlogAutoGen.exe  ← 더블클릭하면 tkinter GUI가 바로 실행됨
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
GUI = HERE / "gui.py"

# 더 이상 launcher 불필요 — gui.py 가 직접 진입점
LAUNCHER = None
LAUNCHER_SRC = None  # 미사용


# ── 아래는 하위 호환을 위해 남겨둠 (실제 사용 안 함) ──
APP = HERE / "app.py"


def _resource(name: str) -> str:
    base = getattr(sys, "_MEIPASS", str(Path(__file__).resolve().parent))
    return str(Path(base) / name)


def _open_browser():
    time.sleep(2.5)
    webbrowser.open("http://localhost:8501")


def main():
    threading.Thread(target=_open_browser, daemon=True).start()

    # streamlit 모듈 진입점 호출
    from streamlit.web import cli as stcli

    sys.argv = [
        "streamlit", "run", _resource("app.py"),
        "--server.headless=true",
        "--global.developmentMode=false",
        "--browser.gatherUsageStats=false",
    ]
    sys.exit(stcli.main())


if __name__ == "__main__":
    main()
'''


def main() -> int:
    # PyInstaller 설치 확인
    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        print("[install] PyInstaller ...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    sep = ";" if sys.platform.startswith("win") else ":"
    add_data = [
        f"{HERE / 'pipeline.py'}{sep}.",
        f"{HERE / 'llm.py'}{sep}.",
        f"{HERE / 'notes_loader.py'}{sep}.",
        f"{HERE / '__init__.py'}{sep}.",
        f"{HERE / 'requirements.txt'}{sep}.",
    ]

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--clean",
        "--name", "BlogAutoGen",
        "--onefile",
        "--windowed",                     # GUI — 콘솔 창 숨김
        "--collect-submodules", "openai",
        "--collect-submodules", "anthropic",
        "--collect-submodules", "google.generativeai",
        "--hidden-import", "bs4",
        "--hidden-import", "lxml",
        "--hidden-import", "tkinter",
    ]
    for d in add_data:
        cmd += ["--add-data", d]
    cmd.append(str(GUI))

    print("[build] " + " ".join(cmd))
    subprocess.check_call(cmd, cwd=str(HERE))

    # 빌드 임시 파일 정리
    for junk in ("build", "BlogAutoGen.spec"):
        p = HERE / junk
        if p.exists():
            if p.is_dir():
                shutil.rmtree(p, ignore_errors=True)
            else:
                p.unlink()

    exe = HERE / "dist" / ("BlogAutoGen.exe" if sys.platform.startswith("win") else "BlogAutoGen")
    print(f"\n[done] {exe}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
