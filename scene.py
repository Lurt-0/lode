import pygame
from collections.abc import Callable

class Scene: #parrent class for all the scenes
    def __init__(self, switch:Callable[[int],None],scale):
        self.scale = scale
        self.switch_scenes = switch
        self.sprites = pygame.sprite.Group()
        self.screen_color = pygame.Color("black")
        self.waiting_for_space = False

    def on_mouse_down(self, pos):
        for x in self.sprites:
            if x.rect.collidepoint(pos):
                x.on_click(x)

    def button_base(self, x):
        x.color = "blue"
        x.text_size = x.base_text_size

    def button_hover(self, x):
        x.color = "red"
        x.text_size =  x.base_text_size + 10* self.scale

    def draw(self, screen):
        screen.fill(self.screen_color)
        self.sprites.update()
        self.sprites.draw(screen)

    def update(self, mouse_pos):
        for x in self.sprites:
            if x.rect.collidepoint(mouse_pos):
                x.on_hover(x)
            else:
                x.base(x)

    def space_pressed(self):
        pass

    def quit(self, x):
        raise SystemExit