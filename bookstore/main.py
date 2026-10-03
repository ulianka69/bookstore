import customtkinter as ctk
from database import init_db
from ui.login_window import LoginWindow
from ui.main_window import MainWindow


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.withdraw()
        self.login_window = None
        self.main_window = None

    def start(self):
        init_db()
        self.show_login()

    def show_login(self):
        if self.main_window is not None:
            try:
                self.main_window.destroy()
            except Exception:
                pass
            self.main_window = None

        if self.login_window is None or not self.login_window.winfo_exists():
            self.login_window = LoginWindow(self, on_success=self.show_main)
        else:
            self.login_window.deiconify()
            self.login_window.lift()

    def show_main(self, user):
        if self.login_window is not None:
            try:
                self.login_window.withdraw()
            except Exception:
                pass

        self.main_window = MainWindow(self, user, on_logout=self.show_login)


def main():
    app = App()
    app.start()
    app.mainloop()


if __name__ == "__main__":
    main()