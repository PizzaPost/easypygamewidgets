from .button import Button
from .entry import Entry
from .font import Font
from .label import Label
from .misc import disable_update_check, link_pygame_window
from .screen import Screen
from .slider import Slider
from .surface import Surface
from .timekeeper import Timekeeper


def flip():
    if not misc.pg:
        misc.check_linked()
    for s in screen.all_screens:
        screen.draw(s, misc.pg)
    for b in button.all_buttons:
        button.draw(b, misc.pg)
    for s in slider.all_sliders:
        slider.draw(s, misc.pg)
    for e in entry.all_entrys:
        entry.draw(e, misc.pg)
    for l in label.all_labels:
        label.draw(l, misc.pg)
    for s in surface.all_surfaces:
        surface.draw(s, misc.pg)
    for t in timekeeper.all_timekeepers:
        timekeeper.draw(t, misc.pg)


def handle_event(event):
    if len(button.all_buttons) > 0:
        for b in button.all_buttons:
            button.react(b, event)
    if len(slider.all_sliders) > 0:
        for s in slider.all_sliders:
            slider.react(s, event)
    if len(entry.all_entrys) > 0:
        for e in entry.all_entrys:
            entry.react(e, event)
    if len(label.all_labels) > 0:
        for l in label.all_labels:
            label.react(l, event)
    if len(surface.all_surfaces) > 0:
        for s in surface.all_surfaces:
            surface.react(s, event)
    if len(timekeeper.all_timekeepers) > 0:
        for t in timekeeper.all_timekeepers:
            timekeeper.react(t, event)


def handle_special_events():
    if len(button.all_buttons) > 0:
        for b in button.all_buttons:
            button.react(b)
    if len(slider.all_sliders) > 0:
        for s in slider.all_sliders:
            slider.react(s)
    if len(label.all_labels) > 0:
        for l in label.all_labels:
            label.react(l)
    if len(surface.all_surfaces) > 0:
        for s in surface.all_surfaces:
            surface.react(s)
    if len(timekeeper.all_timekeepers) > 0:
        for t in timekeeper.all_timekeepers:
            timekeeper.react(t)
