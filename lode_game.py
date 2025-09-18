import random
from scene import Scene
import pygame
from collections.abc import Callable
from base_sprite import Sprite
from tile import Tile

class Lode(Scene): #class for the game scene
    def __init__(self, switch: Callable[[int], None],scale, ai = False):
        super().__init__(switch,scale)
        self.selected_tile = None  #keeps track of start of the currently placed boat
        self.ai = ai #determines if game is against AI
        self.player = 1 #keeps track of the current player
        self.other_player = 2
        self.tiles = pygame.sprite.Group() #iterable group for all tiles
        self.tiles_list = [] #list for tiles, used when group is not effective
        self.sunk = [None,[0,0,1,2,1,1,0,0,0,0,0],[0,0,1,2,1,1,0,0,0,0,0]] #counts how many boats each player has sunk
        self.ai_boat_list = [] #priority list for AI boat shooting
        self.shooting = False #remmbers if we are in the shooting part of the game
        self.my_boats_shown = False
        self.info_shown = False
        self.boat_list = [None,[0,0,1,2,1,1,0,0,0,0,0],[0,0,1,2,1,1,0,0,0,0,0]]
        self.top_display_sprite = Sprite(pygame.Rect(171 * self.scale, 0, 298 * self.scale, 60 * self.scale), "Player 1 is now placing",38 * self.scale)
        self.boats_remaining = Sprite(pygame.Rect(470 * self.scale, 91 * self.scale, 170 * self.scale, 20 * self.scale),f"2:{self.boat_list[self.player][2]}, 3:{self.boat_list[self.player][3]}, 4:{self.boat_list[self.player][4]}, 5:{self.boat_list[self.player][5]}", 20 * self.scale)
        for y in range(10):
            for x in range(10):
                self.tiles.add(tile := Tile(pygame.Rect((x * 30 + 171) * self.scale, (y * 30 + 61) * self.scale, 28 * self.scale, 28 * self.scale), x, y, self.selection_tile_click, self.selection_tile_hover, self.button_base))
                self.tiles_list.append(tile)
        self.load_sprites()

    def load_sprites(self): #loads all relevant sprites
        self.sprites.add(self.top_display_sprite)
        self.sprites.add(self.boats_remaining)
        self.sprites.add(Sprite(pygame.Rect(0, 61 * self.scale, 170 * self.scale, 25 * self.scale),
                                "press TAB for info", 25 * self.scale))
        self.sprites.add(Sprite(pygame.Rect(470 * self.scale, 61 * self.scale, 170 * self.scale, 20 * self.scale),
                                "Boats remaining to place:", 20 * self.scale))
        self.sprites.add(self.tiles)
        if self.shooting:
            self.sprites.add(Sprite(pygame.Rect(470 * self.scale, 61 * self.scale, 170 * self.scale, 20 * self.scale),"Your boats alive:", 20 * self.scale))
        else:
            self.sprites.add(Sprite(pygame.Rect(470* self.scale, 61* self.scale, 170 * self.scale, 20* self.scale),"Boats remaining to place:" ,20 * self.scale))
        self.sprites.add(Sprite(pygame.Rect(470* self.scale, 81 * self.scale, 170 * self.scale, 10 * self.scale), "(format length:number of boats)",10 * self.scale))

    def selection_tile_hover(self, tile): #determines color of tile while selecting
        for x in self.tiles:
            if x in self.can_place_boat(tile,self.selected_tile) and self.selected_tile is not None: x.hover = True
            else: x.hover = False
        if not bool(self.can_place_boat(tile,self.selected_tile)):
            tile.color = pygame.Color(255, 127, 127)
        else:
            tile.color = pygame.Color(127, 255, 127)

    def game_tile_hover(self, tile): #determines color of tile in game
        tile.color =  pygame.Color(127, 255, 127)

    def selection_tile_click(self, tile): #determines what happens on click while selecting
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
                self.boat_list[self.player][len(list)] -= 1
                self.boats_remaining.text =f"2:{self.boat_list[self.player][2]}, 3:{self.boat_list[self.player][3]}, 4:{self.boat_list[self.player][4]}, 5:{self.boat_list[self.player][5]}"
                self.boats_remaining.update()
                if sum(self.boat_list[self.player]) == 0:
                    if self.ai:
                        self.ai_selection(None)
                    else:
                        self.next_player()

    def game_tile_click(self, tile): #determines what happens on click in game
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
                    self.sunk[self.player][len(tile.boat_for_player[self.other_player - 1])] -= 1
                    if sum(self.sunk[self.player]) == 0:
                        self.switch_scenes(2 + self.player)
            else:
                if self.ai and self.player == 1:
                    self.ai_move()
                else:
                    self.top_display_sprite.text = f"Player {self.other_player} is now shoting"
                    self.change_shown_boats()

    def ai_selection(self, tile): #randomly places all the boats
        while sum(self.boat_list[self.player]) > 0:
            length = random.randint(2, 5)
            if self.boat_list[self.player][length] > 0:
                x = random.randint(0, 9)
                y = random.randint(0, 9)
                direction = random.choice([-10, -1, 1, 10])
                if 0 <= (x + 10 * y + (length - 1) * direction) < 100:
                    for x in (list := self.can_place_boat(self.tiles_list[x + 10 * y],self.tiles_list[x + 10 * y + (length - 1) * direction])):
                        x.selected = True
                        x.boat_for_player[self.player - 1] = list
                    if len(list) > 1:
                        self.boat_list[self.player][length] -= 1
        self.next_player()
        if self.ai and self.player == 2:
            self.ai_selection(None)

    def ai_move(self): #mekes ai move
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
                            self.sunk[self.player][len(tile.boat_for_player[self.other_player - 1])] -= 1
                            if sum(self.sunk[self.player]) == 0:
                                self.switch_scenes(2 + self.player)
                    else:
                        self.top_display_sprite.text = f"Player {self.other_player} is now shoting"
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
                        self.top_display_sprite.text = f"Player {self.other_player} is now shoting"
                        self.change_shown_boats()

    def change_shown_boats(self, show_not_hit_boats = False): #changes players or shows preview of your side
        for x in self.tiles:
            if show_not_hit_boats:
                x.on_click = lambda x: None
                x.on_hover = lambda x: None
            elif self.shooting:
                self.boats_remaining.text = f"2:{self.sunk[self.player][2]}, 3:{self.sunk[self.player][3]}, 4:{self.sunk[self.player][4]}, 5:{self.sunk[self.player][5]}"
                x.on_click = self.game_tile_click
                x.on_hover = self.game_tile_hover
            if x.player_shot[self.other_player - 1]:
                x.selected = True
                if x.is_boat_tile[self.player - 1]:
                    x.color_selected = pygame.Color(63,127,63)
                else:
                    x.color_selected = pygame.Color(63, 63, 127)
            elif x.is_boat_tile[self.player-1] and show_not_hit_boats:
                x.selected = True
                x.color_selected = pygame.Color(127,255,127)
            else:
                x.selected = False
        self.player, self.other_player = self.other_player, self.player

    def next_player(self): #swithes players
        for x in self.tiles:
            x.hover = False
            x.boat_start = False
            if x.selected:
                x.is_boat_tile[self.player - 1] = True
                x.selected = False
        if self.player == 1:
            if not self.ai:
                self.top_display_sprite.text = f"Player {self.other_player} is now placing"
            self.player = 2
            self.other_player = 1
            self.boats_remaining.text = f"2:{self.boat_list[self.player][2]}, 3:{self.boat_list[self.player][3]}, 4:{self.boat_list[self.player][4]}, 5:{self.boat_list[self.player][5]}"
            self.boats_remaining.update()
        else:
            self.top_display_sprite.text = f"Player {self.other_player} is now shoting"
            self.player = 1
            self.other_player = 2
            self.start_shooting()

    def start_shooting(self): #activates the game
        self.shooting = True
        self.sprites.empty()
        self.load_sprites()
        for x in self.tiles:
            x.on_click = self.game_tile_click
            x.on_hover = self.game_tile_hover

    def space_pressed(self): #determines what SPACE does
        if not self.shooting:
            self.ai_selection(None)
        elif self.shooting and not self.my_boats_shown:
            self.change_shown_boats(True)
            self.my_boats_shown = True
        elif self.my_boats_shown:
            self.change_shown_boats(False)
            self.my_boats_shown = False

    def tab_pressed(self): #determines what TAB does (shows info)
        if self.info_shown:
            self.sprites.empty()
            self.load_sprites()
            self.info_shown = False
        else:
            self.sprites.empty()
            self.sprites.add(
                Sprite(pygame.Rect(0, 0, 640 * self.scale, 60 * self.scale),
                       "Info:", 60 * self.scale))
            self.sprites.add(
                Sprite(pygame.Rect(0, 120 * self.scale, 640 * self.scale, 60 * self.scale),
                       "Controls:", 60 * self.scale))
            self.sprites.add(
                Sprite(pygame.Rect(0, 220 * self.scale, 640 * self.scale, 40 * self.scale),
                       "press BACKSPACE to return to MENU", 40 * self.scale))
            self.sprites.add(
                Sprite(pygame.Rect(0, 260 * self.scale, 640 * self.scale, 40 * self.scale),
                       "press ESC to quit the game", 40 * self.scale))
            self.sprites.add(
                Sprite(pygame.Rect(0, 300 * self.scale, 640 * self.scale, 40 * self.scale),
                       "press TAB to return", 40 * self.scale))
            if self.shooting:
                self.sprites.add(
                    Sprite(pygame.Rect(0, 180 * self.scale, 640 * self.scale, 40 * self.scale),
                           "press SPACE to show your boats", 40 * self.scale))
                self.sprites.add(
                    Sprite(pygame.Rect(0, 60 * self.scale, 640 * self.scale, 20 * self.scale),
                           "you can try to shoot boat by clicking a tile, boats can't be on dark blue tiles", 20 * self.scale))
                self.sprites.add(
                    Sprite(pygame.Rect(0, 80 * self.scale, 640 * self.scale, 20 * self.scale),
                           "if you hit it will turn green and if you miss your opponent plays", 20 * self.scale))
                self.sprites.add(
                    Sprite(pygame.Rect(0, 100 * self.scale, 640 * self.scale, 20 * self.scale),
                           "you can see, how your opponent is doing by pressing SPACE and on the right", 20 * self.scale))
            else:
                self.sprites.add(
                    Sprite(pygame.Rect(0, 180 * self.scale, 640 * self.scale, 40 * self.scale),
                           "press SPACE automatically place your boats", 40 * self.scale))
                self.sprites.add(
                    Sprite(pygame.Rect(0, 60 * self.scale, 640 * self.scale, 20 * self.scale),
                           "place your boats by clicking on the starting and ending tile, where you want to place it", 20 * self.scale))
                self.sprites.add(
                    Sprite(pygame.Rect(0, 80 * self.scale, 640 * self.scale, 20 * self.scale),
                           "on the right you can see what boats remain to place", 20 * self.scale))
                self.sprites.add(
                    Sprite(pygame.Rect(0, 100 * self.scale, 640 * self.scale, 20 * self.scale),
                           "if you press SPACE all your boats will be placed randomly", 20 * self.scale))
            self.info_shown = True

    def neighbours(self, tile): #helping function, that returns sprite group of neighbouring tiles
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

    def neighbours_selected(self, tile): #helping function, that determines if any of neighbouring tiles are selected
        return_bool = False
        for x in self.neighbours(tile):
            if x.selected:
                return_bool = True
        return return_bool

    def can_place_boat(self,tile, tile2): #helping function, that checks if the boat between tile and tile2 is valid and returns all it's tiles
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
                if self.tiles_list[x + 10*y1].selected or self.neighbours_selected(self.tiles_list[x + 10 * y1]) or self.boat_list[self.player][x2 - x1 + 1] <= 0:
                    return pygame.sprite.Group()
        elif y2 > y1 and x1 == x2:
            for y in range(y1, y2 + 1):
                return_tiles.add(self.tiles_list[x1 + 10*y])
                if self.tiles_list[x1 + 10*y].selected or self.neighbours_selected(self.tiles_list[x1 + 10 * y]) or self.boat_list[self.player][y2 - y1 + 1] <= 0:
                    return pygame.sprite.Group()
        return return_tiles