import pygame
from  base_sprite import Sprite


class Tile(Sprite): # class for tiles of the game
    def __init__(self, rect:pygame.Rect, x, y ,on_click = lambda x = None: None,on_hover = lambda x = None: None,not_hover = lambda x = None: None, text:str = "", text_size = 130):
        super().__init__(rect, text,text_size, on_click, on_hover, not_hover)
        self.color_selected =  pygame.Color("green")
        self.color_hover = pygame.Color(127, 255, 127)
        self.selected = False #determines, if tile shows it's properties
        self.boat_for_player = [pygame.sprite.Group(), pygame.sprite.Group()] #if tile is part of a boat stores all the tiles in this boat
        self.boat_start = False # True if it's the first tile selected while placing a boat
        self.is_boat_tile = [False,False] #stores if a player has placed a boat on this tile
        self.player_shot = [False,False] #stores if a player has shot this tile
        self.x = x #cords of tile
        self.y = y

    def update(self): #overrides Sprite method, updates image
        if self.selected or self.boat_start:
            self.image = self.create_img(self.color_selected, self.text)
        elif self.hover:
            self.image = self.create_img(self.color_hover, self.text)
        else:
            self.image = self.create_img(self.color, self.text)