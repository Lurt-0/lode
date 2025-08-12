import pygame

class Sprite(pygame.sprite.Sprite):
    def __init__(self, rect:pygame.Rect, text:str = "" ,text_size = 130 ,on_click = lambda x = None: None,on_hover = lambda x = None: None,base = lambda x = None: None):
        super().__init__()
        self.on_click = on_click #function activated on sprite click
        self.on_hover = on_hover #function activated upon sprite hovering
        self.base = base #function activated when you don't hover on sprite
        self.rect = rect #rectangle defining pisition on screen
        self.color = "black"
        self.color_hover = "red"
        self.text = text
        self.base_text_size = text_size
        self.text_size = text_size #text size, that changes
        self.text_color = pygame.Color("white")
        self.image = self.create_img(self.color,self.text) #default image, that is drawn when you call the draw function
        self.hover = False

    def create_img(self, color, text = ""): #creates rectangle of color with text writen on it
        img = pygame.Surface(self.rect.size)
        img.fill(color)
        if text != "":
            text_surf=pygame.font.Font.render(pygame.font.SysFont(pygame.font.get_default_font(),self.text_size),text,1,self.text_color)
            text_rect = text_surf.get_rect(center=pygame.Rect((0,0),self.rect.size).center)
            text_surf2=pygame.font.Font.render(pygame.font.SysFont(pygame.font.get_default_font(),self.text_size),text,1,"black")
            text_rect2 = text_surf2.get_rect(center=pygame.Rect(0,0,self.rect.w +16, self.rect.h+16).center)
            img.blit(text_surf2, text_rect2)
            img.blit(text_surf, text_rect)
        return img

    def update(self): #updates appearance of the sprite
        if self.hover:
            self.image = self.create_img(self.color_hover, self.text)
        else:
            self.image = self.create_img(self.color, self.text)