# entry.py
# by PizzaPost
# https://github.com/PizzaPost/easypygamewidgets

import sys

import pygame
from typing_extensions import Unpack, Any

from easypygamewidgets import font, misc
from .assets import TypeHints

pygame.init()


# PERFECTION
# everything private/properties ✅
# basic animations ✅
# free spacing ✅
# cache system ✅
# config suggestions ✅
# optimized set_screen function ✅
# scroll with text ✅
# rgba color ✅
# four different corner radii ✅

class Entry:
    def __init__(self, screen: "easypygamewidgets.Screen | None" = None, auto_size: bool = True, width: int = 180,
                 height: int = 80, placeholder_text: str = "easypygamewidgets Entry",
                 text: str = "", char_limit: int | None = None,
                 show: str | None = None, state: str | None = None,
                 active_unpressed_text_color: tuple | None = (255, 255, 255, 255),
                 disabled_unpressed_text_color: tuple | None = (150, 150, 150, 255),
                 active_hover_text_color: tuple | None = (255, 255, 255, 255),
                 disabled_hover_text_color: tuple | None = (150, 150, 150, 255),
                 active_pressed_text_color: tuple | None = (200, 200, 200, 255),
                 active_unpressed_background_color: tuple | None = (50, 50, 50, 255),
                 disabled_unpressed_background_color: tuple | None = (30, 30, 30, 255),
                 active_hover_background_color: tuple | None = (70, 70, 70, 255),
                 disabled_hover_background_color: tuple | None = (30, 30, 30, 255),
                 active_pressed_background_color: tuple | None = (40, 40, 40, 255),
                 active_unpressed_border_color: tuple | None = (100, 100, 100, 255),
                 disabled_unpressed_border_color: tuple | None = (60, 60, 60, 255),
                 active_hover_border_color: tuple | None = (150, 150, 150, 255),
                 disabled_hover_border_color: tuple | None = (60, 60, 60, 255),
                 active_pressed_border_color: tuple | None = (50, 50, 50, 255),
                 selection_color: tuple | None = (0, 120, 215, 255),
                 disabled_selection_color: tuple | None = (32, 106, 163, 255),
                 border_thickness: int = 2,
                 active_hover_cursor: pygame.Cursor | None = None,
                 disabled_hover_cursor: pygame.Cursor | None = None,
                 active_pressed_cursor: pygame.Cursor | None = None,
                 blinking_cursor: str = "|", blinking_speed: int = 500,
                 font: pygame.font.Font = font.default_font, alignment: str = "left",
                 alignment_spacing: int = 20, top_left_corner_radius: int = 25, top_right_corner_radius: int = 25,
                 bottom_left_corner_radius: int = 25, bottom_right_corner_radius: int = 25, repeat_delay: int = 500,
                 repeat_interval: int = 50, layer=1000, line_spacing: int = 30,
                 tooltip: "easypygamewidgets.Tooltip | None" = None, min_width: int | None = None,
                 max_width: int | None = None, min_height: int | None = None, max_height: int | None = None,
                 data: Any = None):
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
        self._width = width
        self._height = height
        if auto_size:
            if max_width:
                self._width = min(self._width, max_width)
            if min_width:
                self._width = max(self._width, min_width)
            if max_height:
                self._height = min(self._height, max_height)
            if min_height:
                self._height = max(self._height, min_height)
        self._placeholder_text = placeholder_text
        self._text = text
        self._char_limit = char_limit
        self._show = show
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
        self._selection_color = normalize_color(selection_color)
        self._disabled_selection_color = normalize_color(disabled_selection_color)
        self._border_thickness = border_thickness
        cursor_input = {
            "active_hover": active_hover_cursor,
            "disabled_hover": disabled_hover_cursor,
            "active_pressed": active_pressed_cursor
        }
        self._cursors = {}
        for name, cursor in cursor_input.items():
            if isinstance(cursor, pygame.cursors.Cursor):
                self._cursors[name] = cursor
            else:
                if cursor is not None:
                    print(
                        f"No custom cursor is used for the entry {placeholder_text} because it's not a pygame.Cursor object. ({cursor})")
                self._cursors[name] = None
        self._blinking_cursor = blinking_cursor
        self._blinking_speed = blinking_speed
        self._font = font
        self._alignment = alignment
        self._alignment_spacing = alignment_spacing
        self._top_left_corner_radius = top_left_corner_radius
        self._top_right_corner_radius = top_right_corner_radius
        self._bottom_left_corner_radius = bottom_left_corner_radius
        self._bottom_right_corner_radius = bottom_right_corner_radius
        self._repeat_delay = repeat_delay
        self._repeat_interval = repeat_interval
        self._layer = layer
        self._line_spacing = line_spacing
        self._tooltip = tooltip
        if tooltip:
            tooltip.configure(layer=layer + 1)
            if not tooltip.style:
                tooltip.configure(active_unpressed_text_color=self._active_unpressed_text_color,
                                  active_unpressed_background_color=self._active_unpressed_background_color,
                                  active_unpressed_border_color=self._active_unpressed_border_color)
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
        self._selected_text = None
        self._focused = False
        if text:
            self._cursor_position = len(text)
        else:
            self._cursor_position = 0
        self._scroll_offset = 0
        self._drag_start = None
        self._selection_anchor = None
        self._last_text_x = self._rect.left
        self._held_key_info = None
        self._next_repeat_time = 0
        self._cursor_visible = True
        self._last_blink_time = pygame.time.get_ticks()
        self._bindings = {}
        self._scheduled_functions = []
        self._last_visual_state = None
        self._needs_redraw = True
        self._cached_surface = None
        self._local_text_x = 0
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
    def screen(self):
        return self._screen

    @screen.setter
    def screen(self, value):
        self.set_screen(value)

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
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def placeholder_text(self):
        return self._placeholder_text

    @placeholder_text.setter
    def placeholder_text(self, value):
        self._placeholder_text = value

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    @property
    def char_limit(self):
        return self._char_limit

    @char_limit.setter
    def char_limit(self, value):
        self._char_limit = value

    @property
    def show(self):
        return self._show

    @show.setter
    def show(self, value):
        self._show = value

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
    def selection_color(self):
        return self._selection_color

    @selection_color.setter
    def selection_color(self, value):
        self._selection_color = normalize_color(value)

    @property
    def disabled_selection_color(self):
        return self._disabled_selection_color

    @disabled_selection_color.setter
    def disabled_selection_color(self, value):
        self._disabled_selection_color = normalize_color(value)

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
    def blinking_cursor(self):
        return self._blinking_cursor

    @blinking_cursor.setter
    def blinking_cursor(self, value):
        self._blinking_cursor = value

    @property
    def blinking_speed(self):
        return self._blinking_speed

    @blinking_speed.setter
    def blinking_speed(self, value):
        self._blinking_speed = value

    @property
    def font(self):
        return self._font

    @font.setter
    def font(self, value):
        self._font = value
        self._font.set_linesize(self._line_spacing)

    @property
    def alignment(self):
        return self._alignment

    @alignment.setter
    def alignment(self, value):
        self._alignment = value

    @property
    def alignment_spacing(self):
        return self._alignment_spacing

    @alignment_spacing.setter
    def alignment_spacing(self, value):
        self._alignment_spacing = value

    @property
    def top_left_corner_radius(self):
        return self._top_left_corner_radius

    @top_left_corner_radius.setter
    def top_left_corner_radius(self, value):
        self._top_left_corner_radius = value

    @property
    def top_right_corner_radius(self):
        return self._top_right_corner_radius

    @top_right_corner_radius.setter
    def top_right_corner_radius(self, value):
        self._top_right_corner_radius = value

    @property
    def bottom_left_corner_radius(self):
        return self._bottom_left_corner_radius

    @bottom_left_corner_radius.setter
    def bottom_left_corner_radius(self, value):
        self._bottom_left_corner_radius = value

    @property
    def bottom_right_corner_radius(self):
        return self._bottom_right_corner_radius

    @bottom_right_corner_radius.setter
    def bottom_right_corner_radius(self, value):
        self._bottom_right_corner_radius = value

    @property
    def repeat_delay(self):
        return self._repeat_delay

    @repeat_delay.setter
    def repeat_delay(self, value):
        self._repeat_delay = value

    @property
    def repeat_interval(self):
        return self._repeat_interval

    @repeat_interval.setter
    def repeat_interval(self, value):
        self._repeat_interval = value

    @property
    def layer(self):
        return self._layer

    @layer.setter
    def layer(self, value):
        self._layer = value
        misc.resort_layers()

    @property
    def line_spacing(self):
        return self._line_spacing

    @line_spacing.setter
    def line_spacing(self, value):
        self._line_spacing = value
        self._font.set_linesize(value)

    @property
    def tooltip(self):
        return self._tooltip

    @tooltip.setter
    def tooltip(self, value):
        self.set_tooltip(value)

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
    def selected_text(self):
        return self._selected_text

    @selected_text.setter
    def selected_text(self, value):
        self._selected_text = value

    @property
    def focused(self):
        return self._focused

    @focused.setter
    def focused(self, value):
        self._focused = value

    @property
    def cursor_position(self):
        return self._cursor_position

    @cursor_position.setter
    def cursor_position(self, value):
        self._cursor_position = value

    @property
    def scroll_offset(self):
        return self._scroll_offset

    @scroll_offset.setter
    def scroll_offset(self, value):
        self._scroll_offset = value

    @property
    def drag_start(self):
        return self._drag_start

    @drag_start.setter
    def drag_start(self, value):
        self._drag_start = value

    @property
    def selection_anchor(self):
        return self._selection_anchor

    @selection_anchor.setter
    def selection_anchor(self, value):
        self._selection_anchor = value

    @property
    def last_text_x(self):
        return self._last_text_x

    @last_text_x.setter
    def last_text_x(self, value):
        self._last_text_x = value

    @property
    def held_key_info(self):
        return self._held_key_info

    @held_key_info.setter
    def held_key_info(self, value):
        self._held_key_info = value

    @property
    def next_repeat_time(self):
        return self._next_repeat_time

    @next_repeat_time.setter
    def next_repeat_time(self, value):
        self._next_repeat_time = value

    @property
    def cursor_visible(self):
        return self._cursor_visible

    @cursor_visible.setter
    def cursor_visible(self, value):
        self._cursor_visible = value

    @property
    def last_blink_time(self):
        return self._last_blink_time

    @last_blink_time.setter
    def last_blink_time(self, value):
        self._last_blink_time = value

    @property
    def bindings(self):
        return self._bindings

    @bindings.setter
    def bindings(self, value):
        self._bindings = value

    @property
    def scheduled_functions(self):
        return self._scheduled_functions

    @scheduled_functions.setter
    def scheduled_functions(self, value):
        self._scheduled_functions = value

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
    def local_text_x(self):
        return self._local_text_x

    @local_text_x.setter
    def local_text_x(self, value):
        self._local_text_x = value

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

    def _configure(self, **kwargs: Unpack[TypeHints.EntryConfig]):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self._needs_redraw = True
        if any(k in kwargs for k in
               ('auto_size', 'x', 'y', 'width', 'height', 'max_width', 'min_width', 'max_height', 'min_height')):
            if self._max_width:
                self._width = min(self._width, self._max_width)
            if self._min_width:
                self._width = max(self._width, self._min_width)
            if self._max_height:
                self._height = min(self._height, self._max_height)
            if self._min_height:
                self._height = max(self._height, self._min_height)
            self._rect = pygame.Rect(self._x, self._y, self._width, self._height)
        if 'screen' in kwargs:
            self.set_screen(kwargs["screen"])
        return self

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
        self._needs_redraw = True
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

    def _get(self):
        return self._text

    def _text_delete(self, position_start: int = 0, position_end: int | None = None):
        if position_end is None:
            position_end = len(self._text)
        position_start = max(0, min(position_start, len(self._text)))
        position_end = max(0, min(position_end, len(self._text)))
        if position_start < position_end:
            self._text = self._text[:position_start] + self._text[position_end:]
            if self._cursor_position > position_end:
                self._cursor_position -= (position_end - position_start)
            elif self._cursor_position > position_start:
                self._cursor_position = position_start
        self.reset_cursor_blink()

    def _text_insert(self, text: str, position: int = None):
        if position is None:
            position = len(self._text)
        if self._char_limit is not None and len(self._text) + len(text) > self._char_limit:
            return
        self._text = self._text[:position] + text + self._text[position:]
        self._cursor_position += len(text)
        self.reset_cursor_blink()

    def _text_select(self, position_start: int = 0, position_end: int | None = None):
        if position_end is None:
            position_end = len(self._text)
        self._selected_text = [min(position_start, position_end), max(position_start, position_end)]
        self.reset_cursor_blink()

    def _text_copy(self):
        if self._selected_text and self._selected_text[0] != self._selected_text[1]:
            start, end = self._selected_text
            clipboard_text = self._text[start:end]
            pygame.scrap.put(pygame.SCRAP_TEXT, clipboard_text.encode('utf-8'))

    def _text_cut(self):
        if self._selected_text and self._selected_text[0] != self._selected_text[1]:
            self.text_copy()
            self.text_delete(self._selected_text[0], self._selected_text[1])
            self._selected_text = None

    def _text_paste(self):
        if not pygame.scrap.get_init():
            pygame.scrap.init()
        if self._selected_text:
            self.text_delete(self._selected_text[0], self._selected_text[1])
            self._selected_text = None
        clipboard = pygame.scrap.get(pygame.SCRAP_TEXT)
        if clipboard:
            try:
                paste_text = clipboard.decode('utf-8').split('\x00')[0]
                self.text_insert(paste_text, self._cursor_position)
            except Exception as e:
                print(f"Paste error: {e}")

    def _reset_cursor_blink(self):
        self._cursor_visible = True
        self._last_blink_time = pygame.time.get_ticks()

    def _get_display_text(self):
        if self._text:
            if self._show:
                return self._show * len(self._text)
            return self._text
        elif self._placeholder_text and not self._focused:
            return self._placeholder_text
        return ""

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
        tooltip.configure(layer=self._layer + 1)
        if not tooltip.style:
            tooltip.configure(active_unpressed_text_color=self._active_unpressed_text_color,
                              active_unpressed_background_color=self._active_unpressed_background_color,
                              active_unpressed_border_color=self._active_unpressed_border_color)
        return self

    def _remove_tooltip(self):
        if self._tooltip:
            self._tooltip.visible = False
            self._tooltip = None
        return self

    def _schedule(self, function, frames_to_execute):
        if frames_to_execute < 1:
            frames_to_execute = 1
        self._scheduled_functions.append([function, frames_to_execute])
        return self

    def _scale(self, value=None, frames_to_finish=1):
        if frames_to_finish <= 0:
            frames_to_finish = 1
        self._target_scale = 1 if value is None else value
        self._scale_step = (self._target_scale - self._current_scale) / frames_to_finish
        update_animation(self)
        return self

    def _rotate(self, value=None, frames_to_finish=1):
        if frames_to_finish <= 0:
            frames_to_finish = 1
        self._target_rotation = 0 if value is None else value
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
        self._target_offset = (0, 0) if value is None else value
        self._offset_step[0] = (self._target_offset[0] - self._current_offset[0]) / frames_to_finish
        self._offset_step[1] = (self._target_offset[1] - self._current_offset[1]) / frames_to_finish
        update_animation(self)
        return self

    @property
    def configure(self):
        return self._configure

    @property
    def config(self):
        return self._configure

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
    def get(self):
        return self._get

    @property
    def text_delete(self):
        return self._text_delete

    @property
    def text_insert(self):
        return self._text_insert

    @property
    def text_select(self):
        return self._text_select

    @property
    def text_copy(self):
        return self._text_copy

    @property
    def text_cut(self):
        return self._text_cut

    @property
    def text_paste(self):
        return self._text_paste

    @property
    def reset_cursor_blink(self):
        return self._reset_cursor_blink

    @property
    def get_display_text(self):
        return self._get_display_text

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
    def schedule(self):
        return self._schedule

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


