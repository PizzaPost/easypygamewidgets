import pygame

import easypygamewidgets as epw

pygame.init()
window = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
epw.link_pygame_window(window)
epw.set_appearance_mode(2)

label1 = epw.Label(text="Hello World", min_width=450, active_unpressed_background_color=(255, 255, 255, 255)).place(0,
                                                                                                                    10)
label2 = epw.Label(text="You can\ndrag me!", dragable=True).place(0, 75)


def draw():
    window.fill((30, 30, 30))


epw.create_pygame_layer(draw, 500)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        epw.handle_event(event)
    epw.handle_special_events()
    epw.flip()
    clock.tick(60)
pygame.quit()