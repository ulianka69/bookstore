import customtkinter as ctk
from tkinter import messagebox, filedialog
from pathlib import Path
from PIL import Image

from theme import Theme as T
from ui.widgets import (
    Card, PageTitle, PrimaryButton, GhostButton, DangerButton, InputDialog,
)
from models import get_authors, add_author, update_author, delete_author


class AuthorsView(ctk.CTkFrame):
    def __init__(self, master, is_admin=True):
        super().__init__(master, fg_color=T.BG_APP)
        self.is_admin = is_admin

        wrapper = ctk.CTkFrame(self, fg_color="transparent")
        wrapper.pack(fill="both", expand=True, padx=24, pady=20)

        title = PageTitle(wrapper, "Авторы", "Список писателей магазина")
        title.pack(fill="x", pady=(0, 16))

        if is_admin:
            PrimaryButton(title.actions, text="Добавить автора", width=180,
                          command=self.add).pack(side="right")

        self.list_frame = ctk.CTkScrollableFrame(wrapper, fg_color="transparent")
        self.list_frame.pack(fill="both", expand=True)

        self.refresh()

    def refresh(self):
        for w in self.list_frame.winfo_children():
            w.destroy()

        authors = get_authors()
        if not authors:
            self._empty_state()
            return

        for a in authors:
            self._author_card(a)

    def _empty_state(self):
        empty = ctk.CTkFrame(self.list_frame, fg_color="transparent")
        empty.pack(pady=80)
        ctk.CTkLabel(empty, text="Пока нет авторов",
                     font=T.h3(), text_color=T.TEXT).pack()
        ctk.CTkLabel(empty, text="Нажмите «Добавить автора», чтобы начать",
                     font=T.body(), text_color=T.TEXT_MUTED).pack(pady=(4, 0))

    def _author_card(self, a):
        card = Card(self.list_frame)
        card.pack(fill="x", pady=6)
        body = card.body()
        body.grid_columnconfigure(1, weight=1)

        initials = "".join(p[0].upper() for p in a["full_name"].split()[:2])
        ctk.CTkLabel(
            body, text=initials or "?", width=48, height=48,
            corner_radius=24, fg_color=T.PRIMARY, text_color="#ffffff",
            font=ctk.CTkFont(family=T.FONT_FAMILY, size=18, weight="bold"),
        ).grid(row=0, column=0, rowspan=2, padx=(0, 14))

        ctk.CTkLabel(body, text=a["full_name"], font=T.h3(),
                     text_color=T.TEXT, anchor="w").grid(
            row=0, column=1, sticky="ew")

        ctk.CTkLabel(body, text=f"ID: {a['id']}", font=T.small(),
                     text_color=T.TEXT_FAINT, anchor="w").grid(
            row=1, column=1, sticky="ew")

        if self.is_admin:
            actions = ctk.CTkFrame(body, fg_color="transparent")
            actions.grid(row=0, column=2, rowspan=2, padx=(10, 0))
            GhostButton(actions, text="Изм.", width=60, height=34,
                        command=lambda i=a["id"], n=a["full_name"]: self.rename(i, n)
                        ).pack(side="left", padx=(0, 6))
            DangerButton(actions, text="Удал.", width=64, height=34,
                         command=lambda i=a["id"]: self.remove(i)).pack(side="left")

    def add(self):
        InputDialog(self.winfo_toplevel(),
                    title="Новый автор",
                    label="ФИО автора",
                    placeholder="Например: Лев Толстой",
                    on_submit=self._do_add)

    def _do_add(self, name):
        add_author(name)
        self.refresh()

    def rename(self, aid, current):
        InputDialog(self.winfo_toplevel(),
                    title="Переименовать автора",
                    label="Новое имя",
                    initial=current,
                    on_submit=lambda n: self._do_rename(aid, n))

    def _do_rename(self, aid, name):
        update_author(aid, name)
        self.refresh()

    def remove(self, aid):
        if messagebox.askyesno("Удаление", "Удалить автора?"):
            delete_author(aid)
            self.refresh()