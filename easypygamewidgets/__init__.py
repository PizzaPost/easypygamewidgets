import pygame

from .button import Button
from .entry import Entry
from .font import Font
from .label import Label
from .misc import disable_update_check, link_pygame_window, create_pygame_layer
from .screen import Screen
from .slider import Slider
from .surface import Surface
from .timekeeper import Timekeeper
from .tooltip import Tooltip


def flip(pygame_draw_function=None):
    if not misc.pg:
        misc.check_linked()
    for widget in misc.all_widgets:
        if isinstance(widget, tuple):
            if isinstance(widget[0], pygame.Surface):
                if pygame_draw_function:
                    pygame_draw_function()
            else:
                widget[0]()
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
                label.update_animation(widget)
                label.draw(widget, misc.pg)
            elif isinstance(widget, Surface):
                surface.update_animation(widget)
                surface.draw(widget, misc.pg)
            elif isinstance(widget, Timekeeper):
                timekeeper.draw(widget, misc.pg)
            elif isinstance(widget, Tooltip):
                tooltip.draw(widget, misc.pg)
    pygame.display.flip()


def handle_event(event):
    for widget in misc.all_widgets:
        if isinstance(widget, Button):
            button.react(widget, event)
        elif isinstance(widget, Slider):
            slider.react(widget, event)
        elif isinstance(widget, Entry):
            entry.react(widget, event)
        elif isinstance(widget, Label):
            label.react(widget, event)
        elif isinstance(widget, Surface):
            surface.react(widget, event)
        elif isinstance(widget, Timekeeper):
            timekeeper.react(widget, event)


def handle_special_events():
    for widget in misc.all_widgets:
        if isinstance(widget, Button):
            button.react(widget)
        elif isinstance(widget, Slider):
            slider.react(widget)
        elif isinstance(widget, Entry):
            entry.react(widget)
        elif isinstance(widget, Label):
            label.react(widget)
        elif isinstance(widget, Surface):
            surface.react(widget)
        elif isinstance(widget, Timekeeper):
            timekeeper.react(widget)