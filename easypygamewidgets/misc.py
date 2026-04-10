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
        if latest_version != "26.10":
            print("An update is available. Download it now with 'pip install --upgrade easypygamewidgets'")
    except Exception as e:
        print(f"easypygamewidgets: Failed to check for updates: {e}")


def disable_update_check():
    global check_disabled
    check_disabled = True


def check_linked():
    if not isinstance(pg, pygame.Surface):
        print("Please link a pygame window first:\n    easypygamewidgets.link_pygame_window(window)")
        exit(0)


def link_pygame_window(window: pygame.Surface, layer=500):
    global pg
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
