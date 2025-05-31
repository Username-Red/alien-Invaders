import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, damage, image_surface):
        super().__init__()
        self.image = image_surface
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -speed  # negative = move up
        self.damage = damage

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()