def update_animation(entry):
    scale_changed = False
    rotation_changed = False
    if entry.current_scale != entry.target_scale:
        if abs(entry.current_scale - entry.target_scale) <= abs(entry.scale_step):
            entry.current_scale = entry.target_scale
        else:
            entry.current_scale += entry.scale_step
        scale_changed = True
    if entry.current_rotation != entry.target_rotation:
        if abs(entry.current_rotation - entry.target_rotation) <= abs(entry.rotation_step):
            entry.current_rotation = entry.target_rotation
        else:
            entry.current_rotation += entry.rotation_step
        rotation_changed = True
    for x in range(2):
        if entry.current_offset[x] != entry.target_offset[x]:
            if abs(entry.current_offset[x] - entry.target_offset[x]) <= abs(entry.offset_step[x]):
                entry.current_offset[x] = float(entry.target_offset[x])
            else:
                entry.current_offset[x] += entry.offset_step[x]
    if scale_changed or rotation_changed:
        entry.needs_transform = True


def normalize_color(color):
    if color is None:
        return 0, 0, 0, 0
    if len(color) == 3:
        return *color, 255
    return color


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


def render_entry_surface(entry, is_hovering):
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
    base_width = entry.width
    base_height = entry.height
    cached = pygame.Surface((base_width, base_height), pygame.SRCALPHA)
    local_rect = pygame.Rect(0, 0, base_width, base_height)
    pygame.draw.rect(cached, bg_color, local_rect, border_top_left_radius=entry.top_left_corner_radius,
                     border_top_right_radius=entry.top_right_corner_radius,
                     border_bottom_left_radius=entry.bottom_left_corner_radius,
                     border_bottom_right_radius=entry.bottom_right_corner_radius)
    if entry.border_thickness > 0:
        pygame.draw.rect(cached, brd_color, local_rect, width=entry.border_thickness,
                         border_top_left_radius=entry.top_left_corner_radius,
                         border_top_right_radius=entry.top_right_corner_radius,
                         border_bottom_left_radius=entry.bottom_left_corner_radius,
                         border_bottom_right_radius=entry.bottom_right_corner_radius)
    clip_rect = local_rect.inflate(-4, -4)
    cached.set_clip(clip_rect)
    y_pos = local_rect.centery
    display_text = entry.get_display_text()
    drawn_stretched = False
    if entry.alignment == "stretched" and len(display_text) > 1 and not entry.auto_size:
        total_char_width = sum(entry.font.render(char, True, text_color).get_width() for char in display_text)
        available_width = local_rect.width - (entry.alignment_spacing * 2)
        if available_width > total_char_width:
            drawn_stretched = True
            spacing = (available_width - total_char_width) / (len(display_text) - 1)
            current_x = local_rect.left + entry.alignment_spacing
            for char in display_text:
                char_surf = entry.font.render(char, True, text_color)
                char_surf.set_alpha(text_color[3])
                cached.blit(char_surf, char_surf.get_rect(midleft=(current_x, y_pos)))
                current_x += char_surf.get_width() + spacing
    if not drawn_stretched:
        text_surf = entry.font.render(display_text, True, text_color)
        text_surf.set_alpha(text_color[3])
        text_rect = text_surf.get_rect()
        visible_left = local_rect.left + entry.alignment_spacing
        visible_right = local_rect.right - entry.alignment_spacing
        visible_width = visible_right - visible_left
        cursor_x_rel = entry.font.size(display_text[:entry.cursor_position])[0]
        if text_rect.width > visible_width:
            text_rect.midleft = (visible_left, y_pos)
            text_rect.x += entry.scroll_offset
            cursor_screen_x = text_rect.x + cursor_x_rel
            if cursor_screen_x > visible_right:
                entry.scroll_offset -= (cursor_screen_x - visible_right)
            elif cursor_screen_x < visible_left:
                entry.scroll_offset += (visible_left - cursor_screen_x)
            min_scroll = visible_width - text_rect.width
            max_scroll = 0
            entry.scroll_offset = max(min_scroll, min(max_scroll, entry.scroll_offset))
            text_rect.x = visible_left + entry.scroll_offset
        else:
            entry.scroll_offset = 0
            if entry.alignment == "left":
                text_rect.midleft = (visible_left, y_pos)
            elif entry.alignment == "right":
                text_rect.midright = (visible_right, y_pos)
            else:
                text_rect.center = local_rect.center
        if entry.selected_text and entry.selected_text[0] != entry.selected_text[1]:
            start_idx = min(entry.selected_text)
            end_idx = max(entry.selected_text)
            sel_start_x = entry.font.size(display_text[:start_idx])[0]
            sel_end_x = entry.font.size(display_text[:end_idx])[0]
            highlight_rect = pygame.Rect(text_rect.x + sel_start_x, text_rect.top, sel_end_x - sel_start_x,
                                         text_rect.height)
            sel_surf = pygame.Surface((highlight_rect.width, highlight_rect.height), pygame.SRCALPHA)
            sel_surf.fill(selection_color)
            cached.blit(sel_surf, highlight_rect)
            pygame.draw.rect(cached, selection_color, highlight_rect)
        cached.blit(text_surf, text_rect)
        has_selection = entry.selected_text and entry.selected_text[0] != entry.selected_text[1]
        if entry.focused and entry.state == "enabled" and not has_selection:
            if entry.cursor_visible:
                line_x = text_rect.x + cursor_x_rel
                if visible_left - 2 <= line_x <= visible_right + 2:
                    cursor_surf = entry.font.render(entry.blinking_cursor, True, text_color)
                    cursor_surf.set_alpha(text_color[3])
                    cursor_rect = cursor_surf.get_rect(center=(line_x, text_rect.centery))
                    cached.blit(cursor_surf, cursor_rect)
        entry.local_text_x = text_rect.x
    cached.set_clip(None)
    entry.original_surface = cached


