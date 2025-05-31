import pygame

class Badguy(pygame.sprite.Sprite):
    def __init__(self, image, x, y, speed, hp, type_key):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y)) 
        self.hp = hp

        self.direction = 1 
        self.speed = speed 
        self.max_hp = hp
        self.type_key = type_key

    def movePattern(self, screen_width):
        if self.type_key == "boss":
            self.rect.y += self.speed  # Boss slowly descends
        else:
            self.rect.x += self.direction * self.speed

            # Reverse direction if hitting screen edges
            if self.rect.right >= screen_width or self.rect.left <= 0:
                self.direction *= -1
                self.rect.y += 50  # Move down on edge hit

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.kill()
            # Optional: play explosion here
            
