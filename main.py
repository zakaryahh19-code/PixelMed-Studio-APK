# ================================================================
# PixelMed Studio
# Responsive mobile + desktop editor
# Icons are loaded from: image/
# ================================================================

import os
import json
import math
from functools import lru_cache
from datetime import datetime

from kivy.app import App
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line
from kivy.graphics.texture import Texture
from kivy.metrics import dp, sp
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image as KivyImage
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider
from kivy.uix.stencilview import StencilView
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex, get_hex_from_color, platform

from PIL import Image as PILImage


# ================================================================
# Arabic
# ================================================================

try:
    import arabic_reshaper

    try:
        from bidi import get_display
    except ImportError:
        from bidi.algorithm import get_display

    HAS_AR = True

except Exception:
    HAS_AR = False


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def resource_path(rel):
    return os.path.join(BASE_DIR, rel)


# ================================================================
# ICONS
# ================================================================

ICON_FILES = {
    "eraser": "eraser.png",
    "drop": "drop.png",
    "watering": "watering.png",
    "animation": "animation.png",
    "palette": "palette.png",
    "menu": "menu.png",
    "delete": "delete.png",
    "settings": "settings.png",
    "upload": "upload.png",
    "projects": "projects.png",
    "move": "move.png",
    "image": "image.png",
    "gif": "gif.png",
    "pencil": "pencil.png",
}


def icon_path(name):
    filename = ICON_FILES.get(name, "")

    if not filename:
        return ""

    path = resource_path(
        os.path.join("image", filename)
    )

    if os.path.exists(path):
        return path

    return ""


# ================================================================
# FONT
# ================================================================

_REG = resource_path("Cairo-Regular.ttf")
_BOLD = resource_path("Cairo-Bold.ttf")

if os.path.exists(_REG):

    LabelBase.register(
        name="Roboto",
        fn_regular=_REG,
        fn_bold=_BOLD if os.path.exists(_BOLD) else _REG
    )


if platform not in ("android", "ios"):
    Window.size = (900, 450)


def shape_text(text, lang):

    if lang == "ar" and HAS_AR and text:
        return get_display(
            arabic_reshaper.reshape(text)
        )

    return text


# ================================================================
# TRANSLATIONS
# ================================================================

TRANSLATIONS = {

    "ar": {
        "new_project": "مشروع جديد",
        "previous_projects": "المشاريع السابقة",
        "settings": "الإعدادات",
        "canvas_size": "اختر حجم اللوحة",
        "custom_size": "أو أدخل حجماً مخصصاً:",
        "set": "تطبيق",
        "saved_projects": "المشاريع المحفوظة",
        "back": "رجوع",
        "open": "فتح",
        "delete": "حذف",
        "no_projects": "لا توجد مشاريع محفوظة حالياً.",
        "tools": "الأدوات",
        "colors": "الألوان",
        "custom_color": "لون مخصص",
        "clear_canvas": "مسح اللوحة",
        "export_anim": "تصدير الأنيميشن",
        "play": "تشغيل",
        "pause": "إيقاف",
        "add_frame": "+ إضافة",
        "delete_frame": "حذف",
        "speed": "السرعة",
        "move_left": "< يسار",
        "move_right": "يمين >",
        "pencil": "قلم",
        "eraser": "ممحاة",
        "fill": "تعبئة",
        "eyedropper": "قطارة",
        "undo": "تراجع",
        "redo": "إعادة",
        "reset_view": "إعادة اللوحة لمكانها",
        "home": "الرئيسية",
        "language": "اللغة",
        "theme": "نمط الألوان",
        "font_size": "حجم الخط",
        "theme_light": "أبيض ونادي",
        "theme_dark": "الوضع الليلي",
        "theme_emerald": "الزمرد",
        "theme_gameboy": "جيم بوي",
    },

    "en": {
        "new_project": "New Project",
        "previous_projects": "Previous Projects",
        "settings": "Settings",
        "canvas_size": "Choose Canvas Size",
        "custom_size": "Or enter a custom size:",
        "set": "Set",
        "saved_projects": "Saved Projects",
        "back": "Back",
        "open": "Open",
        "delete": "Delete",
        "no_projects": "No saved projects found.",
        "tools": "Tools",
        "colors": "Colors",
        "custom_color": "Custom Color",
        "clear_canvas": "Clear Canvas",
        "export_anim": "Export Animation",
        "play": "Play",
        "pause": "Pause",
        "add_frame": "+ Add",
        "delete_frame": "Delete",
        "speed": "Speed",
        "move_left": "< Left",
        "move_right": "Right >",
        "pencil": "Pencil",
        "eraser": "Eraser",
        "fill": "Fill",
        "eyedropper": "Picker",
        "undo": "Undo",
        "redo": "Redo",
        "reset_view": "Reset View",
        "home": "Home",
        "language": "Language",
        "theme": "Theme",
        "font_size": "Font Size",
        "theme_light": "White & Platinum",
        "theme_dark": "Dark Night",
        "theme_emerald": "Cyber Emerald",
        "theme_gameboy": "Retro GameBoy",
    },

    "fr": {
        "new_project": "Nouveau Projet",
        "previous_projects": "Projets Précédents",
        "settings": "Paramètres",
        "canvas_size": "Taille de la toile",
        "custom_size": "Ou taille personnalisée:",
        "set": "Définir",
        "saved_projects": "Projets Enregistrés",
        "back": "Retour",
        "open": "Ouvrir",
        "delete": "Supprimer",
        "no_projects": "Aucun projet trouvé.",
        "tools": "Outils",
        "colors": "Couleurs",
        "custom_color": "Couleur perso.",
        "clear_canvas": "Effacer la toile",
        "export_anim": "Exporter l'Animation",
        "play": "Jouer",
        "pause": "Pause",
        "add_frame": "+ Ajout",
        "delete_frame": "Suppr",
        "speed": "Vitesse",
        "move_left": "< Gauche",
        "move_right": "Droite >",
        "pencil": "Crayon",
        "eraser": "Gomme",
        "fill": "Remplir",
        "eyedropper": "Pipette",
        "undo": "Annuler",
        "redo": "Rétablir",
        "reset_view": "Réinitialiser la vue",
        "home": "Accueil",
        "language": "Langue",
        "theme": "Thème",
        "font_size": "Taille de Police",
        "theme_light": "Blanc & Platine",
        "theme_dark": "Nuit Noire",
        "theme_emerald": "Émeraude Cyber",
        "theme_gameboy": "Rétro GameBoy",
    }
}


# ================================================================
# THEMES
# ================================================================

THEMES = {

    "light": {
        "bg": "#F6F4EF",
        "panel": "#EDEAE1",
        "card": "#E2DFD4",
        "text": "#3B3B38",
        "btn_bg": "#3B3B38",
        "btn_text": "#F6F4EF",
        "btn_border": "#D6D1C4",
        "border_width": 0
    },

    "dark": {
        "bg": "#1A1A1A",
        "panel": "#232323",
        "card": "#2D2D2D",
        "text": "#D9D7D2",
        "btn_bg": "#2B2B2B",
        "btn_text": "#D9D7D2",
        "btn_border": "#4A4A4A",
        "border_width": 1
    },

    "emerald": {
        "bg": "#0E211D",
        "panel": "#15302B",
        "card": "#1D3F38",
        "text": "#B7D9A0",
        "btn_bg": "#12A183",
        "btn_text": "#0B1D1A",
        "btn_border": "#2FAE8D",
        "border_width": 1
    },

    "gameboy": {
        "bg": "#8B956D",
        "panel": "#9BBC0F",
        "card": "#8BAC0F",
        "text": "#0F380F",
        "btn_bg": "#306230",
        "btn_text": "#9BBC0F",
        "btn_border": "#0F380F",
        "border_width": 1
    }
}


# ================================================================
# STORAGE
# ================================================================

DATA_DIR = None


def init_storage(path):

    global DATA_DIR

    DATA_DIR = path

    os.makedirs(
        DATA_DIR,
        exist_ok=True
    )


def load_json(name, default):

    path = os.path.join(
        DATA_DIR,
        name
    )

    if os.path.exists(path):

        try:

            with open(
                path,
                "r",
                encoding="utf-8"
            ) as f:

                return json.load(f)

        except Exception:
            pass

    return default


def save_json(name, data):

    with open(
        os.path.join(DATA_DIR, name),
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )


def get_export_dir(app):

    candidates = []

    if platform == "android":

        try:

            from android.storage import (
                primary_external_storage_path
            )

            candidates.append(
                os.path.join(
                    primary_external_storage_path(),
                    "Download",
                    "PixelMed"
                )
            )

        except Exception:
            pass

    else:

        candidates.append(
            os.path.join(
                os.path.expanduser("~"),
                "PixelMed Exports"
            )
        )

    candidates.append(
        os.path.join(
            app.user_data_dir,
            "exports"
        )
    )

    for folder in candidates:

        try:

            os.makedirs(
                folder,
                exist_ok=True
            )

            test = os.path.join(
                folder,
                ".test"
            )

            open(test, "w").close()
            os.remove(test)

            return folder

        except Exception:
            continue

    return app.user_data_dir


# ================================================================
# PIXEL HELPERS
# ================================================================

