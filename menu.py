from scene import Scene
import pygame
from collections.abc import Callable
from base_sprite import Sprite

class Menu(Scene): #class for the menu scene
    def __init__(self, switch: Callable[[int], None],scale, end = False, player = 1):
        super().__init__(switch,scale)
        self.move_down = 0 #if the menu is winning, moves sprites down
        if end: #adds text if menu is winning
            self.move_down = 60  * self.scale
            self.sprites.add(Sprite(pygame.Rect(150 * self.scale, 0, 340 * self.scale, 60  * self.scale), f"Player {player} won!", 70 * self.scale))
            self.sprites.add(Sprite(pygame.Rect(150 * self.scale, 60  * self.scale, 340 * self.scale, 30  * self.scale), f"Play again?", 20 * self.scale))
        self.sprites.add(Sprite(pygame.Rect(150 * self.scale, 30  * self.scale + self.move_down ,340 * self.scale,75 * self.scale),"1 Player",60 * self.scale,self.pvAI_button_click,self.button_hover,self.button_base))
        self.sprites.add(Sprite(pygame.Rect(150 * self.scale, 120  * self.scale +  self.move_down, 340 * self.scale, 75 * self.scale),"2 Players",60 * self.scale, self.pvp_button_click, self.button_hover, self.button_base))
        self.sprites.add(Sprite(pygame.Rect(150 * self.scale, 210  * self.scale + self.move_down,340 * self.scale,75 * self.scale),"Quit",60 * self.scale,self.quit,self.button_hover,self.button_base))

    def pvp_button_click(self, x): #zapne hru pro jendoho hráče proti AI
        self.switch_scenes(1)

    def pvAI_button_click(self, x): #zapne hru pro dva hráče
        self.switch_scenes(2)