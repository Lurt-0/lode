from scene import Scene
import pygame
from collections.abc import Callable
from base_sprite import Sprite

class Menu(Scene):
    def __init__(self, switch: Callable[[int], None]):
        super().__init__(switch)
        self.sprites.add(Sprite(pygame.Rect(460,100,1000,200),"1 Player",self.pvAI_button_click,self.button_hover,self.button_base))
        self.sprites.add(Sprite(pygame.Rect(460, 350, 1000, 200),"2 Players", self.pvp_button_click, self.button_hover, self.button_base))
        self.sprites.add(Sprite(pygame.Rect(460,600,1000,200),"Quit",self.quit,self.button_hover,self.button_base))

    def pvp_button_click(self, x):
        self.switch_scenes(1)

    def pvAI_button_click(self, x):
        self.switch_scenes(2)