from scene import Scene
import pygame
from collections.abc import Callable
from base_sprite import Sprite

class Menu(Scene):
    def __init__(self, switch: Callable[[int], None]):
        super().__init__(switch)
        self.sprites.add(Sprite(pygame.Rect(460,100,1000,200),self.pvp_click,self.button_hover,self.button_base,"Hrát"))
        self.sprites.add(Sprite(pygame.Rect(460,400,1000,200),self.quit,self.button_hover,self.button_base,"Konec"))

    def pvp_click(self, x):
        self.switch_scenes(1)

    def pvAI_click(self, x):
        self.switch_scenes(2)