from  base_sprite import Sprite
import pygame

class Lode_sprite(Sprite):
    def __init__(self, rect:pygame.Rect, x, y ,on_click = lambda x: None,on_hover = lambda x: None,not_hover = lambda x: None, text:str = ""):
        super().__init__(rect, on_click, on_hover, not_hover, text)
        self.color_selected = pygame.Color(127, 255, 127)
        self.color_hover = pygame.Color("green")
        self.selected = False
        self.boat_start = False
        self.hover = False
        self.boat_p1 = False
        self.boat_p2 = False
        self.p1_shot = False
        self.p2_shot = False
        self.x = x
        self.y = y

    def update(self):
        if self.selected or self.boat_start:
            self.image = self.create_img(self.rect, self.color_selected, self.text)
        elif self.hover:
            self.image = self.create_img(self.rect, self.color_hover, self.text)
        else:
            self.image = self.create_img(self.rect, self.color, self.text)