import os
import pathlib

import pygame

pygame.init()
default_font_path = os.path.join(pathlib.Path(__file__).resolve().parent,
                                 "assets", "fonts", "roboto mono", "RobotoMono-Regular.ttf")
default_emoji_font_path = os.path.join(pathlib.Path(__file__).resolve().parent,
                                       "assets", "fonts", "emoji", "NotoEmoji-Regular.ttf")

default_font = pygame.font.Font(default_font_path, 26)
emoji_font = pygame.font.Font(default_emoji_font_path, 26)


def create_font(font_path: str = default_font_path, font_size: int = 26):
    return pygame.font.Font(os.path.join(font_path), font_size)