@lru_cache(maxsize=512)
def hex_to_rgb(h):

    h = h.lstrip("#")

    return (
        int(h[0:2], 16),
        int(h[2:4], 16),
        int(h[4:6], 16)
    )


_CHECKER = {}


def checker_buffer(w, h):

    key = (w, h)

    if key not in _CHECKER:

        buf = bytearray(
            w * h * 4
        )

        for r in range(h):

            y = h - 1 - r

            for c in range(w):

                value = (
                    255
                    if (r + c) % 2 == 0
                    else 242
                )

                i = (
                    y * w + c
                ) * 4

                buf[i] = value
                buf[i + 1] = value
                buf[i + 2] = value
                buf[i + 3] = 255

        _CHECKER[key] = bytes(buf)

    return _CHECKER[key]


def build_buffer(frame, w, h):

    buf = bytearray(
        checker_buffer(w, h)
    )

    for (r, c), color in frame.items():

        if (
            0 <= r < h
            and
            0 <= c < w
        ):

            R, G, B = hex_to_rgb(
                color
            )

            i = (
                (h - 1 - r) * w + c
            ) * 4

            buf[i] = R
            buf[i + 1] = G
            buf[i + 2] = B
            buf[i + 3] = 255

    return bytes(buf)


def make_texture(frame, w, h):

    texture = Texture.create(
        size=(w, h),
        colorfmt="rgba"
    )

    texture.mag_filter = "nearest"
    texture.min_filter = "nearest"

    texture.blit_buffer(
        build_buffer(frame, w, h),
        colorfmt="rgba",
        bufferfmt="ubyte"
    )

    return texture


def line_cells(a, b):

    r0, c0 = a
    r1, c1 = b

    dr = abs(r1 - r0)
    dc = abs(c1 - c0)

    sr = 1 if r0 < r1 else -1
    sc = 1 if c0 < c1 else -1

    err = dc - dr

    points = []

    while True:

        points.append(
            (r0, c0)
        )

        if r0 == r1 and c0 == c1:
            break

        e2 = 2 * err

        if e2 > -dr:

            err -= dr
            c0 += sc

        if e2 < dc:

            err += dc
            r0 += sr

    return points


# ================================================================
# BASIC WIDGETS
# ================================================================

class Panel(BoxLayout):

    def __init__(
        self,
        bg="#FFFFFF",
        radius=0,
        **kwargs
    ):

        super().__init__(**kwargs)

        with self.canvas.before:

            self._color = Color(
                *get_color_from_hex(bg)
            )

            self._rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(radius)]
            )

        self.bind(
            pos=self._sync,
            size=self._sync
        )

    def _sync(self, *args):

        self._rect.pos = self.pos
        self._rect.size = self.size

    def set_bg(self, bg):

        self._color.rgba = (
            get_color_from_hex(bg)
        )


class FlatButton(
    ButtonBehavior,
    Label
):

    def __init__(
        self,
        bg="#333333",
        fg="#FFFFFF",
        border=None,
        radius=8,
        **kwargs
    ):

        super().__init__(**kwargs)

        self.color = get_color_from_hex(
            fg
        )

        self._bg = get_color_from_hex(
            bg
        )

        self._radius = dp(radius)

        with self.canvas.before:

            self._c = Color(
                *self._bg
            )

            self._rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[self._radius]
            )

        with self.canvas.after:

            self._bc = Color(
                *(
                    get_color_from_hex(border)
                    if border
                    else
                    (0, 0, 0, 0)
                )
            )

            self._line = Line(
                rounded_rectangle=(
                    self.x,
                    self.y,
                    self.width,
                    self.height,
                    self._radius
                ),
                width=1
            )

        self.bind(
            pos=self._sync,
            size=self._sync,
            state=self._on_state
        )

    def _sync(self, *args):

        self._rect.pos = self.pos

        self._rect.size = self.size

        self._line.rounded_rectangle = (
            self.x,
            self.y,
            self.width,
            self.height,
            self._radius
        )

    def _on_state(self, *args):

        r, g, b, a = self._bg

        factor = (
            0.8
            if self.state == "down"
            else 1.0
        )

        self._c.rgba = (
            r * factor,
            g * factor,
            b * factor,
            a
        )

    def set_colors(self, bg, fg):

        self._bg = get_color_from_hex(
            bg
        )

        self._on_state()

        self.color = get_color_from_hex(
            fg
        )


# ================================================================
# ICON BUTTON
# ================================================================

class IconButton(
    ButtonBehavior,
    BoxLayout
):

    def __init__(
        self,
        text="",
        icon="",
        bg="#E2DFD4",
        fg="#3B3B38",
        icon_size=28,
        vertical=True,
        radius=8,
        **kwargs
    ):

        self._bg = get_color_from_hex(
            bg
        )

        self._fg = get_color_from_hex(
            fg
        )

        self._radius = dp(radius)

        super().__init__(
            orientation=(
                "vertical"
                if vertical
                else
                "horizontal"
            ),
            spacing=dp(2),
            padding=dp(4),
            **kwargs
        )

        with self.canvas.before:

            self._c = Color(
                *self._bg
            )

            self._rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[self._radius]
            )

        self.bind(
            pos=self._sync,
            size=self._sync,
            state=self._on_state
        )

        self.icon_widget = None

        if icon:

            self.icon_widget = KivyImage(
                source=icon,
                size_hint=(None, None),
                size=(
                    dp(icon_size),
                    dp(icon_size)
                ),
                allow_stretch=True,
                keep_ratio=True
            )

            self.add_widget(
                self.icon_widget
            )

        self.label = Label(
            text=text,
            color=self._fg,
            font_size=sp(10),
            bold=True,
            halign="center",
            valign="middle"
        )

        self.label.bind(
            size=lambda inst, size:
            setattr(
                inst,
                "text_size",
                size
            )
        )

        self.add_widget(
            self.label
        )

    def _sync(self, *args):

        self._rect.pos = self.pos
        self._rect.size = self.size

    def _on_state(self, *args):

        r, g, b, a = self._bg

        factor = (
            0.78
            if self.state == "down"
            else 1.0
        )

        self._c.rgba = (
            r * factor,
            g * factor,
            b * factor,
            a
        )

    def set_colors(self, bg, fg):

        self._bg = get_color_from_hex(
            bg
        )

        self._fg = get_color_from_hex(
            fg
        )

        self._on_state()

        self.label.color = self._fg

    def set_text(self, text):

        self.label.text = text


# ================================================================
# THUMBNAILS
# ================================================================

class ThumbImg(Widget):

    def __init__(
        self,
        texture,
        gw,
        gh,
        **kwargs
    ):

        super().__init__(**kwargs)

        self.gw = gw
        self.gh = gh

        with self.canvas:

            Color(1, 1, 1, 1)

            self.rect = Rectangle(
                texture=texture
            )

        self.bind(
            pos=self._sync,
            size=self._sync
        )

    def _sync(self, *args):

        if self.gw <= 0 or self.gh <= 0:
            return

        scale = min(
            self.width / self.gw,
            self.height / self.gh
        )

        w = self.gw * scale
        h = self.gh * scale

        self.rect.size = (
            w,
            h
        )

        self.rect.pos = (
            self.x + (
                self.width - w
            ) / 2,

            self.y + (
                self.height - h
            ) / 2
        )


class Thumb(
    ButtonBehavior,
    BoxLayout
):

    def __init__(
        self,
        index,
        texture,
        gw,
        gh,
        selected,
        theme,
        **kwargs
    ):

        super().__init__(
            orientation="vertical",
            size_hint=(None, 1),
            width=dp(58),
            padding=dp(2),
            **kwargs
        )

        self.index = index
        self._theme = theme

        with self.canvas.before:

            self._c = Color(
                1, 1, 1, 1
            )

            self._bg = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(6)]
            )

        self.bind(
            pos=self._sync,
            size=self._sync
        )

        self.add_widget(
            ThumbImg(
                texture,
                gw,
                gh
            )
        )

        self.lab = Label(
            text="#%d" % (index + 1),
            size_hint_y=None,
            height=dp(14),
            font_size=sp(9),
            bold=True
        )

        self.add_widget(
            self.lab
        )

        self.set_selected(
            selected
        )

    def _sync(self, *args):

        self._bg.pos = self.pos
        self._bg.size = self.size

    def set_selected(self, selected):

        theme = self._theme

        self._c.rgba = get_color_from_hex(
            theme["btn_bg"]
            if selected
            else
            theme["card"]
        )

        self.lab.color = get_color_from_hex(
            theme["btn_text"]
            if selected
            else
            theme["text"]
        )


# ================================================================
# PIXEL CANVAS
# ================================================================

