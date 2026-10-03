import csv
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
from pathlib import Path
from datetime import datetime

from theme import Theme as T
from ui.widgets import (
    Card, PageTitle, PrimaryButton, GhostButton, DangerButton,
    SearchEntry, Select, Badge, Divider,
)
from models import (
    get_books, get_book, add_book, update_book, delete_book,
    get_genres, get_authors, get_book_author_ids,
)


class BookCard(Card):
    def __init__(self, master, book, on_edit, on_delete, is_admin=True):
        super().__init__(master)
        self.book = book

        body = self.body()
        body.grid_columnconfigure(2, weight=1)

        self._cover_img = self._cover(book["cover_path"])
        ctk.CTkLabel(body, image=self._cover_img, text="").grid(
            row=0, column=0, rowspan=3, padx=(0, 12), sticky="n"
        )

        ctk.CTkLabel(body, text=book["title"], font=T.h3(),
                     text_color=T.TEXT, anchor="w", justify="left",
                     wraplength=280).grid(row=0, column=2, sticky="ew")

        meta = ctk.CTkFrame(body, fg_color="transparent")
        meta.grid(row=1, column=2, sticky="w", pady=(4, 0))
        ctk.CTkLabel(meta, text=book["authors"] or "—", font=T.small(),
                     text_color=T.TEXT_MUTED).pack(side="left")
        if book["genre_name"]:
            Badge(meta, book["genre_name"], T.PRIMARY).pack(side="left", padx=(8, 0))

        bottom = ctk.CTkFrame(body, fg_color="transparent")
        bottom.grid(row=2, column=2, sticky="ew", pady=(8, 0))
        ctk.CTkLabel(bottom, text=f"{book['price']} руб.",
                     font=ctk.CTkFont(family=T.FONT_FAMILY, size=15, weight="bold"),
                     text_color=T.SUCCESS).pack(side="left")
        stock_color = T.SUCCESS if book["stock"] > 0 else T.DANGER
        stock_text = f"В наличии: {book['stock']}" if book["stock"] > 0 else "Нет"
        Badge(bottom, stock_text, stock_color).pack(side="left", padx=8)

        if is_admin:
            actions = ctk.CTkFrame(body, fg_color="transparent")
            actions.grid(row=0, column=3, rowspan=3, padx=(10, 0), sticky="n")
            GhostButton(actions, text="Изм.", width=52, height=32,
                        command=lambda: on_edit(book["id"])).pack(pady=(0, 6))
            DangerButton(actions, text="Удал.", width=56, height=32,
                         command=lambda: on_delete(book["id"])).pack()

    def _cover(self, path):
        size = (92, 134)
        if path and Path(path).exists():
            try:
                img = Image.open(path).resize(size, Image.LANCZOS)
                return ctk.CTkImage(light_image=img, dark_image=img, size=size)
            except Exception:
                pass
        img = Image.new("RGB", size, (60, 66, 80))
        return ctk.CTkImage(light_image=img, dark_image=img, size=size)


