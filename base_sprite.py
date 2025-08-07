import pygame

class Sprite(pygame.sprite.Sprite):
    def __init__(self, rect:pygame.Rect ,on_click = lambda x = None: None,on_hover = lambda x = None: None,not_hover = lambda x = None: None, text:str = ""):
        super().__init__()
        self.on_click = on_click
        self.on_hover = on_hover
        self.not_hover = not_hover
        self.rect = rect
        self.color = "green"
        self.hover_color = "red"
        self.text = text
        self.text_size = 20
        self.text_color = pygame.Color("Black")
        self.image = self.create_img(self.rect,self.color,self.text)
        self.hover = False

    def create_img(self, rect, color, text = ""):
        img = pygame.Surface(rect.size)
        img.fill(color)
        if text != "":
            text_surf=pygame.font.Font.render(pygame.font.SysFont(pygame.font.get_default_font(),self.text_size),text,1,self.text_color)
            text_rect = text_surf.get_rect(center=pygame.Rect((0,0),rect.size).center)
            img.blit(text_surf, text_rect)
        return img

    def update(self):
        if self.hover:
            self.image = self.create_img(self.rect, self.color_hover, self.text)
        else:
            self.image = self.create_img(self.rect, self.color, self.text)