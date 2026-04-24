import os
import pathlib

import pygame

from easypygamewidgets import font, misc

pygame.init()


class Tooltip:
    def __init__(self,
                 widget: "easypygamewidgets.Button | easypygamewidgets.Entry | easypygamewidgets.Label | easypygamewidgets.Slider | easypygamewidgets.Surface | easypygamewidgets.Timekeeper | None" = None,
                 auto_size: bool = True, width: int = 180,
                 height: int = 80,
                 text: str = "easypygamewidgets Tooltip",
                 active_unpressed_text_color: tuple | None = None,
                 active_unpressed_background_color: tuple | None = None,
                 active_unpressed_border_color: tuple | None = None,
                 border_thickness: int = 2,
                 active_hover_cursor: pygame.Cursor = None,
                 font: pygame.font.Font = font.tooltip_font, alignment: str = "center",
                 alignment_spacing: int = 20, corner_radius: int = 25, layer=1000, style: str | None = None,
                 suppress_icon=False, icon: "pygame.Surface | easypygamewidgets.Surface | None" = None,
                 line_spacing: int = 30,
                 data=None):
        self.bindings = {}
        self.style = style
        self.icon = None
        self.layer = layer
        if not style:
            self.active_unpressed_text_color = (255, 255, 255)
            self.active_unpressed_background_color = (50, 50, 50)
            self.active_unpressed_border_color = (100, 100, 100)
        if widget:
            widget.set_tooltip(self)
        self.auto_size = auto_size
        self.width = width
        self.height = height
        self.text = text
        self.border_thickness = border_thickness
        if style == "info":
            if not icon:
                self.icon = pygame.image.load(os.path.join(pathlib.Path(__file__).resolve().parent,
                                                           "assets", "tooltip", "info.png"))
            self.active_unpressed_text_color = (255, 255, 255)
            self.active_unpressed_background_color = (46, 55, 90)
            self.active_unpressed_border_color = (39, 78, 194)
        elif style == "warning":
            if not icon:
                self.icon = pygame.image.load(os.path.join(pathlib.Path(__file__).resolve().parent,
                                                           "assets", "tooltip", "warning.png"))
            self.active_unpressed_text_color = (255, 255, 255)
            self.active_unpressed_background_color = (111, 100, 34)
            self.active_unpressed_border_color = (186, 167, 46)
        elif style == "blocked":
            if not icon:
                self.icon = pygame.image.load(os.path.join(pathlib.Path(__file__).resolve().parent,
                                                           "assets", "tooltip", "blocked.png"))
            self.active_unpressed_text_color = (255, 255, 255)
            self.active_unpressed_background_color = (150, 63, 60)
            self.active_unpressed_border_color = (188, 46, 41)
        if active_unpressed_text_color:
            self.active_unpressed_text_color = active_unpressed_text_color
            self.style = "custom"
        if active_unpressed_background_color:
            self.active_unpressed_background_color = active_unpressed_background_color
            self.style = "custom"
        if active_unpressed_border_color:
            self.active_unpressed_border_color = active_unpressed_border_color
            self.style = "custom"
        cursor_input = {
            "active_hover": active_hover_cursor
        }
        self.cursors = {}
        for name, cursor in cursor_input.items():
            if isinstance(cursor, pygame.cursors.Cursor):
                self.cursors[name] = cursor
            else:
                if cursor is not None:
                    print(
                        f"No custom cursor is used for the tooltip {self.text} because it's not a pygame.Cursor object. ({cursor})")
                self.cursors[name] = None
        self.font = font
        self.alignment = alignment
        self.alignment_spacing = alignment_spacing
        self.corner_radius = corner_radius
        self.suppress_icon = suppress_icon
        if icon:
            self.icon = icon
        self.line_spacing = line_spacing
        self.data = data
        self.x = 0
        self.y = 0
        self.pressed = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.original_cursor = None
        self.visible = False
        self.scheduled_functions = []

        self.font.set_linesize(line_spacing)

        misc.add_widget(self)

    def configure(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        if 'x' in kwargs or 'y' in kwargs or 'width' in kwargs or 'height' in kwargs:
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if 'widget' in kwargs:
            kwargs["widget"].set_tooltip(self)
        if 'layer' in kwargs:
            misc.resort_layers()
        if 'line_spacing' in kwargs:
            self.font.set_linesize(self.line_spacing)
        return self

    def config(self, **kwargs):
        self.configure(**kwargs)

    def delete(self):
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

    def show(self):
        self.visible = True
        self.trigger_event("<SHOW>")
        return self

    def hide(self):
        self.visible = False
        self.trigger_event("<HIDE>")
        return self

    def add_widget(self, widget):
        widget.set_tooltip(self)
        return self

    def remove_widget(self, widget):
        widget.set_tooltip(None)
        return self

    def schedule(self, function, frames_to_execute):
        if frames_to_execute < 1:
            frames_to_execute = 1
        self.scheduled_functions.append([function, frames_to_execute])
        return self


def draw(tooltip, surface: pygame.Surface):
    if not tooltip.visible:
        return
    tooltip.font.set_linesize(tooltip.line_spacing)
    mouse_pos = pygame.mouse.get_pos()
    is_hovering = is_point_in_rounded_rect(tooltip, mouse_pos)
    text_color = tooltip.active_unpressed_text_color
    bg_color = tooltip.active_unpressed_background_color
    brd_color = tooltip.active_unpressed_border_color

    if is_hovering:
        if tooltip.state == "enabled":
            cursor_key = "active_hover"
        target_cursor = tooltip.cursors.get(cursor_key)
        if target_cursor:
            current_cursor = pygame.mouse.get_cursor()
            if current_cursor != target_cursor:
                if tooltip.original_cursor is None:
                    tooltip.original_cursor = current_cursor
                pygame.mouse.set_cursor(target_cursor)
    else:
        if tooltip.original_cursor:
            pygame.mouse.set_cursor(tooltip.original_cursor)
            tooltip.original_cursor = None

    if is_hovering and not getattr(tooltip, "is_hovered", False):
        tooltip.is_hovered = True
        tooltip.trigger_event("<SHOW>")
    elif is_hovering and getattr(tooltip, "is_hovered", False):
        tooltip.is_hovered = True
        tooltip.trigger_event("<HOVER>")
    elif not is_hovering and getattr(tooltip, "is_hovered", False):
        tooltip.is_hovered = False
        tooltip.trigger_event("<HIDE>")

    if tooltip.auto_size:
        temp_surf = tooltip.font.render(tooltip.text, True, text_color)
        tooltip.height = temp_surf.get_height() + 20
        icon_offset = tooltip.height if tooltip.icon and not tooltip.suppress_icon else 0
        tooltip.width = temp_surf.get_width() + (tooltip.alignment_spacing * 2) + icon_offset
        tooltip.rect = pygame.Rect(tooltip.x, tooltip.y, tooltip.width, tooltip.height)

    draw_rect = tooltip.rect.move(mouse_pos[0], mouse_pos[1])

    pygame.draw.rect(surface, bg_color, draw_rect, border_radius=tooltip.corner_radius)
    icon_offset = draw_rect.height if tooltip.icon and not tooltip.suppress_icon else 0
    text_area_left = draw_rect.left + icon_offset
    text_area_width = draw_rect.width - icon_offset
    if tooltip.icon and not tooltip.suppress_icon:
        scaled_icon = pygame.transform.smoothscale(
            tooltip.icon if isinstance(tooltip.icon, pygame.Surface) else tooltip.icon.surface,
            (draw_rect.height, draw_rect.height))
        surface.blit(scaled_icon, draw_rect.topleft)
    if brd_color:
        pygame.draw.rect(surface, brd_color, draw_rect, width=tooltip.border_thickness,
                         border_radius=tooltip.corner_radius)
    if tooltip.alignment == "stretched" and len(tooltip.text) > 1 and not tooltip.auto_size:
        total_char_width = sum(tooltip.font.render(char, True, text_color).get_width() for char in tooltip.text)
        available_width = text_area_width - (tooltip.alignment_spacing * 2)
        if available_width > total_char_width:
            spacing = (available_width - total_char_width) / (len(tooltip.text) - 1)
            current_x = text_area_left + tooltip.alignment_spacing
            for char in tooltip.text:
                char_surf = tooltip.font.render(char, True, text_color)
                surface.blit(char_surf, char_surf.get_rect(midleft=(current_x, draw_rect.centery)))
                current_x += char_surf.get_width() + spacing
        else:
            text_surf = tooltip.font.render(tooltip.text, True, text_color)
            surface.blit(text_surf,
                         text_surf.get_rect(center=(text_area_left + text_area_width // 2, draw_rect.centery)))
    else:
        text_surf = tooltip.font.render(tooltip.text, True, text_color)
        text_rect = text_surf.get_rect()
        text_rect.centery = draw_rect.centery
        if tooltip.alignment == "left":
            text_rect.left = text_area_left + tooltip.alignment_spacing
        elif tooltip.alignment == "right":
            text_rect.right = draw_rect.right - tooltip.alignment_spacing
        else:
            text_rect.centerx = text_area_left + (text_area_width // 2)
        surface.blit(text_surf, text_rect)


def is_point_in_rounded_rect(tooltip, point):
    rect = tooltip.rect.move(point[0], point[1])
    if not rect.collidepoint(point): return False
    r = tooltip.corner_radius
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


def react(tooltip, event=None):
    for func in tooltip.scheduled_functions:
        func[1] -= 1
        if func[1] <= 0:
            func[0]()
            tooltip.scheduled_functions.remove(func)