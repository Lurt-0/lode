import random
from scene import Scene
import pygame
from collections.abc import Callable
from base_sprite import Sprite
from lode_sprite import Lode_sprite

class Lode(Scene):
    def __init__(self, switch: Callable[[int,pygame.sprite.Group], None], ai = False):
        super().__init__(switch)
        self.selected_tile = None
        self.ai = ai
        self.tiles = pygame.sprite.Group()
        self.tiles_list = [None]*100
        self.boats_list_p1 = [0,1,2,1,1,0,0,0,0,0]
        self.boats_list_p2 = [0,1,2,1,1,0,0,0,0,0]
        self.active_boat_list = self.boats_list_p1
        self.button_next = Sprite(pygame.Rect(460, 100, 1000, 200), self.button_next_click, self.button_hover,self.button_base, "Další")
        self.load_sprites()

    def load_sprites(self):
        self.sprites.add(Sprite(pygame.Rect(10, 10, 210, 100), self.menu, self.button_hover, self.button_base, "Menu"))
        self.sprites.add(Sprite(pygame.Rect(10, 120, 210, 100), self.debug, self.button_hover, self.button_base, "Dál"))
        for i in range(10):
            for j in range(10):
                self.tiles.add(tile := Lode_sprite(pygame.Rect(i * 100 + 462, j * 100 + 2, 96, 96), i, j, self.selection_tile_click, self.selection_tile_hover, self.button_base))
                self.tiles_list[i + 10 * j] = tile
        self.sprites.add(self.tiles)

    def selection_tile_hover(self, tile):
        for x in self.tiles:
            if x in self.can_place_boat(tile): x.hover = True
            else: x.hover = False
        if not bool(self.can_place_boat(tile)):
            tile.color = "red"

    def selection_tile_click(self, tile):
        if tile.selected is False and self.neighbour_selected(tile) is False:
            for x in (list := self.can_place_boat(tile)):
                if  len(list) == 1:
                    self.selected_tile = x
                    x.boat_start = True
                else:
                    self.selected_tile = None
                    x.selected = True
            if len(list) != 1:
                self.active_boat_list[len(list)-1] -= 1
                if sum(self.active_boat_list) == 0:
                    self.next()

    def menu(self, x):
        self.switch_scenes(0)

    def debug(self, x):
        print(self.neighbour_selected(self.selected_tile))

    def ai_selection(self):
        while sum(self.active_boat_list) != 0:
            rnd = random.randint(0, 1)
            print(rnd)

    def next(self):
        if self.active_boat_list is self.boats_list_p1:
            self.sprites.remove(self.tiles)
            self.active_boat_list = self.boats_list_p2
            if self.ai:
                pass
            else:
                self.sprites.add(self.button_next)
                for x in self.tiles:
                    if x.selected == True:
                        x.boat_p1 = True
                        x.boat_start = False
                        x.selected = False
        else:
            for x in self.tiles:
                if x.selected == True:
                    x.boat_p2 = True
                    x.boat_start = False
                    x.selected = False

    def button_next_click(self, x):
        self.sprites.add(self.tiles)
        self.sprites.remove(self.button_next)

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
        if x2 > x1 and y1 == y2:
            for x in range(x1, x2 + 1):
                return_tiles.add(self.tiles_list[x + 10*y1])
                if self.tiles_list[x + 10*y1].selected is True or self.neighbour_selected(self.tiles_list[x + 10*y1]) or self.active_boat_list[x2-x1] <= 0:
                    return pygame.sprite.Group()
        elif y2 > y1 and x1 == x2:
            for y in range(y1, y2 + 1):
                return_tiles.add(self.tiles_list[x1 + 10*y])
                if self.tiles_list[x1 + 10*y].selected is True or self.neighbour_selected(self.tiles_list[x1 + 10*y]) or self.active_boat_list[y2-y1] <= 0:
                    return pygame.sprite.Group()
        return return_tiles