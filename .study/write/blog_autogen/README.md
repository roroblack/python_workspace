# Blog AutoGen — 기술 블로그 HTML 자동 생성기

`.study/GUIDE.txt` 의 규칙(서사 사슬 구조 · Swiss Style · 인라인 인용 · 터미널 실행
결과 삽입 등)을 따르도록 LLM 에 프롬프트를 구성하고, 결과 HTML 과 보조 스크립트
(`<주제>_runner.py`)을 자동으로 생성·실행해 최종 결과물을 `.study/blog/` 에 저장한다.

## 지원 LLM

- OpenAI (gpt-4o, gpt-4.1, o4-mini 등)
- Anthropic Claude (claude-3-5-sonnet, claude-opus-4 등)
- Google Gemini (gemini-1.5-pro, gemini-2.0-flash 등)

API 키는 UI 에서 직접 입력한다 (저장하지 않음, 세션 메모리에만 유지).

## 실행 — 3가지 방법

### 1) 더블클릭 (가장 간단)

탐색기에서 `blog_autogen\run.bat` 를 더블클릭하면
의존성 자동 설치 후 Streamlit 서버가 뜨고 브라우저가 열린다.

PowerShell 사용자는 `run.ps1` 사용:
```powershell
powershell -ExecutionPolicy Bypass -File blog_autogen\run.ps1
```

### 2) 수동 실행

```powershell
& "c:\_proj\python_workspace\.venv\Scripts\python.exe" -m pip install -r blog_autogen\requirements.txt
& "c:\_proj\python_workspace\.venv\Scripts\streamlit.exe" run blog_autogen\app.py
```

브라우저에서 `http://localhost:8501` 접속.

### 3) 단일 .exe 빌드 (Python 미설치 환경 배포용)

```powershell
& "c:\_proj\python_workspace\.venv\Scripts\python.exe" blog_autogen\build_exe.py
```

→ `blog_autogen\dist\BlogAutoGen.exe` 가 생성된다. 더블클릭하면 서버가 뜨고
브라우저가 자동으로 열린다. (최초 빌드 시 PyInstaller 가 자동 설치되며,
결과 파일은 100MB 이상이 될 수 있다.)

## 사용 흐름

1. 좌측 사이드바: Provider · 모델 선택, API 키 입력.
2. 입력 모드 선택
   - **주제만 입력**: 자유 주제 한 줄 입력
   - **노트 파일 선택**: `.study/notes/` 안의 `.mhtml` / `.txt` / `.docx`(텍스트만 추출)
3. **1단계 — 기획 생성**: LLM 이 GUIDE.txt 규칙대로 챕터별 가설·테스트 코드 JSON 을 만든다.
4. **2단계 — Runner 작성/실행**: JSON 에서 `<주제>_runner.py` 를 만들어
   `.venv` 파이썬으로 실행하고 `logs/*.txt` 를 모은다.
5. **3단계 — HTML 생성**: 실제 실행 로그를 포함한 전체 HTML 을
   `.study/blog/<주제>.html` 로 저장한다.
6. (선택) **Base64/Blogger 변환**: §21 의 _base64.html 도 함께 생성.

## 보안 / 주의

- API 키는 환경변수에 자동 저장되지 않는다. 페이지 새로고침 시 다시 입력.
- runner.py 는 `subprocess` 로 실제 실행되므로, 신뢰할 수 없는 입력에서는 사용 금지.
- 외부 네트워크 접근이 필요한 LLM API 호출은 사용자의 키와 회선으로 직접 이루어진다.
