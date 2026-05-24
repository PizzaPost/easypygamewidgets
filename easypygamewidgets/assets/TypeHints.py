from typing import TypedDict, Callable

import pygame
from typing_extensions import Any


class BindingConfig(TypedDict):
    command: Callable[[], None]
    require_hover: bool


class ButtonConfig(TypedDict, total=False):
    bindings: dict[str, BindingConfig]
    width: int
    height: int
    screen: "easypygamewidgets.Screen"
    state: str
    visible: bool
    auto_size: bool
    text: str
    active_unpressed_text_color: tuple[int, int, int] | tuple[int, int, int, int] | None
    disabled_unpressed_text_color: tuple[int, int, int] | tuple[int, int, int, int] | None
    active_hover_text_color: tuple[int, int, int] | tuple[int, int, int, int] | None
    disabled_hover_text_color: tuple[int, int, int] | tuple[int, int, int, int] | None
    active_pressed_text_color: tuple[int, int, int] | tuple[int, int, int, int] | None
    active_unpressed_background_color: tuple[int, int, int] | tuple[int, int, int, int] | None
    disabled_unpressed_background_color: tuple[int, int, int] | tuple[int, int, int, int] | None
    active_hover_background_color: tuple[int, int, int] | tuple[int, int, int, int] | None
    disabled_hover_background_color: tuple[int, int, int] | tuple[int, int, int, int] | None
    active_pressed_background_color: tuple[int, int, int] | tuple[int, int, int, int] | None
    active_unpressed_border_color: tuple[int, int, int] | tuple[int, int, int, int] | None
    disabled_unpressed_border_color: tuple[int, int, int] | tuple[int, int, int, int] | None
    active_hover_border_color: tuple[int, int, int] | tuple[int, int, int, int] | None
    disabled_hover_border_color: tuple[int, int, int] | tuple[int, int, int, int] | None
    active_pressed_border_color: tuple[int, int, int] | tuple[int, int, int, int] | None
    border_tickness: int
    active_hover_cursor: pygame.Cursor
    disabled_hover_cursor: pygame.Cursor
    active_pressed_cursor: pygame.Cursor
    cursors: dict[str, pygame.Cursor]
    font: pygame.font.Font
    alignment: str
    command: Callable[[], None]
    alignment_spacing: int
    corner_radius: int
    layer: int
    tooltip: "easypygamewidgets.Tooltip"
    line_spacing: int
    min_width: int
    max_width: int
    min_height: int
    max_height: int
    data: Any
    x: int
    y: int
    alive: bool
    pressed: bool
    rect: pygame.Rect
    original_cursor: pygame.Cursor
    scheduled_functions: dict[Callable, int]
    is_hovered: bool
    last_visual_state: tuple[bool, bool]
    needs_redraw: bool
    cached_surface: pygame.Surface
    needs_transform: bool
    original_surface: pygame.Surface
    target_scale: float | int
    current_scale: float | int
    scale_step: float | int
    target_rotation: float | int
    current_rotation: float | int
    rotation_step: float | int
    target_offset: tuple[int, int]
    current_offset: tuple[int, int]
    offset_step: tuple[int, int]
    use_rotozoom: bool


class EntryConfig(TypedDict, total=False):
    screen: "easypygamewidgets.Screen"
    state: str
    visible: bool
    auto_size: bool
    width: int
    height: int
    placeholder_text: str
    text: str
    char_limit: int | None
    show: str
    active_unpressed_text_color: tuple[int, int, int] | tuple[int, int, int, int] | None
    disabled_unpressed_text_color: tuple[int, int, int] | tuple[int, int, int, int] | None
    active_hover_text_color: tuple[int, int, int] | tuple[int, int, int, int] | None
    disabled_hover_text_color: tuple[int, int, int] | tuple[int, int, int, int] | None
    active_pressed_text_color: tuple[int, int, int] | tuple[int, int, int, int] | None
    active_unpressed_background_color: tuple[int, int, int] | tuple[int, int, int, int] | None
    disabled_unpressed_background_color: tuple[int, int, int] | tuple[int, int, int, int] | None
    active_hover_background_color: tuple[int, int, int] | tuple[int, int, int, int] | None
    disabled_hover_background_color: tuple[int, int, int] | tuple[int, int, int, int] | None
    active_pressed_background_color: tuple[int, int, int] | tuple[int, int, int, int] | None
    active_unpressed_border_color: tuple[int, int, int] | tuple[int, int, int, int] | None
    disabled_unpressed_border_color: tuple[int, int, int] | tuple[int, int, int, int] | None
    active_hover_border_color: tuple[int, int, int] | tuple[int, int, int, int] | None
    disabled_hover_border_color: tuple[int, int, int] | tuple[int, int, int, int] | None
    active_pressed_border_color: tuple[int, int, int] | tuple[int, int, int, int] | None
    selection_color: tuple[int, int, int] | tuple[int, int, int, int] | None
    disabled_selection_color: tuple[int, int, int] | tuple[int, int, int, int] | None
    border_tickness: int
    active_hover_cursor: pygame.Cursor
    disabled_hover_cursor: pygame.Cursor
    active_pressed_cursor: pygame.Cursor
    cursors: dict[str, pygame.Cursor]
    blinking_cursor: str
    blinking_speed: int
    font: pygame.font.Font
    alignment: str
    alignment_spacing: int
    corner_radius: int
    repeat_delay: int
    repeat_interval: int
    layer: int
    line_spacing: int
    tooltip: "easypygamewidgets.Tooltip"
    min_width: int
    max_width: int
    min_height: int
    max_height: int
    data: Any
    x: int
    y: int
    alive: bool
    pressed: bool
    rect: pygame.Rect
    original_cursor: pygame.Cursor
    selected_text: str
    focused: bool
    cursor_position: int
    scroll_offset: int
    drag_start: int
    selection_anchor: int
    last_text_x: int
    held_key_info: tuple[int, str]
    next_repeat_time: int
    cursor_visible: bool
    last_blink_time: int
    bindings: dict[str, BindingConfig]
    scheduled_functions: dict[Callable, int]
    is_hovered: bool
    last_visual_state: tuple[bool, bool]
    needs_redraw: bool
    cached_surface: pygame.Surface
    local_text_x: int
    needs_transform: bool
    original_surface: pygame.Surface
    target_scale: float | int
    current_scale: float | int
    scale_step: float | int
    target_rotation: float | int
    current_rotation: float | int
    rotation_step: float | int
    target_offset: tuple[int, int]
    current_offset: tuple[int, int]
    offset_step: tuple[int, int]
    use_rotozoom: bool