"""Blog AutoGen — 데스크톱 GUI (tkinter)

더블클릭 또는 python gui.py 로 실행.
"""
from __future__ import annotations

import sys
import threading
import traceback
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox

ROOT_DIR = Path(__file__).resolve().parent
PROJ_ROOT = Path(r"c:\_proj\python_workspace")

for p in (ROOT_DIR.parent, ROOT_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

# ── 색상 / 폰트 ─────────────────────────────────────────────
BG       = "#1e1e2e"
BG2      = "#2a2a3e"
BG3      = "#181825"
FG       = "#cdd6f4"
ACCENT   = "#89b4fa"
ACCENT2  = "#a6e3a1"
ACCENT3  = "#f38ba8"
ACCENT4  = "#cba6f7"
MUTED    = "#6c7086"
ENTRY_BG = "#313244"
BTN_OK   = "#45475a"
FONT     = ("Consolas", 10)
FONT_B   = ("Consolas", 10, "bold")
FONT_H   = ("Consolas", 12, "bold")
FONT_SM  = ("Consolas", 9)

NOTES_DIR = PROJ_ROOT / ".study" / "notes"
BLOG_DIR  = PROJ_ROOT / ".study" / "blog"

# 폴백 모델 목록 (API fetch 전 표시)
FALLBACK_MODELS: dict[str, list[str]] = {
    "openai":    ["(API 키 입력 후 목록 불러오기)"],
    "anthropic": ["(API 키 입력 후 목록 불러오기)"],
    "gemini":    ["(API 키 입력 후 목록 불러오기)"],
}

PROVIDERS = ["openai", "anthropic", "gemini"]
PROVIDER_LABELS = {"openai": "OpenAI", "anthropic": "Anthropic", "gemini": "Google Gemini"}


# ── API 에서 모델 목록 가져오기 ──────────────────────────────
def fetch_models(provider: str, api_key: str) -> list[str]:
    """실제 API 를 호출해 사용 가능한 모델 ID 목록을 반환한다."""
    if provider == "openai":
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        raw = [m.id for m in client.models.list()]
        # 텍스트 생성 모델만 필터
        keep = [m for m in raw if any(
            m.startswith(p) for p in ("gpt-", "o1", "o3", "o4", "chatgpt")
        )]
        return sorted(keep, reverse=True) or raw[:30]

    if provider == "anthropic":
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        raw = [m.id for m in client.models.list(limit=100)]
        return sorted(raw, reverse=True)

    if provider == "gemini":
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        raw = [
            m.name.replace("models/", "")
            for m in genai.list_models()
            if "generateContent" in (m.supported_generation_methods or [])
        ]
        return sorted(raw, reverse=True)

    return []


# ─────────────────────────────────────────────────────────────
# Options 다이얼로그
# ─────────────────────────────────────────────────────────────
class OptionsDialog(tk.Toplevel):
    """설정 팝업 — API 키, Provider, 모델, Temperature, Max Tokens."""

    def __init__(self, parent: "App"):
        super().__init__(parent)
        self.app = parent
        self.title("Options — API 설정")
        self.configure(bg=BG2)
        self.resizable(False, False)
        self.grab_set()  # 모달

        self._build()
        self._center()

    def _center(self):
        self.update_idletasks()
        pw = self.app.winfo_x() + self.app.winfo_width() // 2
        ph = self.app.winfo_y() + self.app.winfo_height() // 2
        w, h = 480, 520
        self.geometry(f"{w}x{h}+{pw - w//2}+{ph - h//2}")

    # ── UI ───────────────────────────────────────────────
    def _build(self):
        pad = dict(padx=20, pady=6)

        tk.Label(self, text="⚙  Options", bg=BG2, fg=ACCENT,
                 font=FONT_H, anchor="w").pack(fill="x", padx=20, pady=(16, 4))
        tk.Frame(self, bg=MUTED, height=1).pack(fill="x", padx=20)

        # Provider
        self._lbl("Provider")
        self.var_prov = tk.StringVar(value=self.app.var_provider.get())
        frm_p = tk.Frame(self, bg=BG2)
        frm_p.pack(fill="x", **pad)
        for p in PROVIDERS:
            tk.Radiobutton(
                frm_p, text=PROVIDER_LABELS[p], variable=self.var_prov, value=p,
                bg=BG2, fg=FG, selectcolor=BG2, activebackground=BG2,
                activeforeground=ACCENT, font=FONT,
                command=self._on_prov_change,
            ).pack(side="left", padx=(0, 14))

        # API Key
        self._lbl("API Key")
        key_frm = tk.Frame(self, bg=BG2)
        key_frm.pack(fill="x", **pad)
        self.var_key = tk.StringVar(value=self.app.var_key.get())
        self._key_entry = tk.Entry(key_frm, textvariable=self.var_key, show="•",
                                   bg=ENTRY_BG, fg=FG, insertbackground=FG,
                                   relief="flat", font=FONT)
        self._key_entry.pack(side="left", fill="x", expand=True)
        self._show_key = False
        tk.Button(key_frm, text="👁", command=self._toggle_key,
                  bg=BTN_OK, fg=FG, relief="flat", font=FONT_SM,
                  cursor="hand2", padx=4).pack(side="left", padx=(4, 0))

        # 모델 목록
        self._lbl("Model")
        mdl_frm = tk.Frame(self, bg=BG2)
        mdl_frm.pack(fill="x", **pad)
        self.var_model = tk.StringVar(value=self.app.var_model.get())
        self.cb_model = ttk.Combobox(mdl_frm, textvariable=self.var_model,
                                     values=self.app.cb_model["values"] or [""],
                                     state="readonly", font=FONT)
        self.cb_model.pack(side="left", fill="x", expand=True)
        self.btn_fetch = tk.Button(
            mdl_frm, text="↻ 목록 불러오기",
            command=self._fetch_models,
            bg=ACCENT, fg=BG3, relief="flat", font=FONT_SM,
            cursor="hand2", padx=6,
        )
        self.btn_fetch.pack(side="left", padx=(6, 0))

        self.lbl_fetch_status = tk.Label(self, text="", bg=BG2, fg=MUTED,
                                         font=FONT_SM, anchor="w")
        self.lbl_fetch_status.pack(fill="x", padx=20)

        # Temperature
        self._lbl("Temperature")
        temp_frm = tk.Frame(self, bg=BG2)
        temp_frm.pack(fill="x", **pad)
        self.var_temp = tk.DoubleVar(value=self.app.var_temp.get())
        tk.Scale(temp_frm, variable=self.var_temp, from_=0.0, to=1.0,
                 resolution=0.05, orient="horizontal",
                 bg=BG2, fg=FG, troughcolor=ENTRY_BG,
                 highlightthickness=0, sliderlength=16, font=FONT_SM,
                 length=300).pack(side="left")
        tk.Label(temp_frm, textvariable=self.var_temp,
                 bg=BG2, fg=FG, font=FONT_SM, width=4).pack(side="left", padx=(6, 0))

        # Max Tokens
        self._lbl("Max Tokens")
        self.var_tokens = tk.StringVar(value=self.app.var_tokens.get())
        tk.Entry(self, textvariable=self.var_tokens,
                 bg=ENTRY_BG, fg=FG, insertbackground=FG,
                 relief="flat", font=FONT).pack(fill="x", **pad)

        # 출력 경로 정보
        tk.Frame(self, bg=MUTED, height=1).pack(fill="x", padx=20, pady=(12, 4))
        info_frm = tk.Frame(self, bg=BG2)
        info_frm.pack(fill="x", padx=20, pady=4)
        for label, val in [
            ("출력 경로", str(BLOG_DIR)),
            ("노트 경로", str(NOTES_DIR)),
            ("venv Python", r"c:\_proj\python_workspace\.venv\Scripts\python.exe"),
        ]:
            row = tk.Frame(info_frm, bg=BG2)
            row.pack(fill="x", pady=1)
            tk.Label(row, text=f"{label}:", bg=BG2, fg=MUTED,
                     font=FONT_SM, width=12, anchor="w").pack(side="left")
            tk.Label(row, text=val, bg=BG2, fg=FG,
                     font=FONT_SM, anchor="w").pack(side="left")

        # 저장/닫기
        tk.Frame(self, bg=MUTED, height=1).pack(fill="x", padx=20, pady=(12, 4))
        btn_row = tk.Frame(self, bg=BG2)
        btn_row.pack(fill="x", padx=20, pady=(4, 16))
        tk.Button(btn_row, text="저장 후 닫기", command=self._save,
                  bg=ACCENT2, fg=BG3, relief="flat", font=FONT_B,
                  cursor="hand2", padx=12, pady=5).pack(side="right")
        tk.Button(btn_row, text="취소", command=self.destroy,
                  bg=BTN_OK, fg=FG, relief="flat", font=FONT,
                  cursor="hand2", padx=12, pady=5).pack(side="right", padx=(0, 8))

    def _lbl(self, text: str):
        tk.Label(self, text=text, bg=BG2, fg=MUTED,
                 font=FONT_SM, anchor="w").pack(fill="x", padx=20, pady=(8, 0))

    def _toggle_key(self):
        self._show_key = not self._show_key
        self._key_entry.config(show="" if self._show_key else "•")

    def _on_prov_change(self):
        # Provider 바꾸면 모델 목록을 폴백으로 초기화
        p = self.var_prov.get()
        self.cb_model["values"] = FALLBACK_MODELS[p]
        self.var_model.set(FALLBACK_MODELS[p][0])
        self.lbl_fetch_status.config(text="↻ 목록 불러오기를 눌러 최신 모델을 가져오세요.",
                                     fg=MUTED)

    def _fetch_models(self):
        key = self.var_key.get().strip()
        if not key:
            self.lbl_fetch_status.config(text="API Key를 먼저 입력하세요.", fg=ACCENT3)
            return
        prov = self.var_prov.get()
        self.btn_fetch.config(state="disabled", text="불러오는 중…")
        self.lbl_fetch_status.config(text="API 호출 중…", fg=ACCENT)

        def _work():
            try:
                models = fetch_models(prov, key)
                if not models:
                    raise ValueError("모델 목록이 비어 있습니다.")
                def _apply():
                    self.cb_model["values"] = models
                    self.var_model.set(models[0])
                    self.lbl_fetch_status.config(
                        text=f"✓ {len(models)}개 모델 로드 완료", fg=ACCENT2)
                    self.btn_fetch.config(state="normal", text="↻ 목록 불러오기")
                self.after(0, _apply)
            except Exception as e:
                def _err():
                    self.lbl_fetch_status.config(text=f"오류: {e}", fg=ACCENT3)
                    self.btn_fetch.config(state="normal", text="↻ 목록 불러오기")
                self.after(0, _err)

        threading.Thread(target=_work, daemon=True).start()

    def _save(self):
        self.app.var_provider.set(self.var_prov.get())
        self.app.var_key.set(self.var_key.get())
        self.app.var_model.set(self.var_model.get())
        self.app.var_temp.set(self.var_temp.get())
        self.app.var_tokens.set(self.var_tokens.get())
        # 메인 윈도우 헤더의 모델 표시도 갱신
        self.app.cb_model["values"] = self.cb_model["values"]
        self.app.lbl_cur_model.config(
            text=f"{PROVIDER_LABELS[self.var_prov.get()]}  /  {self.var_model.get()}"
        )
        self.destroy()


# ─────────────────────────────────────────────────────────────
# 메인 앱
# ─────────────────────────────────────────────────────────────
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Blog AutoGen")
        self.configure(bg=BG)
        self.resizable(True, True)
        self.minsize(760, 580)

        self._plan       = None
        self._run_result = None
        self._html_path  = None
        self._running    = False

        # 설정 변수 (OptionsDialog 에서 공유)
        self.var_provider = tk.StringVar(value="openai")
        self.var_key      = tk.StringVar(value="")
        self.var_model    = tk.StringVar(value="")
        self.var_temp     = tk.DoubleVar(value=0.3)
        self.var_tokens   = tk.StringVar(value="16000")

        self._build_ui()
        self.after(100, self._center)

    # ── 레이아웃 ───────────────────────────────────────────
    def _build_ui(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self._build_header()
        self._build_main()

    # ── 헤더 바 ──────────────────────────────────────────
    def _build_header(self):
        hdr = tk.Frame(self, bg=BG3, padx=16, pady=8)
        hdr.grid(row=0, column=0, sticky="ew")
        hdr.columnconfigure(1, weight=1)

        tk.Label(hdr, text="Blog AutoGen", bg=BG3, fg=ACCENT,
                 font=FONT_H).grid(row=0, column=0, sticky="w")

        # 현재 모델 표시
        self.lbl_cur_model = tk.Label(
            hdr, text="모델 미설정  —  ⚙ Options 에서 API 키와 모델을 선택하세요",
            bg=BG3, fg=MUTED, font=FONT_SM,
        )
        self.lbl_cur_model.grid(row=0, column=1, sticky="w", padx=16)

        # Options 버튼
        tk.Button(
            hdr, text="⚙  Options",
            command=lambda: OptionsDialog(self),
            bg=ACCENT4, fg=BG3, relief="flat", font=FONT_B,
            cursor="hand2", padx=10, pady=4,
        ).grid(row=0, column=2, sticky="e")

    # ── 메인 영역 ─────────────────────────────────────────
    def _build_main(self):
        main = tk.Frame(self, bg=BG, padx=16, pady=12)
        main.grid(row=1, column=0, sticky="nsew")
        main.columnconfigure(0, weight=1)
        main.rowconfigure(2, weight=1)

        # 입력 모드
        mode_frm = tk.Frame(main, bg=BG)
        mode_frm.grid(row=0, column=0, sticky="ew", pady=(0, 6))
        self.var_mode = tk.StringVar(value="topic")
        for val, txt in (("topic", "주제 직접 입력"), ("notes", "노트 파일 선택")):
            tk.Radiobutton(
                mode_frm, text=txt, variable=self.var_mode, value=val,
                bg=BG, fg=FG, selectcolor=BG, activebackground=BG,
                activeforeground=ACCENT, font=FONT,
                command=self._on_mode_change,
            ).pack(side="left", padx=(0, 16))

        # 입력 필드
        inp_frm = tk.Frame(main, bg=BG)
        inp_frm.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        inp_frm.columnconfigure(1, weight=1)

        # 주제 행
        self.frm_topic = tk.Frame(inp_frm, bg=BG)
        self.frm_topic.grid(row=0, column=0, columnspan=3, sticky="ew")
        tk.Label(self.frm_topic, text="주제", bg=BG, fg=MUTED,
                 font=FONT, width=7, anchor="w").pack(side="left")
        self.var_topic = tk.StringVar()
        tk.Entry(self.frm_topic, textvariable=self.var_topic,
                 bg=ENTRY_BG, fg=FG, insertbackground=FG,
                 relief="flat", font=FONT).pack(side="left", fill="x", expand=True)

        # 노트 행
        self.frm_notes = tk.Frame(inp_frm, bg=BG)
        self.frm_notes.grid(row=1, column=0, columnspan=3, sticky="ew")
        self.frm_notes.grid_remove()
        tk.Label(self.frm_notes, text="파일", bg=BG, fg=MUTED,
                 font=FONT, width=7, anchor="w").pack(side="left")
        self.var_notes_path = tk.StringVar()
        tk.Entry(self.frm_notes, textvariable=self.var_notes_path,
                 bg=ENTRY_BG, fg=MUTED, relief="flat", font=FONT,
                 state="readonly").pack(side="left", fill="x", expand=True)
        tk.Button(self.frm_notes, text="찾기", command=self._pick_notes_file,
                  bg=BTN_OK, fg=FG, relief="flat", font=FONT,
                  cursor="hand2").pack(side="left", padx=(4, 0))

        # 추가 지시
        tk.Label(inp_frm, text="추가 지시", bg=BG, fg=MUTED,
                 font=FONT, width=7, anchor="w").grid(row=2, column=0, sticky="w", pady=(6, 0))
        self.var_extra = tk.StringVar()
        tk.Entry(inp_frm, textvariable=self.var_extra,
                 bg=ENTRY_BG, fg=FG, insertbackground=FG,
                 relief="flat", font=FONT).grid(row=2, column=1, columnspan=2,
                                                sticky="ew", pady=(6, 0))

        # 실행 버튼
        btn_frm = tk.Frame(main, bg=BG)
        btn_frm.grid(row=1, column=0, sticky="e", pady=(36, 0))
        self.btn_plan = self._mk_btn(btn_frm, "1  기획서",  ACCENT,  self._step_plan)
        self.btn_run  = self._mk_btn(btn_frm, "2  Runner", ACCENT2, self._step_run,  state="disabled")
        self.btn_html = self._mk_btn(btn_frm, "3  HTML",   ACCENT4, self._step_html, state="disabled")
        tk.Frame(btn_frm, bg=MUTED, width=1).pack(side="left", fill="y", padx=8)
        self.btn_all  = self._mk_btn(btn_frm, "▶  전체 실행", ACCENT3, self._step_all)
        tk.Frame(btn_frm, bg=MUTED, width=1).pack(side="left", fill="y", padx=8)
        self.btn_open = self._mk_btn(btn_frm, "📂 열기", BTN_OK, self._open_result, state="disabled")

        # 상태 + 로그
        status_frm = tk.Frame(main, bg=BG)
        status_frm.grid(row=2, column=0, sticky="nsew", pady=(8, 0))
        status_frm.columnconfigure(0, weight=1)
        status_frm.rowconfigure(1, weight=1)

        self.lbl_status = tk.Label(status_frm, text="대기 중", bg=BG, fg=MUTED,
                                   font=FONT_SM, anchor="w")
        self.lbl_status.grid(row=0, column=0, sticky="ew", pady=(0, 4))

        self.log_box = scrolledtext.ScrolledText(
            status_frm, bg=BG3, fg=FG, font=FONT_SM,
            relief="flat", state="disabled", wrap="word",
        )
        self.log_box.grid(row=1, column=0, sticky="nsew")
        self.log_box.tag_config("info",  foreground=ACCENT)
        self.log_box.tag_config("ok",    foreground=ACCENT2)
        self.log_box.tag_config("err",   foreground=ACCENT3)
        self.log_box.tag_config("muted", foreground=MUTED)

    # ── 유틸 ─────────────────────────────────────────────
    def _mk_btn(self, parent, text, color, cmd, state="normal"):
        b = tk.Button(parent, text=text, command=cmd,
                      bg=color, fg=BG3, font=FONT_B,
                      relief="flat", cursor="hand2",
                      activebackground=color, activeforeground=BG3,
                      padx=10, pady=5, state=state)
        b.pack(side="left", padx=(0, 4))
        return b

    def _center(self):
        self.update_idletasks()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        w, h = 820, 640
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    def _on_mode_change(self):
        if self.var_mode.get() == "topic":
            self.frm_notes.grid_remove()
            self.frm_topic.grid()
        else:
            self.frm_topic.grid_remove()
            self.frm_notes.grid()

    def _pick_notes_file(self):
        init = str(NOTES_DIR) if NOTES_DIR.exists() else "/"
        path = filedialog.askopenfilename(
            initialdir=init, title="노트 파일 선택",
            filetypes=[("지원 파일", "*.mhtml *.txt *.docx"), ("전체", "*.*")],
        )
        if path:
            self.var_notes_path.set(path)

    def _open_result(self):
        if self._html_path and Path(self._html_path).exists():
            import webbrowser
            webbrowser.open(Path(self._html_path).as_uri())
        else:
            messagebox.showinfo("알림", "아직 생성된 HTML이 없습니다.")

    def _log(self, msg: str, tag: str = ""):
        def _do():
            self.log_box.config(state="normal")
            self.log_box.insert("end", msg + "\n", tag)
            self.log_box.see("end")
            self.log_box.config(state="disabled")
        self.after(0, _do)

    def _set_status(self, msg: str, color: str = FG):
        self.after(0, lambda: self.lbl_status.config(text=msg, fg=color))

    def _set_buttons(self, busy: bool):
        state = "disabled" if busy else "normal"
        self.after(0, lambda: [
            self.btn_plan.config(state=state),
            self.btn_all.config(state=state),
        ])

    # ── LLM 클라이언트 ───────────────────────────────────
    def _make_client(self):
        from blog_autogen.llm import LLMClient, LLMConfig
        key   = self.var_key.get().strip()
        model = self.var_model.get().strip()
        if not key:
            messagebox.showerror("오류", "Options 에서 API Key를 먼저 입력하세요.")
            return None
        if not model or "불러오기" in model:
            messagebox.showerror("오류", "Options 에서 모델을 선택하세요.")
            return None
        return LLMClient(LLMConfig(
            provider=self.var_provider.get(),
            model=model,
            api_key=key,
            temperature=float(self.var_temp.get()),
            max_tokens=int(self.var_tokens.get() or 16000),
        ))

    def _get_topic_and_notes(self) -> tuple[str, str]:
        if self.var_mode.get() == "topic":
            t = self.var_topic.get().strip()
            e = self.var_extra.get().strip()
            return (f"{t} {e}".strip(), "")
        path_str = self.var_notes_path.get().strip()
        extra    = self.var_extra.get().strip()
        if not path_str:
            messagebox.showerror("오류", "노트 파일을 선택하세요.")
            return ("", "")
        from blog_autogen.notes_loader import load_notes
        notes = load_notes(Path(path_str))
        topic = Path(path_str).stem
        if extra:
            topic = f"{topic} — {extra}"
        return (topic, notes)

    # ── 단계별 실행 ──────────────────────────────────────
    def _step_plan(self):
        if self._running:
            return
        client = self._make_client()
        if not client:
            return
        topic, notes = self._get_topic_and_notes()
        if not topic:
            return
        self._running = True
        self._set_buttons(busy=True)
        self._set_status("기획서 생성 중…", ACCENT)

        def _work():
            try:
                from blog_autogen.pipeline import make_plan
                self._log("[1/3] 기획서 생성 중…", "info")
                plan = make_plan(client, topic, notes)
                self._plan = plan
                self._log(f"      slug={plan.slug}, 챕터 {len(plan.chapters)}개", "ok")
                self._set_status(f"기획서 완료: {plan.slug}", ACCENT2)
                self.after(0, lambda: self.btn_run.config(state="normal"))
            except Exception as e:
                self._log(f"[ERROR] {e}", "err")
                self._log(traceback.format_exc(), "err")
                self._set_status("기획서 생성 실패", ACCENT3)
            finally:
                self._running = False
                self._set_buttons(busy=False)

        threading.Thread(target=_work, daemon=True).start()

    def _step_run(self):
        if self._running or self._plan is None:
            return
        self._running = True
        self._set_buttons(busy=True)
        self._set_status("runner.py 실행 중…", ACCENT)

        def _work():
            try:
                from blog_autogen.pipeline import build_runner, run_runner
                self._log("[2/3] runner.py 작성·실행 중…", "info")
                runner_path = build_runner(self._plan)
                result = run_runner(runner_path, log_cb=lambda m: self._log(m, "muted"))
                self._run_result = result
                self._log(f"      완료 rc={result.returncode}", "ok")
                self._set_status(f"runner 완료 (rc={result.returncode})", ACCENT2)
                self.after(0, lambda: self.btn_html.config(state="normal"))
            except Exception as e:
                self._log(f"[ERROR] {e}", "err")
                self._log(traceback.format_exc(), "err")
                self._set_status("runner 실패", ACCENT3)
            finally:
                self._running = False
                self._set_buttons(busy=False)

        threading.Thread(target=_work, daemon=True).start()

    def _step_html(self):
        if self._running or self._run_result is None:
            return
        client = self._make_client()
        if not client:
            return
        self._running = True
        self._set_buttons(busy=True)
        self._set_status("HTML 생성 중…", ACCENT)

        def _work():
            try:
                from blog_autogen.pipeline import generate_html
                self._log("[3/3] HTML 생성 중…", "info")
                path = generate_html(client, self._plan, self._run_result,
                                     log_cb=lambda m: self._log(m, "muted"))
                self._html_path = path
                self._log(f"      저장: {path}", "ok")
                self._set_status(f"완료: {Path(path).name}", ACCENT2)
                self.after(0, lambda: self.btn_open.config(state="normal"))
            except Exception as e:
                self._log(f"[ERROR] {e}", "err")
                self._log(traceback.format_exc(), "err")
                self._set_status("HTML 생성 실패", ACCENT3)
            finally:
                self._running = False
                self._set_buttons(busy=False)

        threading.Thread(target=_work, daemon=True).start()

    def _step_all(self):
        if self._running:
            return
        client = self._make_client()
        if not client:
            return
        topic, notes = self._get_topic_and_notes()
        if not topic:
            return
        self._running = True
        self._set_buttons(busy=True)
        self._plan = self._run_result = self._html_path = None
        for b in (self.btn_run, self.btn_html, self.btn_open):
            b.config(state="disabled")
        self._set_status("전체 실행 중…", ACCENT)

        def _work():
            try:
                from blog_autogen.pipeline import make_plan, build_runner, run_runner, generate_html
                self._log("=" * 52, "muted")
                self._log("[1/3] 기획서 생성 중…", "info")
                plan = make_plan(client, topic, notes)
                self._plan = plan
                self._log(f"      slug={plan.slug}, 챕터 {len(plan.chapters)}개", "ok")

                self._log("[2/3] runner 실행 중…", "info")
                runner = build_runner(plan)
                result = run_runner(runner, log_cb=lambda m: self._log(m, "muted"))
                self._run_result = result
                self._log(f"      rc={result.returncode}", "ok")

                self._log("[3/3] HTML 생성 중…", "info")
                path = generate_html(client, plan, result,
                                     log_cb=lambda m: self._log(m, "muted"))
                self._html_path = path
                self._log(f"      저장: {path}", "ok")
                self._log("=" * 52, "muted")
                self._set_status(f"완료: {Path(path).name}", ACCENT2)
                self.after(0, lambda: [b.config(state="normal")
                                       for b in (self.btn_run, self.btn_html, self.btn_open)])
            except Exception as e:
                self._log(f"[ERROR] {e}", "err")
                self._log(traceback.format_exc(), "err")
                self._set_status("실패", ACCENT3)
            finally:
                self._running = False
                self._set_buttons(busy=False)

        threading.Thread(target=_work, daemon=True).start()


# ─────────────────────────────────────────────────────────────
def main():
    app = App()
    style = ttk.Style(app)
    style.theme_use("clam")
    style.configure("TCombobox",
                    fieldbackground=ENTRY_BG, background=ENTRY_BG,
                    foreground=FG, selectbackground=ENTRY_BG,
                    selectforeground=FG, arrowcolor=FG)
    style.map("TCombobox", fieldbackground=[("readonly", ENTRY_BG)])
    app.mainloop()


if __name__ == "__main__":
    main()


    # ── 레이아웃 ───────────────────────────────────────────
    def _build_ui(self):
        self.columnconfigure(0, weight=0, minsize=240)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # 좌측 패널
        left = tk.Frame(self, bg=BG2, padx=12, pady=12)
        left.grid(row=0, column=0, sticky="nsew")
        self._build_left(left)

        # 우측 패널
        right = tk.Frame(self, bg=BG, padx=12, pady=12)
        right.grid(row=0, column=1, sticky="nsew")
        right.columnconfigure(0, weight=1)
        right.rowconfigure(1, weight=1)
        self._build_right(right)

    def _build_left(self, f):
        # 제목
        tk.Label(f, text="⚙  설정", bg=BG2, fg=ACCENT,
                 font=FONT_H, anchor="w").pack(fill="x", pady=(0, 12))

        # Provider
        self._mk_label(f, "Provider")
        self.var_provider = tk.StringVar(value="openai")
        cb_prov = ttk.Combobox(f, textvariable=self.var_provider,
                               values=list(PROVIDER_MODELS.keys()),
                               state="readonly", font=FONT)
        cb_prov.pack(fill="x", pady=(0, 8))
        cb_prov.bind("<<ComboboxSelected>>", self._on_provider_change)

        # Model
        self._mk_label(f, "Model")
        self.var_model = tk.StringVar(value=PROVIDER_MODELS["openai"][0])
        self.cb_model = ttk.Combobox(f, textvariable=self.var_model,
                                     values=PROVIDER_MODELS["openai"],
                                     state="readonly", font=FONT)
        self.cb_model.pack(fill="x", pady=(0, 8))

        # API Key
        self._mk_label(f, "API Key")
        self.var_key = tk.StringVar()
        ek = tk.Entry(f, textvariable=self.var_key, show="•",
                      bg=ENTRY_BG, fg=FG, insertbackground=FG,
                      relief="flat", font=FONT)
        ek.pack(fill="x", pady=(0, 8))

        # Temperature
        self._mk_label(f, "Temperature")
        frm_t = tk.Frame(f, bg=BG2)
        frm_t.pack(fill="x", pady=(0, 8))
        self.var_temp = tk.DoubleVar(value=0.3)
        sc = tk.Scale(frm_t, variable=self.var_temp, from_=0.0, to=1.0,
                      resolution=0.05, orient="horizontal",
                      bg=BG2, fg=FG, troughcolor=ENTRY_BG,
                      highlightthickness=0, sliderlength=16, font=FONT_SM)
        sc.pack(fill="x")

        # Max tokens
        self._mk_label(f, "Max Tokens")
        self.var_tokens = tk.StringVar(value="16000")
        tk.Entry(f, textvariable=self.var_tokens,
                 bg=ENTRY_BG, fg=FG, insertbackground=FG,
                 relief="flat", font=FONT).pack(fill="x", pady=(0, 8))

        tk.Frame(f, bg=MUTED, height=1).pack(fill="x", pady=10)

        # 상태 표시
        tk.Label(f, text="상태", bg=BG2, fg=MUTED, font=FONT_SM, anchor="w").pack(fill="x")
        self.lbl_status = tk.Label(f, text="대기 중", bg=BG2, fg=FG,
                                   font=FONT_SM, anchor="w", wraplength=200,
                                   justify="left")
        self.lbl_status.pack(fill="x", pady=(2, 8))

        # 결과 열기
        self.btn_open = tk.Button(f, text="📂  결과 HTML 열기",
                                  command=self._open_result,
                                  bg=BTN_OK, fg=FG, font=FONT,
                                  relief="flat", cursor="hand2",
                                  state="disabled")
        self.btn_open.pack(fill="x", pady=(4, 0))

    def _build_right(self, f):
        # ── 입력 영역 ──────────────────────────────────────
        top = tk.Frame(f, bg=BG)
        top.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        top.columnconfigure(1, weight=1)

        tk.Label(top, text="⌨  블로그 글 자동 생성", bg=BG, fg=ACCENT,
                 font=FONT_H).grid(row=0, column=0, columnspan=3,
                                    sticky="w", pady=(0, 10))

        # 입력 모드 탭
        self.var_mode = tk.StringVar(value="topic")
        tab_f = tk.Frame(top, bg=BG)
        tab_f.grid(row=1, column=0, columnspan=3, sticky="w", pady=(0, 6))
        for val, txt in (("topic", "주제 직접 입력"), ("notes", "노트 파일 선택")):
            tk.Radiobutton(tab_f, text=txt, variable=self.var_mode, value=val,
                           bg=BG, fg=FG, selectcolor=BG, activebackground=BG,
                           activeforeground=ACCENT, font=FONT,
                           command=self._on_mode_change).pack(side="left", padx=(0, 16))

        # 주제 입력
        self.frm_topic = tk.Frame(top, bg=BG)
        self.frm_topic.grid(row=2, column=0, columnspan=3, sticky="ew")
        top.rowconfigure(2, weight=0)
        tk.Label(self.frm_topic, text="주제:", bg=BG, fg=MUTED,
                 font=FONT, width=6, anchor="w").pack(side="left")
        self.var_topic = tk.StringVar()
        tk.Entry(self.frm_topic, textvariable=self.var_topic,
                 bg=ENTRY_BG, fg=FG, insertbackground=FG,
                 relief="flat", font=FONT).pack(side="left", fill="x", expand=True)

        # 노트 파일 선택
        self.frm_notes = tk.Frame(top, bg=BG)
        self.frm_notes.grid(row=3, column=0, columnspan=3, sticky="ew")
        self.frm_notes.grid_remove()
        tk.Label(self.frm_notes, text="파일:", bg=BG, fg=MUTED,
                 font=FONT, width=6, anchor="w").pack(side="left")
        self.var_notes_path = tk.StringVar()
        tk.Entry(self.frm_notes, textvariable=self.var_notes_path,
                 bg=ENTRY_BG, fg=MUTED, relief="flat", font=FONT,
                 state="readonly").pack(side="left", fill="x", expand=True)
        tk.Button(self.frm_notes, text="찾기",
                  command=self._pick_notes_file,
                  bg=BTN_OK, fg=FG, relief="flat",
                  font=FONT, cursor="hand2").pack(side="left", padx=(4, 0))

        # 추가 지시
        tk.Label(top, text="추가 지시 (선택):", bg=BG, fg=MUTED,
                 font=FONT_SM, anchor="w").grid(row=4, column=0, columnspan=3,
                                                sticky="w", pady=(8, 2))
        self.var_extra = tk.StringVar()
        tk.Entry(top, textvariable=self.var_extra,
                 bg=ENTRY_BG, fg=FG, insertbackground=FG,
                 relief="flat", font=FONT).grid(row=5, column=0, columnspan=3,
                                                sticky="ew", pady=(0, 10))

        # ── 실행 버튼 ─────────────────────────────────────
        btn_f = tk.Frame(top, bg=BG)
        btn_f.grid(row=6, column=0, columnspan=3, sticky="ew")
        btn_f.columnconfigure((0, 1, 2, 3), weight=1)

        self.btn_plan = self._mk_btn(btn_f, "1  기획서 생성",
                                     ACCENT, self._step_plan, col=0)
        self.btn_run  = self._mk_btn(btn_f, "2  Runner 실행",
                                     ACCENT2, self._step_run, col=1,
                                     state="disabled")
        self.btn_html = self._mk_btn(btn_f, "3  HTML 생성",
                                     "#cba6f7", self._step_html, col=2,
                                     state="disabled")
        self.btn_all  = self._mk_btn(btn_f, "▶  전체 실행",
                                     ACCENT3, self._step_all, col=3)

        # ── 로그 ─────────────────────────────────────────
        tk.Label(f, text="로그", bg=BG, fg=MUTED,
                 font=FONT_SM, anchor="w").grid(row=0, column=0,
                                                sticky="sw", pady=(10, 0))
        self.log_box = scrolledtext.ScrolledText(
            f, bg="#11111b", fg="#a6e3a1", font=FONT_SM,
            relief="flat", state="disabled", wrap="word",
        )
        self.log_box.grid(row=1, column=0, sticky="nsew", pady=(4, 0))

        # 태그
        self.log_box.tag_config("info",  foreground="#89b4fa")
        self.log_box.tag_config("ok",    foreground="#a6e3a1")
        self.log_box.tag_config("err",   foreground="#f38ba8")
        self.log_box.tag_config("muted", foreground="#6c7086")

    # ── 유틸 ─────────────────────────────────────────────
    def _mk_label(self, parent, text):
        tk.Label(parent, text=text, bg=BG2, fg=MUTED,
                 font=FONT_SM, anchor="w").pack(fill="x")

    def _mk_btn(self, parent, text, color, cmd, col, state="normal"):
        b = tk.Button(parent, text=text, command=cmd,
                      bg=color, fg="#1e1e2e", font=FONT_B,
                      relief="flat", cursor="hand2",
                      activebackground=color, activeforeground="#1e1e2e",
                      padx=8, pady=6, state=state)
        b.grid(row=0, column=col, sticky="ew", padx=(0 if col == 0 else 4, 0))
        return b

    def _center(self):
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        w, h = 900, 700
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    def _on_provider_change(self, *_):
        p = self.var_provider.get()
        models = PROVIDER_MODELS.get(p, [])
        self.cb_model["values"] = models
        self.var_model.set(models[0] if models else "")

    def _on_mode_change(self):
        if self.var_mode.get() == "topic":
            self.frm_notes.grid_remove()
            self.frm_topic.grid()
        else:
            self.frm_topic.grid_remove()
            self.frm_notes.grid()

    def _pick_notes_file(self):
        init = str(NOTES_DIR) if NOTES_DIR.exists() else "/"
        path = filedialog.askopenfilename(
            initialdir=init,
            title="노트 파일 선택",
            filetypes=[("지원 파일", "*.mhtml *.txt *.docx"), ("전체", "*.*")],
        )
        if path:
            self.var_notes_path.set(path)

    def _open_result(self):
        if self._html_path and Path(self._html_path).exists():
            import webbrowser
            webbrowser.open(Path(self._html_path).as_uri())
        else:
            messagebox.showinfo("알림", "아직 생성된 HTML이 없습니다.")

    def _log(self, msg: str, tag: str = ""):
        def _do():
            self.log_box.config(state="normal")
            if tag:
                self.log_box.insert("end", msg + "\n", tag)
            else:
                self.log_box.insert("end", msg + "\n")
            self.log_box.see("end")
            self.log_box.config(state="disabled")
        self.after(0, _do)

    def _set_status(self, msg: str, color: str = FG):
        self.after(0, lambda: self.lbl_status.config(text=msg, fg=color))

    def _set_buttons(self, busy: bool):
        state = "disabled" if busy else "normal"
        self.after(0, lambda: [
            self.btn_plan.config(state=state),
            self.btn_all.config(state=state),
        ])

    # ── 공통: LLM 클라이언트 생성 ────────────────────────
    def _make_client(self):
        from blog_autogen.llm import LLMClient, LLMConfig
        key = self.var_key.get().strip()
        if not key:
            messagebox.showerror("오류", "API Key를 입력하세요.")
            return None
        return LLMClient(LLMConfig(
            provider=self.var_provider.get(),
            model=self.var_model.get(),
            api_key=key,
            temperature=float(self.var_temp.get()),
            max_tokens=int(self.var_tokens.get() or 16000),
        ))

    def _get_topic_and_notes(self) -> tuple[str, str]:
        if self.var_mode.get() == "topic":
            topic = self.var_topic.get().strip()
            extra = self.var_extra.get().strip()
            return (f"{topic} {extra}".strip(), "")
        else:
            path_str = self.var_notes_path.get().strip()
            extra    = self.var_extra.get().strip()
            if not path_str:
                messagebox.showerror("오류", "노트 파일을 선택하세요.")
                return ("", "")
            from blog_autogen.notes_loader import load_notes
            notes = load_notes(Path(path_str))
            topic = Path(path_str).stem
            if extra:
                topic = f"{topic} — {extra}"
            return (topic, notes)

    # ── 단계 1: 기획서 ────────────────────────────────────
    def _step_plan(self):
        if self._running:
            return
        client = self._make_client()
        if not client:
            return
        topic, notes = self._get_topic_and_notes()
        if not topic:
            return

        self._running = True
        self._set_buttons(busy=True)
        self._set_status("기획서 생성 중…", ACCENT)

        def _work():
            try:
                from blog_autogen.pipeline import make_plan
                self._log("[1/3] 기획서 생성 중…", "info")
                plan = make_plan(client, topic, notes)
                self._plan = plan
                self._log(f"[1/3] slug={plan.slug}, 챕터 {len(plan.chapters)}개", "ok")
                self._set_status(f"기획서 완료: {plan.slug}", ACCENT2)
                self.after(0, lambda: self.btn_run.config(state="normal"))
            except Exception as e:
                self._log(f"[ERROR] {e}", "err")
                self._log(traceback.format_exc(), "err")
                self._set_status("기획서 생성 실패", ACCENT3)
            finally:
                self._running = False
                self._set_buttons(busy=False)

        threading.Thread(target=_work, daemon=True).start()

    # ── 단계 2: Runner ────────────────────────────────────
    def _step_run(self):
        if self._running or self._plan is None:
            return
        self._running = True
        self._set_buttons(busy=True)
        self._set_status("runner.py 실행 중…", ACCENT)

        def _work():
            try:
                from blog_autogen.pipeline import build_runner, run_runner
                self._log("[2/3] runner.py 작성 중…", "info")
                runner_path = build_runner(self._plan)
                self._log(f"      {runner_path}", "muted")
                result = run_runner(runner_path, log_cb=lambda m: self._log(m, "muted"))
                self._run_result = result
                self._log(f"[2/3] 완료 (rc={result.returncode})", "ok")
                self._set_status(f"runner 완료 (rc={result.returncode})", ACCENT2)
                self.after(0, lambda: self.btn_html.config(state="normal"))
            except Exception as e:
                self._log(f"[ERROR] {e}", "err")
                self._log(traceback.format_exc(), "err")
                self._set_status("runner 실패", ACCENT3)
            finally:
                self._running = False
                self._set_buttons(busy=False)

        threading.Thread(target=_work, daemon=True).start()

    # ── 단계 3: HTML ──────────────────────────────────────
    def _step_html(self):
        if self._running or self._run_result is None:
            return
        client = self._make_client()
        if not client:
            return
        self._running = True
        self._set_buttons(busy=True)
        self._set_status("HTML 생성 중…", ACCENT)

        def _work():
            try:
                from blog_autogen.pipeline import generate_html
                self._log("[3/3] HTML 생성 중…", "info")
                path = generate_html(client, self._plan, self._run_result,
                                     log_cb=lambda m: self._log(m, "muted"))
                self._html_path = path
                self._log(f"[3/3] 저장 완료: {path}", "ok")
                self._set_status(f"완료: {Path(path).name}", ACCENT2)
                self.after(0, lambda: self.btn_open.config(state="normal"))
            except Exception as e:
                self._log(f"[ERROR] {e}", "err")
                self._log(traceback.format_exc(), "err")
                self._set_status("HTML 생성 실패", ACCENT3)
            finally:
                self._running = False
                self._set_buttons(busy=False)

        threading.Thread(target=_work, daemon=True).start()

    # ── 전체 실행 ─────────────────────────────────────────
    def _step_all(self):
        if self._running:
            return
        client = self._make_client()
        if not client:
            return
        topic, notes = self._get_topic_and_notes()
        if not topic:
            return
        self._running = True
        self._set_buttons(busy=True)
        self._plan = None
        self._run_result = None
        self._html_path = None
        self.btn_run.config(state="disabled")
        self.btn_html.config(state="disabled")
        self.btn_open.config(state="disabled")
        self._set_status("전체 실행 중…", ACCENT)

        def _work():
            try:
                from blog_autogen.pipeline import make_plan, build_runner, run_runner, generate_html

                self._log("=" * 48, "muted")
                self._log("[1/3] 기획서 생성 중…", "info")
                plan = make_plan(client, topic, notes)
                self._plan = plan
                self._log(f"      slug={plan.slug}, 챕터 {len(plan.chapters)}개", "ok")

                self._log("[2/3] runner.py 작성·실행 중…", "info")
                runner_path = build_runner(plan)
                result = run_runner(runner_path, log_cb=lambda m: self._log(m, "muted"))
                self._run_result = result
                self._log(f"      returncode={result.returncode}", "ok")

                self._log("[3/3] HTML 생성 중…", "info")
                path = generate_html(client, plan, result,
                                     log_cb=lambda m: self._log(m, "muted"))
                self._html_path = path
                self._log(f"      저장 완료: {path}", "ok")
                self._log("=" * 48, "muted")
                self._set_status(f"완료: {Path(path).name}", ACCENT2)
                self.after(0, lambda: [
                    self.btn_run.config(state="normal"),
                    self.btn_html.config(state="normal"),
                    self.btn_open.config(state="normal"),
                ])
            except Exception as e:
                self._log(f"[ERROR] {e}", "err")
                self._log(traceback.format_exc(), "err")
                self._set_status("실패", ACCENT3)
            finally:
                self._running = False
                self._set_buttons(busy=False)

        threading.Thread(target=_work, daemon=True).start()


# ─────────────────────────────────────────────────────────────
def main():
    # tkinter 스타일
    app = App()

    # ttk 스타일 (Combobox)
    style = ttk.Style(app)
    style.theme_use("clam")
    style.configure("TCombobox",
                    fieldbackground=ENTRY_BG,
                    background=ENTRY_BG,
                    foreground=FG,
                    selectbackground=ENTRY_BG,
                    selectforeground=FG,
                    arrowcolor=FG)
    style.map("TCombobox", fieldbackground=[("readonly", ENTRY_BG)])

    app.mainloop()


if __name__ == "__main__":
    main()
