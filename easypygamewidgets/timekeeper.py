import math
import time

import pygame

from easypygamewidgets import font, misc

pygame.init()


class Timekeeper:
    def __init__(self, screen: "easypygamewidgets.Screen | None" = None, auto_size: bool = True, width: int = 180,
                 height: int = 80, start_at: float | int = 60, end_at: float | int | None = None,
                 show_milliseconds: bool = False, show_seconds: bool = True,
                 show_minutes: bool = False, smart_minutes: bool = True, show_hours: bool = False,
                 smart_hours: bool = True,
                 state: str = "enabled",
                 active_unpressed_text_color: tuple = (255, 255, 255),
                 disabled_unpressed_text_color: tuple = (150, 150, 150),
                 active_hover_text_color: tuple = (255, 255, 255),
                 disabled_hover_text_color: tuple = (150, 150, 150),
                 active_pressed_text_color: tuple = (200, 200, 200),
                 active_unpressed_background_color: tuple = (50, 50, 50),
                 disabled_unpressed_background_color: tuple = (30, 30, 30),
                 active_hover_background_color: tuple = (50, 50, 50),
                 disabled_hover_background_color: tuple = (30, 30, 30),
                 active_pressed_background_color: tuple = (40, 40, 40),
                 active_unpressed_border_color: tuple = (100, 100, 100),
                 disabled_unpressed_border_color: tuple = (60, 60, 60),
                 active_hover_border_color: tuple = (100, 100, 100),
                 disabled_hover_border_color: tuple = (60, 60, 60),
                 active_pressed_border_color: tuple = (50, 50, 50),
                 border_thickness: int = 2,
                 active_hover_cursor: pygame.Cursor = None,
                 disabled_hover_cursor: pygame.Cursor = None,
                 active_pressed_cursor: pygame.Cursor = None,
                 font: pygame.font.Font = font.default_font, alignment: str = "center",
                 alignment_spacing: int = 20, corner_radius: int = 14, ticking: bool = False,
                 type_order: list[str] = ("h", ":", "m", ":", "s", ".", "ms"), reversed: bool = False, layer=1000):
        if screen:
            screen.add_widget(self)
            self.screen = screen
        else:
            self.screen = None
            self.visible = True
            self.state = state
        self.auto_size = auto_size
        self.width = width
        self.height = height
        self.start_at = start_at
        self.end_at = end_at
        self.show_milliseconds = show_milliseconds
        self.show_seconds = show_seconds
        self.show_minutes = show_minutes
        self.smart_minutes = smart_minutes
        self.show_hours = show_hours
        self.smart_hours = smart_hours
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
                        f"No custom cursor is used for the timekeeper {self.text} because it's not a pygame.Cursor object. ({cursor})")
                self.cursors[name] = None
        self.font = font
        self.alignment = alignment
        self.alignment_spacing = alignment_spacing
        self.corner_radius = corner_radius
        self.ticking = ticking
        self.type_order = type_order
        self.reversed = reversed
        self.layer = layer
        self.x = 0
        self.y = 0
        self.alive = True
        self.pressed = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.original_cursor = None
        self.last_updated = None
        self.is_negative = False
        self.bindings = {}

        split_to_values(self, start_at)

        misc.add_widget(self)

    def configure(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        if 'x' in kwargs or 'y' in kwargs or 'width' in kwargs or 'height' in kwargs:
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if 'screen' in kwargs:
            self.set_screen(kwargs["screen"])
        return self

    def config(self, **kwargs):
        self.configure(**kwargs)

    def delete(self):
        self.alive = False
        if self in misc.all_widgets:
            misc.all_widgets.remove(self)

    def place(self, x: int, y: int):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return self

    def bind(self, event: str, command, require_hover: bool = True):
        self.bindings[event] = {"command": command, "require_hover": require_hover}
        return self

    def trigger_event(self, event: str, *args, **kwargs):
        if event in self.bindings:
            binding_data = self.bindings[event]
            command = binding_data["command"]
            require_hover = binding_data["require_hover"]
            if not require_hover or is_point_in_rounded_rect(self, pygame.mouse.get_pos()):
                command(*args, **kwargs)

    def get_display_text(self):
        values = {
            "ms": self.milliseconds if self.show_milliseconds else None,
            "s": self.seconds if self.show_seconds else None,
            "m": self.minutes if (self.show_minutes or (self.smart_minutes and self.minutes != 0)) else None,
            "h": self.hours if (self.show_hours or (self.smart_hours and self.hours != 0)) else None,
        }
        parts = []
        pending_sep = None
        for token in self.type_order:
            if token in values:
                value = values[token]
                if value is not None:
                    if pending_sep and parts:
                        parts.append(pending_sep)
                    if token == "ms":
                        ms_int = int(round(value, 4) * 100) % 100
                        parts.append(f"{ms_int:02}")
                    else:
                        parts.append(f"{value:02}")
                    pending_sep = None
            else:
                pending_sep = token
        display_str = "".join(parts)
        if self.is_negative:
            display_str = "-" + display_str
        return display_str

    def set(self, milliseconds=0, seconds=0, minutes=0, hours=0):
        split_to_values(self, hours * 3600 + minutes * 60 + seconds + milliseconds / 1000)
        return self

    def stop(self):
        self.ticking = False
        return self

    def resume(self):
        self.ticking = True
        return self

    def start(self):
        self.ticking = True
        return self

    def reset(self):
        split_to_values(self, self.start_at)
        return self

    def add(self, amount):
        sign = -1 if self.is_negative else 1
        curr = ((self.hours * 3600) + (self.minutes * 60) + self.seconds + self.milliseconds) * sign
        curr += amount
        split_to_values(self, curr)
        return self

    def subtract(self, amount):
        sign = -1 if self.is_negative else 1
        curr = ((self.hours * 3600) + (self.minutes * 60) + self.seconds + self.milliseconds) * sign
        curr -= amount
        split_to_values(self, curr)
        return self

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


def split_to_values(widget, total_seconds):
    base_seconds = math.floor(total_seconds)
    widget.is_negative = base_seconds < 0
    abs_secs = abs(base_seconds)
    widget.hours = int(abs_secs // 3600)
    widget.minutes = int((abs_secs % 3600) // 60)
    widget.seconds = int(abs_secs % 60)
    widget.milliseconds = abs(total_seconds) - int(abs(abs_secs))


def draw(timekeeper, surface: pygame.Surface):
    if not timekeeper.alive or not timekeeper.visible:
        return
    offset_x, offset_y = get_screen_offset(timekeeper)
    mouse_pos = pygame.mouse.get_pos()
    is_hovering = is_point_in_rounded_rect(timekeeper, mouse_pos)
    if timekeeper.state == "enabled":
        if timekeeper.pressed and is_hovering:
            text_color = timekeeper.active_pressed_text_color
            bg_color = timekeeper.active_pressed_background_color
            brd_color = timekeeper.active_pressed_border_color
        elif is_hovering:
            text_color = timekeeper.active_hover_text_color
            bg_color = timekeeper.active_hover_background_color
            brd_color = timekeeper.active_hover_border_color
        else:
            text_color = timekeeper.active_unpressed_text_color
            bg_color = timekeeper.active_unpressed_background_color
            brd_color = timekeeper.active_unpressed_border_color
    else:
        if is_hovering:
            text_color = timekeeper.disabled_hover_text_color
            bg_color = timekeeper.disabled_hover_background_color
            brd_color = timekeeper.disabled_hover_border_color
        else:
            text_color = timekeeper.disabled_unpressed_text_color
            bg_color = timekeeper.disabled_unpressed_background_color
            brd_color = timekeeper.disabled_unpressed_border_color

    if is_hovering:
        if timekeeper.state == "enabled":
            if timekeeper.pressed:
                cursor_key = "active_pressed"
            else:
                cursor_key = "active_hover"
        else:
            cursor_key = "disabled_hover"
        target_cursor = timekeeper.cursors.get(cursor_key)
        if target_cursor:
            current_cursor = pygame.mouse.get_cursor()
            if current_cursor != target_cursor:
                if timekeeper.original_cursor is None:
                    timekeeper.original_cursor = current_cursor
                pygame.mouse.set_cursor(target_cursor)
    else:
        if timekeeper.original_cursor:
            pygame.mouse.set_cursor(timekeeper.original_cursor)
            timekeeper.original_cursor = None

    if is_hovering and not getattr(timekeeper, "is_hovered", False):
        timekeeper.is_hovered = True
        timekeeper.trigger_event("<MOUSE-IN>")
    elif is_hovering and getattr(timekeeper, "is_hovered", False):
        timekeeper.is_hovered = True
        timekeeper.trigger_event("<HOVER>")
    elif not is_hovering and getattr(timekeeper, "is_hovered", False):
        timekeeper.is_hovered = False
        timekeeper.trigger_event("<MOUSE-OUT>")

    display_text = timekeeper.get_display_text()
    if timekeeper.auto_size:
        text_w = timekeeper.font.size(display_text)[0]
        exact_w = text_w + (timekeeper.alignment_spacing * 2)
        timekeeper.rect.width = (exact_w + 39) // 40 * 40
        timekeeper.rect.height = (timekeeper.font.size(display_text)[1] + 39) // 40 * 40
    draw_rect = timekeeper.rect.move(offset_x, offset_y)
    pygame.draw.rect(surface, bg_color, draw_rect, border_radius=timekeeper.corner_radius)
    if timekeeper.border_thickness > 0:
        pygame.draw.rect(surface, brd_color, draw_rect, width=timekeeper.border_thickness,
                         border_radius=timekeeper.corner_radius)
    old_clip = surface.get_clip()
    clip_rect = draw_rect.inflate(-4, -4)
    surface.set_clip(clip_rect)
    y_pos = draw_rect.centery
    drawn_stretched = False
    if timekeeper.alignment == "stretched" and len(display_text) > 1 and not timekeeper.auto_size:
        total_char_width = sum(timekeeper.font.render(char, True, text_color).get_width() for char in display_text)
        available_width = draw_rect.width - (timekeeper.alignment_spacing * 2)
        if available_width > total_char_width:
            drawn_stretched = True
            spacing = (available_width - total_char_width) / (len(display_text) - 1)
            current_x = draw_rect.left + timekeeper.alignment_spacing
            for char in display_text:
                char_surf = timekeeper.font.render(char, True, text_color)
                surface.blit(char_surf, char_surf.get_rect(midleft=(current_x, y_pos)))
                current_x += char_surf.get_width() + spacing
    if not drawn_stretched:
        text_surf = timekeeper.font.render(display_text, True, text_color)
        text_rect = text_surf.get_rect()
        if timekeeper.alignment == "left":
            text_rect.midleft = (draw_rect.left + timekeeper.alignment_spacing, y_pos)
        elif timekeeper.alignment == "right":
            text_rect.midright = (draw_rect.right - timekeeper.alignment_spacing, y_pos)
        else:
            text_rect.center = draw_rect.center
        surface.blit(text_surf, text_rect)
        timekeeper.last_text_x = text_rect.x
        surface.set_clip(old_clip)


def is_point_in_rounded_rect(timekeeper, point):
    offset_x, offset_y = get_screen_offset(timekeeper)
    rect = timekeeper.rect.move(offset_x, offset_y)
    if not rect.collidepoint(point): return False
    r = timekeeper.corner_radius
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


def react(timekeeper, event=None):
    if timekeeper.state != "enabled" or not timekeeper.visible:
        return
    is_inside = is_point_in_rounded_rect(timekeeper, pygame.mouse.get_pos())
    if event:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and is_inside:
            timekeeper.trigger_event("<PRESS>")
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and is_inside:
            timekeeper.trigger_event("<RELEASE>")
        elif event.type == pygame.KEYDOWN:
            timekeeper.trigger_event("<KEY>")
            if event.unicode:
                timekeeper.trigger_event(event.unicode)
            keyname = pygame.key.name(event.key)
            timekeeper.trigger_event(f"<{keyname.upper()}>")
    else:
        if timekeeper.ticking:
            now = time.time()
            if not timekeeper.last_updated:
                timekeeper.last_updated = now
            dt = now - timekeeper.last_updated
            timekeeper.last_updated = now
            sign = -1 if timekeeper.is_negative else 1
            curr = ((timekeeper.hours * 3600) + (
                    timekeeper.minutes * 60) + timekeeper.seconds + timekeeper.milliseconds) * sign
            change = -dt if timekeeper.reversed else dt
            next_value = curr + change
            if timekeeper.end_at is not None:
                reached_limit = False
                if not timekeeper.reversed and next_value >= timekeeper.end_at and not timekeeper.start_at > timekeeper.end_at:
                    reached_limit = True
                elif timekeeper.reversed and next_value <= timekeeper.end_at and not timekeeper.start_at < timekeeper.end_at:
                    reached_limit = True
                if reached_limit:
                    split_to_values(timekeeper, timekeeper.end_at)
                    timekeeper.stop()
                    timekeeper.trigger_event("<FINISHED>")
                    return
            split_to_values(timekeeper, next_value)
