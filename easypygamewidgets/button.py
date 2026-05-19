import pygame

from easypygamewidgets import font, misc

pygame.init()


class Button:
    def __init__(self, screen: "easypygamewidgets.Screen | None" = None, auto_size: bool = True, width: int = 180,
                 height: int = 80,
                 text: str = "easypygamewidgets Button",
                 state: str | None = None,
                 active_unpressed_text_color: tuple = (255, 255, 255, 255),
                 disabled_unpressed_text_color: tuple = (150, 150, 150, 255),
                 active_hover_text_color: tuple = (255, 255, 255, 255),
                 disabled_hover_text_color: tuple = (150, 150, 150, 255),
                 active_pressed_text_color: tuple = (200, 200, 200, 255),
                 active_unpressed_background_color: tuple = (50, 50, 50, 255),
                 disabled_unpressed_background_color: tuple = (30, 30, 30, 255),
                 active_hover_background_color: tuple = (70, 70, 70, 255),
                 disabled_hover_background_color: tuple = (30, 30, 30, 255),
                 active_pressed_background_color: tuple = (40, 40, 40, 255),
                 active_unpressed_border_color: tuple = (100, 100, 100, 255),
                 disabled_unpressed_border_color: tuple = (60, 60, 60, 255),
                 active_hover_border_color: tuple = (150, 150, 150, 255),
                 disabled_hover_border_color: tuple = (60, 60, 60, 255),
                 active_pressed_border_color: tuple = (50, 50, 50, 255),
                 border_thickness: int = 2,
                 active_hover_cursor: pygame.Cursor = None,
                 disabled_hover_cursor: pygame.Cursor = None,
                 active_pressed_cursor: pygame.Cursor = None,
                 font: pygame.font.Font = font.default_font, alignment: str = "center",
                 command=None, alignment_spacing: int = 60, corner_radius: int = 20, layer=1000, line_spacing: int = 30,
                 tooltip: "easypygamewidgets.Tooltip | None" = None, min_width: int | None = None,
                 max_width: int | None = None, min_height: int | None = None, max_height: int | None = None, data=None):
        self.bindings = {}
        if screen:
            screen.add_widget(self)
            self.screen = screen
            if state:
                self.state = state
        else:
            self.screen = None
            self.visible = True
            if state:
                self.state = state
            else:
                self.state = "enabled"
        self.auto_size = auto_size
        if self.auto_size:
            font.set_linesize(line_spacing)
            lines = text.split("\n")
            total_w = 0
            for line in lines:
                text_w, text_h = font.size(line)
                if text_w > total_w:
                    total_w = text_w
            total_h = len(lines) * line_spacing
            self._width = total_w + (alignment_spacing - 20)
            if min_width:
                self._width = max(self._width, min_width)
            if max_width:
                self._width = min(self._width, max_width)
            self._height = total_h + 20
            if min_height:
                self._height = max(self._height, min_height)
            if max_height:
                self._height = min(self._height, max_height)
        else:
            self._width = width
            self._height = height
        self.text = text
        self.active_unpressed_text_color = normalize_color(active_unpressed_text_color)
        self.disabled_unpressed_text_color = normalize_color(disabled_unpressed_text_color)
        self.active_hover_text_color = normalize_color(active_hover_text_color)
        self.disabled_hover_text_color = normalize_color(disabled_hover_text_color)
        self.active_pressed_text_color = normalize_color(active_pressed_text_color)
        self.active_unpressed_background_color = normalize_color(active_unpressed_background_color)
        self.disabled_unpressed_background_color = normalize_color(disabled_unpressed_background_color)
        self.active_hover_background_color = normalize_color(active_hover_background_color)
        self.disabled_hover_background_color = normalize_color(disabled_hover_background_color)
        self.active_pressed_background_color = normalize_color(active_pressed_background_color)
        self.active_unpressed_border_color = normalize_color(active_unpressed_border_color)
        self.disabled_unpressed_border_color = normalize_color(disabled_unpressed_border_color)
        self.active_hover_border_color = normalize_color(active_hover_border_color)
        self.disabled_hover_border_color = normalize_color(disabled_hover_border_color)
        self.active_pressed_border_color = normalize_color(active_pressed_border_color)
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
        self.layer = layer
        self.tooltip = tooltip
        if tooltip:
            tooltip.configure(layer=self.layer + 1)
            if not tooltip.style:
                tooltip.configure(active_unpressed_text_color=self.active_unpressed_text_color,
                                  active_unpressed_background_color=self.active_unpressed_background_color,
                                  active_unpressed_border_color=self.active_unpressed_border_color)
        self.line_spacing = line_spacing
        self.min_width = min_width
        self.max_width = max_width
        self.min_height = min_height
        self.max_height = max_height
        self.data = data
        self.x = 0
        self.y = 0
        self.alive = True
        self.pressed = False
        self.rect = pygame.Rect(self.x, self.y, self._width, self._height)
        self.original_cursor = None
        self.scheduled_functions = []
        self.is_hovered = False
        self.last_visual_state = None
        self.needs_redraw = True
        self.cached_surface = None
        self.needs_transform = True
        self.original_surface = pygame.Surface((1, 1))
        self.surface = pygame.Surface((1, 1))
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

        self.font.set_linesize(line_spacing)

        misc.add_widget(self)

    @property
    def width(self):
        return int(self._width * self.current_scale)

    @property
    def height(self):
        return int(self._height * self.current_scale)

    def configure(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.needs_redraw = True
        self.needs_transform = True
        if any(k in kwargs for k in
               ('auto_size', 'x', 'y', 'width', 'height', 'text', 'font', 'max_width', 'min_width', 'max_height',
                'min_height')):
            if self.auto_size:
                self.font.set_linesize(self.line_spacing)
                lines = self.text.split("\n")
                total_w = 0
                for line in lines:
                    text_w, text_h = self.font.size(line)
                    if text_w > total_w:
                        total_w = text_w
                total_h = len(lines) * self.line_spacing
                self.width = total_w + (self.alignment_spacing - 20)
                if self.min_width:
                    self.width = max(total_w, self.min_width)
                if self.max_width:
                    self.width = min(total_w, self.max_width)
                self.height = total_h + 20
                if self.min_height:
                    self.height = max(total_h + 20, self.min_height)
                if self.max_height:
                    self.height = min(total_h + 20, self.max_height)
            self.rect = pygame.Rect(self.x, self.y, self._width, self._height)
        if 'screen' in kwargs:
            self.set_screen(kwargs["screen"])
        if 'command' in kwargs:
            self.bind("<RELEASE>", kwargs['command'])
        if 'layer' in kwargs:
            misc.resort_layers()
        if 'line_spacing' in kwargs:
            self.font.set_linesize(self.line_spacing)
        return self

    def config(self, **kwargs):
        self.configure(**kwargs)

    def delete(self):
        self.alive = False
        if self in misc.all_widgets:
            misc.all_widgets.remove(self)

    def place(self, x: int, y: int, mode: str = "px"):
        if mode == "px":
            self.x = x
            self.y = y
        elif mode in ("%", "percent", "percentage"):
            screen_width = misc.pg.get_width()
            screen_height = misc.pg.get_height()
            self.x = int(x * screen_width / 100)
            self.y = int(y * screen_height / 100)
        else:
            self.x = x
            self.y = y
            print(f"Invalid Mode: {mode}\nFallback: px")
        self.rect = pygame.Rect(self.x, self.y, self._width, self._height)
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
                              active_unpressed_background_color=self.active_unpressed_background_color,
                              active_unpressed_border_color=self.active_unpressed_border_color)
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
        update_animation(self)
        return self

    def rotate(self, value=None, frames_to_finish=1):
        if frames_to_finish <= 0:
            frames_to_finish = 1
        if value is None:
            self.target_rotation = 0
        else:
            self.target_rotation = value
        self.rotation_step = (self.target_rotation - self.current_rotation) / frames_to_finish
        update_animation(self)
        return self

    def rotozoom(self, scale=None, rotation=None, frames_to_finish=1):
        if frames_to_finish <= 0:
            frames_to_finish = 1
        self.target_scale = 1 if scale is None else scale
        self.scale_step = (self.target_scale - self.current_scale) / frames_to_finish
        self.target_rotation = 0 if rotation is None else rotation
        self.rotation_step = (self.target_rotation - self.current_rotation) / frames_to_finish
        self.use_rotozoom = True
        update_animation(self)
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
        update_animation(self)
        return self

    def schedule(self, function, frames_to_execute):
        if frames_to_execute < 1:
            frames_to_execute = 1
        self.scheduled_functions.append([function, frames_to_execute])
        return self


