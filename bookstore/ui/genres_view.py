import customtkinter as ctk
from tkinter import messagebox

from theme import Theme as T
from ui.widgets import (
    Card, PageTitle, PrimaryButton, DangerButton, InputDialog, Badge,
)
from models import get_genres, add_genre, delete_genre


class GenresView(ctk.CTkFrame):
    def __init__(self, master, is_admin=True):
        super().__init__(master, fg_color=T.BG_APP)
        self.is_admin = is_admin

        wrapper = ctk.CTkFrame(self, fg_color="transparent")
        wrapper.pack(fill="both", expand=True, padx=24, pady=20)

        title = PageTitle(wrapper, "Жанры", "Категории книг магазина")
        title.pack(fill="x", pady=(0, 16))
        if is_admin:
            PrimaryButton(title.actions, text="Добавить жанр", width=180,
                          command=self.add).pack(side="right")

        self.list_frame = ctk.CTkScrollableFrame(wrapper, fg_color="transparent")
        self.list_frame.pack(fill="both", expand=True)
        self.refresh()

    def refresh(self):
        for w in self.list_frame.winfo_children():
            w.destroy()

        genres = get_genres()
        if not genres:
            empty = ctk.CTkFrame(self.list_frame, fg_color="transparent")
            empty.pack(pady=80)
            ctk.CTkLabel(empty, text="Пока нет жанров",
                         font=T.h3(), text_color=T.TEXT).pack()
            ctk.CTkLabel(empty, text="Нажмите «Добавить жанр», чтобы начать",
                         font=T.body(), text_color=T.TEXT_MUTED).pack(pady=(4, 0))
            return

        for g in genres:
            card = Card(self.list_frame)
            card.pack(fill="x", pady=6)
            body = card.body()

            Badge(body, g["name"], T.PRIMARY).pack(side="left")
            ctk.CTkLabel(body, text=f"ID: {g['id']}", font=T.small(),
                         text_color=T.TEXT_FAINT).pack(side="left", padx=12)

            if self.is_admin:
                DangerButton(body, text="Удалить", width=110, height=34,
                             command=lambda i=g["id"]: self.remove(i)).pack(side="right")

    def add(self):
        InputDialog(self.winfo_toplevel(),
                    title="Новый жанр",
                    label="Название жанра",
                    placeholder="Например: Приключения",
                    on_submit=self._do_add)

    def _do_add(self, name):
        try:
            add_genre(name)
            self.refresh()
        except Exception:
            messagebox.showerror("Ошибка", "Такой жанр уже есть")

    def remove(self, gid):
        if messagebox.askyesno("Удаление", "Удалить жанр?"):
            delete_genre(gid)
            self.refresh()