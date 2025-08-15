import pygame
from menu import Menu
from lode_game import Lode

class Game:
    def __init__(self):
        pygame.init()
        self.active_scene = None # determines what scene is currently shown
        self.scale = pygame.display.Info().current_w // 640 # finds scale of your display
        self.screen = pygame.display.set_mode((self.scale * 640, self.scale * 360), pygame.FULLSCREEN) #game display
        self.clock = pygame.time.Clock()
        self.load_scene(0) #loads menu

    def load_scene(self, id): #loads the correct scene. Can be called in Scene classes
        if id == 0:
            self.active_scene = Menu(self.load_scene ,self.scale)
        elif id == 1:
            self.active_scene = Lode(self.load_scene, self.scale)
        elif id == 2:
            self.active_scene = Lode(self.load_scene, self.scale, True)
        elif id == 3:
            self.active_scene = Menu(self.load_scene, self.scale, True)
        elif id == 4:
            self.active_scene = Menu(self.load_scene, self.scale, True, 2)

    def run(self): #the game runs here
        while True:
            self.active_scene.update(pygame.mouse.get_pos())
            for event in pygame.event.get(): #loads and checks all relevant events
                if event.type == pygame.QUIT:
                    raise SystemExit

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.active_scene.on_mouse_down(event.pos)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.active_scene.space_pressed()
                    if event.key == pygame.K_ESCAPE:
                        self.active_scene.quit(None)
                    if event.key == pygame.K_BACKSPACE:
                        self.active_scene = Menu(self.load_scene, self.scale)

            self.active_scene.draw(self.screen)
            pygame.display.update()
            self.clock.tick(60)


game = Game()
game.run() #starts the game