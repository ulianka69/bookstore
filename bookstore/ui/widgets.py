import customtkinter as ctk
from theme import Theme as T


class Card(ctk.CTkFrame):
    def __init__(self, master, padding=18, accent=False, **kw):
        border = T.PRIMARY if accent else T.BORDER
        super().__init__(
            master,
            corner_radius=T.R_MD,
            fg_color=T.BG_SURFACE,
            border_width=1,
            border_color=border,
            **kw,
        )
        self._padding = padding

    def body(self):
        f = ctk.CTkFrame(self, fg_color="transparent")
        f.pack(fill="both", expand=True, padx=self._padding, pady=self._padding)
        return f


class PageTitle(ctk.CTkFrame):
    def __init__(self, master, title, subtitle=None):
        super().__init__(master, fg_color="transparent")

        left = ctk.CTkFrame(self, fg_color="transparent")
        left.pack(side="left", fill="x", expand=True)

        title_row = ctk.CTkFrame(left, fg_color="transparent")
        title_row.pack(anchor="w")

        ctk.CTkFrame(title_row, width=4, height=26, corner_radius=2,
                     fg_color=T.PRIMARY).pack(side="left", padx=(0, 10))

        ctk.CTkLabel(title_row, text=title, font=T.h1(),
                     text_color=T.TEXT, anchor="w").pack(side="left")

        if subtitle:
            ctk.CTkLabel(left, text=subtitle, font=T.small(),
                         text_color=T.TEXT_MUTED, anchor="w").pack(
                anchor="w", pady=(6, 0), padx=(14, 0))

        self.actions = ctk.CTkFrame(self, fg_color="transparent")
        self.actions.pack(side="right")


class PrimaryButton(ctk.CTkButton):
    def __init__(self, master, **kw):
        kw.setdefault("height", 40)
        kw.setdefault("corner_radius", T.R_SM)
        kw.setdefault("fg_color", T.PRIMARY)
        kw.setdefault("hover_color", T.PRIMARY_HOV)
        kw.setdefault("text_color", "#ffffff")
        kw.setdefault("font", ctk.CTkFont(family=T.FONT_FAMILY, size=13, weight="bold"))
        super().__init__(master, **kw)


class GhostButton(ctk.CTkButton):
    def __init__(self, master, **kw):
        kw.setdefault("height", 40)
        kw.setdefault("corner_radius", T.R_SM)
        kw.setdefault("fg_color", "transparent")
        kw.setdefault("hover_color", T.PRIMARY_SOFT)
        kw.setdefault("border_width", 1)
        kw.setdefault("border_color", T.BORDER)
        kw.setdefault("text_color", T.TEXT)
        kw.setdefault("font", ctk.CTkFont(family=T.FONT_FAMILY, size=13))
        super().__init__(master, **kw)


class DangerButton(ctk.CTkButton):
    def __init__(self, master, **kw):
        kw.setdefault("height", 36)
        kw.setdefault("corner_radius", T.R_SM)
        kw.setdefault("fg_color", T.DANGER)
        kw.setdefault("hover_color", T.DANGER_HOV)
        kw.setdefault("text_color", "#ffffff")
        kw.setdefault("font", ctk.CTkFont(family=T.FONT_FAMILY, size=13, weight="bold"))
        super().__init__(master, **kw)


class Badge(ctk.CTkLabel):
    def __init__(self, master, text, color=T.PRIMARY):
        super().__init__(
            master, text=f"  {text}  ",
            font=T.badge(),
            text_color="#ffffff",
            fg_color=color,
            corner_radius=9,
            padx=8, pady=3,
        )


class SearchEntry(ctk.CTkEntry):
    def __init__(self, master, **kw):
        kw.setdefault("height", 42)
        kw.setdefault("corner_radius", T.R_SM)
        kw.setdefault("border_width", 1)
        kw.setdefault("border_color", T.BORDER)
        kw.setdefault("fg_color", T.BG_ELEVATED)
        kw.setdefault("text_color", T.TEXT)
        kw.setdefault("placeholder_text_color", T.TEXT_FAINT)
        kw.setdefault("font", T.body())
        super().__init__(master, **kw)


class Select(ctk.CTkOptionMenu):
    def __init__(self, master, **kw):
        kw.setdefault("height", 42)
        kw.setdefault("corner_radius", T.R_SM)
        kw.setdefault("fg_color", T.BG_ELEVATED)
        kw.setdefault("button_color", T.BG_ELEVATED)
        kw.setdefault("button_hover_color", T.PRIMARY_SOFT)
        kw.setdefault("dropdown_fg_color", T.BG_SURFACE)
        kw.setdefault("dropdown_hover_color", T.PRIMARY_SOFT)
        kw.setdefault("text_color", T.TEXT)
        kw.setdefault("font", T.body())
        super().__init__(master, **kw)


class Divider(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, height=1, fg_color=T.BORDER_SOFT)


class InputDialog(ctk.CTkToplevel):
    def __init__(self, master, title="Ввод", label="Значение",
                 initial="", placeholder="", on_submit=None):
        super().__init__(master)
        self.on_submit = on_submit
        self.result = None

        self.title(title)
        self.geometry("440x270")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()
        self.configure(fg_color=T.BG_APP)

        self.update_idletasks()
        try:
            px = master.winfo_rootx() + (master.winfo_width() - 440) // 2
            py = master.winfo_rooty() + (master.winfo_height() - 270) // 2
            self.geometry(f"+{max(px, 0)}+{max(py, 0)}")
        except Exception:
            pass

        body = ctk.CTkFrame(self, fg_color=T.BG_SURFACE, corner_radius=T.R_MD,
                            border_width=1, border_color=T.BORDER)
        body.pack(fill="both", expand=True, padx=20, pady=20)

        inner = ctk.CTkFrame(body, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=20, pady=20)

        title_row = ctk.CTkFrame(inner, fg_color="transparent")
        title_row.pack(anchor="w")
        ctk.CTkFrame(title_row, width=4, height=22, corner_radius=2,
                     fg_color=T.PRIMARY).pack(side="left", padx=(0, 8))
        ctk.CTkLabel(title_row, text=title, font=T.h2(),
                     text_color=T.TEXT).pack(side="left")

        ctk.CTkLabel(inner, text=label, font=T.small(),
                     text_color=T.TEXT_MUTED, anchor="w").pack(
            anchor="w", pady=(14, 4), padx=(12, 0))

        self.entry = ctk.CTkEntry(
            inner, height=42, corner_radius=T.R_SM,
            fg_color=T.BG_ELEVATED, border_color=T.BORDER,
            placeholder_text=placeholder, font=T.body(),
        )
        self.entry.pack(fill="x")
        self.entry.insert(0, initial)
        self.entry.focus_set()

        btns = ctk.CTkFrame(inner, fg_color="transparent")
        btns.pack(fill="x", pady=(20, 0))
        PrimaryButton(btns, text="Сохранить", width=150,
                      command=self._submit).pack(side="right")
        GhostButton(btns, text="Отмена", width=110,
                    command=self.destroy).pack(side="right", padx=8)

        self.entry.bind("<Return>", lambda e: self._submit())
        self.bind("<Escape>", lambda e: self.destroy())

    def _submit(self):
        value = self.entry.get().strip()
        if not value:
            self.entry.configure(border_color=T.DANGER)
            return
        self.result = value
        if self.on_submit:
            self.on_submit(value)
        self.destroy()