import sys

import pygame

from easypygamewidgets import fonts

pygame.init()

all_entrys = []


class Entry:
    def __init__(self, screen: "easypygamewidgets.Screen | None" = None, auto_size: bool = True, width: int = 180,
                 height: int = 80, placeholder_text: str = "easypygamewidgets Entry",
                 text: str = "", char_limit: int | None = None,
                 show: str | None = None, state: str = "enabled",
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
                 selection_color: tuple = (0, 120, 215),
                 disabled_selection_color: tuple = (32, 106, 163),
                 border_thickness: int = 2,
                 active_hover_cursor: pygame.Cursor = None,
                 disabled_hover_cursor: pygame.Cursor = None,
                 active_pressed_cursor: pygame.Cursor = None,
                 blinking_cursor: str = "|",
                 font: pygame.font.Font = fonts.default_font, alignment: str = "left",
                 alignment_spacing: int = 20, corner_radius: int = 25, repeat_delay: int = 500,
                 repeat_interval: int = 50):
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
        self.placeholder_text = placeholder_text
        self.text = text
        self.char_limit = char_limit
        self.show = show
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
        self.selection_color = selection_color
        self.disabled_selection_color = disabled_selection_color
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
                        f"No custom cursor is used for the entry {self.text} because it's not a pygame.Cursor object. ({cursor})")
                self.cursors[name] = None
        self.blinking_cursor = blinking_cursor
        self.font = font
        self.alignment = alignment
        self.alignment_spacing = alignment_spacing
        self.corner_radius = corner_radius
        self.repeat_delay = repeat_delay
        self.repeat_interval = repeat_interval
        self.x = 0
        self.y = 0
        self.alive = True
        self.pressed = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.original_cursor = None
        self.selected_text = None
        self.focused = False
        if text:
            self.cursor_position = len(text)
        else:
            self.cursor_position = 0
        self.scroll_offset = 0
        self.drag_start = None
        self.selection_anchor = None
        self.last_text_x = self.rect.left
        self.held_key_info = None
        self.next_repeat_time = 0
        self.cursor_visible = True
        self.last_blink_time = pygame.time.get_ticks()
        self.bindings = {}

        all_entrys.append(self)

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
        if self in all_entrys:
            all_entrys.remove(self)

    def place(self, x: int, y: int):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return self

    def bind(self, event: str, command, require_hover: bool = True):
        if event == "<FOCUS-OUT>" and require_hover:
            print(
                f"{self.text if self.text.strip() != "" else self.placeholder_text} has a binding for <FOCUS-OUT> with require_hover=True, which will never trigger.")
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
        return self.text

    def text_delete(self, position_start: int = 0, position_end: int | None = None):
        if position_end is None:
            position_end = len(self.text)
        position_start = max(0, min(position_start, len(self.text)))
        position_end = max(0, min(position_end, len(self.text)))
        if position_start < position_end:
            self.text = self.text[:position_start] + self.text[position_end:]
            if self.cursor_position > position_end:
                self.cursor_position -= (position_end - position_start)
            elif self.cursor_position > position_start:
                self.cursor_position = position_start
        self.reset_cursor_blink()

    def text_insert(self, text: str, position: int = None):
        if position is None:
            position = len(self.text)
        if self.char_limit is not None and len(self.text) + len(text) > self.char_limit:
            return
        self.text = self.text[:position] + text + self.text[position:]
        self.cursor_position += len(text)
        self.reset_cursor_blink()

    def text_select(self, position_start: int = 0, position_end: int | None = None):
        if position_end is None:
            position_end = len(self.text)
        self.selected_text = [min(position_start, position_end), max(position_start, position_end)]
        self.reset_cursor_blink()

    def text_copy(self):
        if self.selected_text and self.selected_text[0] != self.selected_text[1]:
            start, end = self.selected_text
            clipboard_text = self.text[start:end]
            pygame.scrap.put(pygame.SCRAP_TEXT, clipboard_text.encode('utf-8'))

    def text_cut(self):
        if self.selected_text and self.selected_text[0] != self.selected_text[1]:
            self.text_copy()
            self.text_delete(self.selected_text[0], self.selected_text[1])
            self.selected_text = None

    def text_paste(self):
        if not pygame.scrap.get_init():
            pygame.scrap.init()
        if self.selected_text:
            self.text_delete(self.selected_text[0], self.selected_text[1])
            self.selected_text = None
        clipboard = pygame.scrap.get(pygame.SCRAP_TEXT)
        if clipboard:
            try:
                paste_text = clipboard.decode('utf-8').split('\x00')[0]
                self.text_insert(paste_text, self.cursor_position)
            except Exception as e:
                print(f"Paste error: {e}")

    def reset_cursor_blink(self):
        self.cursor_visible = True
        self.last_blink_time = pygame.time.get_ticks()

    def get_display_text(self):
        if self.text:
            if self.show:
                return self.show * len(self.text)
            return self.text
        elif self.placeholder_text and not self.focused:
            return self.placeholder_text
        return ""

    def set_screen(self, screen):
        if self.screen:
            if self in screen.widgets:
                self.screen.widgets.remove(self)
        self.screen = screen
        screen.add_widget(self)


