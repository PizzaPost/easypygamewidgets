import pygame

pygame.init()

all_surfaces = []


class Surface:
    def __init__(self, surface: pygame.Surface, screen: "easypygamewidgets.Screen | None" = None,
                 state: str = "enabled",
                 active_hover_cursor: pygame.Cursor = None,
                 disabled_hover_cursor: pygame.Cursor = None,
                 active_pressed_cursor: pygame.Cursor = None):
        self.surface = surface
        if screen:
            screen.add_widget(self)
            self.screen = screen
        else:
            self.screen = None
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
        self.x = 0
        self.y = 0
        self.alive = True
        self.pressed = False
        self.rect = surface.get_rect()
        self.original_cursor = None
        self.visible = True
        self.bindings = {}

        all_surfaces.append(self)

    def configure(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        if 'x' in kwargs or 'y' in kwargs or 'surface' in kwargs:
            self.rect = self.surface.get_rect()
        if 'screen' in kwargs:
            self.set_screen(kwargs["screen"])

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

    def bind(self, event: str, command):
        if event not in self.bindings:
            self.bindings[event] = []
        self.bindings[event] = command
        return self

    def trigger_event(self, event: str, *args, **kwargs):
        if event in self.bindings:
            self.bindings[event](*args, **kwargs)

    def set_screen(self, screen):
        if self.screen:
            if self in screen.widgets:
                self.screen.widgets.remove(self)
        self.screen = screen
        screen.add_widget(self)


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
        if event.type == pygame.KEYDOWN and is_inside:
            surface.trigger_event("<KEY>")
            if event.unicode:
                surface.trigger_event(event.unicode)
            keyname = pygame.key.name(event.key)
            surface.trigger_event(f"<{keyname.upper()}>")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and is_inside:
                surface.pressed = True
                surface.trigger_event("<PRESS>")
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and is_inside and surface.pressed:
                surface.pressed = False
                surface.trigger_event("<RELEASE>")
