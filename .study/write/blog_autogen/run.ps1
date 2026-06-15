# ───────────────────────────────────────────────
#  Blog AutoGen — PowerShell 실행기
# ───────────────────────────────────────────────
$ErrorActionPreference = 'Stop'
Set-Location -Path $PSScriptRoot

$venvPy = 'c:\_proj\python_workspace\.venv\Scripts\python.exe'
$venvSt = 'c:\_proj\python_workspace\.venv\Scripts\streamlit.exe'

if (-not (Test-Path $venvPy)) {
    Write-Host "[ERROR] venv 파이썬을 찾을 수 없습니다: $venvPy" -ForegroundColor Red
    Read-Host '계속하려면 Enter'
    exit 1
}

Write-Host '[1/2] 의존성 설치 / 업데이트 확인 ...' -ForegroundColor Cyan
& $venvPy -m pip install -q -r (Join-Path $PSScriptRoot 'requirements.txt')

Write-Host '[2/2] Streamlit 서버 시작 ...' -ForegroundColor Cyan
Write-Host '       브라우저가 자동으로 열리지 않으면 http://localhost:8501 접속' -ForegroundColor DarkGray
& $venvSt run (Join-Path $PSScriptRoot 'app.py') --server.headless=false
