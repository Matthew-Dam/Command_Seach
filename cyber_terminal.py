import customtkinter as ctk
import tkinter as tk
from tkinter import font
import threading
import time
import random
import datetime
import webbrowser
import sys
import io

# ─── STDIN GUARD ─────────────────────────────────────────────────────────────
# Prevents "lost sys.stdin" errors when backend modules call input()
class _DummyStdin(io.RawIOBase):
    def readline(self): return b""
    def read(self, n=-1): return b""
    def readable(self): return True

# ─── THEME ───────────────────────────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Cyberpunk palette
C_BG        = "#0a0a0f"
C_BG2       = "#0d0d1a"
C_PANEL     = "#0f0f1e"
C_BORDER    = "#1a1a3e"
C_NEON_CYAN = "#00f5ff"
C_NEON_PINK = "#ff0080"
C_NEON_PURP = "#bf00ff"
C_NEON_GRN  = "#00ff9f"
C_NEON_YEL  = "#f5ff00"
C_DIM_CYAN  = "#004d55"
C_DIM_PINK  = "#550030"
C_TEXT      = "#c8e6ff"
C_MUTED     = "#4a5a7a"
C_ACCENT    = "#1a2a4a"

FONT_MONO   = ("Courier New", 13)
FONT_MONO_S = ("Courier New", 11)
FONT_MONO_L = ("Courier New", 15, "bold")
FONT_MONO_XL= ("Courier New", 22, "bold")
FONT_TITLE  = ("Courier New", 10)


# ─── HELPERS ─────────────────────────────────────────────────────────────────
def neon_tag_config(widget, tag, fg, bold=False):
    weight = "bold" if bold else "normal"
    widget.tag_config(tag, foreground=fg, font=("Courier New", 12, weight))


# ─── MOCK BACK-END (replace with your real imports) ───────────────────────────
# Remove this block and uncomment the real imports once you run from your project folder
class _MockSite:
    @staticmethod
    def operate_movie_site(url): return True
    @staticmethod
    def operate_music_site(url): return True
    def login(self, k): pass
    def webgo(self, url): pass
    def open_ai(self, url): pass
    SITE_URLS       = {"Netflix": "https://netflix.com", "Hulu": "https://hulu.com", "Prime": "https://primevideo.com"}
    MUSIC_URLS      = {"Spotify": "https://spotify.com", "SoundCloud": "https://soundcloud.com"}
    SOCIAL_LOGIN_URLS = {"twitter": "https://twitter.com", "instagram": "https://instagram.com"}
    AI_URLS         = {"ChatGPT": "https://chat.openai.com", "Gemini": "https://gemini.google.com", "Claude": "https://claude.ai", "Copilot": "https://copilot.microsoft.com", "Perplexity": "https://perplexity.ai"}

try:
    from ais import AIs
    from movie_sites import MovieSites
    from music_site  import MusicSite
    from social_media import SocialMedia
    movies_sites  = MovieSites()
    musics_sites  = MusicSite()
    social_site   = SocialMedia()
    ai_site = AIs()
except ImportError:
    movies_sites  = _MockSite()
    musics_sites  = _MockSite()
    social_site   = _MockSite()
    ai_site = _MockSite()
    movies_sites.MUSIC_URLS = _MockSite.MUSIC_URLS
    social_site.SOCIAL_LOGIN_URLS = _MockSite.SOCIAL_LOGIN_URLS

m_links      = movies_sites.SITE_URLS
mx_links     = musics_sites.MUSIC_URLS
social_links = social_site.SOCIAL_LOGIN_URLS
ai_links = ai_site.AI_URLS

# ─── SCANLINE CANVAS ─────────────────────────────────────────────────────────
class ScanlineCanvas(tk.Canvas):
    def __init__(self, master, **kw):
        super().__init__(master, bg=C_BG, highlightthickness=0, **kw)
        self._offset = 0
        self._draw()

    def _draw(self):
        self.delete("scan")
        h = self.winfo_height() or 800
        w = self.winfo_width()  or 1200
        for y in range(self._offset, h, 6):
            self.create_line(0, y, w, y, fill="#ffffff", tags="scan")
        self._offset = (self._offset + 1) % 6
        self.after(80, self._draw)