def process_key_action(entry, key, unicode_char):
    is_linux = sys.platform.startswith("linux")
    mods = pygame.key.get_mods()
    ctrl = (mods & pygame.KMOD_CTRL) or (mods & pygame.KMOD_META)
    shift = mods & pygame.KMOD_SHIFT
    entry.reset_cursor_blink()
    if key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_HOME, pygame.K_END):
        if shift and entry.selected_text is None:
            entry.selection_anchor = entry.cursor_position
        if key == pygame.K_LEFT:
            entry.cursor_position = max(0, entry.cursor_position - 1)
        elif key == pygame.K_RIGHT:
            entry.cursor_position = min(len(entry.text), entry.cursor_position + 1)
        elif key == pygame.K_HOME:
            entry.cursor_position = 0
        elif key == pygame.K_END:
            entry.cursor_position = len(entry.text)
        if shift:
            entry.text_select(entry.selection_anchor, entry.cursor_position)
        else:
            entry.selected_text = None
            entry.selection_anchor = None
        return
    if ctrl:
        if not is_linux or shift:
            if key == pygame.K_c:
                entry.text_copy()
            elif key == pygame.K_v:
                entry.text_paste()
                entry.trigger_event("<PASTE>")
            elif key == pygame.K_x:
                entry.text_cut()
                entry.trigger_event("<CUT>")
        if key == pygame.K_a:
            entry.selection_anchor = 0
            entry.cursor_position = len(entry.text)
            entry.text_select(0, len(entry.text))
        return
    if key == pygame.K_BACKSPACE:
        if entry.selected_text:
            entry.text_delete(*entry.selected_text)
            entry.selected_text = None
        elif entry.cursor_position > 0:
            entry.text_delete(entry.cursor_position - 1, entry.cursor_position)
        entry.trigger_event("<BACKSPACE>")
        return
    elif key == pygame.K_DELETE:
        if entry.selected_text:
            entry.text_delete(*entry.selected_text)
            entry.selected_text = None
        elif entry.cursor_position < len(entry.text):
            entry.text_delete(entry.cursor_position, entry.cursor_position + 1)
        entry.trigger_event("<DELETE>")
        return
    elif unicode_char.isprintable() and unicode_char != "":
        if entry.selected_text:
            entry.text_delete(*entry.selected_text)
            entry.selected_text = None
        entry.text_insert(unicode_char, entry.cursor_position)
        entry.trigger_event("<TYPING>")


def get_screen_offset(widget):
    if widget.screen:
        return widget.screen.x, widget.screen.y
    return 0, 0


