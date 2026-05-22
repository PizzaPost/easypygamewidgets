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
    active_unpressed_text_color: tuple[int, int, int] | tuple[int, int, int, int]
    disabled_unpressed_text_color: tuple[int, int, int] | tuple[int, int, int, int]
    active_hover_text_color: tuple[int, int, int] | tuple[int, int, int, int]
    disabled_hover_text_color: tuple[int, int, int] | tuple[int, int, int, int]
    active_pressed_text_color: tuple[int, int, int] | tuple[int, int, int, int]
    active_unpressed_background_color: tuple[int, int, int] | tuple[int, int, int, int]
    disabled_unpressed_background_color: tuple[int, int, int] | tuple[int, int, int, int]
    active_hover_background_color: tuple[int, int, int] | tuple[int, int, int, int]
    disabled_hover_background_color: tuple[int, int, int] | tuple[int, int, int, int]
    active_pressed_background_color: tuple[int, int, int] | tuple[int, int, int, int]
    active_unpressed_border_color: tuple[int, int, int] | tuple[int, int, int, int]
    disabled_unpressed_border_color: tuple[int, int, int] | tuple[int, int, int, int]
    active_hover_border_color: tuple[int, int, int] | tuple[int, int, int, int]
    disabled_hover_border_color: tuple[int, int, int] | tuple[int, int, int, int]
    active_pressed_border_color: tuple[int, int, int] | tuple[int, int, int, int]
    border_tickness: int
    active_hover_cursor: pygame.Cursor
    disabled_hover_cursor: pygame.Cursor
    active_pressed_cursor: pygame.Cursor
    cursor: dict[str, pygame.Cursor]
    font: pygame.font.Font
    alignment: str
    command: Callable
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
    target_scale: float
    current_scale: float
    scale_step: float
    target_rotation: float
    current_rotation: float
    rotation_step: float
    target_offset: tuple[int, int]
    current_offset: tuple[int, int]
    offset_step: tuple[int, int]
    use_rotozoom: bool