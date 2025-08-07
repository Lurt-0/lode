import pygame
from collections.abc import Callable

class Scene:
    def __init__(self, switch:Callable[[int],None]):
        self.switch_scenes = switch
        self.sprites = pygame.sprite.Group()

    def on_mouse_down(self, pos):
        for x in self.sprites:
            if x.rect.collidepoint(pos):
                x.on_click(x)

    def button_base(self, x):
        x.color = "blue"
        x.text_size = 120

    def button_hover(self, x):
        x.color = "red"
        x.text_size = 130

    def draw(self, screen):
        screen.fill("black")
        self.sprites.update()
        self.sprites.draw(screen)

    def update(self, mouse_pos):
        for x in self.sprites:
            if x.rect.collidepoint(mouse_pos):
                x.on_hover(x)
            else:
                x.not_hover(x)

    def quit(self, x):
        raise SystemExit

    def menu(self, tile):
        self.switch_scenes(0)