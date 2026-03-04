# EasyPygameWidgets

An easy-to-use UI widget library for pygame, featuring customizable buttons, sliders, text entries, screen management
and much more.

## Features

- **easy integration**: seamlessly works with existing pygame projects
- **customizable widgets**: nearly infinite styling options for colors, sounds, cursors, and more
- **screen management**: built-in screen system for creating different GUIs

## Installation

### Windows
```bash
pip install easypygamewidgets
```

### Linux/macOS
```bash
python3 -m pip install easypygamewidgets
```

## Quick Start

```python
import pygame
import easypygamewidgets as epw

pygame.init()
window = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# link the pygame window
epw.link_pygame_window(window)

# create a screen (optional)
screen = epw.Screen(id="main")

# create a button
button = epw.Button(screen=screen, text="Click Me!", width=200, height=50)
button.place(300, 250)

# create a slider
slider = epw.Slider(screen=screen, text="Volume", start=0, end=100, width=300)
slider.place(250, 350)

# create a text entry
entry = epw.Entry(screen=screen, text="Type here...", width=250)
entry.place(275, 450)

# main game loop
running = True
while running:
    window.fill((30, 30, 30))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # handle widget events
        epw.handle_event(event)

    # handle special widget events
    epw.handle_special_events()

    # draw all widgets
    epw.flip()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
```

## Widgets Documentation

All examples will use the
same [start template code](https://github.com/PizzaPost/pywidgets/blob/master/examples/start_template.py).

### Screen

A container for managing groups of widgets with shared visibility and state.

[example code](https://github.com/PizzaPost/pywidgets/blob/master/examples/screen.py)

### Button

A customizable button widget to run commands when interacted.

[example code](https://github.com/PizzaPost/pywidgets/blob/master/examples/button.py)

### Slider

A slider for selecting values within a specific range.

[example code](https://github.com/PizzaPost/pywidgets/blob/master/examples/slider.py)

### Entry

A text entry with selection and clipboard support.

[example code](https://github.com/PizzaPost/pywidgets/blob/master/examples/entry.py)

### Label

A text display that can be used to drag it into places or show text.

[example code](https://github.com/PizzaPost/pywidgets/blob/master/examples/label.py)

### Surface (images etc.)

This converts your pygame surfaces into an easypygamewidgets widget that can be used in screens.
(All pygame surface commands can be applied to the "surface" attribute of your widget.)

[example code](https://github.com/PizzaPost/pywidgets/blob/master/examples/surface.py)

### Timekeeper

A text display that can show a timer or stopwatch.

[example code](https://github.com/PizzaPost/pywidgets/blob/master/examples/timekeeper.py)

## Module Functions

### Core Functions

```python
# link your pygame window (required before using widgets)
epw.link_pygame_window(pygame_window)

# handle pygame events (call in event loop)
epw.handle_event(pygame_event)

# handle special events (call outside event loop)
epw.handle_special_events()

# draw all widgets to the linked window
epw.flip()
```

## Examples (COMING SOON)

Check the [examples directory](https://github.com/PizzaPost/pywidgets/tree/master/examples) for complete working
examples:

1. **[all widgets example](https://github.com/PizzaPost/pywidgets/blob/master/examples/basic.py)** - simple demo of all
   widgets
2. **[screens with animations](https://github.com/PizzaPost/pywidgets/blob/master/examples/animated_screens.py)** -
   multiple screens with transitions
3. **[settings screen](https://github.com/PizzaPost/pywidgets/blob/master/examples/settings.py)** - interactive settings
   panel with sliders
4. **[login form](https://github.com/PizzaPost/pywidgets/blob/master/examples/login_form.py)** - form with entries and
   validation
5. **[bindings](https://github.com/PizzaPost/pywidgets/blob/master/examples/slider.py)** - binding events to widgets

## Requirements

- python
- pygame
- requests (for update checking in background once)

I recommend using the latest version of libraries.

## Contributing

Contributions are welcome! Please feel free to submit a pull request. Of course will be mentioned :)

## License

This project is licensed under the MIT License - see
the [LICENSE file](https://github.com/PizzaPost/pywidgets/blob/master/LICENSE) for details.

## Support

- Issues: [GitHub Issues](https://github.com/PizzaPost/pywidgets/issues)
- Discord: [My Account](https://www.discord.com/users/916636380967354419)
- Instagram: [My Account](https://www.instagram.com/8002_phil/)

- License: [MIT](https://github.com/PizzaPost/pywidgets/blob/master/LICENSE)
- History: [GitHub History](https://github.com/PizzaPost/pywidgets/commits/master/)

---

Made with ❤️ by PizzaPost