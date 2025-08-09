from  base_sprite import Sprite
import pygame

class Lode_sprite(Sprite):
    def __init__(self, rect:pygame.Rect, x, y ,on_click = lambda x = None: None,on_hover = lambda x = None: None,not_hover = lambda x = None: None, text:str = ""):
        super().__init__(rect, text, on_click, on_hover, not_hover)
        self.color_selected =  pygame.Color("green")
        self.color_hover = pygame.Color(127, 255, 127)
        self.selected = False
        self.boat_for_player = [pygame.sprite.Group(), pygame.sprite.Group()]
        self.boat_start = False
        self.is_boat_tile = [False,False]
        self.player_shot = [False,False]
        self.x = x
        self.y = y

    def update(self):
        if self.selected or self.boat_start:
            self.image = self.create_img(self.rect, self.color_selected, self.text)
        elif self.hover:
            self.image = self.create_img(self.rect, self.color_hover, self.text)
        else:
            self.image = self.create_img(self.rect, self.color, self.text)