def update_animation(button):
    scale_changed = False
    rotation_changed = False
    if button.current_scale != button.target_scale:
        if abs(button.current_scale - button.target_scale) <= abs(button.scale_step):
            button.current_scale = button.target_scale
        else:
            button.current_scale += button.scale_step
        scale_changed = True
    if button.current_rotation != button.target_rotation:
        if abs(button.current_rotation - button.target_rotation) <= abs(button.rotation_step):
            button.current_rotation = button.target_rotation
        else:
            button.current_rotation += button.rotation_step
        rotation_changed = True
    for x in range(2):
        if button.current_offset[x] != button.target_offset[x]:
            if abs(button.current_offset[x] - button.target_offset[x]) <= abs(button.offset_step[x]):
                button.current_offset[x] = float(button.target_offset[x])
            else:
                button.current_offset[x] += button.offset_step[x]
    if scale_changed or rotation_changed:
        button.needs_transform = True


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


def render_button_surface(button, is_hovering):
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

    cached = pygame.Surface((button._width, button._height), pygame.SRCALPHA)
    local_rect = pygame.Rect(0, 0, button._width, button._height)
    pygame.draw.rect(cached, bg_color, local_rect, border_radius=button.corner_radius)
    if brd_color:
        pygame.draw.rect(cached, brd_color, local_rect, width=button.border_thickness,
                         border_radius=button.corner_radius)

    if button.alignment == "stretched" and len(button.text) > 1 and not button.auto_size:
        total_char_width = sum(button.font.render(char, True, text_color).get_width() for char in button.text)
        available_width = local_rect.width - (button.alignment_spacing * 2)
        if available_width > total_char_width:
            spacing = (available_width - total_char_width) / (len(button.text) - 1)
            current_x = local_rect.left + button.alignment_spacing
            for char in button.text:
                char_surf = button.font.render(char, True, text_color)
                char_surf.set_alpha(text_color[3])
                cached.blit(char_surf, char_surf.get_rect(midleft=(current_x, local_rect.centery)))
                current_x += char_surf.get_width() + spacing
        else:
            text_surf = button.font.render(button.text, True, text_color)
            text_surf.set_alpha(text_color[3])
            cached.blit(text_surf, text_surf.get_rect(center=local_rect.center))
    else:
        lines = button.text.split("\n")
        total_text_height = len(lines) * button.line_spacing
        start_y = local_rect.centery - (total_text_height // 2)
        for i, line in enumerate(lines):
            text_surf = button.font.render(line, True, text_color)
            text_surf.set_alpha(text_color[3])
            text_rect = text_surf.get_rect()
            line_centery = start_y + (i * button.line_spacing) + (button.line_spacing // 2)
            if button.alignment == "left":
                text_rect.midleft = (local_rect.left + button.alignment_spacing, line_centery)
            elif button.alignment == "right":
                text_rect.midright = (local_rect.right - button.alignment_spacing, line_centery)
            else:
                text_rect.center = (local_rect.centerx, line_centery)
            cached.blit(text_surf, text_rect)
    button.cached_surface = cached
    button.original_surface = cached


def draw(button, surface: pygame.Surface):
    if not button.alive or not button.visible:
        return
    mouse_pos = pygame.mouse.get_pos()
    is_hovering = is_point_in_rounded_rect(button, mouse_pos)
    current_visual_state = (button.pressed, is_hovering)
    if button.needs_redraw or button.last_visual_state != current_visual_state:
        render_button_surface(button, is_hovering)
        button.last_visual_state = current_visual_state
        button.needs_redraw = False
        button.needs_transform = True

    if button.needs_transform or button.surface is None:
        if button.current_scale != 1 or button.current_rotation != 0:
            new_width = int(button.original_surface.get_width() * button.current_scale)
            new_height = int(button.original_surface.get_height() * button.current_scale)
            if new_width > 0 and new_height > 0:
                if button.use_rotozoom:
                    button.surface = pygame.transform.rotozoom(button.original_surface, button.current_rotation,
                                                               button.current_scale)
                else:
                    scaled_surface = pygame.transform.smoothscale(button.original_surface, (new_width, new_height))
                    button.surface = pygame.transform.rotate(scaled_surface, button.current_rotation)
            else:
                button.surface = pygame.Surface((0, 0), pygame.SRCALPHA)
        else:
            button.surface = button.original_surface.copy()
        old_center = button.rect.center
        button.rect = button.surface.get_rect()
        button.rect.center = old_center
        button.needs_transform = False
    offset_x, offset_y = get_screen_offset(button)
    total_offset_x = offset_x + round(button.current_offset[0])
    total_offset_y = offset_y + round(button.current_offset[1])
    draw_rect = button.rect.move(total_offset_x, total_offset_y)
    surface.blit(button.surface, draw_rect)

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

    if is_hovering and not button.is_hovered:
        button.is_hovered = True
        button.trigger_event("<MOUSE-IN>")
        if button.tooltip:
            button.tooltip.show()
    elif is_hovering and button.is_hovered:
        button.is_hovered = True
        button.trigger_event("<HOVER>")
    elif not is_hovering and button.is_hovered:
        button.is_hovered = False
        button.trigger_event("<MOUSE-OUT>")
        if button.tooltip:
            button.tooltip.hide()


def is_point_in_rounded_rect(button, point):
    offset_x, offset_y = get_screen_offset(button)
    total_offset_x = offset_x + round(button.current_offset[0])
    total_offset_y = offset_y + round(button.current_offset[1])
    rect = button.rect.move(total_offset_x, total_offset_y)
    if not rect.collidepoint(point):
        return False
    x, y = point
    geom_rect = rect
    scale = button.current_scale
    rotation = button.current_rotation
    if scale != 1 or rotation != 0:
        cx, cy = rect.center
        if rotation != 0:
            v = pygame.math.Vector2(x - cx, y - cy)
            v = v.rotate(rotation)
            x, y = cx + v.x, cy + v.y
        base_w = button.width * scale
        base_h = button.height * scale
        geom_rect = pygame.Rect(0, 0, base_w, base_h)
        geom_rect.center = (cx, cy)
        if not geom_rect.collidepoint((x, y)):
            return False
    r = button.corner_radius * scale
    r = min(r, geom_rect.width // 2, geom_rect.height // 2)
    if r <= 0:
        return True
    if (geom_rect.left + r <= x <= geom_rect.right - r) or (geom_rect.top + r <= y <= geom_rect.bottom - r):
        return True
    centers = [
        (geom_rect.left + r, geom_rect.top + r),
        (geom_rect.right - r, geom_rect.top + r),
        (geom_rect.left + r, geom_rect.bottom - r),
        (geom_rect.right - r, geom_rect.bottom - r)
    ]
    for cx, cy in centers:
        if ((x - cx) ** 2 + (y - cy) ** 2) <= r ** 2:
            return True
    return False


def react(button, event=None):
    for func in button.scheduled_functions[:]:
        func[1] -= 1
        if func[1] <= 0:
            func[0]()
            button.scheduled_functions.remove(func)
    if button.state != "enabled" or not button.visible:
        button.pressed = False
        return
    mouse_pos = pygame.mouse.get_pos()
    is_inside = is_point_in_rounded_rect(button, mouse_pos)
    if not event:
        if pygame.mouse.get_pressed()[0]:
            button.trigger_event("<HOLD>")
            if is_inside:
                button.pressed = True
        elif not pygame.mouse.get_pressed()[0]:
            if button.pressed:
                button.trigger_event("<RELEASE>")
                button.pressed = False
    else:
        if event.type == pygame.KEYDOWN:
            button.trigger_event("<KEY>")
            if event.unicode:
                button.trigger_event(event.unicode)
            keyname = pygame.key.name(event.key)
            button.trigger_event(f"<{keyname.upper()}>")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                button.trigger_event("<PRESS>")
                if is_inside:
                    button.pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                button.trigger_event("<RELEASE>")
                button.pressed = False