class PixelCanvas(StencilView):

    MIN_CELL = 2.0
    MAX_CELL = 200.0

    def __init__(
        self,
        editor,
        **kwargs
    ):

        super().__init__(
            **kwargs
        )

        self.ed = editor

        self.gw = 16
        self.gh = 16

        self.cell = 20.0

        self.pan_x = 0
        self.pan_y = 0

        self.tex = None

        self._fitted = False

        self._touches = {}
        self._mode = None
        self._active = False
        self._last = None

        self._g_dist = None
        self._g_mid = (
            0,
            0
        )

        with self.canvas:

            Color(
                1,
                1,
                1,
                1
            )

            self._bg = Rectangle()
            self._img = Rectangle()

        self.bind(
            pos=self.relayout,
            size=self.relayout
        )

    def setup(
        self,
        gw,
        gh
    ):

        self.gw = gw
        self.gh = gh

        self.pan_x = 0
        self.pan_y = 0

        self._fitted = False

        self.refresh()
        self.relayout()

    def refresh(self):

        frame = self.ed.frames_data[
            self.ed.idx
        ]

        self.tex = make_texture(
            frame,
            self.gw,
            self.gh
        )

        self._img.texture = self.tex

        self.canvas.ask_update()

    def set_pixel(
        self,
        r,
        c,
        color
    ):

        frame = self.ed.frames_data[
            self.ed.idx
        ]

        if color:

            R, G, B = hex_to_rgb(
                color
            )

            data = bytes(
                (
                    R,
                    G,
                    B,
                    255
                )
            )

        else:

            value = (
                255
                if (r + c) % 2 == 0
                else 242
            )

            data = bytes(
                (
                    value,
                    value,
                    value,
                    255
                )
            )

        try:

            self.tex.blit_buffer(
                data,
                colorfmt="rgba",
                bufferfmt="ubyte",
                pos=(
                    c,
                    self.gh - 1 - r
                ),
                size=(1, 1)
            )

        except Exception:

            self.refresh()

        self.relayout()

    def fit_view(self):

        if self.width <= 0 or self.height <= 0:
            return

        margin = dp(20)

        available_w = max(
            dp(20),
            self.width - margin
        )

        available_h = max(
            dp(20),
            self.height - margin
        )

        self.cell = min(
            available_w / self.gw,
            available_h / self.gh
        )

        self.cell = max(
            self.MIN_CELL,
            min(
                self.MAX_CELL,
                self.cell
            )
        )

        self.pan_x = (
            self.width
            - self.gw * self.cell
        ) / 2

        self.pan_y = (
            self.height
            - self.gh * self.cell
        ) / 2

        self._fitted = True

        self.relayout()

    def relayout(self, *args):

        self._bg.pos = self.pos
        self._bg.size = self.size

        if not self._fitted:

            Clock.schedule_once(
                lambda dt:
                self.fit_view(),
                0
            )

            return

        w = self.gw * self.cell
        h = self.gh * self.cell

        self._img.size = (
            w,
            h
        )

        self._img.pos = (
            self.x + self.pan_x,
            self.y + self.pan_y
        )

    def cell_at(
        self,
        x,
        y
    ):

        local_x = (
            x - self.x - self.pan_x
        )

        local_y = (
            y - self.y - self.pan_y
        )

        if local_x < 0 or local_y < 0:
            return None

        c = int(
            local_x / self.cell
        )

        r = self.gh - 1 - int(
            local_y / self.cell
        )

        if (
            c < 0
            or c >= self.gw
            or r < 0
            or r >= self.gh
        ):
            return None

        return (
            r,
            c
        )

    def zoom_at(
        self,
        center,
        factor
    ):

        old_cell = self.cell

        new_cell = (
            old_cell * factor
        )

        new_cell = max(
            self.MIN_CELL,
            min(
                self.MAX_CELL,
                new_cell
            )
        )

        if new_cell == old_cell:
            return

        cx, cy = center

        before_x = (
            cx
            - self.x
            - self.pan_x
        )

        before_y = (
            cy
            - self.y
            - self.pan_y
        )

        ratio = (
            new_cell / old_cell
        )

        self.pan_x = (
            self.pan_x
            - before_x * (ratio - 1)
        )

        self.pan_y = (
            self.pan_y
            - before_y * (ratio - 1)
        )

        self.cell = new_cell

        self.relayout()

    def on_touch_down(
        self,
        touch
    ):

        if not self.collide_point(
            *touch.pos
        ):
            return False

        self._touches[touch.uid] = touch

        if len(self._touches) >= 2:

            self._mode = "gesture"

            touches = list(
                self._touches.values()
            )

            a = touches[0]
            b = touches[1]

            self._g_dist = max(
                1.0,
                math.hypot(
                    a.x - b.x,
                    a.y - b.y
                )
            )

            self._g_mid = (
                (a.x + b.x) / 2,
                (a.y + b.y) / 2
            )

            self._end_stroke()

            return True

        if (
            touch.button
            in
            (
                "right",
                "middle"
            )
        ):

            self._mode = "pan"

            self._last = touch.pos

            return True

        self._mode = "draw"

        self._draw_at(
            touch.pos
        )

        return True

    def on_touch_move(
        self,
        touch
    ):

        if touch.uid not in self._touches:
            return False

        self._touches[
            touch.uid
        ] = touch

        if len(self._touches) >= 2:

            touches = list(
                self._touches.values()
            )

            a = touches[0]
            b = touches[1]

            dist = max(
                1.0,
                math.hypot(
                    a.x - b.x,
                    a.y - b.y
                )
            )

            mid = (
                (a.x + b.x) / 2,
                (a.y + b.y) / 2
            )

            if self._g_dist:

                self.zoom_at(
                    mid,
                    dist / self._g_dist
                )

            self._g_dist = dist

            self.pan_x += (
                mid[0]
                - self._g_mid[0]
            )

            self.pan_y += (
                mid[1]
                - self._g_mid[1]
            )

            self._g_mid = mid

            self.relayout()

            return True

        if self._mode == "draw":

            self._draw_at(
                touch.pos
            )

            return True

        if self._mode == "pan":

            dx = (
                touch.x
                - self._last[0]
            )

            dy = (
                touch.y
                - self._last[1]
            )

            self.pan_x += dx
            self.pan_y += dy

            self._last = touch.pos

            self.relayout()

            return True

        return False

    def on_touch_up(
        self,
        touch
    ):

        self._touches.pop(
            touch.uid,
            None
        )

        if not self._touches:

            if self._mode == "draw":
                self._end_stroke()

            self._mode = None
            self._g_dist = None

        return True

    def on_touch_cancel(
        self,
        touch
    ):

        self._touches.pop(
            touch.uid,
            None
        )

        self._end_stroke()

        self._mode = None

        return True

    def _draw_at(
        self,
        pos
    ):

        cell = self.cell_at(
            *pos
        )

        if cell is None:

            self._last = None

            return

        if not self._active:

            self._active = True

            self.ed.begin_stroke()

            self.ed.tool_press(
                *cell
            )

            self._last = cell

            return

        if cell == self._last:
            return

        if self.ed.tool in (
            "pencil",
            "eraser"
        ):

            points = (
                [cell]
                if self._last is None
                else
                line_cells(
                    self._last,
                    cell
                )
            )

            for r, c in points:

                self.ed.paint_with_tool(
                    r,
                    c
                )

        self._last = cell

    def _end_stroke(self):

        self._active = False

        self._last = None

        self.ed.end_stroke()


# ================================================================
# BASE SCREEN
# ================================================================

class BaseScreen(Screen):

    def __init__(
        self,
        app,
        **kwargs
    ):

        super().__init__(
            **kwargs
        )

        self.app = app

    def rebuild(self):

        self.clear_widgets()

        self.build_ui()

    def build_ui(self):
        pass


# ================================================================
# HOME
# ================================================================

