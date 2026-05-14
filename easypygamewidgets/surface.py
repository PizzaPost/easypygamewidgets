import time

import pygame

from easypygamewidgets import misc

pygame.init()


class Surface:
    def __init__(self, surface: pygame.Surface, screen: "easypygamewidgets.Screen | None" = None,
                 state: str | None = None,
                 active_hover_cursor: pygame.Cursor = None,
                 disabled_hover_cursor: pygame.Cursor = None,
                 active_pressed_cursor: pygame.Cursor = None, dragable: bool = False, layer=1000,
                 tooltip: "easypygamewidgets.Tooltip | None" = None, data=None):
        self.surface = surface
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
                        f"No custom cursor is used for the surface {self.text} because it's not a pygame.Cursor object. ({cursor})")
                self.cursors[name] = None
        self.dragable = dragable
        self.layer = layer
        self.tooltip = tooltip
        if tooltip:
            tooltip.configure(layer=self.layer + 1)
            if not tooltip.style:
                tooltip.configure(active_unpressed_text_color=(255, 255, 255, 255),
                                  active_unpressed_background_color=(50, 50, 50, 255),
                                  active_unpressed_border_color=(100, 100, 100, 255))
        self.data = data
        self.x = 0
        self.y = 0
        self.alive = True
        self.pressed = False
        self.rect = surface.get_rect()
        self.original_cursor = None
        self.drag_offset = None
        self.is_dragging = False
        self.last_checked_dragging = None
        self.bindings = {}
        self.original_surface = surface
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
        if 'surface' in kwargs:
            self.original_surface = kwargs["surface"]
        if 'x' in kwargs or 'y' in kwargs or 'surface' in kwargs:
            self.rect = pygame.Rect(self.x, self.y, self.surface.get_width(), self.surface.get_height())
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
        self.rect = pygame.Rect(self.x, self.y, self.surface.get_width(), self.surface.get_height())
        return self

    def bind(self, event: str, command, require_hover: bool = True):
        self.bindings[event] = {"command": command, "require_hover": require_hover}
        return self

    def trigger_event(self, event: str, *args, **kwargs):
        if event in self.bindings:
            binding_data = self.bindings[event]
            command = binding_data["command"]
            require_hover = binding_data["require_hover"]
            offset_x, offset_y = get_screen_offset(self)
            total_offset_x = offset_x + round(self.current_offset[0])
            total_offset_y = offset_y + round(self.current_offset[1])
            if not require_hover or self.rect.move(total_offset_x, total_offset_y).collidepoint(pygame.mouse.get_pos()):
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
            tooltip.configure(active_unpressed_text_color=(255, 255, 255, 255),
                              active_unpressed_background_color=(50, 50, 50, 255),
                              active_unpressed_border_color=(100, 100, 100, 255))
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


def update_animation(surface):
    if surface.current_scale != surface.target_scale:
        if abs(surface.current_scale - surface.target_scale) <= abs(surface.scale_step):
            surface.current_scale = surface.target_scale
        else:
            surface.current_scale += surface.scale_step
    if surface.current_rotation != surface.target_rotation:
        if abs(surface.current_rotation - surface.target_rotation) <= abs(surface.rotation_step):
            surface.current_rotation = surface.target_rotation
        else:
            surface.current_rotation += surface.rotation_step
    for x in range(2):
        if surface.current_offset[x] != surface.target_offset[x]:
            if abs(surface.current_offset[x] - surface.target_offset[x]) <= abs(surface.offset_step[x]):
                surface.current_offset[x] = float(surface.target_offset[x])
            else:
                surface.current_offset[x] += surface.offset_step[x]
    if surface.current_scale != 1 or surface.current_rotation != 0:
        new_width = int(surface.original_surface.get_width() * surface.current_scale)
        new_height = int(surface.original_surface.get_height() * surface.current_scale)
        if new_width > 0 and new_height > 0:
            if surface.use_rotozoom:
                surface.surface = pygame.transform.rotozoom(surface.original_surface, surface.current_rotation,
                                                            surface.current_scale)
            else:
                scaled_surface = pygame.transform.smoothscale(surface.original_surface, (new_width, new_height))
                surface.surface = pygame.transform.rotate(scaled_surface, surface.current_rotation)
            old_center = surface.rect.center
            surface.rect = surface.surface.get_rect()
            surface.rect.center = old_center


def get_screen_offset(widget):
    if widget.screen:
        return widget.screen.x, widget.screen.y
    return 0, 0


