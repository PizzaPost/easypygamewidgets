import time

import pygame

pygame.init()

all_surfaces = []


class Surface:
    def __init__(self, surface: pygame.Surface, screen: "easypygamewidgets.Screen | None" = None,
                 state: str = "enabled",
                 click_sound: str | pygame.mixer.Sound = None,
                 hold_sound: str | pygame.mixer.Sound = None,
                 release_sound: str | pygame.mixer.Sound = None,
                 active_hover_cursor: pygame.cursors = None,
                 disabled_hover_cursor: pygame.cursors = None,
                 active_pressed_cursor: pygame.cursors = None,
                 click_command=None, hold_command=None, release_command=None,
                 holdable: bool = False):
        self.surface = surface
        if screen:
            screen.add_widget(self)
            self.screen = screen
        else:
            self.screen = None
        self.state = state
        if click_sound:
            if isinstance(click_sound, pygame.mixer.Sound):
                self.click_sound = click_sound
            else:
                self.click_sound = pygame.mixer.Sound(click_sound)
        else:
            self.click_sound = None
        if hold_sound:
            if isinstance(hold_sound, pygame.mixer.Sound):
                self.hold_sound = hold_sound
            else:
                self.hold_sound = pygame.mixer.Sound(hold_sound)
        else:
            self.hold_sound = None
        if release_sound:
            if isinstance(release_sound, pygame.mixer.Sound):
                self.release_sound = release_sound
            else:
                self.release_sound = pygame.mixer.Sound(release_sound)
        else:
            self.release_sound = None
        cursor_input = {
            "active_hover": active_hover_cursor,
            "disabled_hover": disabled_hover_cursor,
            "active_pressed": active_pressed_cursor
        }
        self.cursors = {}
        for name, cursor in cursor_input.items():
            if isinstance(cursor, pygame.cursors.Cursor):
                self.cursors[name] = cursor
            else:
                if cursor is not None:
                    print(
                        f"No custom cursor is used for the surface {self.text} because it's not a pygame.cursors.Cursor object. ({cursor})")
                self.cursors[name] = None
        self.click_command = click_command
        self.hold_command = hold_command
        self.release_command = release_command
        self.holdable = holdable
        self.x = 0
        self.y = 0
        self.alive = True
        self.pressed = False
        self.rect = surface.get_rect()
        self.original_cursor = None
        self.visible = True
        self.hold_sound_started = None
        self.hold_sound_length = None

        all_surfaces.append(self)

    def configure(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        if 'x' in kwargs or 'y' in kwargs or 'surface' in kwargs:
            self.rect = self.surface.get_rect()

    def config(self, **kwargs):
        self.configure(**kwargs)

    def delete(self):
        self.alive = False
        if self in all_surfaces:
            all_surfaces.remove(self)

    def place(self, x: int, y: int):
        self.x = x
        self.y = y
        self.rect = self.surface.get_rect()
        return self

    def execute_click(self):
        if self.click_command:
            self.click_command()
        return self

    def execute_hold(self):
        if self.hold_command:
            self.hold_command()
        return self

    def execute_release(self):
        if self.release_command:
            self.release_command()
        return self

    def play_click_sound(self):
        if self.click_sound:
            self.click_sound.play()
        return self

    def play_hold_sound(self):
        if self.hold_sound:
            self.hold_sound.play()
        return self

    def play_release_sound(self):
        if self.release_sound:
            self.release_sound.play()
        return self

    def add_screen(self, screen):
        self.screen = screen
        if not self in screen.widgets:
            screen.widgets.append(self)


def get_screen_offset(widget):
    if widget.screen:
        return widget.screen.x, widget.screen.y
    return 0, 0


def draw(surface, window: pygame.Surface):
    if not surface.alive or not surface.visible:
        return
    mouse_pos = pygame.mouse.get_pos()
    offset_x, offset_y = get_screen_offset(surface)
    interaction_rect = surface.rect.move(offset_x, offset_y)
    is_hovering = interaction_rect.collidepoint(mouse_pos)
    if is_hovering:
        if surface.state == "enabled":
            if surface.pressed:
                cursor_key = "active_pressed"
            else:
                cursor_key = "active_hover"
        else:
            cursor_key = "disabled_hover"
        target_cursor = surface.cursors.get(cursor_key)
        if target_cursor:
            current_cursor = pygame.mouse.get_cursor()
            if current_cursor != target_cursor:
                if surface.original_cursor is None:
                    surface.original_cursor = current_cursor
                pygame.mouse.set_cursor(target_cursor)
    else:
        if surface.original_cursor:
            pygame.mouse.set_cursor(surface.original_cursor)
            surface.original_cursor = None

    offset_x, offset_y = get_screen_offset(surface)
    draw_rect = surface.rect.move(offset_x, offset_y)
    window.blit(surface.surface, draw_rect)


def react(surface, event=None):
    if surface.state != "enabled" or not surface.visible:
        surface.pressed = False
        return
    mouse_pos = pygame.mouse.get_pos()
    offset_x, offset_y = get_screen_offset(surface)
    interaction_rect = surface.rect.move(offset_x, offset_y)
    is_inside = interaction_rect.collidepoint(mouse_pos)
    if not event:
        if pygame.mouse.get_pressed()[0] and is_inside:
            surface.pressed = True
            if surface.holdable:
                if surface.hold_command: surface.hold_command()
                if surface.hold_sound:
                    if surface.hold_sound_started:
                        if surface.hold_sound_started + surface.hold_sound_length > time.time():
                            return
                    surface.hold_sound.play()
                    surface.hold_sound_length = surface.hold_sound.get_length()
                    surface.hold_sound_started = time.time()
        elif not pygame.mouse.get_pressed()[0] and is_inside:
            if surface.pressed:
                surface.pressed = False
                if surface.release_command: surface.release_command()
                if surface.release_sound: surface.release_sound.play()
        elif not pygame.mouse.get_pressed()[0] and not is_inside:
            surface.pressed = False
    else:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and is_inside:
                surface.pressed = True
                if surface.click_command: surface.click_command()
                if surface.click_sound: surface.click_sound.play()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and is_inside and surface.pressed:
                surface.pressed = False
                if surface.release_command: surface.release_command()
                if surface.release_sound: surface.release_sound.play()