def draw(entry, surface: pygame.Surface):
    if not entry.alive or not entry.visible:
        return
    offset_x, offset_y = get_screen_offset(entry)
    if entry.focused and entry.held_key_info:
        current_time = pygame.time.get_ticks()
        if current_time >= entry.next_repeat_time:
            key, unicode_char = entry.held_key_info
            process_key_action(entry, key, unicode_char)
            entry.next_repeat_time = current_time + entry.repeat_interval
    if not pygame.scrap.get_init():
        pygame.scrap.init()
    mouse_pos = pygame.mouse.get_pos()
    is_hovering = is_point_in_rounded_rect(entry, mouse_pos)
    now = pygame.time.get_ticks()
    display_text = entry.get_display_text()
    if entry.state == "enabled":
        if entry.pressed and is_hovering:
            text_color = entry.active_pressed_text_color
            bg_color = entry.active_pressed_background_color
            brd_color = entry.active_pressed_border_color
        elif is_hovering:
            text_color = entry.active_hover_text_color
            bg_color = entry.active_hover_background_color
            brd_color = entry.active_hover_border_color
        else:
            text_color = entry.active_unpressed_text_color
            bg_color = entry.active_unpressed_background_color
            brd_color = entry.active_unpressed_border_color
        selection_color = entry.selection_color
    else:
        if is_hovering:
            text_color = entry.disabled_hover_text_color
            bg_color = entry.disabled_hover_background_color
            brd_color = entry.disabled_hover_border_color
        else:
            text_color = entry.disabled_unpressed_text_color
            bg_color = entry.disabled_unpressed_background_color
            brd_color = entry.disabled_unpressed_border_color
        selection_color = entry.disabled_selection_color

    if is_hovering:
        if entry.state == "enabled":
            if entry.pressed:
                cursor_key = "active_pressed"
            else:
                cursor_key = "active_hover"
        else:
            cursor_key = "disabled_hover"
        target_cursor = entry.cursors.get(cursor_key)
        if target_cursor:
            current_cursor = pygame.mouse.get_cursor()
            if current_cursor != target_cursor:
                if entry.original_cursor is None:
                    entry.original_cursor = current_cursor
                pygame.mouse.set_cursor(target_cursor)
    else:
        if entry.original_cursor:
            pygame.mouse.set_cursor(entry.original_cursor)
            entry.original_cursor = None

    if is_hovering and not getattr(entry, "is_hovered", False):
        entry.is_hovered = True
        entry.trigger_event("<MOUSE-IN>")
    elif is_hovering and getattr(entry, "is_hovered", False):
        entry.is_hovered = True
        entry.trigger_event("<HOVER>")
    elif not is_hovering and getattr(entry, "is_hovered", False):
        entry.is_hovered = False
        entry.trigger_event("<MOUSE-OUT>")

    if entry.auto_size:
        text_w = entry.font.size(display_text)[0]
        required_width = max(entry.width, text_w + (entry.alignment_spacing * 2) + 10)
        if entry.rect.width != required_width:
            entry.rect.width = required_width
    draw_rect = entry.rect.move(offset_x, offset_y)
    pygame.draw.rect(surface, bg_color, draw_rect, border_radius=entry.corner_radius)
    if entry.border_thickness > 0:
        pygame.draw.rect(surface, brd_color, draw_rect, width=entry.border_thickness,
                         border_radius=entry.corner_radius)
    old_clip = surface.get_clip()
    clip_rect = draw_rect.inflate(-4, -4)
    surface.set_clip(clip_rect)
    y_pos = draw_rect.centery
    drawn_stretched = False
    if entry.alignment == "stretched" and len(display_text) > 1 and not entry.auto_size:
        total_char_width = sum(entry.font.render(char, True, text_color).get_width() for char in display_text)
        available_width = draw_rect.width - (entry.alignment_spacing * 2)
        if available_width > total_char_width:
            drawn_stretched = True
            spacing = (available_width - total_char_width) / (len(display_text) - 1)
            current_x = draw_rect.left + entry.alignment_spacing
            for char in display_text:
                char_surf = entry.font.render(char, True, text_color)
                surface.blit(char_surf, char_surf.get_rect(midleft=(current_x, y_pos)))
                current_x += char_surf.get_width() + spacing
    if not drawn_stretched:
        text_surf = entry.font.render(display_text, True, text_color)
        text_rect = text_surf.get_rect()
        if entry.alignment == "left":
            text_rect.midleft = (draw_rect.left + entry.alignment_spacing, y_pos)
        elif entry.alignment == "right":
            text_rect.midright = (draw_rect.right - entry.alignment_spacing, y_pos)
        else:
            text_rect.center = draw_rect.center
        cursor_x_rel = entry.font.size(display_text[:entry.cursor_position])[0]
        visible_left = draw_rect.left + entry.alignment_spacing
        visible_right = draw_rect.right - entry.alignment_spacing
        visible_width = visible_right - visible_left
        if text_rect.width > visible_width and not entry.auto_size:
            text_rect.midleft = (draw_rect.left + entry.alignment_spacing, y_pos)
            text_rect.x += entry.scroll_offset
            cursor_screen_x = text_rect.x + cursor_x_rel
            if cursor_screen_x > visible_right:
                entry.scroll_offset -= (cursor_screen_x - visible_right)
            elif cursor_screen_x < visible_left:
                entry.scroll_offset += (visible_left - cursor_screen_x)
            if text_rect.x > visible_left:
                entry.scroll_offset = 0
                text_rect.x = visible_left
        else:
            entry.scroll_offset = 0
        if entry.selected_text and entry.selected_text[0] != entry.selected_text[1]:
            start_idx = min(entry.selected_text)
            end_idx = max(entry.selected_text)
            sel_start_x = entry.font.size(display_text[:start_idx])[0]
            sel_end_x = entry.font.size(display_text[:end_idx])[0]
            highlight_rect = pygame.Rect(text_rect.x + sel_start_x, text_rect.top, sel_end_x - sel_start_x,
                                         text_rect.height)
            pygame.draw.rect(surface, selection_color, highlight_rect)
        surface.blit(text_surf, text_rect)
        has_selection = entry.selected_text and entry.selected_text[0] != entry.selected_text[1]
        if entry.focused and entry.state == "enabled" and not has_selection:
            if now - entry.last_blink_time > 500:
                entry.cursor_visible = not entry.cursor_visible
                entry.last_blink_time = now
            if entry.cursor_visible:
                line_x = text_rect.x + cursor_x_rel
                if visible_left <= line_x <= visible_right + 2:
                    cursor_surf = entry.font.render(entry.blinking_cursor, True, text_color)
                    cursor_rect = cursor_surf.get_rect(midleft=(line_x, text_rect.centery))
                    surface.blit(cursor_surf, cursor_rect)
        entry.last_text_x = text_rect.x
        surface.set_clip(old_clip)


