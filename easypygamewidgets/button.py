# button.py
# by PizzaPost
# https://github.com/PizzaPost/easypygamewidgets


import pygame
from typing_extensions import Unpack, Any

from easypygamewidgets import font, misc
from .assets import TypeHints

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
                 active_hover_cursor: pygame.Cursor | None = None,
                 disabled_hover_cursor: pygame.Cursor | None = None,
                 active_pressed_cursor: pygame.Cursor | None = None,
                 font: pygame.font.Font = font.default_font, alignment: str = "center",
                 command=None, alignment_spacing: int = 40, corner_radius: int = 20, layer=1000, line_spacing: int = 30,
                 tooltip: "easypygamewidgets.Tooltip | None" = None, min_width: int | None = None,
                 max_width: int | None = None, min_height: int | None = None, max_height: int | None = None,
                 data: Any = None):
        self._bindings = {}
        if screen:
            screen.add_widget(self)
            self._screen = screen
            if state:
                self._state = state
        else:
            self._screen = None
            self._visible = True
            if state:
                self._state = state
            else:
                self._state = "enabled"
        self._auto_size = auto_size
        if self._auto_size:
            font.set_linesize(line_spacing)
            lines = text.split("\n")
            total_w = 0
            for line in lines:
                text_w, text_h = font.size(line)
                if text_w > total_w:
                    total_w = text_w
            total_h = len(lines) * line_spacing
            self._width = total_w + alignment_spacing
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
        self._text = text
        self._active_unpressed_text_color = normalize_color(active_unpressed_text_color)
        self._disabled_unpressed_text_color = normalize_color(disabled_unpressed_text_color)
        self._active_hover_text_color = normalize_color(active_hover_text_color)
        self._disabled_hover_text_color = normalize_color(disabled_hover_text_color)
        self._active_pressed_text_color = normalize_color(active_pressed_text_color)
        self._active_unpressed_background_color = normalize_color(active_unpressed_background_color)
        self._disabled_unpressed_background_color = normalize_color(disabled_unpressed_background_color)
        self._active_hover_background_color = normalize_color(active_hover_background_color)
        self._disabled_hover_background_color = normalize_color(disabled_hover_background_color)
        self._active_pressed_background_color = normalize_color(active_pressed_background_color)
        self._active_unpressed_border_color = normalize_color(active_unpressed_border_color)
        self._disabled_unpressed_border_color = normalize_color(disabled_unpressed_border_color)
        self._active_hover_border_color = normalize_color(active_hover_border_color)
        self._disabled_hover_border_color = normalize_color(disabled_hover_border_color)
        self._active_pressed_border_color = normalize_color(active_pressed_border_color)
        self._border_thickness = border_thickness
        cursor_input = {
            "active_hover": active_hover_cursor,
            "disabled_hover": disabled_hover_cursor,
            "active_pressed": active_pressed_cursor
        }
        self._cursors = {}
        for name, cursor in cursor_input.items():
            if isinstance(cursor, pygame.Cursor):
                self._cursors[name] = cursor
            else:
                if cursor is not None:
                    print(
                        f"No custom cursor is used for the button {text} because it's not a pygame.Cursor object. ({cursor})")
                self._cursors[name] = None
        self._font = font
        self._alignment = alignment
        if command:
            self._bind("<RELEASE>", command)
        self._alignment_spacing = alignment_spacing
        self._corner_radius = corner_radius
        self._layer = layer
        self._tooltip = tooltip
        if tooltip:
            tooltip.configure(_layer=layer + 1)
            if not tooltip.style:
                tooltip.configure(active_unpressed_text_color=self._active_unpressed_text_color,
                                  active_unpressed_background_color=self._active_unpressed_background_color,
                                  active_unpressed_border_color=self._active_unpressed_border_color)
        self._line_spacing = line_spacing
        self._min_width = min_width
        self._max_width = max_width
        self._min_height = min_height
        self._max_height = max_height
        self._data = data
        self._x = 0
        self._y = 0
        self._alive = True
        self._pressed = False
        self._rect = pygame.Rect(self._x, self._y, self._width, self._height)
        self._original_cursor = None
        self._scheduled_functions = []
        self._is_hovered = False
        self._last_visual_state = None
        self._needs_redraw = True
        self._cached_surface = None
        self._needs_transform = True
        self._original_surface = pygame.Surface((1, 1))
        self._target_scale = 1
        self._current_scale = 1
        self._scale_step = 0
        self._target_rotation = 0
        self._current_rotation = 0
        self._rotation_step = 0
        self._target_offset = (0, 0)
        self._current_offset = [0, 0]
        self._offset_step = [0, 0]
        self._use_rotozoom = False

        self._font.set_linesize(line_spacing)

        misc.add_widget(self)

    @property
    def bindings(self):
        return self._bindings

    @bindings.setter
    def bindings(self, value):
        self._bindings = value

    @property
    def width(self):
        return int(self._width * self._current_scale)

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return int(self._height * self._current_scale)

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def screen(self):
        return self._screen

    @screen.setter
    def screen(self, value):
        self._set_screen(value)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        self._visible = value

    @property
    def auto_size(self):
        return self._auto_size

    @auto_size.setter
    def auto_size(self, value):
        self._auto_size = value

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    @property
    def active_unpressed_text_color(self):
        return self._active_unpressed_text_color

    @active_unpressed_text_color.setter
    def active_unpressed_text_color(self, value):
        self._active_unpressed_text_color = normalize_color(value)

    @property
    def disabled_unpressed_text_color(self):
        return self._disabled_unpressed_text_color

    @disabled_unpressed_text_color.setter
    def disabled_unpressed_text_color(self, value):
        self._disabled_unpressed_text_color = normalize_color(value)

    @property
    def active_hover_text_color(self):
        return self._active_hover_text_color

    @active_hover_text_color.setter
    def active_hover_text_color(self, value):
        self._active_hover_text_color = normalize_color(value)

    @property
    def disabled_hover_text_color(self):
        return self._disabled_hover_text_color

    @disabled_hover_text_color.setter
    def disabled_hover_text_color(self, value):
        self._disabled_hover_text_color = normalize_color(value)

    @property
    def active_pressed_text_color(self):
        return self._active_pressed_text_color

    @active_pressed_text_color.setter
    def active_pressed_text_color(self, value):
        self._active_pressed_text_color = normalize_color(value)

    @property
    def active_unpressed_background_color(self):
        return self._active_unpressed_background_color

    @active_unpressed_background_color.setter
    def active_unpressed_background_color(self, value):
        self._active_unpressed_background_color = normalize_color(value)

    @property
    def disabled_unpressed_background_color(self):
        return self._disabled_unpressed_background_color

    @disabled_unpressed_background_color.setter
    def disabled_unpressed_background_color(self, value):
        self._disabled_unpressed_background_color = normalize_color(value)

    @property
    def active_hover_background_color(self):
        return self._active_hover_background_color

    @active_hover_background_color.setter
    def active_hover_background_color(self, value):
        self._active_hover_background_color = normalize_color(value)

    @property
    def disabled_hover_background_color(self):
        return self._disabled_hover_background_color

    @disabled_hover_background_color.setter
    def disabled_hover_background_color(self, value):
        self._disabled_hover_background_color = normalize_color(value)

    @property
    def active_pressed_background_color(self):
        return self._active_pressed_background_color

    @active_pressed_background_color.setter
    def active_pressed_background_color(self, value):
        self._active_pressed_background_color = normalize_color(value)

    @property
    def active_unpressed_border_color(self):
        return self._active_unpressed_border_color

    @active_unpressed_border_color.setter
    def active_unpressed_border_color(self, value):
        self._active_unpressed_border_color = normalize_color(value)

    @property
    def disabled_unpressed_border_color(self):
        return self._disabled_unpressed_border_color

    @disabled_unpressed_border_color.setter
    def disabled_unpressed_border_color(self, value):
        self._disabled_unpressed_border_color = normalize_color(value)

    @property
    def active_hover_border_color(self):
        return self._active_hover_border_color

    @active_hover_border_color.setter
    def active_hover_border_color(self, value):
        self._active_hover_border_color = normalize_color(value)

    @property
    def disabled_hover_border_color(self):
        return self._disabled_hover_border_color

    @disabled_hover_border_color.setter
    def disabled_hover_border_color(self, value):
        self._disabled_hover_border_color = normalize_color(value)

    @property
    def active_pressed_border_color(self):
        return self._active_pressed_border_color

    @active_pressed_border_color.setter
    def active_pressed_border_color(self, value):
        self._active_pressed_border_color = normalize_color(value)

    @property
    def border_thickness(self):
        return self._border_thickness

    @border_thickness.setter
    def border_thickness(self, value):
        self._border_thickness = value

    @property
    def active_hover_cursor(self):
        return self._cursors["active_hover"]

    @active_hover_cursor.setter
    def active_hover_cursor(self, value):
        self._cursors["active_hover"] = value

    @property
    def disabled_hover_cursor(self):
        return self._cursors["disabled_hover"]

    @disabled_hover_cursor.setter
    def disabled_hover_cursor(self, value):
        self._cursors["disabled_hover"] = value

    @property
    def active_pressed_cursor(self):
        return self._cursors["active_pressed"]

    @active_pressed_cursor.setter
    def active_pressed_cursor(self, value):
        self._cursors["active_pressed"] = value

    @property
    def cursors(self):
        return self._cursors

    @cursors.setter
    def cursors(self, value):
        self._cursors = value

    @property
    def font(self):
        return self._font

    @font.setter
    def font(self, value):
        self._font = value

    @property
    def alignment(self):
        return self._alignment

    @alignment.setter
    def alignment(self, value):
        self._alignment = value

    @property
    def command(self):
        return self._bindings["<RELEASE>"]

    @command.setter
    def command(self, value):
        self._bind("<RELEASE>", value)

    @property
    def alignment_spacing(self):
        return self._alignment_spacing

    @alignment_spacing.setter
    def alignment_spacing(self, value):
        self._alignment_spacing = value

    @property
    def corner_radius(self):
        return self._corner_radius

    @corner_radius.setter
    def corner_radius(self, value):
        self._corner_radius = value

    @property
    def layer(self):
        return self._layer

    @layer.setter
    def layer(self, value):
        self._layer = value
        if self._tooltip:
            self._tooltip.configure(_layer=self._layer + 1)
        misc.resort_layers()

    @property
    def tooltip(self):
        return self._tooltip

    @tooltip.setter
    def tooltip(self, value):
        self._set_tooltip(value)

    @property
    def line_spacing(self):
        return self._line_spacing

    @line_spacing.setter
    def line_spacing(self, value):
        self._line_spacing = value

    @property
    def min_width(self):
        return self._min_width

    @min_width.setter
    def min_width(self, value):
        self._min_width = value

    @property
    def max_width(self):
        return self._max_width

    @max_width.setter
    def max_width(self, value):
        self._max_width = value

    @property
    def min_height(self):
        return self._min_height

    @min_height.setter
    def min_height(self, value):
        self._min_height = value

    @property
    def max_height(self):
        return self._max_height

    @max_height.setter
    def max_height(self, value):
        self._max_height = value

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def alive(self):
        return self._alive

    @alive.setter
    def alive(self, value):
        self._alive = value

    @property
    def pressed(self):
        return self._pressed

    @pressed.setter
    def pressed(self, value):
        self._pressed = value

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, value):
        self._rect = value

    @property
    def original_cursor(self):
        return self._original_cursor

    @original_cursor.setter
    def original_cursor(self, value):
        self._original_cursor = value

    @property
    def scheduled_functions(self):
        return self._scheduled_functions

    @scheduled_functions.setter
    def scheduled_functions(self, value):
        self._scheduled_functions = value

    @property
    def is_hovered(self):
        return self._is_hovered

    @is_hovered.setter
    def is_hovered(self, value):
        self._is_hovered = value

    @property
    def last_visual_state(self):
        return self._last_visual_state

    @last_visual_state.setter
    def last_visual_state(self, value):
        self._last_visual_state = value

    @property
    def needs_redraw(self):
        return self._needs_redraw

    @needs_redraw.setter
    def needs_redraw(self, value):
        self._needs_redraw = value

    @property
    def cached_surface(self):
        return self._cached_surface

    @cached_surface.setter
    def cached_surface(self, value):
        self._cached_surface = value

    @property
    def needs_transform(self):
        return self._needs_transform

    @needs_transform.setter
    def needs_transform(self, value):
        self._needs_transform = value

    @property
    def original_surface(self):
        return self._original_surface

    @original_surface.setter
    def original_surface(self, value):
        self._original_surface = value

    @property
    def target_scale(self):
        return self._target_scale

    @target_scale.setter
    def target_scale(self, value):
        self._target_scale = value

    @property
    def current_scale(self):
        return self._current_scale

    @current_scale.setter
    def current_scale(self, value):
        self._current_scale = value

    @property
    def scale_step(self):
        return self._scale_step

    @scale_step.setter
    def scale_step(self, value):
        self._scale_step = value

    @property
    def target_rotation(self):
        return self._target_rotation

    @target_rotation.setter
    def target_rotation(self, value):
        self._target_rotation = value

    @property
    def current_rotation(self):
        return self._current_rotation

    @current_rotation.setter
    def current_rotation(self, value):
        self._current_rotation = value

    @property
    def rotation_step(self):
        return self._rotation_step

    @rotation_step.setter
    def rotation_step(self, value):
        self._rotation_step = value

    @property
    def target_offset(self):
        return self._target_offset

    @target_offset.setter
    def target_offset(self, value):
        self._target_offset = value

    @property
    def current_offset(self):
        return self._current_offset

    @current_offset.setter
    def current_offset(self, value):
        self._current_offset = value

    @property
    def offset_step(self):
        return self._offset_step

    @offset_step.setter
    def offset_step(self, value):
        self._offset_step = value

    @property
    def use_rotozoom(self):
        return self._use_rotozoom

    @use_rotozoom.setter
    def use_rotozoom(self, value):
        self._use_rotozoom = value

    def _configure(self, **kwargs: Unpack[TypeHints.ButtonConfig]):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self._needs_redraw = True
        self._needs_transform = True
        if any(k in kwargs for k in
               ('auto_size', 'x', 'y', 'width', 'height', 'text', 'font', 'max_width', 'min_width', 'max_height',
                'min_height', 'line_spacing', "alignment_spacing")):
            if self._auto_size:
                self._font.set_linesize(self._line_spacing)
                lines = self._text.split("\n")
                total_w = 0
                for line in lines:
                    text_w, text_h = self._font.size(line)
                    if text_w > total_w:
                        total_w = text_w
                total_h = len(lines) * self._line_spacing
                self._width = total_w + self._alignment_spacing
                if self._min_width:
                    self._width = max(self._width, self._min_width)
                if self._max_width:
                    self._width = min(self._width, self._max_width)
                self._height = total_h + 20
                if self._min_height:
                    self._height = max(total_h + 20, self._min_height)
                if self._max_height:
                    self._height = min(total_h + 20, self._max_height)
            self._rect = pygame.Rect(self._x, self._y, self._width, self._height)
        if 'line_spacing' in kwargs:
            self._font.set_linesize(self._line_spacing)
        return self

    def _config(self, **kwargs: Unpack[TypeHints.ButtonConfig]):
        self._configure(**kwargs)

    def _delete(self):
        self._alive = False
        if self in misc.all_widgets:
            misc.all_widgets.remove(self)

    def _place(self, x: int, y: int, mode: str = "px"):
        if mode == "px":
            self._x = x
            self._y = y
        elif mode in ("%", "percent", "percentage"):
            screen_width = misc.pg.get_width()
            screen_height = misc.pg.get_height()
            self._x = int(x * screen_width / 100)
            self._y = int(y * screen_height / 100)
        else:
            self._x = x
            self._y = y
            print(f"Invalid Mode: {mode}\nFallback: px")
        self._rect = pygame.Rect(self._x, self._y, self._width, self._height)
        self._needs_transform = True
        return self

    def _bind(self, event: str, command, require_hover: bool = True):
        self._bindings[event] = {"command": command, "require_hover": require_hover}
        return self

    def _trigger_event(self, event: str, *args, **kwargs):
        if event in self._bindings:
            binding_data = self._bindings[event]
            command = binding_data["command"]
            require_hover = binding_data["require_hover"]
            if not require_hover or is_point_in_rounded_rect(self, pygame.mouse.get_pos()):
                command(*args, **kwargs)

    def _set_screen(self, screen):
        if self in screen.widgets:
            return self
        self._screen = screen
        screen.add_widget(self)
        return self

    def _unbind(self, event: str):
        if event in self._bindings:
            del self._bindings[event]
        return self

    def _unbind_all(self):
        self._bindings.clear()
        return self

    def _set_tooltip(self, tooltip):
        self._tooltip = tooltip
        tooltip.configure(_layer=self._layer + 1)
        if not tooltip.style:
            tooltip.configure(active_unpressed_text_color=self._active_unpressed_text_color,
                              active_unpressed_background_color=self._active_unpressed_background_color,
                              active_unpressed_border_color=self._active_unpressed_border_color)
        return self

    def _remove_tooltip(self):
        if self._tooltip:
            self._tooltip.configure(visible=False)
            self._tooltip = None
        return self

    def _scale(self, value=None, frames_to_finish=1):
        if frames_to_finish <= 0:
            frames_to_finish = 1
        if value is None:
            self._target_scale = 1
        else:
            self._target_scale = value
        self._scale_step = (self._target_scale - self._current_scale) / frames_to_finish
        update_animation(self)
        return self

    def _rotate(self, value=None, frames_to_finish=1):
        if frames_to_finish <= 0:
            frames_to_finish = 1
        if value is None:
            self._target_rotation = 0
        else:
            self._target_rotation = value
        self._rotation_step = (self._target_rotation - self._current_rotation) / frames_to_finish
        update_animation(self)
        return self

    def _rotozoom(self, scale=None, rotation=None, frames_to_finish=1):
        if frames_to_finish <= 0:
            frames_to_finish = 1
        self._target_scale = 1 if scale is None else scale
        self._scale_step = (self._target_scale - self._current_scale) / frames_to_finish
        self._target_rotation = 0 if rotation is None else rotation
        self._rotation_step = (self._target_rotation - self._current_rotation) / frames_to_finish
        self._use_rotozoom = True
        update_animation(self)
        return self

    def _offset(self, value: tuple[int, int], frames_to_finish=1):
        if frames_to_finish <= 0:
            frames_to_finish = 1
        if value is None:
            self._target_offset = (0, 0)
        else:
            self._target_offset = value
        self._offset_step[0] = (self._target_offset[0] - self._current_offset[0]) / frames_to_finish
        self._offset_step[1] = (self._target_offset[1] - self._current_offset[1]) / frames_to_finish
        update_animation(self)
        return self

    def _schedule(self, function, frames_to_execute):
        if frames_to_execute < 1:
            frames_to_execute = 1
        self._scheduled_functions.append([function, frames_to_execute])
        return self

    @property
    def configure(self):
        return self._configure

    @property
    def config(self):
        return self._config

    @property
    def delete(self):
        return self._delete

    @property
    def place(self):
        return self._place

    @property
    def bind(self):
        return self._bind

    @property
    def trigger_event(self):
        return self._trigger_event

    @property
    def set_screen(self):
        return self._set_screen

    @property
    def unbind(self):
        return self._unbind

    @property
    def unbind_all(self):
        return self._unbind_all

    @property
    def set_tooltip(self):
        return self._set_tooltip

    @property
    def remove_tooltip(self):
        return self._remove_tooltip

    @property
    def scale(self):
        return self._scale

    @property
    def rotate(self):
        return self._rotate

    @property
    def rotozoom(self):
        return self._rotozoom

    @property
    def offset(self):
        return self._offset

    @property
    def schedule(self):
        return self._schedule


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
        return 0, 0, 0, 0
    if len(color) == 3:
        return *color, 255
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

    cached = pygame.Surface((button.width, button.height), pygame.SRCALPHA)
    local_rect = pygame.Rect(0, 0, button.width, button.height)
    pygame.draw.rect(cached, bg_color, local_rect, border_radius=button.corner_radius)
    if brd_color:
        pygame.draw.rect(cached, brd_color, local_rect, width=button.border_thickness,
                         border_radius=button.corner_radius)

    if button.alignment == "stretched" and len(button.text) > 1 and not button.auto_size:
        total_char_width = sum(button.font.render(char, True, text_color).get_width() for char in button.text)
        available_width = local_rect.width - button.alignment_spacing
        if available_width > total_char_width:
            spacing = (available_width - total_char_width) / (len(button.text) - 1)
            current_x = local_rect.left + button.alignment_spacing // 2
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

    if button.needs_transform:
        if button.current_scale != 1 or button.current_rotation != 0:
            new_width = int(button.original_surface.get_width() * button.current_scale)
            new_height = int(button.original_surface.get_height() * button.current_scale)
            if new_width > 0 and new_height > 0:
                if button.use_rotozoom:
                    button.cached_surface = pygame.transform.rotozoom(button.original_surface, button.current_rotation,
                                                                      button.current_scale)
                else:
                    scaled_surface = pygame.transform.smoothscale(button.original_surface, (new_width, new_height))
                    button.cached_surface = pygame.transform.rotate(scaled_surface, button.current_rotation)
            else:
                button.cached_surface = pygame.Surface((0, 0), pygame.SRCALPHA)
        else:
            button.surface = button.original_surface.copy()
        old_center = button.rect.center
        button.rect = button.cached_surface.get_rect()
        button.rect.center = old_center
        button.needs_transform = False
    offset_x, offset_y = get_screen_offset(button)
    total_offset_x = offset_x + round(button.current_offset[0])
    total_offset_y = offset_y + round(button.current_offset[1])
    draw_rect = button.rect.move(total_offset_x, total_offset_y)
    surface.blit(button.cached_surface, draw_rect)

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