import customtkinter as ctk


class Theme:
    BG_APP       = ("#eef0fb", "#0d0b1f")
    BG_SURFACE   = ("#ffffff", "#161230")
    BG_ELEVATED  = ("#e6e8fa", "#1e1a3e")
    BG_HOVER     = ("#d9ddf5", "#2a2452")
    BG_SIDEBAR   = ("#f5f4fc", "#120f28")

    BORDER       = ("#dcdff2", "#2a2548")
    BORDER_SOFT  = ("#e8eaf7", "#221d42")

    TEXT         = ("#1a1638", "#f1eefc")
    TEXT_MUTED   = ("#645e88", "#a8a2c9")
    TEXT_FAINT   = ("#9b96b8", "#6e689a")

    PRIMARY       = "#6d5efc"
    PRIMARY_HOV   = "#5a4be0"
    PRIMARY_SOFT  = ("#e9e6ff", "#251f52")
    PRIMARY_DARK  = "#4b3fc7"

    SECONDARY     = "#8b5cf6"
    SECONDARY_HOV = "#7c4ae8"
    ACCENT        = "#a78bfa"

    SUCCESS       = "#10b981"
    WARNING       = "#f59e0b"
    DANGER        = "#ef4444"
    DANGER_HOV    = "#dc2626"
    INFO          = "#3b82f6"

    R_SM = 10
    R_MD = 14
    R_LG = 20

    FONT_FAMILY = "Segoe UI"

    @classmethod
    def h1(cls):   return ctk.CTkFont(family=cls.FONT_FAMILY, size=28, weight="bold")
    @classmethod
    def h2(cls):   return ctk.CTkFont(family=cls.FONT_FAMILY, size=22, weight="bold")
    @classmethod
    def h3(cls):   return ctk.CTkFont(family=cls.FONT_FAMILY, size=16, weight="bold")
    @classmethod
    def body(cls): return ctk.CTkFont(family=cls.FONT_FAMILY, size=13)
    @classmethod
    def small(cls):return ctk.CTkFont(family=cls.FONT_FAMILY, size=12)
    @classmethod
    def badge(cls):return ctk.CTkFont(family=cls.FONT_FAMILY, size=11, weight="bold")
    @classmethod
    def big(cls):  return ctk.CTkFont(family=cls.FONT_FAMILY, size=36, weight="bold")


def apply_theme():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")