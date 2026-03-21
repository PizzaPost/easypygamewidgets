import time

import pygame

pygame.init()

all_surfaces = []


class Surface:
    def __init__(self, surface: pygame.Surface, screen: "easypygamewidgets.Screen | None" = None,
                 state: str = "enabled",
                 active_hover_cursor: pygame.Cursor = None,
                 disabled_hover_cursor: pygame.Cursor = None,
                 active_pressed_cursor: pygame.Cursor = None, dragable: bool = False):
        self.surface = surface
        if screen:
            screen.add_widget(self)
            self.screen = screen
        else:
            self.screen = None
            self.visible = True
            self.state = state
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
                        f"No custom cursor is used for the surface {self.text} because it's not a pygame.Cursor object. ({cursor})")
                self.cursors[name] = None
        self.dragable = dragable
        self.x = 0
        self.y = 0
        self.alive = True
        self.pressed = False
        self.rect = surface.get_rect()
        self.original_cursor = None
        self.drag_offset = None
        self.is_dragging = False
        self.last_checked_dragging = None
        self.bindings = {}

        all_surfaces.append(self)

    def configure(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        if 'x' in kwargs or 'y' in kwargs or 'surface' in kwargs:
            self.rect = pygame.Rect(self.x, self.y, self.surface.get_width(), self.surface.get_height())
        if 'screen' in kwargs:
            self.set_screen(kwargs["screen"])
        return self

    def config(self, **kwargs):
        self.configure(**kwargs)

    def delete(self):
        self.alive = False
        if self in all_surfaces:
            all_surfaces.remove(self)

    def place(self, x: int, y: int):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.surface.get_width(), self.surface.get_height())
        return self

    def bind(self, event: str, command, require_hover: bool = True):
        self.bindings[event] = {"command": command, "require_hover": require_hover}
        return self

    def trigger_event(self, event: str, *args, **kwargs):
        if event in self.bindings:
            binding_data = self.bindings[event]
            command = binding_data["command"]
            require_hover = binding_data["require_hover"]
            if not require_hover or self.rect.collidepoint(pygame.mouse.get_pos()):
                command(*args, **kwargs)

    def set_screen(self, screen):
        if self.screen:
            if self in screen.widgets:
                self.screen.widgets.remove(self)
        self.screen = screen
        screen.add_widget(self)
        return self

    def unbind(self, event: str):
        if event in self.bindings:
            del self.bindings[event]
        return self

    def unbind_all(self):
        self.bindings.clear()
        return self


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

    if is_hovering and not getattr(surface, "is_hovered", False):
        surface.is_hovered = True
        surface.trigger_event("<MOUSE-IN>")
    elif is_hovering and getattr(surface, "is_hovered", False):
        surface.is_hovered = True
        surface.trigger_event("<HOVER>")
    elif not is_hovering and getattr(surface, "is_hovered", False):
        surface.is_hovered = False
        surface.trigger_event("<MOUSE-OUT>")

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
    current_time = time.time()
    if not event:
        if pygame.mouse.get_pressed()[0] and is_inside:
            surface.pressed = True
            surface.trigger_event("<HOLD>")
        elif not pygame.mouse.get_pressed()[0] and is_inside:
            if surface.pressed:
                surface.pressed = False
                surface.trigger_event("<RELEASE>")
        elif not pygame.mouse.get_pressed()[0] and not is_inside:
            surface.pressed = False
    else:
        if event.type == pygame.MOUSEMOTION:
            if surface.pressed and surface.dragable:
                if is_inside or surface.is_dragging:
                    surface.is_dragging = True
                    surface.last_checked_dragging = current_time
                    if surface.drag_offset:
                        new_x = mouse_pos[0] - surface.drag_offset[0] - offset_x
                        new_y = mouse_pos[1] - surface.drag_offset[1] - offset_y
                        surface.place(new_x, new_y)
        if event.type == pygame.KEYDOWN:
            surface.trigger_event("<KEY>")
            if event.unicode:
                surface.trigger_event(event.unicode)
            keyname = pygame.key.name(event.key)
            surface.trigger_event(f"<{keyname.upper()}>")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and is_inside:
                surface.pressed = True
                surface.drag_offset = (mouse_pos[0] - (surface.x + offset_x), mouse_pos[1] - (surface.y + offset_y))
                surface.trigger_event("<PRESS>")
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and is_inside and surface.pressed:
                surface.pressed = False
                surface.is_dragging = False
                surface.trigger_event("<RELEASE>")
    if surface.last_checked_dragging:
        if current_time - surface.last_checked_dragging > 0.2:
            surface.is_dragging = False
    if surface.pressed and not surface.is_dragging:
        surface.trigger_event("<HOLD>")
    if surface.pressed and surface.is_dragging:
        surface.trigger_event("<DRAG>")
