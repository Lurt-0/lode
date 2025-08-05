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