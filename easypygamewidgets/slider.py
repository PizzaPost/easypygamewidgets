import math

import pygame

from easypygamewidgets import font, misc

pygame.init()


class Slider:
    def __init__(self, screen: "easypygamewidgets.Screen | None" = None, auto_size: bool = True, width: int = 180,
                 height: int = 16,
                 text: str = "easypygamewidgets Slider", start: int | float = 0,
                 end: int | float = 100, initial_value: int = None, state: str = "enabled",
                 top_left_corner_radius: int = 25,
                 top_right_corner_radius: int = 25,
                 bottom_left_corner_radius: int = 25,
                 bottom_right_corner_radius: int = 25,
                 dot_radius: int = None,
                 max_extra_dot_radius: int = None,
                 move_text_with_dot_radius: bool = False,
                 active_unpressed_text_color: tuple = (255, 255, 255),
                 disabled_unpressed_text_color: tuple = (150, 150, 150),
                 active_hover_text_color: tuple = (255, 255, 255),
                 disabled_hover_text_color: tuple = (150, 150, 150),
                 active_pressed_text_color: tuple = (255, 255, 255),
                 active_unpressed_used_background_color: tuple = (30, 30, 30),
                 disabled_unpressed_used_background_color: tuple = (20, 20, 20),
                 active_hover_used_background_color: tuple = (30, 30, 30),
                 disabled_hover_used_background_color: tuple = (20, 20, 20),
                 active_pressed_used_background_color: tuple = (30, 30, 30),
                 active_unpressed_unused_background_color: tuple = (60, 60, 60),
                 disabled_unpressed_unused_background_color: tuple = (30, 30, 30),
                 active_hover_unused_background_color: tuple = (60, 60, 60),
                 disabled_hover_unused_background_color: tuple = (30, 30, 30),
                 active_pressed_unused_background_color: tuple = (60, 60, 60),
                 active_unpressed_dot_color: tuple = (255, 255, 255),
                 disabled_unpressed_dot_color: tuple = (150, 150, 150),
                 active_hover_dot_color: tuple = (255, 255, 255),
                 disabled_hover_dot_color: tuple = (150, 150, 150),
                 active_pressed_dot_color: tuple = (200, 200, 200),
                 active_unpressed_border_color: tuple = (100, 100, 100),
                 disabled_unpressed_border_color: tuple = (60, 60, 60),
                 active_hover_border_color: tuple = (150, 150, 150),
                 disabled_hover_border_color: tuple = (60, 60, 60),
                 active_pressed_border_color: tuple = (150, 150, 150),
                 active_pressed_display_color: tuple = (190, 190, 190),
                 active_hover_display_color: tuple = (190, 190, 190),
                 active_unpressed_display_color: tuple = (190, 190, 190),
                 disabled_hover_display_color: tuple = (150, 150, 150),
                 disabled_unpressed_display_color: tuple = (150, 150, 150),
                 border_width: int = 2,
                 active_hover_cursor: pygame.Cursor = None,
                 disabled_hover_cursor: pygame.Cursor = None,
                 active_pressed_cursor: pygame.Cursor = None,
                 font: pygame.font.Font = font.default_font, alignment: str = "center",
                 alignment_spacing: int = 20, show_value_when_pressed: bool = True,
                 show_value_when_hovered: bool = True, show_value_when_unpressed: bool = False,
                 show_value_when_disabled: bool = False, round_display_value: int = 0,
                 show_full_rounding_of_whole_numbers: bool = False, trigger_hold_delay: int = 150, layer=1000,
                 tooltip: "easypygamewidgets.Tooltip | None" = None,
                 data=None):
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
        self.text = text
        self.start = start
        self.end = end
        self.start = start
        self.end = end
        self.value = min(max(initial_value or start, start), end)
        self.top_left_corner_radius = top_left_corner_radius
        self.top_right_corner_radius = top_right_corner_radius
        self.bottom_left_corner_radius = bottom_left_corner_radius
        self.bottom_right_corner_radius = bottom_right_corner_radius
        if not dot_radius:
            self.dot_radius = height // 2
        else:
            self.dot_radius = dot_radius
        if not max_extra_dot_radius:
            self.max_extra_dot_radius = self.dot_radius // 5 + 1
        else:
            self.max_extra_dot_radius = max_extra_dot_radius
        self.move_text_with_dot_radius = move_text_with_dot_radius
        self.active_unpressed_text_color = active_unpressed_text_color
        self.disabled_unpressed_text_color = disabled_unpressed_text_color
        self.active_hover_text_color = active_hover_text_color
        self.disabled_hover_text_color = disabled_hover_text_color
        self.active_pressed_text_color = active_pressed_text_color
        self.active_unpressed_used_background_color = active_unpressed_used_background_color
        self.disabled_unpressed_used_background_color = disabled_unpressed_used_background_color
        self.active_hover_used_background_color = active_hover_used_background_color
        self.disabled_hover_used_background_color = disabled_hover_used_background_color
        self.active_pressed_used_background_color = active_pressed_used_background_color
        self.active_unpressed_unused_background_color = active_unpressed_unused_background_color
        self.disabled_unpressed_unused_background_color = disabled_unpressed_unused_background_color
        self.active_hover_unused_background_color = active_hover_unused_background_color
        self.disabled_hover_unused_background_color = disabled_hover_unused_background_color
        self.active_pressed_unused_background_color = active_pressed_unused_background_color
        self.active_unpressed_dot_color = active_unpressed_dot_color
        self.disabled_unpressed_dot_color = disabled_unpressed_dot_color
        self.active_hover_dot_color = active_hover_dot_color
        self.disabled_hover_dot_color = disabled_hover_dot_color
        self.active_pressed_dot_color = active_pressed_dot_color
        self.active_unpressed_border_color = active_unpressed_border_color
        self.disabled_unpressed_border_color = disabled_unpressed_border_color
        self.active_hover_border_color = active_hover_border_color
        self.disabled_hover_border_color = disabled_hover_border_color
        self.active_pressed_border_color = active_pressed_border_color
        self.active_pressed_display_color = active_pressed_display_color
        self.active_hover_display_color = active_hover_display_color
        self.active_unpressed_display_color = active_unpressed_display_color
        self.disabled_hover_display_color = disabled_hover_display_color
        self.disabled_unpressed_display_color = disabled_unpressed_display_color
        self.border_width = border_width
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
                        f"No custom cursor is used for the slider {self.text} because it's not a pygame.Cursor object. ({cursor})")
                self.cursors[name] = None
        self.font = font
        self.alignment = alignment
        self.alignment_spacing = alignment_spacing
        self.show_value_when_pressed = show_value_when_pressed
        self.show_value_when_hovered = show_value_when_hovered
        self.show_value_when_unpressed = show_value_when_unpressed
        self.show_value_when_disabled = show_value_when_disabled
        self.round_display_value = round_display_value
        self.show_full_rounding_of_whole_numbers = show_full_rounding_of_whole_numbers
        self.trigger_hold_delay = trigger_hold_delay
        self.layer = layer
        self.tooltip = tooltip
        if tooltip:
            tooltip.configure(layer=self.layer + 1)
            if not tooltip.style:
                tooltip.configure(active_unpressed_text_color=self.active_unpressed_text_color,
                                  active_unpressed_background_color=self.active_unpressed_used_background_color,
                                  active_unpressed_border_color=self.active_unpressed_border_color)
        self.data = data
        self.x = 0
        self.y = font.render(text, True, (255, 255, 255)).get_height()
        self.alive = True
        self.pressed = False
        self.rect = pygame.Rect(self.x, self.y, self.width, 60)
        self.original_cursor = None
        self.extra_dot_radius = 0
        self.pressed_before = False
        self.last_value_update_time = 0
        self.bindings = {}

        misc.add_widget(self)

    def configure(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        if 'x' in kwargs or 'y' in kwargs or 'width' in kwargs:
            self.rect = pygame.Rect(self.x, self.y, self.width, 60)
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
        self.rect = pygame.Rect(self.x, self.y, self.width, 60)
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

    def get(self):
        return self.value

    def set(self, value):
        self.value = min(max(value, self.start), self.end)

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

    def set_tooltip(self, tooltip):
        self.tooltip = tooltip
        tooltip.configure(layer=self.layer + 1)
        if not tooltip.style:
            tooltip.configure(active_unpressed_text_color=self.active_unpressed_text_color,
                              active_unpressed_background_color=self.active_unpressed_used_background_color,
                              active_unpressed_border_color=self.active_unpressed_border_color)
        return self

    def remove_tooltip(self):
        self.tooltip = None
        return self


def get_screen_offset(widget):
    if widget.screen:
        return widget.screen.x, widget.screen.y
    return 0, 0


def draw(slider, surface: pygame.Surface):
    if not slider.alive or not slider.visible:
        return
    mouse_pos = pygame.mouse.get_pos()
    is_hovering = is_point_in_rounded_rect(slider, mouse_pos)
    if slider.state == "enabled":
        if slider.pressed:
            text_color = slider.active_pressed_text_color
            bg_color_used = slider.active_pressed_used_background_color
            bg_color_unused = slider.active_pressed_unused_background_color
            brd_color = slider.active_pressed_border_color
            dot_color = slider.active_pressed_dot_color
            display_color = slider.active_pressed_display_color
        elif is_hovering:
            text_color = slider.active_hover_text_color
            bg_color_used = slider.active_hover_used_background_color
            bg_color_unused = slider.active_hover_unused_background_color
            brd_color = slider.active_hover_border_color
            dot_color = slider.active_hover_dot_color
            display_color = slider.active_hover_display_color
        else:
            text_color = slider.active_unpressed_text_color
            bg_color_used = slider.active_unpressed_used_background_color
            bg_color_unused = slider.active_unpressed_unused_background_color
            brd_color = slider.active_unpressed_border_color
            dot_color = slider.active_unpressed_dot_color
            display_color = slider.active_unpressed_display_color
    else:
        if is_hovering:
            text_color = slider.disabled_hover_text_color
            bg_color_used = slider.disabled_hover_used_background_color
            bg_color_unused = slider.disabled_hover_unused_background_color
            brd_color = slider.disabled_hover_border_color
            dot_color = slider.disabled_hover_dot_color
            display_color = slider.disabled_hover_display_color
        else:
            text_color = slider.disabled_unpressed_text_color
            bg_color_used = slider.disabled_unpressed_used_background_color
            bg_color_unused = slider.disabled_unpressed_unused_background_color
            brd_color = slider.disabled_unpressed_border_color
            dot_color = slider.disabled_unpressed_dot_color
            display_color = slider.disabled_unpressed_display_color

    if is_hovering:
        if slider.state == "enabled":
            if slider.pressed:
                cursor_key = "active_pressed"
            else:
                cursor_key = "active_hover"
        else:
            cursor_key = "disabled_hover"
        target_cursor = slider.cursors.get(cursor_key)
        if target_cursor:
            current_cursor = pygame.mouse.get_cursor()
            if current_cursor != target_cursor:
                if slider.original_cursor is None:
                    slider.original_cursor = current_cursor
                pygame.mouse.set_cursor(target_cursor)
    else:
        if slider.original_cursor:
            pygame.mouse.set_cursor(slider.original_cursor)
            slider.original_cursor = None

    if is_hovering and not getattr(slider, "is_hovered", False):
        slider.is_hovered = True
        slider.trigger_event("<MOUSE-IN>")
        if slider.tooltip:
            slider.tooltip.show()
    elif is_hovering and getattr(slider, "is_hovered", False):
        slider.is_hovered = True
        slider.trigger_event("<HOVER>")
    elif not is_hovering and getattr(slider, "is_hovered", False):
        slider.is_hovered = False
        slider.trigger_event("<MOUSE-OUT>")
        if slider.tooltip:
            slider.tooltip.hide()
    if slider.tooltip.visible:
        if not slider.pressed and not is_hovering:
            slider.tooltip.hide()

    temp_surf = slider.font.render(slider.text, True, text_color)
    if slider.auto_size:
        slider.width = temp_surf.get_width() + 40 + (slider.alignment_spacing - 20)
        slider.rect = pygame.Rect(slider.x, slider.y, slider.width, slider.height)

    offset_x, offset_y = get_screen_offset(slider)
    offset_y += temp_surf.get_height() * 1.25
    draw_rect = slider.rect.move(offset_x, offset_y)

    track_y = draw_rect.centery + 5
    track_rect = pygame.Rect(draw_rect.x, track_y - (slider.height // 2), draw_rect.width, slider.height)
    max_radius = min(track_rect.width, track_rect.height) // 2
    tl = min(slider.top_left_corner_radius, max_radius)
    tr = min(slider.top_right_corner_radius, max_radius)
    bl = min(slider.bottom_left_corner_radius, max_radius)
    br = min(slider.bottom_right_corner_radius, max_radius)
    pygame.draw.rect(surface, bg_color_unused, track_rect, border_top_left_radius=tl, border_top_right_radius=tr,
                     border_bottom_left_radius=bl, border_bottom_right_radius=br)
    if slider.end - slider.start != 0:
        pct = (slider.value - slider.start) / (slider.end - slider.start)
    else:
        pct = 0
    pct = max(0, min(1, pct))
    used_width = int(track_rect.width * pct)
    if used_width > 0:
        clip_surf = pygame.Surface(track_rect.size, pygame.SRCALPHA)
        mask_rect = pygame.Rect(0, 0, track_rect.width, track_rect.height)
        pygame.draw.rect(clip_surf, (255, 255, 255), mask_rect, border_top_left_radius=tl,
                         border_bottom_left_radius=bl, border_top_right_radius=tr,
                         border_bottom_right_radius=br)
        used_fill_rect = pygame.Rect(0, 0, used_width, track_rect.height)
        fill_surf = pygame.Surface(track_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(fill_surf, bg_color_used, used_fill_rect)
        clip_surf.blit(fill_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        surface.blit(clip_surf, track_rect.topleft)
    if brd_color:
        pygame.draw.rect(surface, brd_color, track_rect, width=slider.border_width, border_top_left_radius=tl,
                         border_top_right_radius=tr, border_bottom_left_radius=bl,
                         border_bottom_right_radius=br)
    dot_x = track_rect.x + used_width
    dot_x = max(track_rect.left + slider.dot_radius, min(dot_x, track_rect.right - slider.dot_radius))
    pygame.draw.circle(surface, dot_color, (int(dot_x), int(track_rect.centery)),
                       slider.dot_radius + slider.extra_dot_radius)
    if (slider.state == "enabled" or slider.show_value_when_disabled) and (
            slider.show_value_when_pressed and slider.pressed or slider.show_value_when_hovered and is_hovering and not slider.pressed or slider.show_value_when_unpressed):
        if slider.show_full_rounding_of_whole_numbers:
            text_surf = slider.font.render(str(round(slider.value, slider.round_display_value)), True, display_color)
        elif not slider.show_full_rounding_of_whole_numbers and round(slider.value,
                                                                      slider.round_display_value) % 1 == 0:
            text_surf = slider.font.render(str(round(slider.value, slider.round_display_value)).replace(".0", ""), True,
                                           display_color)
        elif not slider.show_full_rounding_of_whole_numbers:
            text_surf = slider.font.render(str(round(slider.value, slider.round_display_value)), True, display_color)
        text_rect = text_surf.get_rect()
        if slider.move_text_with_dot_radius:
            text_rect.center = (dot_x, track_rect.centery + 25 + slider.dot_radius + slider.extra_dot_radius)
        else:
            text_rect.center = (dot_x, track_rect.centery + 25 + slider.dot_radius)
        surface.blit(text_surf, text_rect)

    text_surf = slider.font.render(slider.text, True, text_color)
    text_rect = text_surf.get_rect()
    if slider.move_text_with_dot_radius:
        text_y_center = track_rect.centery - 25 - slider.dot_radius - slider.extra_dot_radius
    else:
        text_y_center = track_rect.centery - 25 - slider.dot_radius

    if slider.alignment == "stretched" and len(slider.text) > 1 and not slider.auto_size:
        total_char_width = sum(slider.font.render(char, True, text_color).get_width() for char in slider.text)
        available_width = draw_rect.width - (slider.alignment_spacing * 2)
        if available_width > total_char_width:
            spacing = (available_width - total_char_width) / (len(slider.text) - 1)
            current_x = draw_rect.left + slider.alignment_spacing
            for char in slider.text:
                char_surf = slider.font.render(char, True, text_color)
                surface.blit(char_surf, char_surf.get_rect(midleft=(current_x, text_y_center)))
                current_x += char_surf.get_width() + spacing
        else:
            surface.blit(text_surf, text_surf.get_rect(center=(draw_rect.centerx, text_y_center)))
    else:
        if slider.alignment == "left":
            text_rect.midleft = (draw_rect.left + slider.alignment_spacing, text_y_center)
        elif slider.alignment == "right":
            text_rect.midright = (draw_rect.right - slider.alignment_spacing, text_y_center)
        else:
            text_rect.center = (draw_rect.centerx, text_y_center)
        surface.blit(text_surf, text_rect)


def is_point_in_rounded_rect(slider, point):
    offset_x, offset_y = get_screen_offset(slider)
    draw_rect = slider.rect.move(offset_x, offset_y)
    temp_surf = slider.font.render(slider.text, True, (0, 0, 0))
    track_y = draw_rect.centery + 10 + temp_surf.get_height()
    track_rect = pygame.Rect(draw_rect.x, track_y - (slider.height // 2), draw_rect.width, slider.height)
    x, y = point
    if not track_rect.collidepoint(point):
        return False
    max_radius = min(track_rect.width, track_rect.height) // 2
    tl = min(slider.top_left_corner_radius, max_radius)
    tr = min(slider.top_right_corner_radius, max_radius)
    bl = min(slider.bottom_left_corner_radius, max_radius)
    br = min(slider.bottom_right_corner_radius, max_radius)
    if x < track_rect.left + tl and y < track_rect.top + tl:
        cx, cy = track_rect.left + tl, track_rect.top + tl
        if (x - cx) ** 2 + (y - cy) ** 2 > tl ** 2:
            return False
    elif x > track_rect.right - tr and y < track_rect.top + tr:
        cx, cy = track_rect.right - tr, track_rect.top + tr
        if (x - cx) ** 2 + (y - cy) ** 2 > tr ** 2:
            return False
    elif x < track_rect.left + bl and y > track_rect.bottom - bl:
        cx, cy = track_rect.left + bl, track_rect.bottom - bl
        if (x - cx) ** 2 + (y - cy) ** 2 > bl ** 2:
            return False
    elif x > track_rect.right - br and y > track_rect.bottom - br:
        cx, cy = track_rect.right - br, track_rect.bottom - br
        if (x - cx) ** 2 + (y - cy) ** 2 > br ** 2:
            return False
    return True


def react(slider, event=None):
    if slider.state != "enabled" or not slider.visible:
        return
    mouse_pos = pygame.mouse.get_pos()
    is_inside = is_point_in_rounded_rect(slider, mouse_pos)

    def update_value():
        offset_x, offset_y = get_screen_offset(slider)
        draw_rect = slider.rect.move(offset_x, offset_y)

        relative_x = mouse_pos[0] - draw_rect.x
        pct = relative_x / draw_rect.width
        pct = max(0, min(1, pct))
        new_slider_value = slider.start + (pct * (slider.end - slider.start))
        moved = slider.value != new_slider_value
        slider.value = new_slider_value
        current_time = pygame.time.get_ticks()
        if not slider.pressed_before:
            slider.trigger_event("<PRESS>")
            slider.pressed_before = True
        else:
            if moved:
                slider.last_value_update_time = current_time
                slider.trigger_event("<DRAG>")
            else:
                if current_time - slider.last_value_update_time > slider.trigger_hold_delay:
                    slider.trigger_event("<HOLD>")

    if not event:
        if pygame.mouse.get_pressed()[0] and is_inside:
            slider.pressed = True
        if slider.pressed:
            if pygame.mouse.get_pressed()[0]:
                update_value()
            else:
                slider.pressed = False
                slider.pressed_before = False
                slider.trigger_event("<RELEASE>")
    else:
        if event.type == pygame.KEYDOWN:
            slider.trigger_event("<KEY>")
            if event.unicode:
                slider.trigger_event(event.unicode)
            keyname = pygame.key.name(event.key)
            slider.trigger_event(f"<{keyname.upper()}>")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and is_inside:
                slider.pressed = True
                update_value()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                slider.pressed = False
                slider.pressed_before = False
                slider.trigger_event("<RELEASE>")
        elif event.type == pygame.MOUSEMOTION:
            if slider.pressed:
                update_value()
    t = pygame.time.get_ticks() * 0.01
    pulse = (1 - math.cos(t * math.pi)) * 0.5
    if slider.pressed:
        slider.extra_dot_radius = min(slider.max_extra_dot_radius, slider.extra_dot_radius + pulse)
    else:
        slider.extra_dot_radius = max(0, slider.extra_dot_radius - pulse)
