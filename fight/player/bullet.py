from turtle import position
import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, position: pygame.Vector2, direction: pygame.Vector2, damage=10):
        super().__init__()
        self.size = (12, 12)
        self.image = pygame.Surface(self.size)
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        speed = 15
        direction = direction.copy()
        if direction.length() != 0:
            direction.scale_to_length(speed)
        else:
            direction = pygame.Vector2(1, 1)
            direction.scale_to_length(speed)

        self.movement = direction.copy()
        self.position = position.copy()
        self.damage = damage

    def update(self, elapsed_time):
        movement = self.movement * (33.33 / elapsed_time)
        self.position += movement

        if self.position.x + self.size[0] < 0 or self.position.x - self.size[0] > 1280 or\
                self.position.y + self.size[1] < 0 or self.position.y - self.size[1] > 720:
            self.kill()

        self.rect.center = (self.position.x, self.position.y)
