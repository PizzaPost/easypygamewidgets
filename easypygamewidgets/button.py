import pygame

from easypygamewidgets import fonts

pygame.init()

all_buttons = []


class Button:
    def __init__(self, screen: "easypygamewidgets.Screen | None" = None, auto_size: bool = True, width: int = 180,
                 height: int = 80,
                 text: str = "easypygamewidgets Button",
                 state: str = "enabled",
                 active_unpressed_text_color: tuple = (255, 255, 255),
                 disabled_unpressed_text_color: tuple = (150, 150, 150),
                 active_hover_text_color: tuple = (255, 255, 255),
                 disabled_hover_text_color: tuple = (150, 150, 150),
                 active_pressed_text_color: tuple = (200, 200, 200),
                 active_unpressed_background_color: tuple = (50, 50, 50),
                 disabled_unpressed_background_color: tuple = (30, 30, 30),
                 active_hover_background_color: tuple = (70, 70, 70),
                 disabled_hover_background_color: tuple = (30, 30, 30),
                 active_pressed_background_color: tuple = (40, 40, 40),
                 active_unpressed_border_color: tuple = (100, 100, 100),
                 disabled_unpressed_border_color: tuple = (60, 60, 60),
                 active_hover_border_color: tuple = (150, 150, 150),
                 disabled_hover_border_color: tuple = (60, 60, 60),
                 active_pressed_border_color: tuple = (50, 50, 50),
                 border_thickness: int = 2,
                 active_hover_cursor: pygame.Cursor = None,
                 disabled_hover_cursor: pygame.Cursor = None,
                 active_pressed_cursor: pygame.Cursor = None,
                 font: pygame.font.Font = fonts.default_font, alignment: str = "center",
                 command=None, alignment_spacing: int = 20, corner_radius: int = 25):
        self.bindings = {}
        if screen:
            screen.add_widget(self)
            self.screen = screen
        else:
            self.screen = None
        self.auto_size = auto_size
        self.width = width
        self.height = height
        self.text = text
        self.state = state
        self.active_unpressed_text_color = active_unpressed_text_color
        self.disabled_unpressed_text_color = disabled_unpressed_text_color
        self.active_hover_text_color = active_hover_text_color
        self.disabled_hover_text_color = disabled_hover_text_color
        self.active_pressed_text_color = active_pressed_text_color
        self.active_unpressed_background_color = active_unpressed_background_color
        self.disabled_unpressed_background_color = disabled_unpressed_background_color
        self.active_hover_background_color = active_hover_background_color
        self.disabled_hover_background_color = disabled_hover_background_color
        self.active_pressed_background_color = active_pressed_background_color
        self.active_unpressed_border_color = active_unpressed_border_color
        self.disabled_unpressed_border_color = disabled_unpressed_border_color
        self.active_hover_border_color = active_hover_border_color
        self.disabled_hover_border_color = disabled_hover_border_color
        self.active_pressed_border_color = active_pressed_border_color
        self.border_thickness = border_thickness
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
                        f"No custom cursor is used for the button {self.text} because it's not a pygame.Cursor object. ({cursor})")
                self.cursors[name] = None
        self.font = font
        self.alignment = alignment
        if command:
            self.bind("<RELEASE>", command)
        self.alignment_spacing = alignment_spacing
        self.corner_radius = corner_radius
        self.x = 0
        self.y = 0
        self.alive = True
        self.pressed = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.original_cursor = None
        self.visible = True

        all_buttons.append(self)

    def configure(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        if 'x' in kwargs or 'y' in kwargs or 'width' in kwargs or 'height' in kwargs:
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if 'screen' in kwargs:
            self.set_screen(kwargs["screen"])

    def config(self, **kwargs):
        self.configure(**kwargs)

    def delete(self):
        self.alive = False
        if self in all_buttons:
            all_buttons.remove(self)

    def place(self, x: int, y: int):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return self

    def bind(self, event: str, command):
        if event not in self.bindings:
            self.bindings[event] = []
        self.bindings[event].append(command)
        return self

    def trigger_event(self, event: str, *args, **kwargs):
        if event in self.bindings:
            for command in self.bindings[event]:
                command(*args, **kwargs)

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


def draw(button, surface: pygame.Surface):
    if not button.alive or not button.visible:
        return
    mouse_pos = pygame.mouse.get_pos()
    is_hovering = is_point_in_rounded_rect(button, mouse_pos)
    if button.state == "enabled":
        if button.pressed and is_hovering:
            text_color = button.active_pressed_text_color
            bg_color = button.active_pressed_background_color
            brd_color = button.active_pressed_border_color
        elif is_hovering:
            text_color = button.active_hover_text_color
            bg_color = button.active_hover_background_color
            brd_color = button.active_hover_border_color
        else:
            text_color = button.active_unpressed_text_color
            bg_color = button.active_unpressed_background_color
            brd_color = button.active_unpressed_border_color
    else:
        if is_hovering:
            text_color = button.disabled_hover_text_color
            bg_color = button.disabled_hover_background_color
            brd_color = button.disabled_hover_border_color
        else:
            text_color = button.disabled_unpressed_text_color
            bg_color = button.disabled_unpressed_background_color
            brd_color = button.disabled_unpressed_border_color

    if is_hovering:
        if button.state == "enabled":
            if button.pressed:
                cursor_key = "active_pressed"
            else:
                cursor_key = "active_hover"
        else:
            cursor_key = "disabled_hover"
        target_cursor = button.cursors.get(cursor_key)
        if target_cursor:
            current_cursor = pygame.mouse.get_cursor()
            if current_cursor != target_cursor:
                if button.original_cursor is None:
                    button.original_cursor = current_cursor
                pygame.mouse.set_cursor(target_cursor)
    else:
        if button.original_cursor:
            pygame.mouse.set_cursor(button.original_cursor)
            button.original_cursor = None

    if is_hovering and not getattr(button, "is_hovered", False):
        button.is_hovered = True
        button.trigger_event("<MOUSE-IN>")
    elif is_hovering and getattr(button, "is_hovered", False):
        button.is_hovered = True
        button.trigger_event("<HOVER>")
    elif not is_hovering and getattr(button, "is_hovered", False):
        button.is_hovered = False
        button.trigger_event("<MOUSE-OUT>")

    if button.auto_size:
        temp_surf = button.font.render(button.text, True, text_color)
        button.width = temp_surf.get_width() + 40 + (button.alignment_spacing - 20)
        button.height = temp_surf.get_height() + 20
        button.rect = pygame.Rect(button.x, button.y, button.width, button.height)

    offset_x, offset_y = get_screen_offset(button)
    draw_rect = button.rect.move(offset_x, offset_y)

    pygame.draw.rect(surface, bg_color, draw_rect, border_radius=button.corner_radius)
    if brd_color:
        pygame.draw.rect(surface, brd_color, draw_rect, width=button.border_thickness,
                         border_radius=button.corner_radius)
    if button.alignment == "stretched" and len(button.text) > 1 and not button.auto_size:
        total_char_width = sum(button.font.render(char, True, text_color).get_width() for char in button.text)
        available_width = draw_rect.width - (button.alignment_spacing * 2)
        if available_width > total_char_width:
            spacing = (available_width - total_char_width) / (len(button.text) - 1)
            current_x = draw_rect.left + button.alignment_spacing
            for char in button.text:
                char_surf = button.font.render(char, True, text_color)
                surface.blit(char_surf, char_surf.get_rect(midleft=(current_x, draw_rect.centery)))
                current_x += char_surf.get_width() + spacing
        else:
            text_surf = button.font.render(button.text, True, text_color)
            surface.blit(text_surf, text_surf.get_rect(center=draw_rect.center))
    else:
        text_surf = button.font.render(button.text, True, text_color)
        text_rect = text_surf.get_rect()
        if button.alignment == "left":
            text_rect.midleft = (draw_rect.left + button.alignment_spacing, draw_rect.centery)
        elif button.alignment == "right":
            text_rect.midright = (draw_rect.right - button.alignment_spacing, draw_rect.centery)
        else:
            text_rect.center = draw_rect.center
        surface.blit(text_surf, text_rect)


def is_point_in_rounded_rect(button, point):
    offset_x, offset_y = get_screen_offset(button)
    rect = button.rect.move(offset_x, offset_y)
    if not rect.collidepoint(point): return False
    r = button.corner_radius
    r = min(r, rect.width // 2, rect.height // 2)
    if r <= 0: return True
    x, y = point
    if (rect.left + r <= x <= rect.right - r) or (rect.top + r <= y <= rect.bottom - r):
        return True
    centers = [(rect.left + r, rect.top + r), (rect.right - r, rect.top + r),
               (rect.left + r, rect.bottom - r), (rect.right - r, rect.bottom - r)]
    for cx, cy in centers:
        if ((x - cx) ** 2 + (y - cy) ** 2) <= r ** 2: return True
    return False


def react(button, event=None):
    if button.state != "enabled" or not button.visible:
        button.pressed = False
        return
    mouse_pos = pygame.mouse.get_pos()
    is_inside = is_point_in_rounded_rect(button, mouse_pos)
    if not event:
        if pygame.mouse.get_pressed()[0] and is_inside:
            button.pressed = True
            button.trigger_event("<HOLD>")
        elif not pygame.mouse.get_pressed()[0] and is_inside:
            if button.pressed:
                button.pressed = False
                button.trigger_event("<RELEASE>")
        elif not pygame.mouse.get_pressed()[0] and not is_inside:
            button.pressed = False
    else:
        if event.type == pygame.KEYDOWN and is_inside:
            button.trigger_event("<KEY>")
            if event.unicode:
                button.trigger_event(event.unicode)
            keyname = pygame.key.name(event.key)
            button.trigger_event(f"<{keyname.upper()}>")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and is_inside:
                button.pressed = True
                button.trigger_event("<PRESS>")
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and is_inside and button.pressed:
                button.pressed = False
                button.trigger_event("<RELEASE>")
