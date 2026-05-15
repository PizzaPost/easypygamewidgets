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
                 line_spacing: int = 30, min_width: int | None = None, max_width: int | None = None,
                 min_height: int | None = None, max_height: int | None = None,
                 data=None):
        self.bindings = {}
        self.style = style
        self.icon = None
        self.layer = layer
        if not style:
            self.active_unpressed_text_color = normalize_color((255, 255, 255, 255))
            self.active_unpressed_background_color = normalize_color((50, 50, 50, 255))
            self.active_unpressed_border_color = normalize_color((100, 100, 100, 255))
        if widget:
            widget.set_tooltip(self)
        self.auto_size = auto_size
        self.width = width
        self.height = height
        if auto_size:
            if min_width:
                self.width = max(width, min_width)
            if max_width:
                self.width = min(width, max_width)
            if min_height:
                self.height = max(height, min_height)
            if max_height:
                self.height = min(height, max_height)
        self.text = text
        self.border_thickness = border_thickness
        if style == "info":
            if not icon:
                self.icon = pygame.image.load(os.path.join(pathlib.Path(__file__).resolve().parent,
                                                           "assets", "tooltip", "info.png"))
            self.active_unpressed_text_color = normalize_color((255, 255, 255, 255))
            self.active_unpressed_background_color = normalize_color((46, 55, 90, 255))
            self.active_unpressed_border_color = normalize_color((39, 78, 194, 255))
        elif style == "warning":
            if not icon:
                self.icon = pygame.image.load(os.path.join(pathlib.Path(__file__).resolve().parent,
                                                           "assets", "tooltip", "warning.png"))
            self.active_unpressed_text_color = normalize_color((255, 255, 255, 255))
            self.active_unpressed_background_color = normalize_color((111, 100, 34, 255))
            self.active_unpressed_border_color = normalize_color((186, 167, 46, 255))
        elif style == "blocked":
            if not icon:
                self.icon = pygame.image.load(os.path.join(pathlib.Path(__file__).resolve().parent,
                                                           "assets", "tooltip", "blocked.png"))
            self.active_unpressed_text_color = normalize_color((255, 255, 255, 255))
            self.active_unpressed_background_color = normalize_color((150, 63, 60, 255))
            self.active_unpressed_border_color = normalize_color((188, 46, 41, 255))

        if active_unpressed_text_color:
            self.active_unpressed_text_color = normalize_color(active_unpressed_text_color)
            self.style = "custom"
        if active_unpressed_background_color:
            self.active_unpressed_background_color = normalize_color(active_unpressed_background_color)
            self.style = "custom"
        if active_unpressed_border_color:
            self.active_unpressed_border_color = normalize_color(active_unpressed_border_color)
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
        self.min_width = min_width
        self.max_width = max_width
        self.min_height = min_height
        self.max_height = max_height
        self.data = data
        self.x = 0
        self.y = 0
        self.pressed = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.original_cursor = None
        self.visible = False
        self.scheduled_functions = []
        self.needs_redraw = True
        self.cached_surface = None

        self.font.set_linesize(line_spacing)

        misc.add_widget(self)

    def configure(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.needs_redraw = True
        if any(k in kwargs for k in
               ('auto_size', 'x', 'y', 'width', 'height', 'min_width', 'max_width', 'min_height', 'max_height')):
            if self.auto_size:
                if self.min_width:
                    self.width = max(self.width, self.min_width)
                if self.max_width:
                    self.width = min(self.width, self.max_width)
                if self.min_height:
                    self.height = max(self.height, self.min_height)
                if self.max_height:
                    self.height = min(self.height, self.max_height)
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


def normalize_color(color):
    if color is None:
        return (0, 0, 0, 0)
    if len(color) == 3:
        return (*color, 255)
    return color


def render_tooltip_surface(tooltip):
    text_color = tooltip.active_unpressed_text_color
    bg_color = tooltip.active_unpressed_background_color
    brd_color = tooltip.active_unpressed_border_color
    if tooltip.auto_size:
        temp_surf = tooltip.font.render(tooltip.text, True, text_color)
        tooltip.height = temp_surf.get_height() + 20
        icon_offset = tooltip.height if tooltip.icon and not tooltip.suppress_icon else 0
        tooltip.width = temp_surf.get_width() + (tooltip.alignment_spacing * 2) + icon_offset
        if tooltip.min_width:
            tooltip.width = max(tooltip.width, tooltip.min_width)
        if tooltip.max_width:
            tooltip.width = min(tooltip.width, tooltip.max_width)
        if tooltip.min_height:
            tooltip.height = max(tooltip.height, tooltip.min_height)
        if tooltip.max_height:
            tooltip.height = min(tooltip.height, tooltip.max_height)
        tooltip.rect = pygame.Rect(tooltip.x, tooltip.y, tooltip.width, tooltip.height)
    cached = pygame.Surface((tooltip.width, tooltip.height), pygame.SRCALPHA)
    local_rect = pygame.Rect(0, 0, tooltip.width, tooltip.height)
    tmp = pygame.Surface(pygame.Rect(local_rect).size, pygame.SRCALPHA)
    pygame.draw.rect(tmp, bg_color, tmp.get_rect(), border_radius=tooltip.corner_radius)
    cached.blit(tmp, local_rect)
    icon_offset = local_rect.height if tooltip.icon and not tooltip.suppress_icon else 0
    text_area_left = icon_offset
    text_area_width = local_rect.width - icon_offset
    if tooltip.icon and not tooltip.suppress_icon:
        scaled_icon = pygame.transform.smoothscale(tooltip.icon if isinstance(tooltip.icon, pygame.Surface)
                                                   else tooltip.icon.surface, (local_rect.height,
                                                                               local_rect.height))
        cached.blit(scaled_icon, (0, 0))
    if brd_color:
        tmp = pygame.Surface(pygame.Rect(local_rect).size, pygame.SRCALPHA)
        pygame.draw.rect(tmp, brd_color, tmp.get_rect(), width=tooltip.border_thickness,
                         border_radius=tooltip.corner_radius)
        cached.blit(tmp, local_rect)
    if tooltip.alignment == "stretched" and len(tooltip.text) > 1 and not tooltip.auto_size:
        total_char_width = sum(tooltip.font.render(char, True, text_color).get_width() for char in tooltip.text)
        available_width = text_area_width - (tooltip.alignment_spacing * 2)
        if available_width > total_char_width:
            spacing = (available_width - total_char_width) / (len(tooltip.text) - 1)
            current_x = text_area_left + tooltip.alignment_spacing
            for char in tooltip.text:
                char_surf = tooltip.font.render(char, True, text_color)
                char_surf.set_alpha(text_color[3])
                cached.blit(char_surf, char_surf.get_rect(midleft=(current_x, local_rect.centery)))
                current_x += char_surf.get_width() + spacing
        else:
            text_surf = tooltip.font.render(tooltip.text, True, text_color)
            text_surf.set_alpha(text_color[3])
            cached.blit(text_surf,
                        text_surf.get_rect(center=(text_area_left + text_area_width // 2, local_rect.centery)))
    else:
        text_surf = tooltip.font.render(tooltip.text, True, text_color)
        text_surf.set_alpha(text_color[3])
        text_rect = text_surf.get_rect()
        text_rect.centery = local_rect.centery
        if tooltip.alignment == "left":
            text_rect.left = text_area_left + tooltip.alignment_spacing
        elif tooltip.alignment == "right":
            text_rect.right = local_rect.right - tooltip.alignment_spacing
        else:
            text_rect.centerx = text_area_left + (text_area_width // 2)
        cached.blit(text_surf, text_rect)
    tooltip.cached_surface = cached
    tooltip.needs_redraw = False


def draw(tooltip, surface: pygame.Surface):
    if not tooltip.visible:
        return
    tooltip.font.set_linesize(tooltip.line_spacing)
    mouse_pos = pygame.mouse.get_pos()
    is_hovering = is_point_in_rounded_rect(tooltip, mouse_pos)
    if tooltip.needs_redraw or tooltip.cached_surface is None:
        render_tooltip_surface(tooltip)
    if is_hovering:
        cursor_key = "active_hover"
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

    draw_rect = tooltip.rect.move(mouse_pos[0], mouse_pos[1])
    surface.blit(tooltip.cached_surface, draw_rect)


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