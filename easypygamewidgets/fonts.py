import os
import pathlib

import pygame

pygame.init()

default_font = pygame.font.Font(
    os.path.join(pathlib.Path(__file__).resolve().parent, "assets", "fonts", "roboto mono", "RobotoMono-Regular.ttf"),
    26)
emoji_font = pygame.font.Font(
    os.path.join(pathlib.Path(__file__).resolve().parent, "assets", "fonts", "emoji", "NotoEmoji-Regular.ttf"), 26)