class HomeScreen(BaseScreen):

    selected_size = None

    def build_ui(self):

        app = self.app
        theme = app.theme

        root = Panel(
            bg=theme["bg"],
            orientation="vertical",
            padding=dp(10),
            spacing=dp(6)
        )

        top = BoxLayout(
            size_hint_y=None,
            height=dp(38)
        )

        top.add_widget(
            Widget()
        )

        top.add_widget(
            app.btn(
                app.t("settings"),
                lambda:
                app.goto("settings"),
                "card",
                13,
                True,
                size_hint=(None, 1),
                width=dp(120)
            )
        )

        root.add_widget(
            top
        )

        body = BoxLayout(
            orientation="horizontal",
            spacing=dp(16)
        )

        left = BoxLayout(
            orientation="vertical",
            spacing=dp(8)
        )

        logo = resource_path(
            "logo.png"
        )

        if os.path.exists(logo):

            left.add_widget(
                KivyImage(
                    source=logo,
                    size_hint_y=None,
                    height=dp(60)
                )
            )

        left.add_widget(
            app.lbl(
                "PixelMed Studio",
                26,
                True,
                height=dp(42)
            )
        )

        left.add_widget(
            app.btn(
                app.t("new_project"),
                self.on_new_project,
                "main",
                15,
                True,
                size_hint_y=None,
                height=dp(46)
            )
        )

        left.add_widget(
            app.btn(
                app.t("previous_projects"),
                lambda:
                app.goto("projects"),
                "card",
                15,
                True,
                size_hint_y=None,
                height=dp(46)
            )
        )

        self.warning = app.lbl(
            "",
            12,
            color=(
                1,
                0.36,
                0.36,
                1
            )
        )

        left.add_widget(
            self.warning
        )

        left.add_widget(
            Widget()
        )

        body.add_widget(
            left
        )

        right = Panel(
            bg=theme["panel"],
            radius=12,
            orientation="vertical",
            padding=dp(12),
            spacing=dp(6)
        )

        right.add_widget(
            app.lbl(
                app.t("canvas_size"),
                15,
                True
            )
        )

        presets = BoxLayout(
            size_hint_y=None,
            height=dp(40),
            spacing=dp(6)
        )

        self.size_buttons = {}

        for size in (
            "16x16",
            "32x32",
            "64x64"
        ):

            button = app.btn(
                size,
                lambda s=size:
                self.select_size(s),
                "card",
                13
            )

            presets.add_widget(
                button
            )

            self.size_buttons[
                size
            ] = button

        right.add_widget(
            presets
        )

        right.add_widget(
            app.lbl(
                app.t("custom_size"),
                12
            )
        )

        row = BoxLayout(
            size_hint_y=None,
            height=dp(38),
            spacing=dp(6)
        )

        self.w_entry = TextInput(
            hint_text="W",
            multiline=False,
            input_filter="int"
        )

        self.h_entry = TextInput(
            hint_text="H",
            multiline=False,
            input_filter="int"
        )

        row.add_widget(
            self.w_entry
        )

        row.add_widget(
            app.lbl(
                "x",
                16,
                size_hint=(
                    None,
                    1
                ),
                width=dp(18)
            )
        )

        row.add_widget(
            self.h_entry
        )

        right.add_widget(
            row
        )

        right.add_widget(
            app.btn(
                app.t("set"),
                self.confirm_custom_size,
                "main",
                12,
                size_hint_y=None,
                height=dp(34)
            )
        )

        right.add_widget(
            Widget()
        )

        body.add_widget(
            right
        )

        root.add_widget(
            body
        )

        self.add_widget(
            root
        )

        if (
            self.selected_size
            in
            self.size_buttons
        ):

            self.select_size(
                self.selected_size
            )

    def select_size(
        self,
        size
    ):

        theme = self.app.theme

        self.selected_size = size

        for s, button in self.size_buttons.items():

            if s == size:

                button.set_colors(
                    theme["btn_bg"],
                    theme["btn_text"]
                )

            else:

                button.set_colors(
                    theme["card"],
                    theme["text"]
                )

        self.w_entry.text = ""
        self.h_entry.text = ""
        self.warning.text = ""

    def confirm_custom_size(self):

        w = self.w_entry.text.strip()
        h = self.h_entry.text.strip()

        if (
            w.isdigit()
            and
            h.isdigit()
            and
            1 <= int(w) <= 256
            and
            1 <= int(h) <= 256
        ):

            theme = self.app.theme

            self.selected_size = (
                "%sx%s"
                %
                (
                    w,
                    h
                )
            )

            for button in self.size_buttons.values():

                button.set_colors(
                    theme["card"],
                    theme["text"]
                )

            self.warning.text = ""

        else:

            self.warning.text = (
                "Invalid numbers (1-256)."
            )

    def on_new_project(self):

        if not self.selected_size:

            self.warning.text = (
                "Please choose a canvas size."
            )

            return

        w, h = self.selected_size.split("x")

        self.app.start_new_project(
            int(w),
            int(h)
        )


# ================================================================
# SETTINGS
# ================================================================

class SettingsScreen(BaseScreen):

    def build_ui(self):

        app = self.app
        theme = app.theme

        root = Panel(
            bg=theme["bg"],
            orientation="vertical",
            padding=dp(10),
            spacing=dp(8)
        )

        header = BoxLayout(
            size_hint_y=None,
            height=dp(38),
            spacing=dp(10)
        )

        header.add_widget(
            app.btn(
                app.t("back"),
                lambda:
                app.goto("home"),
                "card",
                13,
                size_hint=(
                    None,
                    1
                ),
                width=dp(100)
            )
        )

        header.add_widget(
            app.lbl(
                app.t("settings"),
                20,
                True,
                size_hint=(
                    1,
                    1
                )
            )
        )

        root.add_widget(
            header
        )

        box = Panel(
            bg=theme["panel"],
            radius=12,
            orientation="vertical",
            padding=dp(12),
            spacing=dp(6)
        )

        box.add_widget(
            app.lbl(
                app.t("language"),
                14,
                True
            )
        )

        languages = [
            ("العربية", "ar"),
            ("English", "en"),
            ("Français", "fr")
        ]

        row = BoxLayout(
            size_hint_y=None,
            height=dp(38),
            spacing=dp(6)
        )

        for label, code in languages:

            row.add_widget(
                app.btn(
                    shape_text(
                        label,
                        "ar"
                    ),
                    lambda c=code:
                    app.update_settings(
                        lang=c
                    ),
                    "main"
                    if app.lang == code
                    else
                    "card",
                    12
                )
            )

        box.add_widget(
            row
        )

        box.add_widget(
            app.lbl(
                app.t("theme"),
                14,
                True
            )
        )

        row = BoxLayout(
            size_hint_y=None,
            height=dp(38),
            spacing=dp(6)
        )

        for key in (
            "light",
            "dark",
            "emerald",
            "gameboy"
        ):

            row.add_widget(
                app.btn(
                    app.tr(
                        "theme_" + key
                    ),
                    lambda k=key:
                    app.update_settings(
                        theme=k
                    ),
                    "main"
                    if app.theme_key == key
                    else
                    "card",
                    11
                )
            )

        box.add_widget(
            row
        )

        box.add_widget(
            app.lbl(
                app.t("font_size"),
                14,
                True
            )
        )

        row = BoxLayout(
            size_hint_y=None,
            height=dp(38),
            spacing=dp(6)
        )

        row.add_widget(
            app.btn(
                "A -",
                lambda:
                app.update_settings(
                    scale=app.font_scale - 0.1
                ),
                "card",
                14,
                True,
                size_hint=(
                    None,
                    1
                ),
                width=dp(60)
            )
        )

        row.add_widget(
            app.lbl(
                "%.1f"
                %
                app.font_scale,
                14,
                True,
                size_hint=(
                    None,
                    1
                ),
                width=dp(60)
            )
        )

        row.add_widget(
            app.btn(
                "A +",
                lambda:
                app.update_settings(
                    scale=app.font_scale + 0.1
                ),
                "card",
                14,
                True,
                size_hint=(
                    None,
                    1
                ),
                width=dp(60)
            )
        )

        row.add_widget(
            Widget()
        )

        box.add_widget(
            row
        )

        box.add_widget(
            Widget()
        )

        root.add_widget(
            box
        )

        self.add_widget(
            root
        )


# ================================================================
# PROJECTS
# ================================================================

class ProjectsScreen(BaseScreen):

    def on_pre_enter(self, *args):

        self.rebuild()

    def build_ui(self):

        app = self.app
        theme = app.theme

        root = Panel(
            bg=theme["bg"],
            orientation="vertical",
            padding=dp(10),
            spacing=dp(8)
        )

        header = BoxLayout(
            size_hint_y=None,
            height=dp(38),
            spacing=dp(10)
        )

        header.add_widget(
            app.btn(
                app.t("back"),
                lambda:
                app.goto("home"),
                "card",
                13,
                size_hint=(
                    None,
                    1
                ),
                width=dp(100)
            )
        )

        header.add_widget(
            app.lbl(
                app.t("saved_projects"),
                20,
                True
            )
        )

        root.add_widget(
            header
        )

        scroll = ScrollView(
            do_scroll_x=False,
            bar_width=dp(3)
        )

        listing = GridLayout(
            cols=1,
            size_hint_y=None,
            spacing=dp(6),
            padding=dp(2)
        )

        listing.bind(
            minimum_height=listing.setter(
                "height"
            )
        )

        projects = load_json(
            "saved_projects.json",
            {}
        )

        if not projects:

            listing.add_widget(
                app.lbl(
                    app.t("no_projects"),
                    15,
                    height=dp(60)
                )
            )

        for pid, info in projects.items():

            card = Panel(
                bg=theme["card"],
                radius=10,
                orientation="horizontal",
                size_hint_y=None,
                height=dp(64),
                padding=dp(8),
                spacing=dp(6)
            )

            texts = BoxLayout(
                orientation="vertical"
            )

            texts.add_widget(
                app.lbl(
                    "Project: %s"
                    % pid,
                    13,
                    True,
                    halign="left"
                )
            )

            frame_count = len(
                info.get(
                    "frames",
                    [1]
                )
            )

            texts.add_widget(
                app.lbl(
                    "Size: %sx%s | Frames: %d | %s"
                    %
                    (
                        info["width"],
                        info["height"],
                        frame_count,
                        info.get(
                            "updated_at",
                            "N/A"
                        )
                    ),
                    11,
                    halign="left"
                )
            )

            card.add_widget(
                texts
            )

            card.add_widget(
                app.btn(
                    app.t("open"),
                    lambda p=pid:
                    app.load_existing_project(p),
                    "main",
                    12,
                    size_hint=(
                        None,
                        1
                    ),
                    width=dp(70)
                )
            )

            card.add_widget(
                app.btn(
                    app.t("delete"),
                    lambda p=pid:
                    self.delete_project(p),
                    "danger",
                    12,
                    size_hint=(
                        None,
                        1
                    ),
                    width=dp(70)
                )
            )

            listing.add_widget(
                card
            )

        scroll.add_widget(
            listing
        )

        root.add_widget(
            scroll
        )

        self.add_widget(
            root
        )

    def delete_project(self, pid):

        projects = load_json(
            "saved_projects.json",
            {}
        )

        if pid in projects:

            del projects[pid]

            save_json(
                "saved_projects.json",
                projects
            )

        Clock.schedule_once(
            lambda dt:
            self.rebuild(),
            0
        )


