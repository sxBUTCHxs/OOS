import pygame
class DeleteMenu:
    def __init__(self):
        size = pygame.Vector2(100, 75)
        self.btn = pygame.Surface(size)
        self.btn.fill((130,130,130))
        font = pygame.font.Font(None, 40)
        btn_text = font.render("Delete", True, (0,0,0))
        btn_text_rect = btn_text.get_rect()
        btn_text_rect.center = size / 2
        self.btn.blit(btn_text, btn_text_rect)

        self.btn_rect = self.btn.get_rect()
        self.btn_rect.right = 1260
        self.btn_rect.bottom = 700
        
    def is_mouse_on_play(self):
        return self.btn_rect.collidepoint(pygame.mouse.get_pos())

    def update(self):

        if self.is_mouse_on_play():
            self.btn.set_alpha(255)
            self.btn.set_alpha(255)
        else:#make the image more transparent
            self.btn.set_alpha(100)
            self.btn.set_alpha(100)
        

    def draw(self, screen):
        screen.blit(self.btn, self.btn_rect)