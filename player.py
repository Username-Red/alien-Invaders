import pygame
from bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, image, x, y, bullet_group, bullet_img):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.bullet_group = bullet_group
        self.bullet_img = bullet_img
        self.fire_cooldown = 300
        self.last_fired = pygame.time.get_ticks()

    def fire(self, speed=5, damage=1):
        now = pygame.time.get_ticks()
        if now - self.last_fired >= self.fire_cooldown:
            bullet = Bullet(self.rect.centerx, self.rect.top, speed, damage, self.bullet_img)
            self.bullet_group.add(bullet)
            self.last_fired = now
