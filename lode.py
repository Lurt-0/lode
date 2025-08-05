from scene import Scene
import pygame
from collections.abc import Callable
from base_sprite import Sprite
from lode_sprite import Lode_sprite

class Lode(Scene):
    def __init__(self, switch: Callable[[int,pygame.sprite.Group], None], AI = False):
        super().__init__(switch)
        self.selected_tile = None
        self.tiles = pygame.sprite.Group()
        self.tiles_list = [None]*100
        self.boats_list_p1 = [0,1,2,1,1,0,0,0,0,0]
        self.boats_list_p2 = [0,1,2,1,1,0,0,0,0,0]
        self.active_boat_list = self.boats_list_p1
        self.sprites.add(Sprite(pygame.Rect(10, 10, 210, 100), self.menu, self.button_hover, self.button_base, "Zpět"))
        self.sprites.add(Sprite(pygame.Rect(10, 120, 210, 100), self.on_2p_click, self.button_hover, self.button_base, "Dál"))
        for i in range(10):
            for j in range(10):
                self.tiles.add(tile:=Lode_sprite(pygame.Rect(i*100 + 462 ,j*100 + 2,96,96),i,j,self.button_click,self.tile_hover, self.button_base))
                self.tiles_list[i + 10*j] = tile
        self.boat_sprites = pygame.sprite.Group()
        self.sprites.add(self.tiles)
        if AI:
            pass
        else:
            pass

    def button_base(self, x):
        x.color = "blue"
        x.text_size = 60

    def button_hover(self, x):
        x.color = "red"
        x.text_size = 70

    def tile_hover(self, tile):
        for x in self.tiles:
            if x in self.can_place_boat(tile): x.hover = True
            else: x.hover = False
        if not bool(self.can_place_boat(tile)):
            tile.color = "red"


    def button_click(self, tile):
        if tile.selected is False and self.neighbour_selected(tile) is False:
            for x in (list := self.can_place_boat(tile)):
                if  len(list) == 1:
                    self.selected_tile = x
                    x.boat_start = True
                else:
                    self.selected_tile = None
                    x.selected = True
            self.active_boat_list[len(list)-1] -= 1

    def neighbour_selected(self, tile):
        x = tile.x
        y = tile.y
        if 0 <= (right := x + 10*y + 1) < 100:
            if self.tiles_list[right].selected: return True
        if 0 <= (left := x + 10*y -1 ) < 100:
            if self.tiles_list[left].selected: return True
        if 0 <= (top := x + 10*y +10 ) < 100:
            if self.tiles_list[top].selected: return True
        if 0 <= (bottom := x + 10*y -10 ) < 100:
            if self.tiles_list[bottom].selected: return True
        return False

    def menu(self, x):
        self.switch_scenes(0)

    def on_2p_click(self, x):
        print(self.neighbour_selected(self.selected_tile))

    def can_place_boat(self,tile):
        return_tiles = pygame.sprite.Group()
        if self.selected_tile is None:
            if tile.selected is False and self.neighbour_selected(tile) is False:
                return_tiles.add(tile)
            return return_tiles
        x1, x2 = tile.x, self.selected_tile.x
        y1, y2 = tile.y, self.selected_tile.y
        if x1 > x2: x1, x2 = x2, x1
        if y1 > y2: y1, y2 = y2, y1
        for n in self.tiles:
            if x2 > x1:
                if n.x in range(x1, x2 + 1) and n.y == y1 == y2 and self.active_boat_list[x2-x1] > 0:
                    return_tiles.add(n)
                    if n.selected is True or self.neighbour_selected(n):
                        return pygame.sprite.Group()
            else:
                if n.y in range(y1, y2 + 1) and n.x == x1 == x1 and self.active_boat_list[y2-y1] > 0:
                    return_tiles.add(n)
                    if n.selected is True or self.neighbour_selected(n):
                        return pygame.sprite.Group()
        return return_tiles
