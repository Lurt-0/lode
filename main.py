import pygame
from menu import Menu
from lode_game import Lode

class Game:
    def __init__(self):
        pygame.init()
        self.active_scene = None
        self.screen = pygame.display.set_mode((1920,1080), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.load_scene(0)
        self.waiting = False

    def load_scene(self, id):
        if id == 0:
            self.active_scene = Menu(self.load_scene)
        elif id == 1:
            self.active_scene = Lode(self.load_scene)
        elif id == 2:
            self.active_scene = Lode(self.load_scene, True)
        elif id == 3:
            self.active_scene = Lode(self.load_scene, True)
        elif id == 4:
            self.active_scene = Lode(self.load_scene, True)

    def run(self):
        while True:
            self.active_scene.update(pygame.mouse.get_pos())
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.active_scene.on_mouse_down(event.pos)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.active_scene.space_pressed()
                    if event.key == pygame.K_ESCAPE:
                        self.active_scene = Menu(self.load_scene)

            self.active_scene.draw(self.screen)
            pygame.display.update()
            self.clock.tick(60)


game = Game()
game.run()