# ─── GLITCH LABEL ────────────────────────────────────────────────────────────
class GlitchLabel(tk.Label):
    CHARS = "!@#$%^&*<>?/\\|{}[]~`0123456789ABCDEF"

    def __init__(self, master, text, fg=C_NEON_CYAN, **kw):
        self._real = text
        super().__init__(master, text=text, fg=fg, bg=C_BG,
                         font=FONT_MONO_XL, **kw)
        self._glitching = False

    def glitch(self):
        if self._glitching:
            return
        self._glitching = True
        self._run(8)

    def _run(self, n):
        if n <= 0:
            self.config(text=self._real)
            self._glitching = False
            return
        scrambled = "".join(
            c if random.random() > 0.3 else random.choice(self.CHARS)
            for c in self._real
        )
        self.config(text=scrambled)
        self.after(60, lambda: self._run(n - 1))


# ─── MAIN APP ────────────────────────────────────────────────────────────────
class CyberTerminal(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("OBEDIENT AGENT v1.0 // COMMAND SEARCH")
        self.geometry("600x500")
        self.minsize(200, 200)
        self.configure(fg_color=C_BG)
        self._history    = []
        self._hist_idx   = -1
        self._boot_done  = False
        self._build_ui()
        self.after(200, self._boot_sequence)

    # ── UI BUILD ──────────────────────────────────────────────────────────────
    def _build_ui(self):
        # ── TOP BAR ──
        topbar = tk.Frame(self, bg=C_BG, height=56)
        topbar.pack(fill="x", padx=0, pady=0)
        topbar.pack_propagate(False)

        self._title_lbl = GlitchLabel(topbar, "COMMAND SEARCH", fg=C_NEON_CYAN)
        self._title_lbl.pack(side="left", padx=20, pady=8)

        self._clock_lbl = tk.Label(topbar, text="", fg=C_NEON_PINK,
                                   bg=C_BG, font=FONT_TITLE)
        self._clock_lbl.pack(side="right", padx=20)
        self._tick_clock()

        status_dot = tk.Label(topbar, text="● ONLINE", fg=C_NEON_GRN,
                              bg=C_BG, font=FONT_TITLE)
        status_dot.pack(side="right", padx=10)

        # divider
        tk.Frame(self, bg=C_NEON_CYAN, height=1).pack(fill="x", padx=0)

        # ── BODY (left panel + terminal) ──
        body = tk.Frame(self, bg=C_BG)
        body.pack(fill="both", expand=True, padx=0, pady=0)

        # ── LEFT SIDEBAR (scrollable) ──
        sidebar_outer = tk.Frame(body, bg=C_BG2, width=210)
        sidebar_outer.pack(side="left", fill="y")
        sidebar_outer.pack_propagate(False)

        tk.Label(sidebar_outer, text="// QUICK LAUNCH", fg=C_MUTED,
                 bg=C_BG2, font=FONT_TITLE).pack(anchor="w", padx=14, pady=(14, 4))

        tk.Frame(sidebar_outer, bg=C_BORDER, height=1).pack(fill="x", padx=8)

        sb_canvas = tk.Canvas(sidebar_outer, bg=C_BG2, highlightthickness=0,
                              bd=0, width=194)
        sb_canvas.pack(side="left", fill="both", expand=True)

        sb_scroll = tk.Scrollbar(sidebar_outer, orient="vertical",
                                 command=sb_canvas.yview,
                                 bg=C_BG2, troughcolor=C_BG2,
                                 activebackground=C_DIM_CYAN,
                                 width=4, relief="flat", bd=0)
        sb_scroll.pack(side="right", fill="y")
        sb_canvas.configure(yscrollcommand=sb_scroll.set)

        inner = tk.Frame(sb_canvas, bg=C_BG2)
        inner_win = sb_canvas.create_window((0, 0), window=inner, anchor="nw")

        def _on_canvas_configure(e):
            sb_canvas.itemconfig(inner_win, width=e.width)
        sb_canvas.bind("<Configure>", _on_canvas_configure)

        def _refresh_scroll(e=None):
            sb_canvas.configure(scrollregion=sb_canvas.bbox("all"))
            self._bind_sidebar_scroll(inner, sb_canvas)
        inner.bind("<Configure>", _refresh_scroll)

        self._build_sidebar_section(inner, "MOVIES", m_links,      C_NEON_CYAN, "open")
        self._build_sidebar_section(inner, "MUSIC",  mx_links,     C_NEON_PINK, "open")
        self._build_sidebar_section(inner, "LOGIN",  social_links, C_NEON_PURP, "login")
        self._build_sidebar_section(inner, "AI",     ai_links,     C_NEON_YEL,  "ai")
        self._sb_canvas = sb_canvas

        # separator
        tk.Frame(body, bg=C_BORDER, width=1).pack(side="left", fill="y")

        # ── RIGHT: terminal area ──
        right = tk.Frame(body, bg=C_BG)
        right.pack(side="left", fill="both", expand=True)

        # scanlines behind output
        self._scan = ScanlineCanvas(right)
        self._scan.place(relwidth=1, relheight=1)

        # output text box
        out_frame = tk.Frame(right, bg=C_BG)
        out_frame.pack(fill="both", expand=True, padx=18, pady=(14, 6))

        self._output = tk.Text(
            out_frame,
            bg=C_BG, fg=C_TEXT,
            font=FONT_MONO_S,
            insertbackground=C_NEON_CYAN,
            selectbackground=C_DIM_CYAN,
            relief="flat", bd=0,
            state="disabled",
            wrap="word",
            cursor="arrow",
        )
        self._output.pack(fill="both", expand=True)

        sb = tk.Scrollbar(out_frame, command=self._output.yview,
                          bg=C_BG, troughcolor=C_BG, activebackground=C_DIM_CYAN,
                          width=6, relief="flat", bd=0)
        sb.pack(side="right", fill="y")
        self._output.config(yscrollcommand=sb.set)

        # colour tags
        neon_tag_config(self._output, "cyan",   C_NEON_CYAN,  bold=True)
        neon_tag_config(self._output, "pink",   C_NEON_PINK,  bold=True)
        neon_tag_config(self._output, "purp",   C_NEON_PURP,  bold=True)
        neon_tag_config(self._output, "green",  C_NEON_GRN,   bold=True)
        neon_tag_config(self._output, "yellow", C_NEON_YEL,   bold=False)
        neon_tag_config(self._output, "muted",  C_MUTED,      bold=False)
        neon_tag_config(self._output, "error",  C_NEON_PINK,  bold=True)
        neon_tag_config(self._output, "text",   C_TEXT,       bold=False)

        # ── INPUT ROW ──
        inp_row = tk.Frame(right, bg=C_BG, height=52)
        inp_row.pack(fill="x", padx=18, pady=(0, 14))
        inp_row.pack_propagate(False)

        tk.Frame(right, bg=C_NEON_PURP, height=1).pack(fill="x", padx=18)

        prompt_lbl = tk.Label(inp_row, text="▶", fg=C_NEON_CYAN,
                              bg=C_BG, font=FONT_MONO_L)
        prompt_lbl.pack(side="left", padx=(0, 8), pady=8)

        self._entry = tk.Entry(
            inp_row,
            bg=C_BG, fg=C_NEON_CYAN,
            insertbackground=C_NEON_CYAN,
            font=FONT_MONO_L,
            relief="flat", bd=0,
            highlightthickness=0,
        )
        self._entry.pack(side="left", fill="both", expand=True, ipady=8)
        self._entry.bind("<Return>",   self._on_enter)
        self._entry.bind("<Up>",       self._hist_up)
        self._entry.bind("<Down>",     self._hist_down)
        self._entry.bind("<Tab>",      self._autocomplete)
        self._entry.focus()

        exec_btn = tk.Button(
            inp_row, text="EXEC",
            bg=C_DIM_CYAN, fg=C_NEON_CYAN,
            activebackground=C_NEON_CYAN, activeforeground=C_BG,
            font=("Courier New", 11, "bold"),
            relief="flat", bd=0, padx=16, cursor="hand2",
            command=self._on_enter,
        )
        exec_btn.pack(side="right", padx=(8, 0), pady=8)

        # status bar
        tk.Frame(self, bg=C_BORDER, height=1).pack(fill="x")
        statusbar = tk.Frame(self, bg=C_BG2, height=24)
        statusbar.pack(fill="x")
        statusbar.pack_propagate(False)
        self._status_lbl = tk.Label(
            statusbar, text="SYSTEM READY  //  TYPE 'help' FOR COMMANDS",
            fg=C_MUTED, bg=C_BG2, font=FONT_TITLE
        )
        self._status_lbl.pack(side="left", padx=14)

    def _bind_sidebar_scroll(self, widget, canvas):
        widget.bind("<MouseWheel>",
            lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        widget.bind("<Button-4>",
            lambda e: canvas.yview_scroll(-1, "units"))
        widget.bind("<Button-5>",
            lambda e: canvas.yview_scroll(1, "units"))
        for child in widget.winfo_children():
            self._bind_sidebar_scroll(child, canvas)

    def _build_sidebar_section(self, parent, title, links, color, cmd_prefix):
        tk.Label(parent, text=f"── {title}", fg=color,
                 bg=C_BG2, font=("Courier New", 10, "bold")).pack(
            anchor="w", padx=14, pady=(10, 2))
        for name in links:
            display = name[:18]
            btn = tk.Button(
                parent, text=f"  {display}",
                bg=C_BG2, fg=C_TEXT,
                activebackground=C_ACCENT, activeforeground=color,
                relief="flat", bd=0,
                font=FONT_TITLE, anchor="w", cursor="hand2",
                command=lambda n=name, p=cmd_prefix: self._sidebar_launch(p, n),
            )
            btn.pack(fill="x", padx=6, pady=1)

    # ── CLOCK ────────────────────────────────────────────────────────────────
    def _tick_clock(self):
        now = datetime.datetime.now().strftime("%Y.%m.%d  %H:%M:%S")
        self._clock_lbl.config(text=now,fg=C_NEON_GRN)
        self.after(1000, self._tick_clock)

    # ── OUTPUT HELPERS ────────────────────────────────────────────────────────
    def _write(self, text, tag="text", newline=True):
        self._output.config(state="normal")
        self._output.insert("end", text + ("\n" if newline else ""), tag)
        self._output.see("end")
        self._output.config(state="disabled")

    def _writeln(self):
        self._write("", "text", newline=True)

    def _divider(self, color="cyan"):
        self._write("─" * 62, color)

    def _prompt_echo(self, cmd):
        self._write(f"▶  {cmd}", "cyan")

    # ── BOOT SEQUENCE ─────────────────────────────────────────────────────────
    def _boot_sequence(self):
        lines = [
            ("COMMAND SEARCH  //  OBEDIENT AGENT v1.0",        "red"),
            ("INITIALIZING SUBSYSTEMS...",                      "muted"),
            ("",                                                "text"),
            (f"  [{len(m_links):02d}] MOVIE SITES LOADED",     "pink"),
            (f"  [{len(mx_links):02d}] MUSIC SITES LOADED",    "purp"),
            (f"  [{len(social_links):02d}] SOCIAL LOGINS INDEXED", "green"),
            (f"  [{len(ai_links):02d}] AI TOOLS INDEXED",      "yellow"),
            ("",                                                "text"),
            ("ALL SYSTEMS NOMINAL  //  READY FOR INPUT",       "yellow"),
            ("",                                                "text"),
            ("TYPE 'help' TO SEE AVAILABLE COMMANDS",          "muted"),
        ]
        self._divider("purp")
        self._stream_boot(lines, 0)

    def _stream_boot(self, lines, idx):
        if idx >= len(lines):
            self._divider("purp")
            self._boot_done = True
            self._title_lbl.glitch()
            return
        text, tag = lines[idx]
        self._write(text, tag)
        self.after(90, lambda: self._stream_boot(lines, idx + 1))

    # ── COMMAND PROCESSING ────────────────────────────────────────────────────
    def _on_enter(self, event=None):
        raw = self._entry.get().strip()
        if not raw:
            return
        self._entry.delete(0, "end")
        self._history.append(raw)
        self._hist_idx = len(self._history)
        self._writeln()
        self._prompt_echo(raw)
        self._status_lbl.config(text=f"EXECUTING: {raw.upper()}")
        threading.Thread(target=self._dispatch, args=(raw,), daemon=True).start()

    def _dispatch(self, user_input):
        cmd = user_input.lower().strip()

        if cmd == "help":
            self._show_help()

        elif cmd == "cls":
            self._output.config(state="normal")
            self._output.delete("1.0", "end")
            self._output.config(state="disabled")

        elif cmd == "list movies":
            self._list_sites("MOVIE SITES", m_links, "pink")

        elif cmd == "list music":
            self._list_sites("MUSIC SITES", mx_links, "purp")

        elif cmd == "list social":
            self._list_sites("SOCIAL LOGINS", social_links, "green")

        elif cmd == "list ai":
            self._list_sites("AI TOOLS", ai_links, "yellow")

        elif cmd.startswith("open "):
            web = cmd[5:].strip()
            self._cmd_open(web)

        elif cmd.startswith("search "):
            # format: search <sitename> <query>   e.g. search youtube funny cats
            parts = cmd[7:].strip().split(" ", 1)
            if len(parts) < 2:
                self._write("  USAGE: search <site> <query>", "yellow")
                self._write("  EXAMPLE: search youtube funny cats", "muted")
            else:
                self._cmd_search(parts[0], parts[1])

        elif cmd.startswith("login "):
            web = cmd[6:].strip()
            self._cmd_login(web)

        elif cmd.startswith("ai "):
            web = cmd[3:].strip()
            self._cmd_ai(web)

        else:
            self._write(f"  SEARCHING BING: \"{user_input}\"...", "yellow")
            try:
                movies_sites.webgo(f"https://www.bing.com/search?q={user_input}")
                self._write("  BROWSER LAUNCHED.", "green")
            except Exception as e:
                self._write(f"  ERROR: {e}", "error")

        self.after(0, lambda: self._status_lbl.config(
            text="SYSTEM READY  //  TYPE 'help' FOR COMMANDS"))

    def _cmd_open(self, web):
        matched = False
        for site, url in m_links.items():
            if web in site.lower():
                self._write(f"  LAUNCHING MOVIE SITE: {site.upper()}", "pink")
                _real_stdin = sys.stdin
                try:
                    sys.stdin = _DummyStdin()
                    movies_sites.operate_movie_site(url)
                    self._write("  ✓ DONE", "green")
                except EOFError:
                    self._write("  ✓ DONE", "green")
                except Exception as e:
                    self._write(f"  ERROR: {e}", "error")
                finally:
                    sys.stdin = _real_stdin
                matched = True
                break
        if not matched:
            for site, url in mx_links.items():
                if web in site.lower():
                    self._write(f"  LAUNCHING MUSIC SITE: {site.upper()}", "purp")
                    _real_stdin = sys.stdin
                    try:
                        sys.stdin = _DummyStdin()
                        musics_sites.operate_music_site(url)
                        self._write("  ✓ DONE", "green")
                    except EOFError:
                        self._write("  ✓ DONE", "green")
                    except Exception as e:
                        self._write(f"  ERROR: {e}", "error")
                    finally:
                        sys.stdin = _real_stdin
                    matched = True
                    break
        if not matched:
            self._write(f"  ✗ NO SITE FOUND MATCHING: \"{web}\"", "error")
            self._write("  TRY: list movies  |  list music", "muted")

    def _cmd_search(self, site, query):
        for name, url in m_links.items():
            if site in name.lower():
                self._write(f"  SEARCHING {name.upper()} FOR: \"{query}\"", "pink")
                try:
                    movies_sites.search_movie_site(url, query)
                    self._write("  ✓ BROWSER LAUNCHED", "green")
                except Exception as e:
                    self._write(f"  ERROR: {e}", "error")
                return
        self._write(f"  ✗ NO SITE FOUND MATCHING: \"{site}\"", "error")
        self._write("  TRY: list movies", "muted")
        found = False
        for k in social_links:
            if web in k.lower():
                self._write(f"  INITIATING LOGIN: {k.upper()}", "purp")
                _real_stdin = sys.stdin
                try:
                    sys.stdin = _DummyStdin()
                    social_site.login(k)
                    self._write("  ✓ AUTH SEQUENCE STARTED", "green")
                except EOFError:
                    self._write("  ✓ AUTH SEQUENCE STARTED", "green")
                except Exception as e:
                    self._write(f"  ERROR: {e}", "error")
                finally:
                    sys.stdin = _real_stdin
                found = True
                break
        if not found:
            self._write(f"  ✗ NO LOGIN FOUND FOR: \"{web}\"", "error")
            self._write("  TRY: list social", "muted")

    def _cmd_ai(self, web):
        found = False
        for name, url in ai_links.items():
            if web in name.lower():
                self._write(f"  CONNECTING TO AI: {name.upper()}", "yellow")
                try:
                    # Try the AIs class method first, fall back to webbrowser
                    opened = False
                    if hasattr(ai_site, 'open_ai') and callable(ai_site.open_ai):
                        try:
                            result = ai_site.open_ai(url)
                            if result is not False:
                                opened = True
                        except Exception:
                            pass
                    if not opened and hasattr(ai_site, 'webgo') and callable(ai_site.webgo):
                        try:
                            ai_site.webgo(url)
                            opened = True
                        except Exception:
                            pass
                    if not opened:
                        webbrowser.open(url)
                    self._write(f"  ✓ {name.upper()} LAUNCHED", "green")
                except Exception as e:
                    self._write(f"  ERROR: {e}", "error")
                found = True
                break
        if not found:
            self._write(f"  ✗ NO AI FOUND MATCHING: \"{web}\"", "error")
            self._write("  TRY: list ai", "muted")

    def _list_sites(self, title, links, tag):
        self._divider(tag)
        self._write(f"  {title}", tag)
        self._divider(tag)
        for i, name in enumerate(links, 1):
            self._write(f"  [{i:02d}]  {name}", "text")
        self._divider(tag)

    def _show_help(self):
        self._divider("cyan")
        self._write("  AVAILABLE COMMANDS", "cyan")
        self._divider("cyan")
        cmds = [
            ("open <name>",       "Open a movie or music site",  "pink"),
            ("login <name>",      "Log into a social platform",  "purp"),
            ("ai <name>",         "Launch an AI tool",           "yellow"),
            ("list movies",    "Show all movie sites",        "pink"),
            ("list music",     "Show all music sites",        "purp"),
            ("list social",    "Show all social logins",      "green"),
            ("list ai",        "Show all AI tools",           "yellow"),
            ("<any text>",     "Search Bing in browser",      "muted"),
            ("clear",          "Clear terminal output",       "muted"),
            ("help",           "Show this help screen",       "cyan"),
        ]
        for cmd, desc, tag in cmds:
            self._write(f"  {cmd:<22} — {desc}", tag)
        self._write("", "text")
        self._write("  KEYBOARD SHORTCUTS:", "cyan")
        self._write("  ↑ / ↓  — Scroll command history", "muted")
        self._write("  TAB    — Autocomplete site name",  "muted")
        self._divider("cyan")

    # ── HISTORY + AUTOCOMPLETE ────────────────────────────────────────────
    def _hist_up(self, event):
        if not self._history:
            return
        self._hist_idx = max(0, self._hist_idx - 1)
        self._entry.delete(0, "end")
        self._entry.insert(0, self._history[self._hist_idx])

    def _hist_down(self, event):
        if not self._history:
            return
        self._hist_idx = min(len(self._history), self._hist_idx + 1)
        self._entry.delete(0, "end")
        if self._hist_idx < len(self._history):
            self._entry.insert(0, self._history[self._hist_idx])

    def _autocomplete(self, event):
        text = self._entry.get().lower().strip()
        all_names = (
            [f"open {k.lower()}"  for k in m_links]  +
            [f"open {k.lower()}"  for k in mx_links] +
            [f"login {k.lower()}" for k in social_links] +
            [f"ai {k.lower()}"    for k in ai_links]
        )
        matches = [n for n in all_names if n.startswith(text)]
        if len(matches) == 1:
            self._entry.delete(0, "end")
            self._entry.insert(0, matches[0])
        elif len(matches) > 1:
            self._write("", "text")
            self._write("  AUTOCOMPLETE MATCHES:", "yellow")
            for m in matches:
                self._write(f"    {m}", "muted")
        return "break"
    # ── SIDEBAR QUICK LAUNCH ──────────────────────────────────────────────────
    def _sidebar_launch(self, prefix, name):
        cmd = f"{prefix} {name}"
        self._entry.delete(0, "end")
        self._entry.insert(0, cmd)
        self._on_enter()


# ─── ENTRY POINT ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = CyberTerminal()
    app.mainloop()