def draw(entry, surface: pygame.Surface):
    if not entry.alive or not entry.visible:
        return
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

    has_selection = entry.selected_text and entry.selected_text[0] != entry.selected_text[1]
    if entry.focused and entry.state == "enabled" and not has_selection:
        if now - entry.last_blink_time > entry.blinking_speed:
            entry.cursor_visible = not entry.cursor_visible
            entry.last_blink_time = now

    entry.font.set_linesize(entry.line_spacing)
    if entry.auto_size:
        text_w, text_h = entry.font.size(display_text)
        actual_height = max(text_h, entry.line_spacing)
        required_width = max(entry.width, text_w + (entry.alignment_spacing * 2) + 10)
        required_height = max(entry.height, actual_height + (entry.alignment_spacing * 2) + 10)
        if entry.max_width:
            required_width = min(required_width, entry.max_width)
        if entry.min_width:
            required_width = max(required_width, entry.min_width)
        if entry.max_height:
            required_height = min(required_height, entry.max_height)
        if entry.min_height:
            required_height = max(required_height, entry.min_height)

        if entry.width != required_width:
            entry.width = required_width
            entry.needs_redraw = True
        if entry.height != required_height:
            entry.height = required_height
            entry.needs_redraw = True

    current_visual_state = (entry.pressed, is_hovering, entry.cursor_visible)
    if entry.needs_redraw or entry.last_visual_state != current_visual_state:
        temp_topleft = entry.rect.topleft
        entry.rect.size = (entry.width, entry.height)
        entry.rect.topleft = temp_topleft
        render_entry_surface(entry, is_hovering)
        entry.last_visual_state = current_visual_state
        entry.needs_redraw = True
        entry.needs_transform = True

    if entry.needs_transform:
        if entry.current_scale != 1 or entry.current_rotation != 0:
            new_width = int(entry.original_surface.get_width() * entry.current_scale)
            new_height = int(entry.original_surface.get_height() * entry.current_scale)
            if new_width > 0 and new_height > 0:
                if entry.use_rotozoom:
                    entry.cached_surface = pygame.transform.rotozoom(entry.original_surface, entry.current_rotation,
                                                                     entry.current_scale)
                else:
                    scaled_surface = pygame.transform.smoothscale(entry.original_surface, (new_width, new_height))
                    entry.cached_surface = pygame.transform.rotate(scaled_surface, entry.current_rotation)
            else:
                entry.cached_surface = pygame.Surface((0, 0), pygame.SRCALPHA)
        else:
            entry.cached_surface = entry.original_surface.copy()
        old_topleft = entry.rect.topleft
        entry.rect = entry.cached_surface.get_rect()
        entry.rect.topleft = old_topleft
        entry.needs_transform = False
    offset_x, offset_y = get_screen_offset(entry)
    total_offset_x = offset_x + round(entry.current_offset[0])
    total_offset_y = offset_y + round(entry.current_offset[1])
    draw_rect = entry.rect.move(total_offset_x, total_offset_y)
    surface.blit(entry.cached_surface, draw_rect)

    entry.last_text_x = entry.local_text_x + draw_rect.x

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
        if entry.tooltip:
            entry.tooltip.show()
    elif is_hovering and getattr(entry, "is_hovered", False):
        entry.is_hovered = True
        entry.trigger_event("<HOVER>")
    elif not is_hovering and getattr(entry, "is_hovered", False):
        entry.is_hovered = False
        entry.trigger_event("<MOUSE-OUT>")
        if entry.tooltip:
            entry.tooltip.hide()


