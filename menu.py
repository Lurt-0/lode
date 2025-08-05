from scene import Scene
import pygame
from collections.abc import Callable
from base_sprite import Sprite


class Menu(Scene):
    def __init__(self, switch: Callable[[int], None]):
        super().__init__(switch)
        self.sprites.add(Sprite(pygame.Rect(460,100,1000,200),self.on_1p_click,self.button_hover,self.button_base,"Hrát"))
        self.sprites.add(Sprite(pygame.Rect(460,400,1000,200),self.quit,self.button_hover,self.button_base,"Konec"))


    def button_base(self, x):
        x.color = "blue"
        x.text_size = 60

    def button_hover(self, x):
        x.color = "red"
        x.text_size = 70

    def button_click(self, x):
        x.selected = True

    def on_1p_click(self, x):
        self.switch_scenes(1)

    def on_2p_click(self, x):
        self.switch_scenes(3)