def is_point_in_rounded_rect(entry, point):
    offset_x, offset_y = get_screen_offset(entry)
    rect = entry.rect.move(offset_x, offset_y)
    if not rect.collidepoint(point): return False
    r = entry.corner_radius
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


def react(entry, event=None):
    if entry.state != "enabled" or not entry.visible:
        return
    display_text = entry.get_display_text()

    def get_idx_at_mouse(mouse_x):
        curr_x = entry.last_text_x
        for i, char in enumerate(display_text):
            char_w = entry.font.size(char)[0]
            if mouse_x < curr_x + char_w / 2: return i
            curr_x += char_w
        return min(len(display_text), len(entry.text))

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        entry.trigger_event("<PRESS>")
        if not entry.focused:
            entry.trigger_event("<FOCUS-IN>")
        if is_point_in_rounded_rect(entry, event.pos):
            entry.pressed = True
            idx = get_idx_at_mouse(event.pos[0])
            # This somehow has to be redone because """return min(len(display_text), len(entry.text))""" doesn't work
            entry.cursor_position = min(len(entry.text), idx)
            entry.selection_anchor = idx
            entry.selected_text = None
            if not entry.focused:
                entry.focused = True
            entry.reset_cursor_blink()
        else:
            if entry.focused:
                entry.trigger_event("<FOCUS-OUT>")
            entry.focused = False
    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
        entry.trigger_event("<RELEASE>")
        entry.pressed = False
        entry.selection_anchor = None
    elif event.type == pygame.MOUSEMOTION and entry.pressed:
        if entry.selection_anchor is not None:
            entry.cursor_position = get_idx_at_mouse(event.pos[0])
            entry.text_select(entry.selection_anchor, entry.cursor_position)
            entry.reset_cursor_blink()
    elif event.type == pygame.KEYDOWN and entry.focused:
        process_key_action(entry, event.key, event.unicode)
        entry.held_key_info = (event.key, event.unicode)
        entry.next_repeat_time = pygame.time.get_ticks() + entry.repeat_delay
        entry.trigger_event("<KEY>")
        if event.unicode:
            entry.trigger_event(event.unicode)
        keyname = pygame.key.name(event.key)
        entry.trigger_event(f"<{keyname.upper()}>")
    elif event.type == pygame.KEYUP:
        if entry.held_key_info and event.key == entry.held_key_info[0]:
            entry.held_key_info = None