# ================================================================
# EDITOR
# ================================================================

class EditorScreen(BaseScreen):

    COLORS = [
        "#000000",
        "#FFFFFF",
        "#FF3B30",
        "#FF9500",
        "#FFCC00",
        "#34C759",
        "#00C7BE",
        "#007AFF",
        "#5856D6",
        "#AF52DE",
        "#8E5A3D",
        "#8E8E93"
    ]

    def __init__(
        self,
        app,
        **kwargs
    ):

        super().__init__(
            app,
            **kwargs
        )

        self.tool = "pencil"

        self.current_color = "#000000"

        self.grid_w = 16
        self.grid_h = 16

        self.frames_data = [
            {}
        ]

        self.idx = 0

        self.fps = 8

        self.playing = False

        self._play_ev = None

        self.undo_stack = []
        self.redo_stack = []

        self.thumbs = []

        self.pc = None

        self._compact_layout = None

        self._resize_event = None

        Window.bind(
            size=self._on_window_size
        )

    # ------------------------------------------------------------
    # Responsive detection
    # ------------------------------------------------------------

    def _on_window_size(
        self,
        *args
    ):

        compact = (
            Window.width < dp(700)
            or
            (
                Window.height < dp(520)
                and
                Window.width < dp(900)
            )
        )

        if (
            compact
            ==
            self._compact_layout
        ):
            return

        if self.app.sm.current != "editor":
            return

        if self._resize_event:

            self._resize_event.cancel()

        self._resize_event = Clock.schedule_once(
            lambda dt:
            self.rebuild(),
            0.08
        )

    # ------------------------------------------------------------
    # Setup
    # ------------------------------------------------------------

    def setup(
        self,
        w,
        h,
        frames
    ):

        self.stop_play()

        self.grid_w = w
        self.grid_h = h

        self.frames_data = (
            [
                dict(frame)
                for frame in frames
            ]
            if frames
            else
            [{}]
        )

        self.idx = 0

        self.undo_stack = []
        self.redo_stack = []

        self.rebuild()

    def rebuild(self):

        self.stop_play()

        super().rebuild()

    # ============================================================
    # RESPONSIVE UI
    # ============================================================

    def build_ui(self):

        app = self.app
        theme = app.theme

        compact = (
            Window.width < dp(700)
            or
            (
                Window.height < dp(520)
                and
                Window.width < dp(900)
            )
        )

        self._compact_layout = compact

        # ========================================================
        # PHONE
        # ========================================================

        if compact:

            root = Panel(
                bg=theme["bg"],
                orientation="vertical",
                padding=dp(5),
                spacing=dp(5)
            )

            # ----------------------------------------------------
            # TOP TOOL BAR
            # ----------------------------------------------------

            tool_scroll = ScrollView(
                do_scroll_x=True,
                do_scroll_y=False,
                size_hint_y=None,
                height=dp(74),
                bar_width=dp(2)
            )

            tool_row = BoxLayout(
                orientation="horizontal",
                size_hint_x=None,
                spacing=dp(5),
                padding=dp(2)
            )

            tool_row.bind(
                minimum_width=
                tool_row.setter(
                    "width"
                )
            )

            self.tool_buttons = {}

            tools = (
                (
                    "pencil",
                    "pencil",
                    "pencil"
                ),
                (
                    "eraser",
                    "eraser",
                    "eraser"
                ),
                (
                    "fill",
                    "drop",
                    "fill"
                ),
                (
                    "eyedropper",
                    "watering",
                    "picker"
                )
            )

            for key, icon, label in tools:

                button = app.icon_btn(
                    label,
                    icon,
                    lambda k=key:
                    self.select_tool(k),
                    "main"
                    if key == self.tool
                    else "card",
                    9,
                    30,
                    True,
                    size_hint=(
                        None,
                        None
                    ),
                    size=(
                        dp(62),
                        dp(66)
                    )
                )

                self.tool_buttons[
                    key
                ] = button

                tool_row.add_widget(
                    button
                )

            extra = (
                (
                    "undo",
                    "projects",
                    self.undo,
                    "card"
                ),
                (
                    "redo",
                    "move",
                    self.redo,
                    "card"
                ),
                (
                    "clear",
                    "delete",
                    self.clear_canvas,
                    "danger"
                ),
                (
                    "export",
                    "animation",
                    self.open_export_dialog,
                    "green"
                ),
                (
                    "home",
                    "menu",
                    self.go_home,
                    "card"
                )
            )

            for label, icon, callback, kind in extra:

                tool_row.add_widget(
                    app.icon_btn(
                        label,
                        icon,
                        callback,
                        kind,
                        9,
                        30,
                        True,
                        size_hint=(
                            None,
                            None
                        ),
                        size=(
                            dp(62),
                            dp(66)
                        )
                    )
                )

            tool_scroll.add_widget(
                tool_row
            )

            root.add_widget(
                tool_scroll
            )

            # ----------------------------------------------------
            # COLORS
            # ----------------------------------------------------

            color_scroll = ScrollView(
                do_scroll_x=True,
                do_scroll_y=False,
                size_hint_y=None,
                height=dp(42),
                bar_width=dp(2)
            )

            color_row = BoxLayout(
                orientation="horizontal",
                size_hint_x=None,
                spacing=dp(4),
                padding=dp(2)
            )

            color_row.bind(
                minimum_width=
                color_row.setter(
                    "width"
                )
            )

            for color in self.COLORS:

                color_row.add_widget(
                    FlatButton(
                        bg=color,
                        fg="#000000",
                        border="#D9D9D7",
                        radius=6,
                        text="",
                        size_hint=(
                            None,
                            None
                        ),
                        size=(
                            dp(32),
                            dp(32)
                        ),
                        on_release=
                        lambda *_, c=color:
                        self.set_color(c)
                    )
                )

            color_row.add_widget(
                app.icon_btn(
                    "color",
                    "palette",
                    self.pick_custom_color,
                    "card",
                    8,
                    24,
                    True,
                    size_hint=(
                        None,
                        None
                    ),
                    size=(
                        dp(58),
                        dp(34)
                    )
                )
            )

            color_scroll.add_widget(
                color_row
            )

            root.add_widget(
                color_scroll
            )

            # ----------------------------------------------------
            # FIXED DRAWING AREA
            # ----------------------------------------------------

            canvas_box = Panel(
                bg="#FFFFFF",
                radius=8,
                orientation="vertical",
                padding=dp(2)
            )

            self.pc = PixelCanvas(
                self,
                size_hint=(1, 1)
            )

            canvas_box.add_widget(
                self.pc
            )

            root.add_widget(
                canvas_box
            )

            # ----------------------------------------------------
            # RESET
            # ----------------------------------------------------

            reset_row = BoxLayout(
                size_hint_y=None,
                height=dp(34),
                spacing=dp(5)
            )

            reset_row.add_widget(
                Widget()
            )

            reset_row.add_widget(
                app.icon_btn(
                    "reset",
                    "image",
                    self.reset_view,
                    "card",
                    9,
                    22,
                    False,
                    size_hint=(
                        None,
                        1
                    ),
                    width=dp(105)
                )
            )

            root.add_widget(
                reset_row
            )

            # ----------------------------------------------------
            # TIMELINE
            # ----------------------------------------------------

            root.add_widget(
                self.build_timeline(
                    compact=True
                )
            )

            self.add_widget(
                root
            )

        # ========================================================
        # DESKTOP / TABLET LANDSCAPE
        # ========================================================

        else:

            root = Panel(
                bg=theme["bg"],
                orientation="horizontal",
                padding=dp(5),
                spacing=dp(5)
            )

            # ----------------------------------------------------
            # SIDEBAR
            # ----------------------------------------------------

            wrap = Panel(
                bg=theme["panel"],
                size_hint=(
                    None,
                    1
                ),
                width=dp(156)
            )

            scroll = ScrollView(
                do_scroll_x=False,
                bar_width=dp(3)
            )

            side = BoxLayout(
                orientation="vertical",
                size_hint_y=None,
                padding=dp(6),
                spacing=dp(4)
            )

            side.bind(
                minimum_height=
                side.setter(
                    "height"
                )
            )

            H = dp(36)

            side.add_widget(
                app.icon_btn(
                    "home",
                    "menu",
                    self.go_home,
                    "card",
                    10,
                    25,
                    False,
                    size_hint_y=None,
                    height=H
                )
            )

            history = BoxLayout(
                size_hint_y=None,
                height=dp(34),
                spacing=dp(4)
            )

            history.add_widget(
                app.icon_btn(
                    "undo",
                    "projects",
                    self.undo,
                    "card",
                    9,
                    22,
                    False
                )
            )

            history.add_widget(
                app.icon_btn(
                    "redo",
                    "move",
                    self.redo,
                    "card",
                    9,
                    22,
                    False
                )
            )

            side.add_widget(
                history
            )

            side.add_widget(
                app.lbl(
                    app.t("tools"),
                    13,
                    True
                )
            )

            self.tool_buttons = {}

            for key, icon in (
                ("pencil", "pencil"),
                ("eraser", "eraser"),
                ("fill", "drop"),
                ("eyedropper", "watering")
            ):

                button = app.icon_btn(
                    app.tr(key),
                    icon,
                    lambda k=key:
                    self.select_tool(k),
                    "main"
                    if key == self.tool
                    else "card",
                    10,
                    24,
                    False,
                    size_hint_y=None,
                    height=H
                )

                self.tool_buttons[
                    key
                ] = button

                side.add_widget(
                    button
                )

            side.add_widget(
                app.lbl(
                    app.t("colors"),
                    13,
                    True
                )
            )

            grid = GridLayout(
                cols=4,
                size_hint_y=None,
                height=dp(96),
                spacing=dp(3),
                row_default_height=dp(30),
                row_force_default=True
            )

            for color in self.COLORS:

                grid.add_widget(
                    FlatButton(
                        bg=color,
                        fg="#000000",
                        border="#D9D9D7",
                        radius=6,
                        text="",
                        on_release=
                        lambda *_, c=color:
                        self.set_color(c)
                    )
                )

            side.add_widget(
                grid
            )

            self.color_preview = Panel(
                bg=self.current_color,
                radius=6,
                size_hint_y=None,
                height=dp(30)
            )

            side.add_widget(
                self.color_preview
            )

            side.add_widget(
                app.icon_btn(
                    app.t("custom_color"),
                    "palette",
                    self.pick_custom_color,
                    "card",
                    9,
                    22,
                    False,
                    size_hint_y=None,
                    height=dp(34)
                )
            )

            side.add_widget(
                app.icon_btn(
                    app.t("clear_canvas"),
                    "delete",
                    self.clear_canvas,
                    "danger",
                    9,
                    22,
                    False,
                    size_hint_y=None,
                    height=dp(34)
                )
            )

            side.add_widget(
                app.icon_btn(
                    app.t("export_anim"),
                    "animation",
                    self.open_export_dialog,
                    "green",
                    9,
                    22,
                    False,
                    size_hint_y=None,
                    height=H
                )
            )

            scroll.add_widget(
                side
            )

            wrap.add_widget(
                scroll
            )

            root.add_widget(
                wrap
            )

            # ----------------------------------------------------
            # CANVAS + TIMELINE
            # ----------------------------------------------------

            right = BoxLayout(
                orientation="vertical"
            )

            area = FloatLayout()

            self.pc = PixelCanvas(
                self,
                size_hint=(1, 1)
            )

            area.add_widget(
                self.pc
            )

            area.add_widget(
                app.icon_btn(
                    app.t("reset_view"),
                    "image",
                    self.reset_view,
                    "card",
                    9,
                    22,
                    False,
                    size_hint=(
                        None,
                        None
                    ),
                    size=(
                        dp(140),
                        dp(32)
                    ),
                    pos_hint={
                        "right": 0.99,
                        "top": 0.98
                    }
                )
            )

            right.add_widget(
                area
            )

            right.add_widget(
                self.build_timeline(
                    compact=False
                )
            )

            root.add_widget(
                right
            )

            self.add_widget(
                root
            )

        self.pc.setup(
            self.grid_w,
            self.grid_h
        )

        self.refresh_timeline()

    # ============================================================
    # TIMELINE
    # ============================================================

    def build_timeline(
        self,
        compact=False
    ):

        app = self.app
        theme = app.theme

        height = (
            dp(94)
            if compact
            else
            dp(98)
        )

        bar = Panel(
            bg=theme["panel"],
            orientation="horizontal",
            size_hint_y=None,
            height=height,
            padding=dp(4),
            spacing=dp(5)
        )

        controls = BoxLayout(
            orientation=(
                "horizontal"
                if compact
                else
                "vertical"
            ),
            size_hint_x=None,
            width=(
                dp(180)
                if compact
                else
                dp(80)
            ),
            spacing=dp(3)
        )

        self.play_btn = app.icon_btn(
            app.t("play"),
            "animation",
            self.toggle_play,
            "green",
            9,
            22,
            compact
        )

        controls.add_widget(
            self.play_btn
        )

        controls.add_widget(
            app.icon_btn(
                app.t("add_frame"),
                "image",
                self.add_frame,
                "card",
                9,
                22,
                compact
            )
        )

        controls.add_widget(
            app.icon_btn(
                app.t("delete_frame"),
                "delete",
                self.delete_frame,
                "danger",
                9,
                22,
                compact
            )
        )

        bar.add_widget(
            controls
        )

        fps = BoxLayout(
            orientation="vertical",
            size_hint_x=None,
            width=dp(100),
            spacing=dp(1)
        )

        self.fps_label = app.lbl(
            app.shape(
                "%s: %d FPS"
                %
                (
                    app.tr("speed"),
                    self.fps
                )
            ),
            10,
            True
        )

        fps.add_widget(
            Widget()
        )

        fps.add_widget(
            self.fps_label
        )

        slider = Slider(
            min=1,
            max=30,
            value=self.fps,
            step=1,
            size_hint_y=None,
            height=dp(30)
        )

        slider.bind(
            value=self.on_fps
        )

        fps.add_widget(
            slider
        )

        fps.add_widget(
            Widget()
        )

        bar.add_widget(
            fps
        )

        order = BoxLayout(
            orientation=(
                "horizontal"
                if compact
                else
                "vertical"
            ),
            size_hint_x=None,
            width=(
                dp(126)
                if compact
                else
                dp(80)
            ),
            spacing=dp(3)
        )

        order.add_widget(
            app.icon_btn(
                app.t("move_left"),
                "move",
                lambda:
                self.move_frame(-1),
                "card",
                9,
                22,
                compact
            )
        )

        order.add_widget(
            app.icon_btn(
                app.t("move_right"),
                "move",
                lambda:
                self.move_frame(1),
                "card",
                9,
                22,
                compact
            )
        )

        bar.add_widget(
            order
        )

        self.thumb_scroll = ScrollView(
            do_scroll_y=False,
            bar_width=dp(3)
        )

        self.thumb_box = BoxLayout(
            orientation="horizontal",
            size_hint_x=None,
            spacing=dp(4)
        )

        self.thumb_box.bind(
            minimum_width=
            self.thumb_box.setter(
                "width"
            )
        )

        self.thumb_scroll.add_widget(
            self.thumb_box
        )

        bar.add_widget(
            self.thumb_scroll
        )

        return bar

    def refresh_timeline(self):

        self.thumb_box.clear_widgets()

        self.thumbs = []

        theme = self.app.theme

        for i, frame in enumerate(
            self.frames_data
        ):

            thumbnail = Thumb(
                i,
                make_texture(
                    frame,
                    self.grid_w,
                    self.grid_h
                ),
                self.grid_w,
                self.grid_h,
                i == self.idx,
                theme
            )

            thumbnail.bind(
                on_release=
                lambda inst, i=i:
                self.select_frame(i)
            )

            self.thumb_box.add_widget(
                thumbnail
            )

            self.thumbs.append(
                thumbnail
            )

    def _sync_selection(self):

        for thumb in self.thumbs:

            thumb.set_selected(
                thumb.index == self.idx
            )

    # ============================================================
    # TOOLS
    # ============================================================

    def select_tool(
        self,
        tool
    ):

        self.tool = tool

        theme = self.app.theme

        for key, button in self.tool_buttons.items():

            if key == tool:

                button.set_colors(
                    theme["btn_bg"],
                    theme["btn_text"]
                )

            else:

                button.set_colors(
                    theme["card"],
                    theme["text"]
                )

    def set_color(
        self,
        color
    ):

        self.current_color = color

        preview = getattr(
            self,
            "color_preview",
            None
        )

        if preview:

            preview.set_bg(
                color
            )

    def pick_custom_color(self):

        picker = ColorPicker(
            color=get_color_from_hex(
                self.current_color
            )
        )

        box = BoxLayout(
            orientation="vertical",
            spacing=dp(6)
        )

        box.add_widget(
            picker
        )

        row = BoxLayout(
            size_hint_y=None,
            height=dp(40),
            spacing=dp(6)
        )

        popup = Popup(
            title=self.app.t(
                "custom_color"
            ),
            content=box,
            size_hint=(
                0.85,
                0.95
            )
        )

        def ok():

            self.set_color(
                get_hex_from_color(
                    picker.color
                )[:7]
            )

            popup.dismiss()

        row.add_widget(
            self.app.btn(
                "OK",
                ok,
                "green",
                13,
                True
            )
        )

        row.add_widget(
            self.app.btn(
                "Cancel",
                popup.dismiss,
                "card",
                13
            )
        )

        box.add_widget(
            row
        )

        popup.open()

    def reset_view(self):

        self.pc.fit_view()

    def go_home(self):

        self.stop_play()

        self.app.save_current_project(
            self.frames_data
        )

        self.app.goto(
            "home"
        )

    # ============================================================
    # DRAWING
    # ============================================================

    def begin_stroke(self):

        if self.tool in (
            "pencil",
            "eraser",
            "fill"
        ):

            self.push_state()

    def tool_press(
        self,
        r,
        c
    ):

        if self.tool == "pencil":

            self.paint_cell(
                r,
                c,
                self.current_color
            )

        elif self.tool == "eraser":

            self.paint_cell(
                r,
                c,
                None
            )

        elif self.tool == "fill":

            self.flood_fill(
                r,
                c,
                self.current_color
            )

        elif self.tool == "eyedropper":

            color = self.frames_data[
                self.idx
            ].get(
                (r, c)
            )

            if color:

                self.set_color(
                    color
                )

                self.select_tool(
                    "pencil"
                )

    def paint_with_tool(
        self,
        r,
        c
    ):

        if self.tool == "pencil":

            self.paint_cell(
                r,
                c,
                self.current_color
            )

        elif self.tool == "eraser":

            self.paint_cell(
                r,
                c,
                None
            )

    def end_stroke(self):

        self.refresh_timeline()

        self.app.save_current_project(
            self.frames_data
        )

    def paint_cell(
        self,
        r,
        c,
        color
    ):

        data = self.frames_data[
            self.idx
        ]

        if color is None:

            data.pop(
                (r, c),
                None
            )

        else:

            data[
                (r, c)
            ] = color

        self.pc.set_pixel(
            r,
            c,
            color
        )

    def flood_fill(
        self,
        r,
        c,
        new_color
    ):

        data = self.frames_data[
            self.idx
        ]

        target = data.get(
            (r, c)
        )

        if target == new_color:
            return

        stack = [
            (r, c)
        ]

        visited = set()

        while stack:

            rr, cc = stack.pop()

            if (
                (rr, cc)
                in visited
                or
                not (
                    0 <= rr < self.grid_h
                    and
                    0 <= cc < self.grid_w
                )
            ):
                continue

            if data.get(
                (rr, cc)
            ) != target:
                continue

            visited.add(
                (rr, cc)
            )

            data[
                (rr, cc)
            ] = new_color

            stack.extend(
                [
                    (rr + 1, cc),
                    (rr - 1, cc),
                    (rr, cc + 1),
                    (rr, cc - 1)
                ]
            )

        self.pc.refresh()

    def clear_canvas(self):

        if self.frames_data[
            self.idx
        ]:

            self.push_state()

            self.frames_data[
                self.idx
            ] = {}

            self.pc.refresh()

            self.refresh_timeline()

            self.app.save_current_project(
                self.frames_data
            )

    # ============================================================
    # UNDO / REDO
    # ============================================================

    def push_state(self):

        self.undo_stack.append(
            (
                self.idx,
                [
                    frame.copy()
                    for frame in self.frames_data
                ]
            )
        )

        self.redo_stack.clear()

        if len(
            self.undo_stack
        ) > 30:

            self.undo_stack.pop(
                0
            )

    def undo(self):

        if not self.undo_stack:
            return

        self.redo_stack.append(
            (
                self.idx,
                [
                    frame.copy()
                    for frame in self.frames_data
                ]
            )
        )

        self.idx, self.frames_data = (
            self.undo_stack.pop()
        )

        self._after_history()

    def redo(self):

        if not self.redo_stack:
            return

        self.undo_stack.append(
            (
                self.idx,
                [
                    frame.copy()
                    for frame in self.frames_data
                ]
            )
        )

        self.idx, self.frames_data = (
            self.redo_stack.pop()
        )

        self._after_history()

    def _after_history(self):

        self.idx = min(
            self.idx,
            len(self.frames_data) - 1
        )

        self.pc.refresh()

        self.refresh_timeline()

        self.app.save_current_project(
            self.frames_data
        )

    # ============================================================
    # FRAMES
    # ============================================================

    def select_frame(
        self,
        index
    ):

        if (
            0 <= index
            < len(self.frames_data)
        ):

            self.idx = index

            self.pc.refresh()

            self._sync_selection()

    def add_frame(self):

        self.push_state()

        data = self.frames_data[
            self.idx
        ].copy()

        self.idx += 1

        self.frames_data.insert(
            self.idx,
            data
        )

        self.pc.refresh()

        self.refresh_timeline()

        self.app.save_current_project(
            self.frames_data
        )

    def delete_frame(self):

        if len(
            self.frames_data
        ) <= 1:

            return

        self.push_state()

        self.frames_data.pop(
            self.idx
        )

        if (
            self.idx
            >=
            len(self.frames_data)
        ):

            self.idx = (
                len(self.frames_data)
                - 1
            )

        self.pc.refresh()

        self.refresh_timeline()

        self.app.save_current_project(
            self.frames_data
        )

    def move_frame(
        self,
        direction
    ):

        new_index = (
            self.idx
            + direction
        )

        if (
            0 <= new_index
            < len(self.frames_data)
        ):

            self.push_state()

            frames = self.frames_data

            frames[
                self.idx
            ], frames[
                new_index
            ] = frames[
                new_index
            ], frames[
                self.idx
            ]

            self.idx = new_index

            self.refresh_timeline()

            self.app.save_current_project(
                self.frames_data
            )

    # ============================================================
    # ANIMATION
    # ============================================================

    def on_fps(
        self,
        instance,
        value
    ):

        self.fps = int(value)

        self.fps_label.text = (
            self.app.shape(
                "%s: %d FPS"
                %
                (
                    self.app.tr(
                        "speed"
                    ),
                    self.fps
                )
            )
        )

    def toggle_play(self):

        if self.playing:

            self.stop_play()

        else:

            self.playing = True

            self.play_btn.set_text(
                self.app.t(
                    "pause"
                )
            )

            self.play_btn.set_colors(
                "#D93030",
                "#FFFFFF"
            )

            self._play_ev = (
                Clock.schedule_once(
                    self._tick,
                    1.0 / self.fps
                )
            )

    def _tick(
        self,
        dt
    ):

        if not self.playing:
            return

        self.idx = (
            self.idx + 1
        ) % len(
            self.frames_data
        )

        self.pc.refresh()

        self._sync_selection()

        self._play_ev = (
            Clock.schedule_once(
                self._tick,
                1.0 / self.fps
            )
        )

    def stop_play(self):

        self.playing = False

        if self._play_ev:

            self._play_ev.cancel()

            self._play_ev = None

        button = getattr(
            self,
            "play_btn",
            None
        )

        if button:

            button.set_text(
                self.app.t(
                    "play"
                )
            )

            button.set_colors(
                "#2E7D32",
                "#FFFFFF"
            )

    # ============================================================
    # EXPORT
    # ============================================================

    def open_export_dialog(self):

        app = self.app

        box = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(8)
        )

        popup = Popup(
            title="Export Project",
            content=box,
            size_hint=(
                0.6,
                0.85
            )
        )

        def run(format_name):

            popup.dismiss()

            Clock.schedule_once(
                lambda dt:
                self.export_gif()
                if format_name == "GIF"
                else
                self.export_png_sequence(),
                0.15
            )

        box.add_widget(
            app.btn(
                "Animated GIF",
                lambda:
                run("GIF"),
                "green",
                14,
                True
            )
        )

        box.add_widget(
            app.btn(
                "PNG Sequence",
                lambda:
                run("PNG"),
                "main",
                13
            )
        )

        box.add_widget(
            app.btn(
                "Cancel",
                popup.dismiss,
                "card",
                13
            )
        )

        popup.open()

    def generate_frame_image(
        self,
        frame,
        scale=20
    ):

        image = PILImage.new(
            "RGBA",
            (
                self.grid_w,
                self.grid_h
            ),
            (
                0,
                0,
                0,
                0
            )
        )

        for (
            r,
            c
        ), color in frame.items():

            if (
                0 <= r < self.grid_h
                and
                0 <= c < self.grid_w
            ):

                R, G, B = hex_to_rgb(
                    color
                )

                image.putpixel(
                    (
                        c,
                        r
                    ),
                    (
                        R,
                        G,
                        B,
                        255
                    )
                )

        return image.resize(
            (
                self.grid_w * scale,
                self.grid_h * scale
            ),
            resample=PILImage.NEAREST
        )

    def export_gif(self):

        stamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        path = os.path.join(
            get_export_dir(self.app),
            "pixelmed_%s.gif"
            % stamp
        )

        try:

            images = [
                self.generate_frame_image(
                    frame
                )
                for frame in self.frames_data
            ]

            images[0].save(
                path,
                save_all=True,
                append_images=images[1:],
                optimize=False,
                duration=int(
                    1000 / self.fps
                ),
                loop=0
            )

            self.app.show_message(
                "Success",
                "GIF exported successfully!\n%s"
                % path
            )

        except Exception as error:

            self.app.show_message(
                "Error",
                "Failed to export GIF:\n%s"
                % error
            )

    def export_png_sequence(self):

        stamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        folder = os.path.join(
            get_export_dir(self.app),
            "pixelmed_%s_frames"
            % stamp
        )

        try:

            os.makedirs(
                folder,
                exist_ok=True
            )

            for i, frame in enumerate(
                self.frames_data
            ):

                self.generate_frame_image(
                    frame
                ).save(
                    os.path.join(
                        folder,
                        "frame_%03d.png"
                        % (
                            i + 1
                        )
                    ),
                    "PNG"
                )

            self.app.show_message(
                "Success",
                "Exported %d frames to:\n%s"
                %
                (
                    len(
                        self.frames_data
                    ),
                    folder
                )
            )

        except Exception as error:

            self.app.show_message(
                "Error",
                "Failed to export PNG sequence:\n%s"
                % error
            )


