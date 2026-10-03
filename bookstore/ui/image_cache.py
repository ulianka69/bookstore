from pathlib import Path
from PIL import Image
import customtkinter as ctk


_cache: dict[tuple[str, int, int], ctk.CTkImage] = {}

PLACEHOLDER_COLOR = (60, 66, 80)


def get_cover(path: str | None, size: tuple[int, int] = (80, 116)):
    key = (str(path), size[0], size[1])
    if key in _cache:
        return _cache[key]

    img = _load_or_placeholder(path, size)
    ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=size)
    _cache[key] = ctk_img
    return ctk_img


def _load_or_placeholder(path: str | None, size: tuple[int, int]) -> Image.Image:
    if path:
        p = Path(path)
        if p.exists():
            try:
                img = Image.open(p).convert("RGB")
                img = _cover_fit(img, size)
                return img
            except Exception:
                pass


    img = Image.new("RGB", size, PLACEHOLDER_COLOR)
    return img


def _cover_fit(img: Image.Image, size: tuple[int, int]) -> Image.Image:
    target_w, target_h = size
    src_w, src_h = img.size
    if src_w == 0 or src_h == 0:
        return Image.new("RGB", size, PLACEHOLDER_COLOR)


    ratio = max(target_w / src_w, target_h / src_h)
    new_w = int(src_w * ratio)
    new_h = int(src_h * ratio)
    img = img.resize((new_w, new_h), Image.LANCZOS)


    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    return img.crop((left, top, left + target_w, top + target_h))


def clear_cache():
    _cache.clear()