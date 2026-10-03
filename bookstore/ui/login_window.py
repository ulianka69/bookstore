import customtkinter as ctk
from theme import Theme as T, apply_theme
from ui.widgets import PrimaryButton, Card
from auth import login, register


class LoginWindow(ctk.CTkToplevel):
    def __init__(self, master, on_success):
        super().__init__(master)
        self.on_success = on_success
        self.master_app = master

        apply_theme()
        self.title("BookStore - вход")
        self.geometry("1000x620")
        self.minsize(900, 560)

        self.grid_columnconfigure(0, weight=5)
        self.grid_columnconfigure(1, weight=4)
        self.grid_rowconfigure(0, weight=1)

        self._build_left()
        self._build_right()

    def _build_left(self):
        left = ctk.CTkFrame(self, corner_radius=0, fg_color=("#e8e6fb", "#151235"))
        left.grid(row=0, column=0, sticky="nsew")

        inner = ctk.CTkFrame(left, fg_color="transparent")
        inner.place(relx=0.5, rely=0.5, anchor="center")

        mark = ctk.CTkFrame(inner, width=96, height=96,
                            corner_radius=28, fg_color=T.PRIMARY)
        mark.pack()
        mark.pack_propagate(False)
        ctk.CTkLabel(mark, text="B",
                     font=ctk.CTkFont(family=T.FONT_FAMILY, size=48, weight="bold"),
                     text_color="#ffffff").place(relx=0.5, rely=0.5, anchor="center")

        brand_row = ctk.CTkFrame(inner, fg_color="transparent")
        brand_row.pack(pady=(22, 4))
        ctk.CTkLabel(brand_row, text="Book",
                     font=ctk.CTkFont(family=T.FONT_FAMILY, size=40, weight="bold"),
                     text_color=T.PRIMARY).pack(side="left")
        ctk.CTkLabel(brand_row, text="Store",
                     font=ctk.CTkFont(family=T.FONT_FAMILY, size=40, weight="bold"),
                     text_color=T.TEXT).pack(side="left")

        ctk.CTkLabel(inner, text="Учёт книг, авторов и жанров",
                     font=T.body(), text_color=T.TEXT_MUTED).pack()

        feats = ctk.CTkFrame(inner, fg_color="transparent")
        feats.pack(pady=28)
        for text in [
            "Каталог с обложками",
            "Поиск и сортировка",
            "Роли администратора",
        ]:
            row = ctk.CTkFrame(feats, fg_color="transparent")
            row.pack(anchor="w", pady=4)
            ctk.CTkFrame(row, width=6, height=6, corner_radius=3,
                         fg_color=T.PRIMARY).pack(side="left", padx=(0, 10))
            ctk.CTkLabel(row, text=text, font=T.body(),
                         text_color=T.TEXT_MUTED).pack(side="left")

    def _build_right(self):
        right = ctk.CTkFrame(self, corner_radius=0, fg_color=T.BG_APP)
        right.grid(row=0, column=1, sticky="nsew")

        card = Card(right, width=380, height=460)
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.pack_propagate(False)

        body = card.body()
        ctk.CTkLabel(body, text="Добро пожаловать",
                     font=T.h2(), text_color=T.TEXT).pack(anchor="w")
        ctk.CTkLabel(body, text="Войдите или создайте аккаунт",
                     font=T.small(), text_color=T.TEXT_MUTED).pack(anchor="w", pady=(2, 18))

        self.tab = ctk.CTkTabview(
            body, corner_radius=T.R_MD,
            fg_color=T.BG_ELEVATED,
            segmented_button_fg_color=T.BG_ELEVATED,
            segmented_button_selected_color=T.PRIMARY,
            segmented_button_selected_hover_color=T.PRIMARY_HOV,
            segmented_button_unselected_color=T.BG_ELEVATED,
            segmented_button_unselected_hover_color=T.BG_HOVER,
            text_color=T.TEXT,
        )
        self.tab.pack(fill="both", expand=True)

        self.tab.add("Вход")
        self.tab.add("Регистрация")

        f1 = self.tab.tab("Вход")
        ctk.CTkLabel(f1, text="Логин", font=T.small(),
                     text_color=T.TEXT_MUTED).pack(anchor="w", pady=(6, 2))
        self.login_user = ctk.CTkEntry(f1, height=40, corner_radius=T.R_SM,
                                       fg_color=T.BG_SURFACE, border_color=T.BORDER,
                                       font=T.body())
        self.login_user.pack(fill="x")

        ctk.CTkLabel(f1, text="Пароль", font=T.small(),
                     text_color=T.TEXT_MUTED).pack(anchor="w", pady=(10, 2))
        self.login_pass = ctk.CTkEntry(f1, height=40, corner_radius=T.R_SM,
                                       fg_color=T.BG_SURFACE, border_color=T.BORDER,
                                       show="*", font=T.body())
        self.login_pass.pack(fill="x")

        PrimaryButton(f1, text="Войти", command=self._do_login).pack(
            fill="x", pady=(18, 4))
        self.login_msg = ctk.CTkLabel(f1, text="", font=T.small(),
                                      text_color=T.DANGER)
        self.login_msg.pack()

        f2 = self.tab.tab("Регистрация")
        ctk.CTkLabel(f2, text="Логин", font=T.small(),
                     text_color=T.TEXT_MUTED).pack(anchor="w", pady=(6, 2))
        self.reg_user = ctk.CTkEntry(f2, height=40, corner_radius=T.R_SM,
                                     fg_color=T.BG_SURFACE, border_color=T.BORDER,
                                     font=T.body())
        self.reg_user.pack(fill="x")

        ctk.CTkLabel(f2, text="Пароль", font=T.small(),
                     text_color=T.TEXT_MUTED).pack(anchor="w", pady=(10, 2))
        self.reg_pass = ctk.CTkEntry(f2, height=40, corner_radius=T.R_SM,
                                     fg_color=T.BG_SURFACE, border_color=T.BORDER,
                                     show="*", font=T.body())
        self.reg_pass.pack(fill="x")

        ctk.CTkLabel(f2, text="Повтор пароля", font=T.small(),
                     text_color=T.TEXT_MUTED).pack(anchor="w", pady=(10, 2))
        self.reg_pass2 = ctk.CTkEntry(f2, height=40, corner_radius=T.R_SM,
                                      fg_color=T.BG_SURFACE, border_color=T.BORDER,
                                      show="*", font=T.body())
        self.reg_pass2.pack(fill="x")

        PrimaryButton(f2, text="Создать аккаунт",
                      command=self._do_register).pack(fill="x", pady=(18, 4))
        self.reg_msg = ctk.CTkLabel(f2, text="", font=T.small(),
                                    text_color=T.DANGER)
        self.reg_msg.pack()

    def _do_login(self):
        user = login(self.login_user.get(), self.login_pass.get())
        if user:
            self.withdraw()
            self.on_success(user)
        else:
            self.login_msg.configure(text="Неверный логин или пароль")

    def _do_register(self):
        u, p1, p2 = self.reg_user.get(), self.reg_pass.get(), self.reg_pass2.get()
        if p1 != p2:
            self.reg_msg.configure(text="Пароли не совпадают", text_color=T.DANGER)
            return
        ok, msg = register(u, p1)
        self.reg_msg.configure(text=msg, text_color=T.SUCCESS if ok else T.DANGER)
        if ok:
            self.tab.set("Вход")
            self.login_user.delete(0, "end")
            self.login_user.insert(0, u)

    def destroy(self):
        try:
            self.master_app.destroy()
        except Exception:
            pass