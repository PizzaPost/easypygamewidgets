import pygame

pygame.init()

all_screens = []


class Screen:
    def __init__(self, id: str,
                 widgets: "list[easypygamewidgets.Button | easypygamewidgets.Entry | easypygamewidgets.Slider | easypygamewidgets.Label] | easypygamewidgets.Surface | None" = None,
                 darken_background_with_alpha: int = 0, x: int = 0, y: int = 0):
        if not id in all_screens:
            self.id = id
            self.widgets = widgets if widgets is not None else []
            self.darken_background_with_alpha = max(min(darken_background_with_alpha, 255), 0)
            self.visible = False
            self.enabled = True
            self.x = x
            self.y = y

            all_screens.append(self)
        else:
            print(f"{id} is already defined")

    def add_widget(self, widget):
        if widget in self.widgets:
            widget.screen.remove_widget(widget)
        self.widgets.append(widget)
        widget.screen = self

    def remove_widget(self, widget):
        if widget in self.widgets:
            self.widgets.remove(widget)

    def show(self):
        self.visible = True
        self.update_widget_state()
        return self

    def hide(self):
        self.visible = False
        self.update_widget_state()
        return self

    def enable(self):
        self.enabled = True
        self.update_widget_state()
        return self

    def disable(self):
        self.enabled = False
        self.update_widget_state()
        return self

    def update_widget_state(self):
        for widget in self.widgets:
            if self.enabled:
                widget.state = "enabled"
            else:
                widget.state = "disabled"
            if self.visible:
                widget.visible = True
            else:
                widget.visible = False

    def place(self, x, y):
        self.x = x
        self.y = y
        return self


def draw(screen, surface: pygame.Surface):
    if screen.darken_background_with_alpha:
        background_surf = pygame.Surface(surface.get_size())
        background_surf.fill((0, 0, 0))
        background_surf.set_alpha(screen.darken_background_with_alpha)
        surface.blit(background_surf, (0, 0))
