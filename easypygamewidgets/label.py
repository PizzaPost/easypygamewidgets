import time

import pygame

from easypygamewidgets import font, misc

pygame.init()


class Label:
    def __init__(self, screen: "easypygamewidgets.Screen | None" = None, auto_size: bool = True, width: int = 180,
                 height: int = 80,
                 text: str = "easypygamewidgets Label", state="enabled",
                 active_hover_text_color: tuple | None = (255, 255, 255, 255),
                 active_hover_shadow_color: tuple | None = (50, 50, 50, 200),
                 active_hover_background_color: tuple | None = None,
                 active_hover_underline_color: tuple | None = None,
                 active_hover_strikethrough_color: tuple | None = None,
                 active_hover_border_color: tuple | None = None,
                 active_pressed_text_color: tuple | None = (255, 255, 255, 255),
                 active_pressed_shadow_color: tuple | None = (50, 50, 50, 200),
                 active_pressed_background_color: tuple | None = None,
                 active_pressed_underline_color: tuple | None = None,
                 active_pressed_strikethrough_color: tuple | None = None,
                 active_pressed_border_color: tuple | None = None,
                 active_unpressed_text_color: tuple | None = (255, 255, 255, 255),
                 active_unpressed_shadow_color: tuple | None = (50, 50, 50, 200),
                 active_unpressed_background_color: tuple | None = None,
                 active_unpressed_underline_color: tuple | None = None,
                 active_unpressed_strikethrough_color: tuple | None = None,
                 active_unpressed_border_color: tuple | None = None,
                 disabled_hover_text_color: tuple | None = (150, 150, 150, 255),
                 disabled_hover_shadow_color: tuple | None = (50, 50, 50, 200),
                 disabled_hover_background_color: tuple | None = None,
                 disabled_hover_underline_color: tuple | None = None,
                 disabled_hover_strikethrough_color: tuple | None = None,
                 disabled_hover_border_color: tuple | None = None,
                 disabled_unpressed_text_color: tuple | None = (150, 150, 150, 255),
                 disabled_unpressed_shadow_color: tuple | None = (50, 50, 50, 200),
                 disabled_unpressed_background_color: tuple | None = None,
                 disabled_unpressed_underline_color: tuple | None = None,
                 disabled_unpressed_strikethrough_color: tuple | None = None,
                 disabled_unpressed_border_color: tuple | None = None,
                 border_thickness: int = 2,
                 active_hover_cursor: pygame.Cursor = None,
                 disabled_hover_cursor: pygame.Cursor = None,
                 active_pressed_cursor: pygame.Cursor = None,
                 font: pygame.font.Font = font.default_font, alignment: str = "center",
                 alignment_spacing: int = 20, dragable: bool = False, top_left_corner_radius: int = 25,
                 top_right_corner_radius: int = 25, bottom_left_corner_radius: int = 25,
                 bottom_right_corner_radius: int = 25, layer=1000, line_spacing=30,
                 tooltip: "easypygamewidgets.Tooltip | None" = None, data=None):
        font.set_linesize(line_spacing)
        lines = str(text).split("\n")
        max_w = max((font.render(line, True, (255, 255, 255)).get_width() for line in lines), default=0)
        total_h = sum(font.render(line, True, (255, 255, 255)).get_height() for line in lines)
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
            self.width = max_w + 40 + (alignment_spacing - 20)
            self.height = total_h + 20
        else:
            self.width = width + alignment_spacing
            self.height = height
        self.text = text

        self.active_hover_text_color = normalize_color(active_hover_text_color)
        self.active_hover_shadow_color = normalize_color(active_hover_shadow_color)
        self.active_hover_background_color = normalize_color(active_hover_background_color)
        if active_hover_underline_color:
            self.active_hover_underline_color = normalize_color(active_hover_underline_color)
            self.underline = True
        else:
            self.active_hover_underline_color = self.active_hover_text_color
        if active_hover_strikethrough_color:
            self.active_hover_strikethrough_color = normalize_color(active_hover_strikethrough_color)
            self.strikethrough = True
        else:
            self.active_hover_strikethrough_color = self.active_hover_text_color
        self.active_hover_border_color = normalize_color(active_hover_border_color)

        self.active_pressed_text_color = normalize_color(active_pressed_text_color)
        self.active_pressed_shadow_color = normalize_color(active_pressed_shadow_color)
        self.active_pressed_background_color = normalize_color(active_pressed_background_color)
        if active_pressed_underline_color:
            self.active_pressed_underline_color = normalize_color(active_pressed_underline_color)
            self.underline = True
        else:
            self.active_pressed_underline_color = self.active_pressed_text_color
        if active_pressed_strikethrough_color:
            self.active_pressed_strikethrough_color = normalize_color(active_pressed_strikethrough_color)
            self.strikethrough = True
        else:
            self.active_pressed_strikethrough_color = self.active_pressed_text_color
        self.active_pressed_border_color = normalize_color(active_pressed_border_color)

        self.active_unpressed_text_color = normalize_color(active_unpressed_text_color)
        self.active_unpressed_shadow_color = normalize_color(active_unpressed_shadow_color)
        self.active_unpressed_background_color = normalize_color(active_unpressed_background_color)
        if active_unpressed_underline_color:
            self.active_unpressed_underline_color = normalize_color(active_unpressed_underline_color)
            self.underline = True
        else:
            self.active_unpressed_underline_color = self.active_unpressed_text_color
        if active_unpressed_strikethrough_color:
            self.active_unpressed_strikethrough_color = normalize_color(active_unpressed_strikethrough_color)
            self.strikethrough = True
        else:
            self.active_unpressed_strikethrough_color = self.active_unpressed_text_color
        self.active_unpressed_border_color = normalize_color(active_unpressed_border_color)

        self.disabled_hover_text_color = normalize_color(disabled_hover_text_color)
        self.disabled_hover_shadow_color = normalize_color(disabled_hover_shadow_color)
        self.disabled_hover_background_color = normalize_color(disabled_hover_background_color)
        if disabled_hover_underline_color:
            self.disabled_hover_underline_color = normalize_color(disabled_hover_underline_color)
            self.underline = True
        else:
            self.disabled_hover_underline_color = self.disabled_hover_text_color
        if disabled_hover_strikethrough_color:
            self.disabled_hover_strikethrough_color = normalize_color(disabled_hover_strikethrough_color)
            self.strikethrough = True
        else:
            self.disabled_hover_strikethrough_color = self.disabled_hover_text_color
        self.disabled_hover_border_color = normalize_color(disabled_hover_border_color)

        self.disabled_unpressed_text_color = normalize_color(disabled_unpressed_text_color)
        self.disabled_unpressed_shadow_color = normalize_color(disabled_unpressed_shadow_color)
        self.disabled_unpressed_background_color = normalize_color(disabled_unpressed_background_color)
        if disabled_unpressed_underline_color:
            self.disabled_unpressed_underline_color = normalize_color(disabled_unpressed_underline_color)
            self.underline = True
        else:
            self.disabled_unpressed_underline_color = self.disabled_unpressed_text_color
        if disabled_unpressed_strikethrough_color:
            self.disabled_unpressed_strikethrough_color = normalize_color(disabled_unpressed_strikethrough_color)
            self.strikethrough = True
        else:
            self.disabled_unpressed_strikethrough_color = self.disabled_unpressed_text_color
        self.disabled_unpressed_border_color = normalize_color(disabled_unpressed_border_color)

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
        self.tooltip = tooltip
        if tooltip:
            tooltip.configure(layer=self.layer + 1)
            if not tooltip.style:
                if not self.active_unpressed_background_color:
                    bg_color = (50, 50, 50, 255)
                if not self.active_unpressed_border_color:
                    bd_color = (100, 100, 100, 255)
                tooltip.configure(active_unpressed_text_color=self.active_unpressed_text_color,
                                  active_unpressed_background_color=self.active_unpressed_background_color if self.active_unpressed_background_color else bg_color,
                                  active_unpressed_border_color=self.active_unpressed_border_color if self.active_unpressed_border_color else bd_color)
        self.line_spacing = line_spacing
        self.data = data
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
        self.needs_redraw = True
        self.needs_transform = True
        self.last_visual_state = None
        self.original_surface = None
        self.surface = None
        self.target_scale = 1
        self.current_scale = 1
        self.scale_step = 0
        self.target_rotation = 0
        self.current_rotation = 0
        self.rotation_step = 0
        self.target_offset = (0, 0)
        self.current_offset = [0, 0]
        self.offset_step = [0, 0]
        self.use_rotozoom = False
        self.scheduled_functions = []

        misc.add_widget(self)

    def configure(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.needs_redraw = True
        layout_keys = ('x', 'y', 'width', 'height', 'text', 'line_spacing', 'font', 'alignment_spacing', 'auto_size')
        if any(k in kwargs for k in layout_keys):
            self.font.set_linesize(self.line_spacing)
            lines = str(self.text).split("\n")
            max_w = max((self.font.render(line, True, (255, 255, 255)).get_width() for line in lines),
                        default=0) + self.alignment_spacing
            tot_h = sum(self.font.render(line, True, (255, 255, 255)).get_height() for line in lines)
            if self.auto_size:
                self.width = max_w + 40 + (self.alignment_spacing - 20)
                self.height = tot_h + 20
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if 'screen' in kwargs:
            self.set_screen(kwargs["screen"])
        if 'layer' in kwargs:
            misc.resort_layers()
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
        self.needs_transform = True
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
        self.needs_redraw = True
        return self

    def set_underline(self, value: bool):
        self.underline = value
        self.needs_redraw = True
        return self

    def unbind(self, event: str):
        if event in self.bindings:
            del self.bindings[event]
        return self

    def unbind_all(self):
        self.bindings.clear()
        return self

    def set_tooltip(self, tooltip):
        self.tooltip = tooltip
        tooltip.configure(layer=self.layer + 1)
        if not tooltip.style:
            if not self.active_unpressed_background_color:
                bg_color = (50, 50, 50)
            if not self.active_unpressed_border_color:
                bd_color = (100, 100, 100)
            tooltip.configure(active_unpressed_text_color=self.active_unpressed_text_color,
                              active_unpressed_background_color=self.active_unpressed_background_color if self.active_unpressed_background_color else bg_color,
                              active_unpressed_border_color=self.active_unpressed_border_color if self.active_unpressed_border_color else bd_color)
        return self

    def remove_tooltip(self):
        if self.tooltip:
            self.tooltip.visible = False
            self.tooltip = None
        return self

    def scale(self, value=None, frames_to_finish=1):
        if frames_to_finish <= 0:
            frames_to_finish = 1
        if value is None:
            self.target_scale = 1
        else:
            self.target_scale = value
        self.scale_step = (self.target_scale - self.current_scale) / frames_to_finish
        return self

    def rotate(self, value=None, frames_to_finish=1):
        if frames_to_finish <= 0:
            frames_to_finish = 1
        if value is None:
            self.target_rotation = 0
        else:
            self.target_rotation = value
        self.rotation_step = (self.target_rotation - self.current_rotation) / frames_to_finish
        return self

    def rotozoom(self, scale=None, rotation=None, frames_to_finish=1):
        if frames_to_finish <= 0:
            frames_to_finish = 1
        self.target_scale = 1 if scale is None else scale
        self.scale_step = (self.target_scale - self.current_scale) / frames_to_finish
        self.target_rotation = 0 if rotation is None else rotation
        self.rotation_step = (self.target_rotation - self.current_rotation) / frames_to_finish
        self.use_rotozoom = True
        return self

    def offset(self, value: tuple[int, int], frames_to_finish=1):
        if frames_to_finish <= 0:
            frames_to_finish = 1
        if value is None:
            self.target_offset = (0, 0)
        else:
            self.target_offset = value
        self.offset_step[0] = (self.target_offset[0] - self.current_offset[0]) / frames_to_finish
        self.offset_step[1] = (self.target_offset[1] - self.current_offset[1]) / frames_to_finish
        return self

    def schedule(self, function, frames_to_execute):
        if frames_to_execute < 1:
            frames_to_execute = 1
        self.scheduled_functions.append([function, frames_to_execute])
        return self


def update_animation(label):
    scale_changed = False
    rotation_changed = False
    if label.current_scale != label.target_scale:
        if abs(label.current_scale - label.target_scale) <= abs(label.scale_step):
            label.current_scale = label.target_scale
        else:
            label.current_scale += label.scale_step
        scale_changed = True
    if label.current_rotation != label.target_rotation:
        if abs(label.current_rotation - label.target_rotation) <= abs(label.rotation_step):
            label.current_rotation = label.target_rotation
        else:
            label.current_rotation += label.rotation_step
        rotation_changed = True
    for x in range(2):
        if label.current_offset[x] != label.target_offset[x]:
            if abs(label.current_offset[x] - label.target_offset[x]) <= abs(label.offset_step[x]):
                label.current_offset[x] = float(label.target_offset[x])
            else:
                label.current_offset[x] += label.offset_step[x]

    if scale_changed or rotation_changed:
        label.needs_transform = True


def normalize_color(color):
    if color is None:
        return (0, 0, 0, 0)
    if len(color) == 3:
        return (*color, 255)
    return color


def get_screen_offset(widget):
    if widget.screen:
        return widget.screen.x, widget.screen.y
    return 0, 0


def render_base_surface(label, is_hovering):
    if label.state == "enabled":
        if label.pressed:
            text_color = label.active_pressed_text_color
            bg_color = label.active_pressed_background_color
            shadow_color = label.active_pressed_shadow_color
            underline_color = label.active_pressed_underline_color
            strikethrough_color = label.active_pressed_strikethrough_color
            brd_color = label.active_pressed_border_color
        elif is_hovering:
            text_color = label.active_hover_text_color
            bg_color = label.active_hover_background_color
            shadow_color = label.active_hover_shadow_color
            underline_color = label.active_hover_underline_color
            strikethrough_color = label.active_hover_strikethrough_color
            brd_color = label.active_hover_border_color
        else:
            text_color = label.active_unpressed_text_color
            bg_color = label.active_unpressed_background_color
            shadow_color = label.active_unpressed_shadow_color
            underline_color = label.active_unpressed_underline_color
            strikethrough_color = label.active_unpressed_strikethrough_color
            brd_color = label.active_unpressed_border_color
    else:
        if is_hovering:
            text_color = label.disabled_hover_text_color
            bg_color = label.disabled_hover_background_color
            shadow_color = label.disabled_hover_shadow_color
            underline_color = label.disabled_hover_underline_color
            strikethrough_color = label.disabled_hover_strikethrough_color
            brd_color = label.disabled_hover_border_color
        else:
            text_color = label.disabled_unpressed_text_color
            bg_color = label.disabled_unpressed_background_color
            shadow_color = label.disabled_unpressed_shadow_color
            underline_color = label.disabled_unpressed_underline_color
            strikethrough_color = label.disabled_unpressed_strikethrough_color
            brd_color = label.disabled_unpressed_border_color

    if label.auto_size:
        label.font.set_linesize(label.line_spacing)
        lines = str(label.text).split("\n")
        max_w = max((label.font.render(line, True, text_color).get_width() for line in lines), default=0)
        tot_h = sum(label.font.render(line, True, text_color).get_height() for line in lines)
        label.width = max_w + 40 + (label.alignment_spacing - 20)
        label.height = tot_h + 20
        label.rect = pygame.Rect(label.x, label.y, label.width, label.height)
    label.original_surface = pygame.Surface((label.width, label.height), pygame.SRCALPHA)
    draw_req_rect = pygame.Rect(0, 0, label.width, label.height)
    if bg_color:
        shape_surf = pygame.Surface((label.width, label.height), pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, bg_color, draw_req_rect,
                         border_top_left_radius=label.top_left_corner_radius,
                         border_top_right_radius=label.top_right_corner_radius,
                         border_bottom_left_radius=label.bottom_left_corner_radius,
                         border_bottom_right_radius=label.bottom_right_corner_radius)
        shape_surf.set_alpha(bg_color[3])
        label.original_surface.blit(shape_surf, (0, 0))
    if brd_color:
        shape_surf = pygame.Surface((label.width, label.height), pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, brd_color, draw_req_rect, width=label.border_thickness,
                         border_top_left_radius=label.top_left_corner_radius,
                         border_top_right_radius=label.top_right_corner_radius,
                         border_bottom_left_radius=label.bottom_left_corner_radius,
                         border_bottom_right_radius=label.bottom_right_corner_radius)
        shape_surf.set_alpha(brd_color[3])
        label.original_surface.blit(shape_surf, (0, 0))

    def render_text_line(txt, color, rect_ref, offset=(0, 0)):
        lines = str(txt).split("\n")
        if not lines: return None
        total_height = sum(label.font.render(line, True, color).get_height() for line in lines)
        current_y = rect_ref.centery - total_height // 2 + offset[1]
        union_rect = None
        for line in lines:
            line_surf = label.font.render(line, True, color)
            line_h = line_surf.get_height()
            cx, cy = rect_ref.centerx + offset[0], current_y + line_h // 2
            if label.alignment == "stretched" and len(line) > 1:
                total_char_width = sum(label.font.render(char, True, color).get_width() for char in line)
                available_width = rect_ref.width - (label.alignment_spacing * 2)
                if available_width > total_char_width:
                    spacing = (available_width - total_char_width) / (len(line) - 1)
                    curr_x = rect_ref.left + label.alignment_spacing + offset[0]
                    line_rect = None
                    for char in line:
                        char_s = label.font.render(char, True, color)
                        char_s.set_alpha(color[3])
                        char_r = char_s.get_rect(midleft=(curr_x, cy))
                        label.original_surface.blit(char_s, char_r)
                        curr_x += char_s.get_width() + spacing
                        if line_rect is None:
                            line_rect = char_r.copy()
                        else:
                            line_rect.union_ip(char_r)
                    if union_rect is None:
                        union_rect = line_rect
                    else:
                        union_rect.union_ip(line_rect)
                    current_y += line_h
                    continue
            txt_rect = line_surf.get_rect()
            if label.alignment == "left":
                txt_rect.midleft = (rect_ref.left + label.alignment_spacing + offset[0], cy)
            elif label.alignment == "right":
                txt_rect.midright = (rect_ref.right - label.alignment_spacing + offset[0], cy)
            else:
                txt_rect.center = (cx, cy)
            line_surf.set_alpha(color[3])
            label.original_surface.blit(line_surf, txt_rect)
            if union_rect is None:
                union_rect = txt_rect.copy()
            else:
                union_rect.union_ip(txt_rect)
            current_y += line_h
        return union_rect

    surface_rect = label.original_surface.get_rect()
    if shadow_color and shadow_color[3] > 0:
        render_text_line(label.text, shadow_color, surface_rect, offset=(2, 2))
    final_text_rect = render_text_line(label.text, text_color, surface_rect)
    if final_text_rect:
        if underline_color and label.underline:
            shape_surf = pygame.Surface(final_text_rect.size, pygame.SRCALPHA)
            shape_surf_rect = shape_surf.get_rect()
            start_pos = (shape_surf_rect.left, shape_surf_rect.bottom - 2)
            end_pos = (shape_surf_rect.right, shape_surf_rect.bottom - 2)
            shape_surf.set_alpha(underline_color[3])
            pygame.draw.line(shape_surf, underline_color, start_pos, end_pos, 2)
            label.original_surface.blit(shape_surf, final_text_rect)
        if strikethrough_color and label.strikethrough:
            shape_surf = pygame.Surface(final_text_rect.size, pygame.SRCALPHA)
            shape_surf_rect = shape_surf.get_rect()
            start_pos = (shape_surf_rect.left, shape_surf_rect.centery)
            end_pos = (shape_surf_rect.right, shape_surf_rect.centery)
            shape_surf.set_alpha(strikethrough_color[3])
            pygame.draw.line(shape_surf, strikethrough_color, start_pos, end_pos, 2)
            label.original_surface.blit(shape_surf, final_text_rect)
    label.last_visual_state = (is_hovering)
    label.needs_redraw = False
    label.needs_transform = True


def draw(label, surface: pygame.Surface):
    if not label.alive or not label.visible:
        return
    offset_x, offset_y = get_screen_offset(label)
    total_offset_x = offset_x + round(label.current_offset[0])
    total_offset_y = offset_y + round(label.current_offset[1])
    mouse_pos = pygame.mouse.get_pos()
    is_hovering = is_point_in_rounded_rect(label, mouse_pos)
    current_visual_state = (is_hovering)
    if label.needs_redraw or current_visual_state != label.last_visual_state:
        render_base_surface(label, is_hovering)
    if label.needs_transform or label.surface is None:
        if label.current_scale != 1 or label.current_rotation != 0:
            new_width = int(label.original_surface.get_width() * label.current_scale)
            new_height = int(label.original_surface.get_height() * label.current_scale)
            if new_width > 0 and new_height > 0:
                if label.use_rotozoom:
                    label.surface = pygame.transform.rotozoom(label.original_surface, label.current_rotation,
                                                              label.current_scale)
                else:
                    scaled_surface = pygame.transform.smoothscale(label.original_surface, (new_width, new_height))
                    label.surface = pygame.transform.rotate(scaled_surface, label.current_rotation)
            else:
                label.surface = pygame.Surface((0, 0), pygame.SRCALPHA)
        else:
            label.surface = label.original_surface.copy()
        base_rect = pygame.Rect(label.x, label.y, label.width, label.height)
        old_center = base_rect.center
        label.rect = label.surface.get_rect()
        label.rect.center = old_center
        label.needs_transform = False
    draw_rect = label.rect.move(total_offset_x, total_offset_y)
    surface.blit(label.surface, draw_rect)
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
        if label.tooltip:
            label.tooltip.show()
    elif is_hovering and getattr(label, "is_hovered", False):
        label.is_hovered = True
        label.trigger_event("<HOVER>")
    elif not is_hovering and getattr(label, "is_hovered", False):
        label.is_hovered = False
        label.trigger_event("<MOUSE-OUT>")
        if label.tooltip:
            label.tooltip.hide()


def is_point_in_rounded_rect(label, point):
    offset_x, offset_y = get_screen_offset(label)
    total_offset_x = offset_x + round(label.current_offset[0])
    total_offset_y = offset_y + round(label.current_offset[1])
    rect = label.rect.move(total_offset_x, total_offset_y)
    if not rect.collidepoint(point):
        return False
    x, y = point
    geom_rect = rect
    scale = label.current_scale
    rotation = label.current_rotation
    if scale != 1 or rotation != 0:
        cx, cy = rect.center
        if rotation != 0:
            v = pygame.math.Vector2(x - cx, y - cy)
            v = v.rotate(rotation)
            x, y = cx + v.x, cy + v.y
        base_w = label.width * scale
        base_h = label.height * scale
        geom_rect = pygame.Rect(0, 0, base_w, base_h)
        geom_rect.center = (cx, cy)
        if not geom_rect.collidepoint((x, y)):
            return False
    tl_r = label.top_left_corner_radius * scale
    tr_r = label.top_right_corner_radius * scale
    bl_r = label.bottom_left_corner_radius * scale
    br_r = label.bottom_right_corner_radius * scale
    max_r = max(tl_r, tr_r, bl_r, br_r)
    if (geom_rect.left + max_r <= x <= geom_rect.right - max_r) or \
            (geom_rect.top + max_r <= y <= geom_rect.bottom - max_r):
        return True
    if x < geom_rect.left + tl_r and y < geom_rect.top + tl_r:
        cx, cy = geom_rect.left + tl_r, geom_rect.top + tl_r
        return (x - cx) ** 2 + (y - cy) ** 2 <= tl_r ** 2
    if x > geom_rect.right - tr_r and y < geom_rect.top + tr_r:
        cx, cy = geom_rect.right - tr_r, geom_rect.top + tr_r
        return (x - cx) ** 2 + (y - cy) ** 2 <= tr_r ** 2
    if x < geom_rect.left + bl_r and y > geom_rect.bottom - bl_r:
        cx, cy = geom_rect.left + bl_r, geom_rect.bottom - bl_r
        return (x - cx) ** 2 + (y - cy) ** 2 <= bl_r ** 2
    if x > geom_rect.right - br_r and y > geom_rect.bottom - br_r:
        cx, cy = geom_rect.right - br_r, geom_rect.bottom - br_r
        return (x - cx) ** 2 + (y - cy) ** 2 <= br_r ** 2
    return True


def react(label, event=None):
    for func in label.scheduled_functions:
        func[1] -= 1
        if func[1] <= 0:
            func[0]()
            label.scheduled_functions.remove(func)
    if label.state != "enabled" or not label.visible:
        label.pressed = False
        return
    current_time = time.time()
    mouse_pos = pygame.mouse.get_pos()
    is_inside = is_point_in_rounded_rect(label, mouse_pos)
    screen_off_x, screen_off_y = get_screen_offset(label)
    total_offset_x = screen_off_x + round(label.current_offset[0])
    total_offset_y = screen_off_y + round(label.current_offset[1])
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
                        new_x = mouse_pos[0] - label.drag_offset[0] - total_offset_x
                        new_y = mouse_pos[1] - label.drag_offset[1] - total_offset_y
                        label.place(new_x, new_y)
        elif event.type == pygame.MOUSEBUTTONDOWN and is_inside:
            if event.button == 1:
                label.pressed = True
                label.drag_offset = (mouse_pos[0] - (label.x + total_offset_x),
                                     mouse_pos[1] - (label.y + total_offset_y))
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