class BookForm(ctk.CTkToplevel):
    def __init__(self, master, book_id=None, on_save=None):
        super().__init__(master)
        self.book_id = book_id
        self.on_save = on_save
        self.cover_src = None

        self.title("Редактирование книги" if book_id else "Новая книга")
        self.geometry("580x760")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()
        self.configure(fg_color=T.BG_APP)

        self.genres = get_genres()
        self.authors = get_authors()
        self.author_vars = {}

        container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=12, pady=12)

        self._section(container, "Основное")
        self.title_e = self._field(container, "Название *", "Введите название")
        self.desc_e = self._field_area(container, "Описание", height=90)

        row = ctk.CTkFrame(container, fg_color="transparent")
        row.pack(fill="x", pady=(8, 0))
        row.grid_columnconfigure((0, 1, 2), weight=1, uniform="x")
        self.price_e = self._mini(row, "Цена, руб.", 0, "0")
        self.year_e = self._mini(row, "Год", 1, "2024")
        self.stock_e = self._mini(row, "Кол-во", 2, "0")

        self._section(container, "Классификация")
        ctk.CTkLabel(container, text="Жанр", font=T.small(),
                     text_color=T.TEXT_MUTED).pack(anchor="w")
        genre_names = [g["name"] for g in self.genres] or ["—"]
        self.genre_var = ctk.StringVar(value=genre_names[0])
        Select(container, values=genre_names,
               variable=self.genre_var).pack(fill="x", pady=(4, 12))

        ctk.CTkLabel(container, text="Авторы", font=T.small(),
                     text_color=T.TEXT_MUTED).pack(anchor="w")
        authors_frame = ctk.CTkScrollableFrame(container, height=120,
                                               fg_color=T.BG_ELEVATED,
                                               corner_radius=T.R_SM)
        authors_frame.pack(fill="x", pady=(4, 12))
        if not self.authors:
            ctk.CTkLabel(authors_frame,
                         text="Сначала добавьте авторов на странице Авторы",
                         text_color=T.WARNING).pack(anchor="w", pady=4)
        for a in self.authors:
            var = ctk.BooleanVar()
            ctk.CTkCheckBox(authors_frame, text=a["full_name"], variable=var,
                            font=T.body(), text_color=T.TEXT,
                            fg_color=T.PRIMARY, hover_color=T.PRIMARY_HOV
                            ).pack(anchor="w", pady=3)
            self.author_vars[a["id"]] = var

        self._section(container, "Обложка")
        cover_row = ctk.CTkFrame(container, fg_color="transparent")
        cover_row.pack(fill="x")
        GhostButton(cover_row, text="Выбрать файл",
                    command=self._pick_cover).pack(side="left")
        self.cover_label = ctk.CTkLabel(cover_row, text="файл не выбран",
                                        font=T.small(), text_color=T.TEXT_FAINT)
        self.cover_label.pack(side="left", padx=12)

        bottom = ctk.CTkFrame(self, fg_color=T.BG_SURFACE, corner_radius=0, height=64)
        bottom.pack(fill="x", side="bottom")
        bottom.pack_propagate(False)
        PrimaryButton(bottom, text="Сохранить", width=170,
                      command=self._save).pack(side="right", padx=16, pady=13)
        GhostButton(bottom, text="Отмена", width=110,
                    command=self.destroy).pack(side="right", pady=13)

        if book_id:
            self._load()

    def _section(self, parent, text):
        ctk.CTkLabel(parent, text=text, font=T.h3(),
                     text_color=T.TEXT).pack(anchor="w", pady=(14, 6))
        Divider(parent).pack(fill="x", pady=(0, 10))

    def _field(self, parent, label, placeholder=""):
        ctk.CTkLabel(parent, text=label, font=T.small(),
                     text_color=T.TEXT_MUTED).pack(anchor="w")
        e = ctk.CTkEntry(parent, height=40, corner_radius=T.R_SM,
                         fg_color=T.BG_ELEVATED, border_color=T.BORDER,
                         placeholder_text=placeholder, font=T.body())
        e.pack(fill="x", pady=(4, 8))
        return e

    def _field_area(self, parent, label, height=90):
        ctk.CTkLabel(parent, text=label, font=T.small(),
                     text_color=T.TEXT_MUTED).pack(anchor="w")
        t = ctk.CTkTextbox(parent, height=height, corner_radius=T.R_SM,
                           fg_color=T.BG_ELEVATED, border_color=T.BORDER,
                           border_width=1, font=T.body())
        t.pack(fill="x", pady=(4, 8))
        return t

    def _mini(self, parent, label, col, placeholder):
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.grid(row=0, column=col, padx=4, sticky="ew")
        ctk.CTkLabel(f, text=label, font=T.small(),
                     text_color=T.TEXT_MUTED).pack(anchor="w")
        e = ctk.CTkEntry(f, height=40, corner_radius=T.R_SM,
                         fg_color=T.BG_ELEVATED, border_color=T.BORDER,
                         placeholder_text=placeholder, font=T.body())
        e.pack(fill="x", pady=(4, 0))
        return e

    def _pick_cover(self):
        path = filedialog.askopenfilename(
            title="Выберите обложку",
            filetypes=[("Изображения", "*.png *.jpg *.jpeg *.bmp *.webp")])
        if path:
            self.cover_src = path
            self.cover_label.configure(text=Path(path).name, text_color=T.SUCCESS)

    def _load(self):
        b = get_book(self.book_id)
        self.title_e.insert(0, b["title"])
        self.desc_e.insert("1.0", b["description"] or "")
        self.price_e.insert(0, str(b["price"] or 0))
        self.year_e.insert(0, str(b["year"] or ""))
        self.stock_e.insert(0, str(b["stock"] or 0))
        for g in self.genres:
            if g["id"] == b["genre_id"]:
                self.genre_var.set(g["name"])
                break
        for a_id in get_book_author_ids(self.book_id):
            if a_id in self.author_vars:
                self.author_vars[a_id].set(True)
        if b["cover_path"]:
            self.cover_label.configure(text=Path(b["cover_path"]).name)

    def _save(self):
        try:
            title = self.title_e.get().strip()
            if not title:
                messagebox.showerror("Ошибка", "Введите название книги")
                return
            price = float(self.price_e.get().replace(",", ".") or 0)
            year_raw = self.year_e.get().strip()
            year = int(year_raw) if year_raw else None
            stock = int(self.stock_e.get() or 0)
            genre_id = None
            for g in self.genres:
                if g["name"] == self.genre_var.get():
                    genre_id = g["id"]
                    break
            author_ids = [aid for aid, var in self.author_vars.items() if var.get()]
            desc = self.desc_e.get("1.0", "end").strip()

            if self.book_id:
                update_book(self.book_id, title, desc, price, year,
                            genre_id, stock, self.cover_src, author_ids)
            else:
                add_book(title, desc, price, year, genre_id, stock,
                         self.cover_src, author_ids)
            if self.on_save:
                self.on_save()
            self.destroy()
        except ValueError:
            messagebox.showerror("Ошибка", "Проверьте числа: цена, год, количество")


