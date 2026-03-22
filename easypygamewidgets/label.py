import time

import pygame

from easypygamewidgets import font, misc

pygame.init()


class Label:
    def __init__(self, screen: "easypygamewidgets.Screen | None" = None, auto_size: bool = True, width: int = 180,
                 height: int = 80,
                 text: str = "easypygamewidgets Label", state="enabled",
                 active_hover_text_color: tuple = (255, 255, 255),
                 active_hover_text_color_alpha: int = 255,
                 active_hover_shadow_color: tuple = (50, 50, 50),
                 active_hover_shadow_color_alpha: int = 200,
                 active_hover_background_color: tuple | None = None,
                 active_hover_background_color_alpha: int = 255,
                 active_hover_underline_color: tuple | None = None,
                 active_hover_underline_color_alpha: int = 255,
                 active_hover_strikethrough_color: tuple | None = None,
                 active_hover_strikethrough_color_alpha: int = 255,
                 active_hover_border_color: tuple = (),
                 active_hover_border_color_alpha: int = 255,
                 active_pressed_text_color: tuple = (255, 255, 255),
                 active_pressed_text_color_alpha: int = 255,
                 active_pressed_shadow_color: tuple = (50, 50, 50),
                 active_pressed_shadow_color_alpha: int = 200,
                 active_pressed_background_color: tuple | None = None,
                 active_pressed_background_color_alpha: int = 255,
                 active_pressed_underline_color: tuple | None = None,
                 active_pressed_underline_color_alpha: int = 255,
                 active_pressed_strikethrough_color: tuple | None = None,
                 active_pressed_strikethrough_color_alpha: int = 255,
                 active_pressed_border_color: tuple = (),
                 active_pressed_border_color_alpha: int = 255,
                 active_unpressed_text_color: tuple = (255, 255, 255),
                 active_unpressed_text_color_alpha: int = 255,
                 active_unpressed_shadow_color: tuple = (50, 50, 50),
                 active_unpressed_shadow_color_alpha: int = 200,
                 active_unpressed_background_color: tuple | None = None,
                 active_unpressed_background_color_alpha: int = 255,
                 active_unpressed_underline_color: tuple | None = None,
                 active_unpressed_underline_color_alpha: int = 255,
                 active_unpressed_strikethrough_color: tuple | None = None,
                 active_unpressed_strikethrough_color_alpha: int = 255,
                 active_unpressed_border_color: tuple = (),
                 active_unpressed_border_color_alpha: int = 255,
                 disabled_hover_text_color: tuple = (150, 150, 150),
                 disabled_hover_text_color_alpha: int = 255,
                 disabled_hover_shadow_color: tuple = (50, 50, 50),
                 disabled_hover_shadow_color_alpha: int = 200,
                 disabled_hover_background_color: tuple | None = None,
                 disabled_hover_background_color_alpha: int = 255,
                 disabled_hover_underline_color: tuple | None = None,
                 disabled_hover_underline_color_alpha: int = 255,
                 disabled_hover_strikethrough_color: tuple | None = None,
                 disabled_hover_strikethrough_color_alpha: int = 255,
                 disabled_hover_border_color: tuple = (),
                 disabled_hover_border_color_alpha: int = 255,
                 disabled_unpressed_text_color: tuple = (150, 150, 150),
                 disabled_unpressed_text_color_alpha: int = 255,
                 disabled_unpressed_shadow_color: tuple = (50, 50, 50),
                 disabled_unpressed_shadow_color_alpha: int = 200,
                 disabled_unpressed_background_color: tuple | None = None,
                 disabled_unpressed_background_color_alpha: int = 255,
                 disabled_unpressed_underline_color: tuple | None = None,
                 disabled_unpressed_underline_color_alpha: int = 255,
                 disabled_unpressed_strikethrough_color: tuple | None = None,
                 disabled_unpressed_strikethrough_color_alpha: int = 255,
                 disabled_unpressed_border_color: tuple = (),
                 disabled_unpressed_border_color_alpha: int = 255,
                 border_thickness: int = 2,
                 active_hover_cursor: pygame.Cursor = None,
                 disabled_hover_cursor: pygame.Cursor = None,
                 active_pressed_cursor: pygame.Cursor = None,
                 font: pygame.font.Font = font.default_font, alignment: str = "center",
                 alignment_spacing: int = 20, dragable: bool = False, top_left_corner_radius: int = 25,
                 top_right_corner_radius: int = 25, bottom_left_corner_radius: int = 25,
                 bottom_right_corner_radius: int = 25, layer=1000):
        tmp = font.render(text, True, (255, 255, 255))
        if screen:
            screen.add_widget(self)
            self.screen = screen
        else:
            self.screen = None
            self.visible = True
            self.state = state
        self.strikethrough = False
        self.underline = False
        self.auto_size = auto_size
        if auto_size:
            self.width = tmp.get_width() + 40 + (alignment_spacing - 20)
            self.height = tmp.get_height() + 20
        else:
            self.width = width
            self.height = height
        self.text = text
        self.active_hover_text_color = active_hover_text_color
        self.active_hover_text_color_alpha = active_hover_text_color_alpha
        self.active_hover_shadow_color = active_hover_shadow_color
        self.active_hover_shadow_color_alpha = active_hover_shadow_color_alpha
        self.active_hover_background_color = active_hover_background_color
        self.active_hover_background_color_alpha = active_hover_background_color_alpha
        if active_hover_underline_color:
            self.active_hover_underline_color = active_hover_underline_color
            self.underline = True
        else:
            self.active_hover_underline_color = active_hover_text_color
        self.active_hover_underline_color_alpha = active_hover_underline_color_alpha
        if active_hover_strikethrough_color:
            self.active_hover_strikethrough_color = active_hover_strikethrough_color
            self.strikethrough = True
        else:
            self.active_hover_strikethrough_color = active_hover_text_color
        self.active_hover_strikethrough_color_alpha = active_hover_strikethrough_color_alpha
        self.active_hover_border_color = active_hover_border_color
        self.active_hover_border_color_alpha = active_hover_border_color_alpha
        self.active_pressed_text_color = active_pressed_text_color
        self.active_pressed_text_color_alpha = active_pressed_text_color_alpha
        self.active_pressed_shadow_color = active_pressed_shadow_color
        self.active_pressed_shadow_color_alpha = active_pressed_shadow_color_alpha
        self.active_pressed_background_color = active_pressed_background_color
        self.active_pressed_background_color_alpha = active_pressed_background_color_alpha
        if active_pressed_underline_color:
            self.active_pressed_underline_color = active_pressed_underline_color
            self.underline = True
        else:
            self.active_pressed_underline_color = active_pressed_text_color
        self.active_pressed_underline_color_alpha = active_pressed_underline_color_alpha
        if active_pressed_strikethrough_color:
            self.active_pressed_strikethrough_color = active_pressed_strikethrough_color
            self.strikethrough = True
        else:
            self.active_pressed_strikethrough_color = active_pressed_text_color
        self.active_pressed_strikethrough_color_alpha = active_pressed_strikethrough_color_alpha
        self.active_pressed_border_color = active_pressed_border_color
        self.active_pressed_border_color_alpha = active_pressed_border_color_alpha
        self.active_unpressed_text_color = active_unpressed_text_color
        self.active_unpressed_text_color_alpha = active_unpressed_text_color_alpha
        self.active_unpressed_shadow_color = active_unpressed_shadow_color
        self.active_unpressed_shadow_color_alpha = active_unpressed_shadow_color_alpha
        self.active_unpressed_background_color = active_unpressed_background_color
        self.active_unpressed_background_color_alpha = active_unpressed_background_color_alpha
        if active_unpressed_underline_color:
            self.active_unpressed_underline_color = active_unpressed_underline_color
            self.underline = True
        else:
            self.active_unpressed_underline_color = active_unpressed_text_color
        self.active_unpressed_underline_color_alpha = active_unpressed_underline_color_alpha
        if active_unpressed_strikethrough_color:
            self.active_unpressed_strikethrough_color = active_unpressed_strikethrough_color
            self.strikethrough = True
        else:
            self.active_unpressed_strikethrough_color = active_unpressed_text_color
        self.active_unpressed_strikethrough_color_alpha = active_unpressed_strikethrough_color_alpha
        self.active_unpressed_border_color = active_unpressed_border_color
        self.active_unpressed_border_color_alpha = active_unpressed_border_color_alpha
        self.disabled_hover_text_color = disabled_hover_text_color
        self.disabled_hover_text_color_alpha = disabled_hover_text_color_alpha
        self.disabled_hover_shadow_color = disabled_hover_shadow_color
        self.disabled_hover_shadow_color_alpha = disabled_hover_shadow_color_alpha
        self.disabled_hover_background_color = disabled_hover_background_color
        self.disabled_hover_background_color_alpha = disabled_hover_background_color_alpha
        if disabled_hover_underline_color:
            self.disabled_hover_underline_color = disabled_hover_underline_color
            self.underline = True
        else:
            self.disabled_hover_underline_color = disabled_hover_text_color
        self.disabled_hover_underline_color_alpha = disabled_hover_underline_color_alpha
        if disabled_hover_strikethrough_color:
            self.disabled_hover_strikethrough_color = disabled_hover_strikethrough_color
            self.strikethrough = True
        else:
            self.disabled_hover_strikethrough_color = disabled_hover_text_color
        self.disabled_hover_strikethrough_color_alpha = disabled_hover_strikethrough_color_alpha
        self.disabled_hover_border_color = disabled_hover_border_color
        self.disabled_hover_border_color_alpha = disabled_hover_border_color_alpha
        self.disabled_unpressed_text_color = disabled_unpressed_text_color
        self.disabled_unpressed_text_color_alpha = disabled_unpressed_text_color_alpha
        self.disabled_unpressed_shadow_color = disabled_unpressed_shadow_color
        self.disabled_unpressed_shadow_color_alpha = disabled_unpressed_shadow_color_alpha
        self.disabled_unpressed_background_color = disabled_unpressed_background_color
        self.disabled_unpressed_background_color_alpha = disabled_unpressed_background_color_alpha
        if disabled_unpressed_underline_color:
            self.disabled_unpressed_underline_color = disabled_unpressed_underline_color
            self.underline = True
        else:
            self.disabled_unpressed_underline_color = disabled_unpressed_text_color
        self.disabled_unpressed_underline_color_alpha = disabled_unpressed_underline_color_alpha
        if disabled_unpressed_strikethrough_color:
            self.disabled_unpressed_strikethrough_color = disabled_unpressed_strikethrough_color
            self.strikethrough = True
        else:
            self.disabled_unpressed_strikethrough_color = disabled_unpressed_text_color
        self.disabled_unpressed_strikethrough_color_alpha = disabled_unpressed_strikethrough_color_alpha
        self.disabled_unpressed_border_color = disabled_unpressed_border_color
        self.disabled_unpressed_border_color_alpha = disabled_unpressed_border_color_alpha
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
                        f"No custom cursor is used for the label {self.text} because it's not a pygame.Cursor object. ({cursor})")
                self.cursors[name] = None
        self.font = font
        self.alignment = alignment
        self.alignment_spacing = alignment_spacing
        self.dragable = dragable
        self.top_left_corner_radius = top_left_corner_radius
        self.top_right_corner_radius = top_right_corner_radius
        self.bottom_left_corner_radius = bottom_left_corner_radius
        self.bottom_right_corner_radius = bottom_right_corner_radius
        self.layer = layer
        self.x = 0
        self.y = 0
        self.alive = True
        self.pressed = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.original_cursor = None
        self.drag_offset = None
        self.is_dragging = False
        self.last_checked_dragging = None
        self.bindings = {}

        misc.add_widget(self)

    def configure(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        if 'x' in kwargs or 'y' in kwargs or 'width' in kwargs or 'height' in kwargs or 'text' in kwargs:
            tmp = self.font.render(self.text, True, (255, 255, 255))
            self.rect = pygame.Rect(self.x, self.y, tmp.get_width(), tmp.get_height())
            self.width = self.rect.width + 40 + (self.alignment_spacing - 20)
            self.height = self.rect.height + 20
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

    def set_screen(self, screen):
        if self.screen:
            if self in screen.widgets:
                self.screen.widgets.remove(self)
        self.screen = screen
        screen.add_widget(self)
        return self

    def set_strikethrough(self, value: bool):
        self.strikethrough = value
        return self

    def set_underline(self, value: bool):
        self.underline = value
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


def combine_color_with_alpha(rgb, alpha):
    if not rgb: return None
    return (*rgb, alpha)


def draw(label, surface: pygame.Surface):
    if not label.alive or not label.visible:
        return
    mouse_pos = pygame.mouse.get_pos()
    is_hovering = is_point_in_rounded_rect(label, mouse_pos)
    if label.state == "enabled":
        if label.pressed:
            text_color = label.active_pressed_text_color
            bg_color = label.active_pressed_background_color
            shadow_color = label.active_pressed_shadow_color
            underline_color = label.active_pressed_underline_color
            strikethrough_color = label.active_pressed_strikethrough_color
            brd_color = label.active_pressed_border_color
            text_color_alpha = label.active_pressed_text_color_alpha
            bg_color_alpha = label.active_pressed_background_color_alpha
            shadow_color_alpha = label.active_pressed_shadow_color_alpha
            underline_color_alpha = label.active_pressed_underline_color_alpha
            strikethrough_color_alpha = label.active_pressed_strikethrough_color_alpha
            brd_color_alpha = label.active_pressed_border_color_alpha
        elif is_hovering:
            text_color = label.active_hover_text_color
            bg_color = label.active_hover_background_color
            shadow_color = label.active_hover_shadow_color
            underline_color = label.active_hover_underline_color
            strikethrough_color = label.active_hover_strikethrough_color
            brd_color = label.active_hover_border_color
            text_color_alpha = label.active_hover_text_color_alpha
            bg_color_alpha = label.active_hover_background_color_alpha
            shadow_color_alpha = label.active_hover_shadow_color_alpha
            underline_color_alpha = label.active_hover_underline_color_alpha
            strikethrough_color_alpha = label.active_hover_strikethrough_color_alpha
            brd_color_alpha = label.active_hover_border_color_alpha
        else:
            text_color = label.active_unpressed_text_color
            bg_color = label.active_unpressed_background_color
            shadow_color = label.active_unpressed_shadow_color
            underline_color = label.active_unpressed_underline_color
            strikethrough_color = label.active_unpressed_strikethrough_color
            brd_color = label.active_unpressed_border_color
            text_color_alpha = label.active_unpressed_text_color_alpha
            bg_color_alpha = label.active_unpressed_background_color_alpha
            shadow_color_alpha = label.active_unpressed_shadow_color_alpha
            underline_color_alpha = label.active_unpressed_underline_color_alpha
            strikethrough_color_alpha = label.active_unpressed_strikethrough_color_alpha
            brd_color_alpha = label.active_unpressed_border_color_alpha
    else:
        if is_hovering:
            text_color = label.disabled_hover_text_color
            bg_color = label.disabled_hover_background_color
            shadow_color = label.disabled_hover_shadow_color
            underline_color = label.disabled_hover_underline_color
            strikethrough_color = label.disabled_hover_strikethrough_color
            brd_color = label.disabled_hover_border_color
            text_color_alpha = label.disabled_hover_text_color_alpha
            bg_color_alpha = label.disabled_hover_background_color_alpha
            shadow_color_alpha = label.disabled_hover_shadow_color_alpha
            underline_color_alpha = label.disabled_hover_underline_color_alpha
            strikethrough_color_alpha = label.disabled_hover_strikethrough_color_alpha
            brd_color_alpha = label.disabled_hover_border_color_alpha
        else:
            text_color = label.disabled_unpressed_text_color
            bg_color = label.disabled_unpressed_background_color
            shadow_color = label.disabled_unpressed_shadow_color
            underline_color = label.disabled_unpressed_underline_color
            strikethrough_color = label.disabled_unpressed_strikethrough_color
            brd_color = label.disabled_unpressed_border_color
            text_color_alpha = label.disabled_unpressed_text_color_alpha
            bg_color_alpha = label.disabled_unpressed_background_color_alpha
            shadow_color_alpha = label.disabled_unpressed_shadow_color_alpha
            underline_color_alpha = label.disabled_unpressed_underline_color_alpha
            strikethrough_color_alpha = label.disabled_unpressed_strikethrough_color_alpha
            brd_color_alpha = label.disabled_unpressed_border_color_alpha

    text_color = combine_color_with_alpha(text_color, text_color_alpha)
    bg_color = combine_color_with_alpha(bg_color, bg_color_alpha)
    shadow_color = combine_color_with_alpha(shadow_color, shadow_color_alpha)
    underline_color = combine_color_with_alpha(underline_color, underline_color_alpha)
    strikethrough_color = combine_color_with_alpha(strikethrough_color, strikethrough_color_alpha)
    brd_color = combine_color_with_alpha(brd_color, brd_color_alpha)

    if is_hovering:
        if label.state == "enabled":
            if label.pressed:
                cursor_key = "active_pressed"
            else:
                cursor_key = "active_hover"
        else:
            cursor_key = "disabled_hover"
        target_cursor = label.cursors.get(cursor_key)
        if target_cursor:
            current_cursor = pygame.mouse.get_cursor()
            if current_cursor != target_cursor:
                if label.original_cursor is None:
                    label.original_cursor = current_cursor
                pygame.mouse.set_cursor(target_cursor)
    else:
        if label.original_cursor:
            pygame.mouse.set_cursor(label.original_cursor)
            label.original_cursor = None

    if is_hovering and not getattr(label, "is_hovered", False):
        label.is_hovered = True
        label.trigger_event("<MOUSE-IN>")
    elif is_hovering and getattr(label, "is_hovered", False):
        label.is_hovered = True
        label.trigger_event("<HOVER>")
    elif not is_hovering and getattr(label, "is_hovered", False):
        label.is_hovered = False
        label.trigger_event("<MOUSE-OUT>")

    if label.auto_size:
        temp_surf = label.font.render(label.text, True, text_color)
        label.width = temp_surf.get_width() + 40 + (label.alignment_spacing - 20)
        label.height = temp_surf.get_height() + 20
        label.rect = pygame.Rect(label.x, label.y, label.width, label.height)

    offset_x, offset_y = get_screen_offset(label)
    draw_rect = label.rect.move(offset_x, offset_y)

    draw_req_rect = pygame.Rect(0, 0, draw_rect.width, draw_rect.height)
    if bg_color:
        shape_surf = pygame.Surface((draw_rect.width, draw_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, bg_color, draw_req_rect,
                         border_top_left_radius=label.top_left_corner_radius,
                         border_top_right_radius=label.top_right_corner_radius,
                         border_bottom_left_radius=label.bottom_left_corner_radius,
                         border_bottom_right_radius=label.bottom_right_corner_radius)
        shape_surf.set_alpha(bg_color[3])
        surface.blit(shape_surf, draw_rect)
    if brd_color:
        shape_surf = pygame.Surface((draw_rect.width, draw_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, brd_color, draw_req_rect, width=label.border_thickness,
                         border_top_left_radius=label.top_left_corner_radius,
                         border_top_right_radius=label.top_right_corner_radius,
                         border_bottom_left_radius=label.bottom_left_corner_radius,
                         border_bottom_right_radius=label.bottom_right_corner_radius)
        shape_surf.set_alpha(bg_color[3])
        surface.blit(shape_surf, draw_rect)

    def render_text_line(txt, color, rect_ref, offset=(0, 0)):
        cx, cy = rect_ref.centerx + offset[0], rect_ref.centery + offset[1]
        if label.alignment == "stretched" and len(txt) > 1 and not label.auto_size:
            total_char_width = sum(label.font.render(char, True, color).get_width() for char in txt)
            available_width = rect_ref.width - (label.alignment_spacing * 2)
            if available_width > total_char_width:
                spacing = (available_width - total_char_width) / (len(txt) - 1)
                current_x = rect_ref.left + label.alignment_spacing + offset[0]
                for char in txt:
                    char_surf = label.font.render(char, True, color)
                    char_surf.set_alpha(color[3])
                    char_rect = char_surf.get_rect(midleft=(current_x, cy))
                    surface.blit(char_surf, char_rect)
                    current_x += char_surf.get_width() + spacing
                return pygame.Rect(rect_ref.left + label.alignment_spacing + offset[0],
                                   rect_ref.top + offset[1], available_width, rect_ref.height)
            txt_surf = label.font.render(txt, True, color)
            txt_rect = txt_surf.get_rect(center=(cx, cy))
        else:
            txt_surf = label.font.render(txt, True, color)
            txt_rect = txt_surf.get_rect()
            if label.alignment == "left":
                txt_rect.midleft = (rect_ref.left + label.alignment_spacing + offset[0], cy)
            elif label.alignment == "right":
                txt_rect.midright = (rect_ref.right - label.alignment_spacing + offset[0], cy)
            else:
                txt_rect.center = (cx, cy)
        txt_surf.set_alpha(color[3])
        surface.blit(txt_surf, txt_rect)
        return txt_rect

    if shadow_color and shadow_color[3] > 0:
        render_text_line(label.text, shadow_color, draw_rect, offset=(2, 2))
    final_text_rect = render_text_line(label.text, text_color, draw_rect)
    if final_text_rect:
        if underline_color and label.underline:
            shape_surf = pygame.Surface(final_text_rect.size, pygame.SRCALPHA)
            shape_surf_rect = shape_surf.get_rect()
            start_pos = (shape_surf_rect.left, shape_surf_rect.bottom - 2)
            end_pos = (shape_surf_rect.right, shape_surf_rect.bottom - 2)
            shape_surf.set_alpha(underline_color[3])
            pygame.draw.line(shape_surf, underline_color, start_pos, end_pos, 2)
            surface.blit(shape_surf, final_text_rect)
        if strikethrough_color and label.strikethrough:
            shape_surf = pygame.Surface(final_text_rect.size, pygame.SRCALPHA)
            shape_surf_rect = shape_surf.get_rect()
            start_pos = (shape_surf_rect.left, shape_surf_rect.centery)
            end_pos = (shape_surf_rect.right, shape_surf_rect.centery)
            shape_surf.set_alpha(strikethrough_color[3])
            pygame.draw.line(shape_surf, strikethrough_color, start_pos, end_pos, 2)
            surface.blit(shape_surf, final_text_rect)


def is_point_in_rounded_rect(label, point):
    offset_x, offset_y = get_screen_offset(label)
    rect = label.rect.move(offset_x, offset_y)
    if not rect.collidepoint(point): return False
    max_r = max(label.top_left_corner_radius, label.top_right_corner_radius,
                label.bottom_left_corner_radius, label.bottom_right_corner_radius)
    if (rect.left + max_r <= point[0] <= rect.right - max_r) or \
            (rect.top + max_r <= point[1] <= rect.bottom - max_r):
        return True
    x, y = point
    if x < rect.left + label.top_left_corner_radius and y < rect.top + label.top_left_corner_radius:
        cx, cy = rect.left + label.top_left_corner_radius, rect.top + label.top_left_corner_radius
        return (x - cx) ** 2 + (y - cy) ** 2 <= label.top_left_corner_radius ** 2
    if x > rect.right - label.top_right_corner_radius and y < rect.top + label.top_right_corner_radius:
        cx, cy = rect.right - label.top_right_corner_radius, rect.top + label.top_right_corner_radius
        return (x - cx) ** 2 + (y - cy) ** 2 <= label.top_right_corner_radius ** 2
    if x < rect.left + label.bottom_left_corner_radius and y > rect.bottom - label.bottom_left_corner_radius:
        cx, cy = rect.left + label.bottom_left_corner_radius, rect.bottom - label.bottom_left_corner_radius
        return (x - cx) ** 2 + (y - cy) ** 2 <= label.bottom_left_corner_radius ** 2
    if x > rect.right - label.bottom_right_corner_radius and y > rect.bottom - label.bottom_right_corner_radius:
        cx, cy = rect.right - label.bottom_right_corner_radius, rect.bottom - label.bottom_right_corner_radius
        return (x - cx) ** 2 + (y - cy) ** 2 <= label.bottom_right_corner_radius ** 2
    return True


def react(label, event=None):
    if label.state != "enabled" or not label.visible:
        label.pressed = False
        return
    current_time = time.time()
    mouse_pos = pygame.mouse.get_pos()
    is_inside = is_point_in_rounded_rect(label, mouse_pos)
    screen_off_x, screen_off_y = get_screen_offset(label)
    if event:
        if event.type == pygame.KEYDOWN:
            label.trigger_event("<KEY>")
            if event.unicode:
                label.trigger_event(event.unicode)
            keyname = pygame.key.name(event.key)
            label.trigger_event(f"<{keyname.upper()}>")
        if event.type == pygame.MOUSEMOTION:
            if label.pressed and label.dragable:
                if is_inside or label.is_dragging:
                    label.is_dragging = True
                    label.last_checked_dragging = current_time
                    if label.drag_offset:
                        new_x = mouse_pos[0] - label.drag_offset[0] - screen_off_x
                        new_y = mouse_pos[1] - label.drag_offset[1] - screen_off_y
                        label.place(new_x, new_y)
        elif event.type == pygame.MOUSEBUTTONDOWN and is_inside:
            if event.button == 1:
                label.pressed = True
                label.drag_offset = (mouse_pos[0] - (label.x + screen_off_x), mouse_pos[1] - (label.y + screen_off_y))
                label.trigger_event("<PRESS>")
        elif event.type == pygame.MOUSEBUTTONUP and is_inside:
            if event.button == 1:
                label.pressed = False
                label.is_dragging = False
                label.trigger_event("<RELEASE>")
    if label.last_checked_dragging:
        if current_time - label.last_checked_dragging > 0.2:
            label.is_dragging = False
    if label.pressed and not label.is_dragging:
        label.trigger_event("<HOLD>")
    if label.pressed and label.is_dragging:
        label.trigger_event("<DRAG>")
