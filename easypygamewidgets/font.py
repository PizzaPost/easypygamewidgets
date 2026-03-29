import os
import pathlib

import pygame

pygame.init()
pack_font_path = pathlib.Path(__file__).resolve().parent / "assets" / "fonts"
default_font_path = os.path.join(pack_font_path / "roboto mono" / "RobotoMono-Regular.ttf")
default_emoji_font_path = os.path.join(pack_font_path / "emoji" / "NotoEmoji-Regular.ttf")

default_font = pygame.font.Font(default_font_path, 26)
tooltip_font = pygame.font.Font(default_font_path, 16)
emoji_font = pygame.font.Font(default_emoji_font_path, 26)


class Font:
    def __init__(self, font_path: str = default_font_path, font_size: int = 26):
        self.font = pygame.font.Font(font_path, font_size)

    def __getattr__(self, attr):
        return getattr(self.font, attr)