def draw(surface, window: pygame.Surface):
    if not surface.alive or not surface.visible:
        return
    mouse_pos = pygame.mouse.get_pos()
    offset_x, offset_y = get_screen_offset(surface)
    total_offset_x = offset_x + round(surface.current_offset[0])
    total_offset_y = offset_y + round(surface.current_offset[1])
    interaction_rect = surface.rect.move(total_offset_x, total_offset_y)
    is_hovering = interaction_rect.collidepoint(mouse_pos)
    if is_hovering:
        if surface.state == "enabled":
            if surface.pressed:
                cursor_key = "active_pressed"
            else:
                cursor_key = "active_hover"
        else:
            cursor_key = "disabled_hover"
        target_cursor = surface.cursors.get(cursor_key)
        if target_cursor:
            current_cursor = pygame.mouse.get_cursor()
            if current_cursor != target_cursor:
                if surface.original_cursor is None:
                    surface.original_cursor = current_cursor
                pygame.mouse.set_cursor(target_cursor)
    else:
        if surface.original_cursor:
            pygame.mouse.set_cursor(surface.original_cursor)
            surface.original_cursor = None

    if is_hovering and not getattr(surface, "is_hovered", False):
        surface.is_hovered = True
        surface.trigger_event("<MOUSE-IN>")
        if surface.tooltip:
            surface.tooltip.show()
    elif is_hovering and getattr(surface, "is_hovered", False):
        surface.is_hovered = True
        surface.trigger_event("<HOVER>")
    elif not is_hovering and getattr(surface, "is_hovered", False):
        surface.is_hovered = False
        surface.trigger_event("<MOUSE-OUT>")
        if surface.tooltip:
            surface.tooltip.hide()

    draw_rect = surface.rect.move(total_offset_x, total_offset_y)
    window.blit(surface.surface, draw_rect)


def react(surface, event=None):
    for func in surface.scheduled_functions:
        func[1] -= 1
        if func[1] <= 0:
            func[0]()
            surface.scheduled_functions.remove(func)
    if surface.state != "enabled" or not surface.visible:
        surface.pressed = False
        return
    mouse_pos = pygame.mouse.get_pos()
    offset_x, offset_y = get_screen_offset(surface)
    total_offset_x = offset_x + round(surface.current_offset[0])
    total_offset_y = offset_y + round(surface.current_offset[1])
    interaction_rect = surface.rect.move(total_offset_x, total_offset_y)
    is_inside = interaction_rect.collidepoint(mouse_pos)
    current_time = time.time()
    if not event:
        if pygame.mouse.get_pressed()[0] and is_inside:
            surface.pressed = True
            surface.trigger_event("<HOLD>")
        elif not pygame.mouse.get_pressed()[0] and is_inside:
            if surface.pressed:
                surface.pressed = False
                surface.trigger_event("<RELEASE>")
        elif not pygame.mouse.get_pressed()[0] and not is_inside:
            surface.pressed = False
    else:
        if event.type == pygame.MOUSEMOTION:
            if surface.pressed and surface.dragable:
                if is_inside or surface.is_dragging:
                    surface.is_dragging = True
                    surface.last_checked_dragging = current_time
                    if surface.drag_offset:
                        new_x = mouse_pos[0] - surface.drag_offset[0] - total_offset_x
                        new_y = mouse_pos[1] - surface.drag_offset[1] - total_offset_y
                        surface.place(new_x, new_y)
        if event.type == pygame.KEYDOWN:
            surface.trigger_event("<KEY>")
            if event.unicode:
                surface.trigger_event(event.unicode)
            keyname = pygame.key.name(event.key)
            surface.trigger_event(f"<{keyname.upper()}>")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                surface.trigger_event("<PRESS>")
                if is_inside:
                    surface.pressed = True
                    surface.drag_offset = (mouse_pos[0] - (surface.x + total_offset_x),
                                           mouse_pos[1] - (surface.y + total_offset_y))
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and surface.pressed:
                surface.trigger_event("<RELEASE>")
                surface.pressed = False
                surface.is_dragging = False
    if surface.last_checked_dragging:
        if current_time - surface.last_checked_dragging > 0.2:
            surface.is_dragging = False
    if surface.pressed and not surface.is_dragging:
        surface.trigger_event("<HOLD>")
    if surface.pressed and surface.is_dragging:
        surface.trigger_event("<DRAG>")