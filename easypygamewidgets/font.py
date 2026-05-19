# font.py
# by PizzaPost
# https://github.com/PizzaPost/easypygamewidgets

import os
import pathlib

import pygame

pygame.init()
pack_font_path = pathlib.Path(__file__).resolve().parent / "assets" / "fonts"
default_font_path = os.path.join(pack_font_path / "roboto mono" / "RobotoMono-Regular.ttf")
default_emoji_font_path = os.path.join(pack_font_path / "emoji" / "NotoEmoji-Regular.ttf")


class Font:
    def __init__(self, font_path: str = default_font_path, font_size: int = 26, line_spacing: int | None = None,
                 bold: bool = False, italic: bool = False):
        self.font = pygame.font.Font(font_path, font_size)
        self.font.set_bold(bold)
        self.font.set_italic(italic)
        self.font.set_linesize(line_spacing) if line_spacing else self.font.set_linesize(font_size + 4)

    def __getattr__(self, attr):
        return getattr(self.font, attr)


class SysFont:
    def __init__(self, font: str = "Arial", font_size: int = 26, line_spacing: int | None = None, bold: bool = False,
                 italic: bool = False):
        self.font = pygame.font.SysFont(font, font_size)
        self.font.set_bold(bold)
        self.font.set_italic(italic)
        self.font.set_linesize(line_spacing) if line_spacing else self.font.set_linesize(font_size + 4)

    def __getattr__(self, attr):
        return getattr(self.font, attr)


default_font = Font(default_font_path, 26, None)
tooltip_font = Font(default_font_path, 16, None)
emoji_font = Font(default_emoji_font_path, 26, None)
