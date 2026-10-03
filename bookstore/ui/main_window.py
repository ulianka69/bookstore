import customtkinter as ctk
from theme import Theme as T, apply_theme
from ui.books_view import BooksView
from ui.authors_view import AuthorsView
from ui.genres_view import GenresView


class MainWindow(ctk.CTkToplevel):
    def __init__(self, master, user, on_logout=None):
        super().__init__(master)
        self.user = user
        self.on_logout = on_logout
        self.master_app = master

        apply_theme()

        self.title("BookStore")
        self.geometry("1360x820")
        self.minsize(1180, 700)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self._build_sidebar()
        self._build_content()
        self.show_page("books")

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _on_close(self):
        try:
            self.master_app.destroy()
        except Exception:
            pass

    def _build_sidebar(self):
        bar = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color=T.BG_SIDEBAR)
        bar.grid(row=0, column=0, sticky="nsew")
        bar.grid_propagate(False)

        logo = ctk.CTkFrame(bar, fg_color="transparent")
        logo.pack(fill="x", padx=18, pady=(24, 30))

        mark = ctk.CTkFrame(logo, width=42, height=42,
                            corner_radius=12, fg_color=T.PRIMARY)
        mark.pack(side="left")
        mark.pack_propagate(False)
        ctk.CTkLabel(mark, text="B", font=ctk.CTkFont(
            family=T.FONT_FAMILY, size=20, weight="bold"),
            text_color="#ffffff").place(relx=0.5, rely=0.5, anchor="center")

        brand = ctk.CTkFrame(logo, fg_color="transparent")
        brand.pack(side="left", padx=(10, 0))
        ctk.CTkLabel(brand, text="BookStore",
                     font=ctk.CTkFont(family=T.FONT_FAMILY, size=17, weight="bold"),
                     text_color=T.TEXT, anchor="w").pack(anchor="w")
        ctk.CTkLabel(brand, text="книжный магазин",
                     font=ctk.CTkFont(family=T.FONT_FAMILY, size=11),
                     text_color=T.TEXT_MUTED, anchor="w").pack(anchor="w")

        ctk.CTkLabel(bar, text="  МЕНЮ", font=ctk.CTkFont(
            family=T.FONT_FAMILY, size=11, weight="bold"),
            text_color=T.TEXT_FAINT, anchor="w").pack(
            fill="x", padx=24, pady=(0, 6))

        self.nav_buttons = {}
        for key, label in [
            ("books", "Книги"),
            ("authors", "Авторы"),
            ("genres", "Жанры"),
        ]:
            wrap = ctk.CTkFrame(bar, fg_color="transparent")
            wrap.pack(fill="x", padx=14, pady=2)

            accent = ctk.CTkFrame(wrap, width=3, height=38,
                                  corner_radius=2, fg_color="transparent")
            accent.pack(side="left", fill="y", padx=(0, 6))

            btn = ctk.CTkButton(
                wrap, text=f"   {label}",
                anchor="w", height=38, corner_radius=T.R_SM,
                fg_color="transparent", hover_color=T.PRIMARY_SOFT,
                text_color=T.TEXT,
                font=ctk.CTkFont(family=T.FONT_FAMILY, size=14),
                command=lambda k=key: self.show_page(k),
            )
            btn.pack(side="left", fill="x", expand=True)

            self.nav_buttons[key] = (btn, accent)

        bottom = ctk.CTkFrame(bar, fg_color="transparent")
        bottom.pack(side="bottom", fill="x", padx=16, pady=16)
        ctk.CTkFrame(bottom, height=1, fg_color=T.BORDER_SOFT).pack(
            fill="x", pady=(0, 12))

        prof = ctk.CTkFrame(bottom, fg_color=T.BG_ELEVATED,
                            corner_radius=T.R_MD, border_width=1,
                            border_color=T.BORDER_SOFT)
        prof.pack(fill="x")
        inner = ctk.CTkFrame(prof, fg_color="transparent")
        inner.pack(fill="x", padx=12, pady=10)

        ctk.CTkLabel(
            inner, text=user_initials(self.user["username"]),
            width=38, height=38, corner_radius=19,
            fg_color=T.PRIMARY, text_color="#ffffff",
            font=ctk.CTkFont(family=T.FONT_FAMILY, size=14, weight="bold"),
        ).pack(side="left")

        info = ctk.CTkFrame(inner, fg_color="transparent")
        info.pack(side="left", padx=10)
        ctk.CTkLabel(info, text=self.user["username"],
                     font=ctk.CTkFont(family=T.FONT_FAMILY, size=13, weight="bold"),
                     text_color=T.TEXT, anchor="w").pack(anchor="w")
        role = "Администратор" if self.user["role"] == "admin" else "Пользователь"
        ctk.CTkLabel(info, text=role, font=T.small(),
                     text_color=T.TEXT_MUTED, anchor="w").pack(anchor="w")

        ctk.CTkButton(
            bottom, text="Выйти", height=36, corner_radius=T.R_SM,
            fg_color="transparent", hover_color=T.PRIMARY_SOFT,
            border_width=1, border_color=T.BORDER, text_color=T.TEXT,
            font=T.body(), command=self.logout,
        ).pack(fill="x", pady=(10, 0))

    def _build_content(self):
        self.content = ctk.CTkFrame(self, fg_color=T.BG_APP, corner_radius=0)
        self.content.grid(row=0, column=1, sticky="nsew")

        is_admin = self.user["role"] == "admin"

        self.pages = {
            "books":   BooksView(self.content, is_admin=is_admin),
            "authors": AuthorsView(self.content, is_admin=is_admin),
            "genres":  GenresView(self.content, is_admin=is_admin),
        }
        for p in self.pages.values():
            p.place(relx=0, rely=0, relwidth=1, relheight=1)

    def show_page(self, key):
        page = self.pages[key]
        page.lift()

        for k, (btn, accent) in self.nav_buttons.items():
            if k == key:
                btn.configure(fg_color=T.PRIMARY_SOFT, text_color=T.PRIMARY)
                accent.configure(fg_color=T.PRIMARY)
            else:
                btn.configure(fg_color="transparent", text_color=T.TEXT)
                accent.configure(fg_color="transparent")

        if hasattr(page, "refresh"):
            page.refresh()

    def logout(self):
        self.withdraw()
        if self.on_logout:
            self.on_logout()


def user_initials(name):
    return "".join(p[0].upper() for p in name.split()[:2]) or name[:2].upper()