def is_point_in_rounded_rect(entry, point):
    offset_x, offset_y = get_screen_offset(entry)
    total_offset_x = offset_x + round(entry.current_offset[0])
    total_offset_y = offset_y + round(entry.current_offset[1])
    rect = entry.rect.move(total_offset_x, total_offset_y)
    if not rect.collidepoint(point):
        return False
    x, y = point
    geom_rect = rect
    scale = entry.current_scale
    rotation = entry.current_rotation
    if scale != 1 or rotation != 0:
        cx, cy = rect.center
        if rotation != 0:
            v = pygame.math.Vector2(x - cx, y - cy)
            v = v.rotate(rotation)
            x, y = cx + v.x, cy + v.y
        base_w = entry.width * scale
        base_h = entry.height * scale
        geom_rect = pygame.Rect(0, 0, base_w, base_h)
        geom_rect.center = (cx, cy)
        if not geom_rect.collidepoint((x, y)):
            return False
    tl_r = entry.top_left_corner_radius * scale
    tr_r = entry.top_right_corner_radius * scale
    bl_r = entry.bottom_left_corner_radius * scale
    br_r = entry.bottom_right_corner_radius * scale
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


def react(entry, event=None):
    for func in entry.scheduled_functions[:]:
        func[1] -= 1
        if func[1] <= 0:
            func[0]()
            entry.scheduled_functions.remove(func)
    if entry.state != "enabled" or not entry.visible:
        entry.pressed = False
        entry.focused = False
        return
    display_text = entry.get_display_text()
    is_inside = is_point_in_rounded_rect(entry, pygame.mouse.get_pos())

    def get_idx_at_mouse(mouse_x):
        curr_x = entry.last_text_x
        for i, char in enumerate(display_text):
            char_w = entry.font.size(char)[0]
            if mouse_x < curr_x + char_w / 2: return i
            curr_x += char_w
        return min(len(display_text), len(entry.text))

    if event:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if is_inside:
                entry.trigger_event("<PRESS>")
            if not entry.focused:
                entry.trigger_event("<FOCUS-IN>")
            if is_inside:
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
        elif event.type == pygame.KEYDOWN:
            if entry.focused:
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