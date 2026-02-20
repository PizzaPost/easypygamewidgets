import pygame

import easypygamewidgets as epw

pygame.init()
window = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
epw.link_pygame_window(window)

screen = epw.Screen(id="surface_example", visible=True)

img_surface = epw.Surface(surface=pygame.image.load("surface_example.png"), screen=screen,
                          active_hover_cursor=pygame.cursors.tri_left)
img_surface.bind("<RELEASE>", lambda: exit(0))
img_surface.place(0, 0)
screen.update_widget_state()

screen.x = 100
screen.y = 100

running = True
while running:
    window.fill((30, 30, 30))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        epw.handle_event(event)
    epw.handle_special_events()
    epw.flip()
    pygame.display.update()
    clock.tick(60)
pygame.quit()
