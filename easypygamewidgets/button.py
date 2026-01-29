import time

import pygame

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
                 click_sound: str | pygame.mixer.Sound = None,
                 hold_sound: str | pygame.mixer.Sound = None,
                 release_sound: str | pygame.mixer.Sound = None,
                 active_hover_cursor: pygame.cursors = None,
                 disabled_hover_cursor: pygame.cursors = None,
                 active_pressed_cursor: pygame.cursors = None,
                 font: pygame.font.Font = pygame.font.Font(None, 38), alignment: str = "center",
                 alignment_spacing: int = 20, click_command=None, hold_command=None, release_command=None,
                 holdable: bool = False, corner_radius: int = 25):
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
        if click_sound:
            if isinstance(click_sound, pygame.mixer.Sound):
                self.click_sound = click_sound
            else:
                self.click_sound = pygame.mixer.Sound(click_sound)
        else:
            self.click_sound = None
        if hold_sound:
            if isinstance(hold_sound, pygame.mixer.Sound):
                self.hold_sound = hold_sound
            else:
                self.hold_sound = pygame.mixer.Sound(hold_sound)
        else:
            self.hold_sound = None
        if release_sound:
            if isinstance(release_sound, pygame.mixer.Sound):
                self.release_sound = release_sound
            else:
                self.release_sound = pygame.mixer.Sound(release_sound)
        else:
            self.release_sound = None
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
                        f"No custom cursor is used for the button {self.text} because it's not a pygame.cursors.Cursor object. ({cursor})")
                self.cursors[name] = None
        self.font = font
        self.alignment = alignment
        self.alignment_spacing = alignment_spacing
        self.click_command = click_command
        self.hold_command = hold_command
        self.release_command = release_command
        self.holdable = holdable
        self.corner_radius = corner_radius
        self.x = 0
        self.y = 0
        self.alive = True
        self.pressed = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.original_cursor = None
        self.visible = True
        self.hold_sound_started = None
        self.hold_sound_length = None

        all_buttons.append(self)

    def configure(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        if 'x' in kwargs or 'y' in kwargs or 'width' in kwargs or 'height' in kwargs:
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

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

    def execute_click(self):
        if self.click_command:
            self.click_command()
        return self

    def execute_hold(self):
        if self.hold_command:
            self.hold_command()
        return self

    def execute_release(self):
        if self.release_command:
            self.release_command()
        return self

    def play_click_sound(self):
        if self.click_sound:
            self.click_sound.play()
        return self

    def play_hold_sound(self):
        if self.hold_sound:
            self.hold_sound.play()
        return self

    def play_release_sound(self):
        if self.release_sound:
            self.release_sound.play()
        return self

    def add_screen(self, screen):
        self.screen = screen
        if not self in screen.widgets:
            screen.widgets.append(self)


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
            if button.holdable:
                if button.hold_command: button.hold_command()
                if button.hold_sound:
                    if button.hold_sound_started:
                        if button.hold_sound_started + button.hold_sound_length > time.time():
                            return
                    button.hold_sound.play()
                    button.hold_sound_length = button.hold_sound.get_length()
                    button.hold_sound_started = time.time()
        elif not pygame.mouse.get_pressed()[0] and is_inside:
            if button.pressed:
                button.pressed = False
                if button.release_command: button.release_command()
                if button.release_sound: button.release_sound.play()
        elif not pygame.mouse.get_pressed()[0] and not is_inside:
            button.pressed = False
    else:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and is_inside:
                button.pressed = True
                if button.click_command: button.click_command()
                if button.click_sound: button.click_sound.play()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and is_inside and button.pressed:
                button.pressed = False
                if button.release_command: button.release_command()
                if button.release_sound: button.release_sound.play()