class BooksView(ctk.CTkFrame):
    def __init__(self, master, is_admin=True):
        super().__init__(master, fg_color=T.BG_APP)
        self.is_admin = is_admin

        wrapper = ctk.CTkFrame(self, fg_color="transparent")
        wrapper.pack(fill="both", expand=True, padx=24, pady=20)

        title_row = PageTitle(wrapper, "Каталог книг",
                              "Управление ассортиментом магазина")
        title_row.pack(fill="x", pady=(0, 16))

        GhostButton(title_row.actions, text="Экспорт CSV", width=140,
                    command=self.export_csv).pack(side="right", padx=(8, 0))
        GhostButton(title_row.actions, text="Обновить", width=110,
                    command=self.refresh).pack(side="right", padx=(8, 0))
        if is_admin:
            PrimaryButton(title_row.actions, text="Добавить книгу", width=170,
                          command=self.add_book).pack(side="right")

        filters = Card(wrapper)
        filters.pack(fill="x", pady=(0, 16))
        fb = filters.body()

        self.search_e = SearchEntry(fb, width=320,
                                    placeholder_text="Поиск по названию или описанию")
        self.search_e.pack(side="left")
        self.search_e.bind("<KeyRelease>", lambda e: self.refresh())

        ctk.CTkLabel(fb, text="Сортировка", font=T.small(),
                     text_color=T.TEXT_MUTED).pack(side="left", padx=(16, 6))
        self.sort_var = ctk.StringVar(value="title")
        Select(fb, values=["title", "year", "price", "stock", "created_at"],
               variable=self.sort_var, width=140,
               command=lambda _: self.refresh()).pack(side="left")

        self.order_var = ctk.StringVar(value="ASC")
        Select(fb, values=["ASC", "DESC"], variable=self.order_var,
               width=100, command=lambda _: self.refresh()).pack(side="left", padx=6)

        ctk.CTkLabel(fb, text="Жанр", font=T.small(),
                     text_color=T.TEXT_MUTED).pack(side="left", padx=(16, 6))
        self.genre_filter = ctk.StringVar(value="Все жанры")
        self.genre_menu = Select(fb, values=["Все жанры"],
                                 variable=self.genre_filter, width=170,
                                 command=lambda _: self.refresh())
        self.genre_menu.pack(side="left")

        self.stats_label = ctk.CTkLabel(wrapper, text="", font=T.small(),
                                        text_color=T.TEXT_MUTED)
        self.stats_label.pack(anchor="w", pady=(0, 8))

        self.grid_frame = ctk.CTkScrollableFrame(wrapper, fg_color="transparent")
        self.grid_frame.pack(fill="both", expand=True)
        self.grid_frame.grid_columnconfigure((0, 1), weight=1, uniform="bookcol")

        self.genres = {}
        self._reload_filters()
        self.refresh()

    def _reload_filters(self):
        genres = get_genres()
        self.genres = {g["name"]: g["id"] for g in genres}
        self.genre_menu.configure(values=["Все жанры"] + list(self.genres.keys()))

    def refresh(self):
        for w in self.grid_frame.winfo_children():
            w.destroy()

        genre_id = self.genres.get(self.genre_filter.get())
        books = get_books(
            query=self.search_e.get(),
            genre_id=genre_id,
            sort_by=self.sort_var.get(),
            order=self.order_var.get(),
        )

        self.stats_label.configure(text=f"Найдено книг: {len(books)}")

        if not books:
            empty = ctk.CTkFrame(self.grid_frame, fg_color="transparent")
            empty.grid(row=0, column=0, columnspan=2, pady=80)
            ctk.CTkLabel(empty, text="Ничего не найдено",
                         font=T.h3(), text_color=T.TEXT).pack()
            ctk.CTkLabel(empty, text="Попробуйте изменить фильтры или добавьте книгу",
                         font=T.body(), text_color=T.TEXT_MUTED).pack(pady=(4, 0))
            return

        for i, b in enumerate(books):
            row, col = divmod(i, 2)
            card = BookCard(self.grid_frame, b, self.edit_book,
                            self.remove_book, is_admin=self.is_admin)
            card.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")

    def add_book(self):
        self._reload_filters()
        BookForm(self.winfo_toplevel(), on_save=self.refresh)

    def edit_book(self, book_id):
        self._reload_filters()
        BookForm(self.winfo_toplevel(), book_id=book_id, on_save=self.refresh)

    def remove_book(self, book_id):
        if messagebox.askyesno("Удаление", "Удалить эту книгу?"):
            delete_book(book_id)
            self.refresh()

    def export_csv(self):
        genre_id = self.genres.get(self.genre_filter.get())
        books = get_books(
            query=self.search_e.get(),
            genre_id=genre_id,
            sort_by=self.sort_var.get(),
            order=self.order_var.get(),
        )
        if not books:
            messagebox.showinfo("Экспорт", "Нет данных для экспорта")
            return

        default_name = f"books_{datetime.now():%Y%m%d_%H%M%S}.csv"
        path = filedialog.asksaveasfilename(
            title="Сохранить CSV",
            defaultextension=".csv",
            initialfile=default_name,
            filetypes=[("CSV", "*.csv"), ("Все файлы", "*.*")],
        )
        if not path:
            return

        try:
            with open(path, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f, delimiter=";")
                writer.writerow([
                    "ID", "Название", "Авторы", "Жанр", "Год",
                    "Цена, руб.", "Наличие, шт.", "Описание",
                ])
                for b in books:
                    writer.writerow([
                        b["id"],
                        b["title"],
                        b["authors"] or "",
                        b["genre_name"] or "",
                        b["year"] or "",
                        b["price"],
                        b["stock"],
                        (b["description"] or "").replace("\n", " "),
                    ])
            messagebox.showinfo("Экспорт", f"Сохранено: {Path(path).name}")
        except Exception as e:
            messagebox.showerror("Ошибка экспорта", str(e))