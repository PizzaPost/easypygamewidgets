import pygame

from .button import Button
from .entry import Entry
from .font import Font
from .label import Label
from .misc import disable_update_check, link_pygame_window
from .screen import Screen
from .slider import Slider
from .surface import Surface
from .timekeeper import Timekeeper


def flip(pygame_draw_function: function = None):
    if not misc.pg:
        misc.check_linked()
    for widget in misc.all_widgets:
        if isinstance(widget, tuple):
            if pygame_draw_function:
                pygame_draw_function()
        else:
            if isinstance(widget, Screen):
                screen.draw(widget, misc.pg)
            elif isinstance(widget, Button):
                button.draw(widget, misc.pg)
            elif isinstance(widget, Slider):
                slider.draw(widget, misc.pg)
            elif isinstance(widget, Entry):
                entry.draw(widget, misc.pg)
            elif isinstance(widget, Label):
                label.draw(widget, misc.pg)
            elif isinstance(widget, Surface):
                surface.draw(widget, misc.pg)
            elif isinstance(widget, Timekeeper):
                timekeeper.draw(widget, misc.pg)
    pygame.display.flip()


def handle_event(event):
    for widget in misc.all_widgets:
        if isinstance(widget, Button):
            button.react(b, event)
            button.react(b)
        elif isinstance(widget, Slider):
            slider.react(widget, event)
            slider.react(widget)
        elif isinstance(widget, Entry):
            entry.react(widget, event)
        elif isinstance(widget, Label):
            label.react(widget, event)
            label.react(widget)
        elif isinstance(widget, Surface):
            surface.react(widget, event)
            surface.react(widget)
        elif isinstance(widget, Timekeeper):
            timekeeper.react(widget, event)
            timekeeper.react(widget)
