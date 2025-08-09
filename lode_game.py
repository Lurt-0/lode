import random
from scene import Scene
import pygame
from collections.abc import Callable
from base_sprite import Sprite
from lode_sprite import Lode_sprite

class Lode(Scene):
    def __init__(self, switch: Callable[[int], None], ai = False):
        super().__init__(switch)
        self.selected_tile = None
        self.ai = ai
        self.player = 1
        self.other_player = 2
        self.tiles = pygame.sprite.Group()
        self.tiles_list = []
        self.boats_list_p1 = [0,0,1,2,1,1,0,0,0,0,0]
        self.boats_list_p2 = [0,0,1,2,1,1,0,0,0,0,0]
        self.sunk = [0,0]
        self.ai_boat_list = []
        self.game_running = False
        self.my_boats_shown = False
        self.showing_info = False
        self.active_boat_list = self.boats_list_p1
        self.button_next = Sprite(pygame.Rect(460, 100, 1000, 200), "Další", self.button_next_click, self.button_hover,self.button_base)
        self.useful_button = Sprite(pygame.Rect(3, 210, 390, 180), "Generate", self.ai_selection, self.button_hover, self.button_base)
        self.load_sprites()

    def load_sprites(self):
        self.sprites.add(Sprite(pygame.Rect(460,840,1000,200),"info text"))
        self.sprites.add(Sprite(pygame.Rect(1637, 898, 280, 140), "Quit", self.quit, self.button_hover, self.button_base))
        self.sprites.add(self.useful_button)
        for y in range(10):
            for x in range(10):
                self.tiles.add(tile := Lode_sprite(pygame.Rect(x * 94 + 492, y * 94 + 142, 90, 90), x, y, self.selection_tile_click, self.selection_tile_hover, self.button_base))
                self.tiles_list.append(tile)
        self.sprites.add(self.tiles)

    def selection_tile_hover(self, tile):
        for x in self.tiles:
            if x in self.can_place_boat(tile,self.selected_tile) and self.selected_tile is not None: x.hover = True
            else: x.hover = False
        if not bool(self.can_place_boat(tile,self.selected_tile)):
            tile.color = pygame.Color(255, 127, 127)
        else:
            tile.color = pygame.Color(127, 255, 127)

    def game_tile_hover(self, tile):
        tile.color =  pygame.Color(127, 255, 127)

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
                    if self.ai:
                        self.ai_selection(None)
                    else:
                        self.next()

    def game_tile_click(self, tile):
        if not tile.player_shot[self.player - 1]:
            tile.player_shot[self.player - 1] = True
            tile.selected = True
            if tile.is_boat_tile[self.other_player - 1]:
                tile.color_selected = pygame.Color(63,127,63)
                sunk = True
                for x in tile.boat_for_player[self.other_player - 1]:
                    if x.selected is False:
                        sunk = False
                if sunk:
                    for x in tile.boat_for_player[self.other_player - 1]:
                        for y in self.neighbours(x):
                            y.selected = True
                            y.player_shot[self.player - 1] = True
                            if not y.is_boat_tile[self.other_player - 1]:
                                y.color_selected = pygame.Color(63, 63, 127)
                    self.sunk[self.player - 1] += 1
                    if self.sunk[self.player - 1] == 5:
                        self.switch_scenes(0)
            else:
                if self.ai and self.player == 1:
                    self.ai_move()
                else:
                    self.button_next_display(f"player {self.other_player} is now shoting")
                    self.change_shown_boats()

    def ai_move(self):
        self.change_shown_boats()
        while self.player == 2:
            if len(self.ai_boat_list) > 0:
                tile = self.ai_boat_list.pop(random.randint(0,len(self.ai_boat_list)-1))
                if not tile.player_shot[self.player - 1]:
                    tile.player_shot[self.player - 1] = True
                    tile.selected = True
                    if tile.is_boat_tile[self.other_player - 1]:
                        self.ai_boat_list.clear()
                        axis_x = False
                        for x in self.neighbours(tile):
                            if x.is_boat_tile[self.other_player - 1]:
                                if x.x == tile.x:
                                    axis_x = True
                        for n in range(10):
                            if axis_x:
                                row_tile = self.tiles_list[tile.x + 10*n]
                            else:
                                row_tile = self.tiles_list[tile.y*10 + n]
                            if not row_tile.selected:
                                add = False
                                for x in self.neighbours(row_tile):
                                    if x.selected and x.is_boat_tile[self.other_player - 1]:
                                        add = True
                                if add:
                                    self.ai_boat_list.append(row_tile)
                        sunk = True
                        for x in tile.boat_for_player[self.other_player - 1]:
                            if x.selected is False:
                                sunk = False
                        if sunk:
                            for x in tile.boat_for_player[self.other_player - 1]:
                                for y in self.neighbours(x):
                                    y.selected = True
                                    y.player_shot[self.player - 1] = True
                            self.sunk[self.player - 1] += 1
                            if self.sunk[self.player - 1] == 5:
                                self.switch_scenes(0)
                    else:
                        self.button_next_display(f"player {self.other_player} is now shoting")
                        self.change_shown_boats()
            else:
                rnd = random.randint(0,99)
                tile = self.tiles_list[rnd]
                if not tile.player_shot[self.player - 1]:
                    tile.player_shot[self.player - 1] = True
                    tile.selected = True
                    if tile.is_boat_tile[self.other_player - 1]:
                        for x in self.neighbours(tile):
                            self.ai_boat_list.append(x)
                    else:
                        self.button_next_display(f"player {self.other_player} is now shoting")
                        self.change_shown_boats()

    def change_shown_boats(self, show_nonhit_boats = False):
        for x in self.tiles:
            if show_nonhit_boats:
                x.on_click = lambda x: None
                x.on_hover = lambda x: None
            elif self.game_running:
                x.on_click = self.game_tile_click
                x.on_hover = self.game_tile_hover
            if x.player_shot[self.other_player - 1]:
                x.selected = True
                if x.is_boat_tile[self.player - 1]:
                    x.color_selected = pygame.Color(63,127,63)
                else:
                    x.color_selected = pygame.Color(63, 63, 127)
            elif x.is_boat_tile[self.player-1] and show_nonhit_boats:
                x.selected = True
                x.color_selected = pygame.Color(127,255,127)
            else:
                x.selected = False
        self.player, self.other_player = self.other_player, self.player

    def ai_selection(self, tile):
        while sum(self.active_boat_list) > 0:
            length = random.randint(2, 5)
            if self.active_boat_list[length] > 0:
                x = random.randint(0, 9)
                y = random.randint(0, 9)
                direction = random.choice([-10,-1,1,10])
                if 0 <= (x + 10*y + (length-1)*direction) < 100:
                    for x in (list := self.can_place_boat(self.tiles_list[x + 10*y], self.tiles_list[x + 10*y + (length-1)*direction])):
                        x.selected = True
                        x.boat_for_player[self.player - 1] = list
                    if len(list) > 1:
                        self.active_boat_list[length] -= 1
        self.next()
        if self.ai and self.player == 2:
            self.ai_selection(None)

    def next(self):
        for x in self.tiles:
            if x.selected:
                x.is_boat_tile[self.player - 1] = True
                x.boat_start = False
                x.selected = False
        if self.player == 1:
            if not self.ai:
                self.button_next_display(f"player {self.other_player} is now placing")
            self.player = 2
            self.other_player = 1
            self.active_boat_list = self.boats_list_p2
        else:
            self.button_next_display(f"player {self.other_player} is now shoting")
            self.player = 1
            self.other_player = 2
            self.active_boat_list = self.boats_list_p1
            self.start_game()

    def start_game(self):
        self.game_running = True
        for x in self.tiles:
            x.on_click = self.game_tile_click
            x.on_hover = self.game_tile_hover
        self.useful_button.text = "Show"
        self.useful_button.on_click = self.button_boats_show

    def space_pressed(self):
        if self.game_running and not self.my_boats_shown:
            self.change_shown_boats(True)
            self.useful_button.text = "Hide"
            self.useful_button.on_click = self.button_boats_hide
            self.my_boats_shown = True
        elif self.my_boats_shown:
            self.change_shown_boats(False)
            self.useful_button.text = "Show"
            self.useful_button.on_click = self.button_boats_show
            self.my_boats_shown = False


    def button_boats_show(self, tile):
        self.change_shown_boats(True)
        self.useful_button.text = "Hide"
        self.useful_button.on_click = self.button_boats_hide
        self.my_boats_shown = True

    def button_boats_hide(self, tile):
        self.change_shown_boats(False)
        self.useful_button.text = "Show"
        self.useful_button.on_click = self.button_boats_show
        self.my_boats_shown = False

    def button_next_display(self, text):
        self.button_next.text = text
        self.sprites.remove(self.tiles)
        self.sprites.remove(self.useful_button)
        self.sprites.add(self.button_next)

    def button_next_click(self, tile):
        self.sprites.add(self.tiles)
        self.sprites.add(self.useful_button)
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