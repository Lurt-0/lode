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
        self.player = 1
        self.other_player = 2
        self.tiles = pygame.sprite.Group()
        self.tiles_list = [None]*100
        self.boats_list_p1 = [0,0,1,2,1,1,0,0,0,0,0]
        self.boats_list_p2 = [0,0,1,2,1,1,0,0,0,0,0]
        self.sunk = [0,0]
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
            if x in self.can_place_boat(tile,self.selected_tile): x.hover = True
            else: x.hover = False
        if not bool(self.can_place_boat(tile,self.selected_tile)):
            tile.color = "red"

    def game_tile_hover(self, tile):
        for x in self.tiles:
            if x is tile:
                x.hover = True
            else:
                x.hover = False

    def selection_tile_click(self, tile):
        if not tile.selected and not self.neighbours_selected(tile):
            for x in (list := self.can_place_boat(tile, self.selected_tile)):
                if  len(list) == 1:
                    self.selected_tile = x
                    x.boat_start = True
                else:
                    self.selected_tile = None
                    x.selected = True
                    x.boat_for_player[self.player - 1] = list
            if len(list) > 1:
                self.active_boat_list[len(list)] -= 1
                if sum(self.active_boat_list) == 0:
                    self.next()

    def game_tile_click(self, tile):
        if not tile.player_shot[self.player - 1]:
            tile.player_shot[self.player - 1] = True
            tile.selected = True
            if tile.is_boat_tile[self.other_player - 1]:
                tile.color_selected = pygame.Color(127, 255, 127)
                sunk = True
                for x in tile.boat_for_player[self.other_player - 1]:
                    if x.selected is False:
                        sunk = False
                if sunk:
                    self.button_next_display("boat sunk")
                    for x in tile.boat_for_player[self.other_player - 1]:
                        for y in self.neighbours(x):
                            y.selected = True
                            y.player_shot[self.player - 1] = True
                            if not y.is_boat_tile[self.other_player - 1]:
                                y.color_selected = pygame.Color(255, 127, 127)
                    self.sunk[self.player - 1] += 1
                    if self.sunk[self.player - 1] == 5:
                        self.switch_scenes(0)

            else:
                tile.color_selected = pygame.Color(255, 127, 127)
                self.button_next_display(f"player {self.other_player} is now playing")
                for x in self.tiles:
                    if x.player_shot[self.other_player - 1]:
                        x.selected = True
                        if x.is_boat_tile[self.player - 1]:
                            x.color_selected = pygame.Color(127, 255, 127)
                        else:
                            x.color_selected = pygame.Color(255, 127, 127)
                    else:
                        x.selected = False
                self.player, self.other_player = self.other_player, self.player

    def debug(self, tile):
        self.ai_selection()

    def ai_selection(self):
        while sum(self.active_boat_list) > 0:
            rnd = random.randint(0, 399)
            if self.active_boat_list[(rnd % 4) + 2] > 0:
                length = rnd % 4 + 2
                rnd = (rnd - length + 2) // 4
                x = rnd % 10
                rnd = (rnd - x) // 10
                y = rnd % 10
                direction = random.choice([-10,-1,1,10])
                if 0 <= (x + 10*y + (length-1)*direction) < 100:
                    for x in (list := self.can_place_boat(self.tiles_list[x + 10*y], self.tiles_list[x + 10*y + (length-1)*direction])):
                        x.selected = True
                        x.boat_for_player[self.player - 1] = list
                    if len(list) > 1:
                        self.active_boat_list[length] -= 1
        self.next()

    def next(self):
        for x in self.tiles:
            if x.selected:
                x.is_boat_tile[self.player - 1] = True
                x.boat_start = False
                x.selected = False
        if self.player == 1:
            self.button_next_display(f"player {self.other_player} is now placing")
            self.player = 2
            self.other_player = 1
            self.active_boat_list = self.boats_list_p2
        else:
            self.player = 1
            self.other_player = 2
            self.active_boat_list = self.boats_list_p1
            self.start_game()

    def start_game(self):
        for x in self.tiles:
            x.on_click = self.game_tile_click
            x.on_hover = self.game_tile_hover

    def button_next_display(self, text):
        self.button_next.text = text
        self.sprites.remove(self.tiles)
        self.sprites.add(self.button_next)

    def button_next_click(self, tile):
        self.sprites.add(self.tiles)
        self.sprites.remove(self.button_next)

    def neighbours(self, tile):
        return_tiles = pygame.sprite.Group()
        x = tile.x
        y = tile.y
        if x < 9:
            return_tiles.add(self.tiles_list[x + 10*y + 1])
        if 0 < x:
            return_tiles.add(self.tiles_list[x + 10*y - 1])
        if y < 9:
            return_tiles.add(self.tiles_list[x + 10*y + 10])
        if 0 < y:
            return_tiles.add(self.tiles_list[x + 10*y - 10])
        return return_tiles

    def neighbours_selected(self, tile):
        return_bool = False
        for x in self.neighbours(tile):
            if x.selected:
                return_bool = True
        return return_bool

    def can_place_boat(self,tile, tile2):
        return_tiles = pygame.sprite.Group()
        if tile2 is None:
            if not tile.selected and not self.neighbours_selected(tile):
                return_tiles.add(tile)
            return return_tiles
        x1, x2 = tile.x, tile2.x
        y1, y2 = tile.y, tile2.y
        if x1 > x2: x1, x2 = x2, x1
        if y1 > y2: y1, y2 = y2, y1
        if x2 > x1 and y1 == y2:
            for x in range(x1, x2 + 1):
                return_tiles.add(self.tiles_list[x + 10*y1])
                if self.tiles_list[x + 10*y1].selected or self.neighbours_selected(self.tiles_list[x + 10 * y1]) or self.active_boat_list[x2 - x1 + 1] <= 0:
                    return pygame.sprite.Group()
        elif y2 > y1 and x1 == x2:
            for y in range(y1, y2 + 1):
                return_tiles.add(self.tiles_list[x1 + 10*y])
                if self.tiles_list[x1 + 10*y].selected or self.neighbours_selected(self.tiles_list[x1 + 10 * y]) or self.active_boat_list[y2 - y1 + 1] <= 0:
                    return pygame.sprite.Group()
        return return_tiles