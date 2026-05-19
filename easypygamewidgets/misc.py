# misc.py
# by PizzaPost
# https://github.com/PizzaPost/pywidgets

import ctypes

import pygame
import requests

pg = None
check_disabled = False
all_widgets = []


def check_update():
    global check_disabled
    if check_disabled: return
    url = "https://raw.githubusercontent.com/PizzaPost/pywidgets/master/info.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        latest_version = data["version"]
        current_version = "26.20"
        if latest_version != current_version:
            print(f"An update is available. Download it now with 'pip install --upgrade easypygamewidgets'\n"
                  f"You're currently on: {current_version}\n"
                  f"The newest version is: {latest_version}")
    except Exception as e:
        print(f"easypygamewidgets: Failed to check for updates: {e}")


def disable_update_check():
    global check_disabled
    check_disabled = True


def check_linked():
    if not isinstance(pg, pygame.Surface):
        print("Please link a pygame window first:\n    easypygamewidgets.link_pygame_window(window)")
        exit(0)


def check_pygame_version():
    try:
        import pygame
        if not hasattr(pygame, "IS_CE"): raise ImportError
    except ImportError:
        print("[INFO] easypygamewidgets 26.9+ requires 'pygame-ce'.\n"
              "Existing 'pygame' installation detected. You have four ways to resolve this:\n"
              "1. Update to Python 3.14+ and install pygame-ce:\n"
              "     pip install pygame-ce\n"
              "2. Replace pygame with pygame-ce (recommended):\n"
              "     pip uninstall pygame && pip install pygame-ce\n"
              "3. Isolation: Use a virtual environment (venv) for this project.\n"
              "4. Legacy: Roll back to an older version of this library:\n"
              "     pip install 'easypygamewidgets<=26.8' --force-reinstall")
        exit(1)


def link_pygame_window(window: pygame.Surface, layer=500):
    global pg
    check_pygame_version()
    check_update()
    pg = window
    all_widgets.append((pg, layer))


def add_widget(widget):
    all_widgets.append(widget)
    resort_layers()


def create_pygame_layer(function, layer):
    all_widgets.append((function, layer))
    resort_layers()


def resort_layers():
    all_widgets.sort(key=lambda w: w[1] if isinstance(w, tuple) else w.layer)


def set_appearance_mode(mode):
    hwnd = pygame.display.get_wm_info()["window"]
    tmp = ctypes.c_int(mode)
    ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, ctypes.byref(tmp), ctypes.sizeof(tmp))