# ================================================================
# APPLICATION
# ================================================================

class PixelMedApp(App):

    title = "PixelMed Studio"

    def build(self):

        init_storage(
            self.user_data_dir
        )

        settings = load_json(
            "app_settings.json",
            {
                "lang": "ar",
                "theme": "light",
                "font_scale": 1.0
            }
        )

        self.lang = settings.get(
            "lang",
            "ar"
        )

        self.theme_key = settings.get(
            "theme",
            "light"
        )

        self.font_scale = settings.get(
            "font_scale",
            1.0
        )

        self.current_project_id = None

        self.grid_w = None
        self.grid_h = None

        if os.path.exists(
            resource_path("logo.png")
        ):

            self.icon = resource_path(
                "logo.png"
            )

        if platform == "android":

            try:

                from android.permissions import (
                    request_permissions,
                    Permission
                )

                request_permissions(
                    [
                        Permission.WRITE_EXTERNAL_STORAGE,
                        Permission.READ_EXTERNAL_STORAGE
                    ]
                )

            except Exception:
                pass

        if platform in (
            "android",
            "ios"
        ):

            Window.softinput_mode = (
                "below_target"
            )

        Window.clearcolor = (
            get_color_from_hex(
                self.theme["bg"]
            )
        )

        Window.bind(
            on_keyboard=self.on_key
        )

        self.sm = ScreenManager(
            transition=NoTransition()
        )

        self.screens = {
            "home":
                HomeScreen(
                    self,
                    name="home"
                ),

            "settings":
                SettingsScreen(
                    self,
                    name="settings"
                ),

            "projects":
                ProjectsScreen(
                    self,
                    name="projects"
                ),

            "editor":
                EditorScreen(
                    self,
                    name="editor"
                )
        }

        for screen in self.screens.values():

            screen.rebuild()

            self.sm.add_widget(
                screen
            )

        self.sm.current = "home"

        return self.sm

    # ============================================================
    # HELPERS
    # ============================================================

    @property
    def theme(self):

        return THEMES.get(
            self.theme_key,
            THEMES["light"]
        )

    def tr(
        self,
        key
    ):

        return TRANSLATIONS.get(
            self.lang,
            TRANSLATIONS["en"]
        ).get(
            key,
            key
        )

    def shape(
        self,
        text
    ):

        return shape_text(
            text,
            self.lang
        )

    def t(
        self,
        key
    ):

        return self.shape(
            self.tr(key)
        )

    def fs(
        self,
        base
    ):

        return sp(
            base * self.font_scale
        )

    # ============================================================
    # NORMAL BUTTON
    # ============================================================

    def btn(
        self,
        text,
        callback=None,
        kind="card",
        font=12,
        bold=False,
        **kwargs
    ):

        theme = self.theme

        border = (
            theme["btn_border"]
            if theme["border_width"]
            else None
        )

        if kind == "main":

            bg = theme["btn_bg"]
            fg = theme["btn_text"]

        elif kind == "danger":

            bg = "#FF5C5C"
            fg = "#FFFFFF"

        elif kind == "green":

            bg = "#2E7D32"
            fg = "#FFFFFF"

        else:

            bg = theme["card"]
            fg = theme["text"]

        button = FlatButton(
            bg=bg,
            fg=fg,
            border=border,
            text=text,
            font_size=self.fs(font),
            bold=bold,
            **kwargs
        )

        if callback:

            button.bind(
                on_release=
                lambda *_:
                callback()
            )

        return button

    # ============================================================
    # ICON BUTTON
    # ============================================================

    def icon_btn(
        self,
        text,
        icon,
        callback=None,
        kind="card",
        font=10,
        icon_size=28,
        vertical=True,
        **kwargs
    ):

        theme = self.theme

        if kind == "main":

            bg = theme["btn_bg"]
            fg = theme["btn_text"]

        elif kind == "danger":

            bg = "#FF5C5C"
            fg = "#FFFFFF"

        elif kind == "green":

            bg = "#2E7D32"
            fg = "#FFFFFF"

        else:

            bg = theme["card"]
            fg = theme["text"]

        button = IconButton(
            text=self.shape(
                text
            ),
            icon=icon_path(
                icon
            ),
            bg=bg,
            fg=fg,
            icon_size=icon_size,
            vertical=vertical,
            **kwargs
        )

        button.label.font_size = self.fs(
            font
        )

        if callback:

            button.bind(
                on_release=
                lambda *_:
                callback()
            )

        return button

    # ============================================================
    # LABEL
    # ============================================================

    def lbl(
        self,
        text,
        size=13,
        bold=False,
        **kwargs
    ):

        color = kwargs.pop(
            "color",
            get_color_from_hex(
                self.theme["text"]
            )
        )

        kwargs.setdefault(
            "size_hint_y",
            None
        )

        kwargs.setdefault(
            "height",
            self.fs(size) * 1.9
        )

        label = Label(
            text=text,
            font_size=self.fs(size),
            bold=bold,
            color=color,
            **kwargs
        )

        if kwargs.get(
            "halign"
        ) in (
            "left",
            "right"
        ):

            label.bind(
                size=lambda instance, size:
                setattr(
                    instance,
                    "text_size",
                    (
                        size[0],
                        size[1]
                    )
                )
            )

        return label

    # ============================================================
    # POPUP
    # ============================================================

    def show_message(
        self,
        title,
        text
    ):

        label = Label(
            text=text,
            halign="center",
            valign="middle"
        )

        label.bind(
            size=lambda instance, size:
            setattr(
                instance,
                "text_size",
                size
            )
        )

        Popup(
            title=title,
            content=label,
            size_hint=(
                0.75,
                0.6
            )
        ).open()

    # ============================================================
    # NAVIGATION
    # ============================================================

    def goto(
        self,
        name
    ):

        self.sm.current = name

    def update_settings(
        self,
        lang=None,
        theme=None,
        scale=None
    ):

        if lang:
            self.lang = lang

        if theme:
            self.theme_key = theme

        if scale is not None:

            self.font_scale = round(
                min(
                    1.4,
                    max(
                        0.8,
                        scale
                    )
                ),
                1
            )

        save_json(
            "app_settings.json",
            {
                "lang": self.lang,
                "theme": self.theme_key,
                "font_scale": self.font_scale
            }
        )

        Window.clearcolor = (
            get_color_from_hex(
                self.theme["bg"]
            )
        )

        Clock.schedule_once(
            lambda dt:
            [
                screen.rebuild()
                for screen
                in self.screens.values()
            ],
            0
        )

    # ============================================================
    # PROJECTS
    # ============================================================

    def start_new_project(
        self,
        w,
        h
    ):

        self.current_project_id = (
            datetime.now().strftime(
                "proj_%Y%m%d_%H%M%S"
            )
        )

        self.grid_w = w
        self.grid_h = h

        self.screens[
            "editor"
        ].setup(
            w,
            h,
            [
                {}
            ]
        )

        self.goto(
            "editor"
        )

    def load_existing_project(
        self,
        pid
    ):

        projects = load_json(
            "saved_projects.json",
            {}
        )

        if pid not in projects:
            return

        project = projects[
            pid
        ]

        self.current_project_id = pid

        self.grid_w = project[
            "width"
        ]

        self.grid_h = project[
            "height"
        ]

        frames = []

        for frame_data in project.get(
            "frames",
            [
                project.get(
                    "pixels",
                    {}
                )
            ]
        ):

            frame = {}

            for key, color in frame_data.items():

                r, c = map(
                    int,
                    key.split(",")
                )

                frame[
                    (
                        r,
                        c
                    )
                ] = color

            frames.append(
                frame
            )

        self.screens[
            "editor"
        ].setup(
            self.grid_w,
            self.grid_h,
            frames
        )

        self.goto(
            "editor"
        )

    def save_current_project(
        self,
        frames_data
    ):

        if not self.current_project_id:
            return

        projects = load_json(
            "saved_projects.json",
            {}
        )

        projects[
            self.current_project_id
        ] = {

            "id":
                self.current_project_id,

            "width":
                self.grid_w,

            "height":
                self.grid_h,

            "updated_at":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M"
                ),

            "frames":
                [
                    {
                        "%d,%d"
                        %
                        (
                            r,
                            c
                        ):
                        color

                        for (
                            r,
                            c
                        ), color
                        in frame.items()
                    }

                    for frame
                    in frames_data
                ]
        }

        save_json(
            "saved_projects.json",
            projects
        )

    # ============================================================
    # ANDROID BACK
    # ============================================================

    def on_key(
        self,
        window,
        key,
        *args
    ):

        if key == 27:

            current = self.sm.current

            if current == "home":
                return False

            if current == "editor":

                self.screens[
                    "editor"
                ].go_home()

            else:

                self.goto(
                    "home"
                )

            return True

        return False

    def on_pause(self):

        editor = self.screens[
            "editor"
        ]

        self.save_current_project(
            editor.frames_data
        )

        return True


# ================================================================
# RUN
# ================================================================

if __name__ == "__main__":

    PixelMedApp().run()