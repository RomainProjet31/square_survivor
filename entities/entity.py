import pygame

from utils.math_utils import Vec


class Entity:

    def __init__(self, current_map, size, speed, x, y, collider, color=(0, 0, 0)):
        self.current_map = current_map
        self.collider = collider
        self.vel = Vec(0.0, 0.0)
        self.speed = speed
        self.alive = True

        self.surf = pygame.Surface((size, size))
        self.surf.fill(color)

        self.rect = self.surf.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, dt):
        """ Apply a reset on the vector """
        self.manage_shifting(dt)
        self.vel.reset()

    def manage_shifting(self, dt):
        new_pos_x = self.rect.x + self.vel.x * dt * self.speed
        new_pos_y = self.rect.y + self.vel.y * dt * self.speed

        if new_pos_x > 0 and new_pos_x + self.rect.w < self.get_screen_width():
            self.rect.x = new_pos_x
        if new_pos_y > 0 and new_pos_y + self.rect.h < self.get_screen_height():
            self.rect.y = new_pos_y

    def handle_collision(self):
        for entity in self.current_map.entities[0]:
            if entity.collider and self.rect.colliderect(entity.rect):
                if self.vel.x > 0 and entity.rect.collidepoint(
                        self.rect.midright) or self.vel.x < 0 and entity.rect.collidepoint(self.rect.midleft):
                    self.vel.x = 0
                if self.vel.y > 0 and entity.rect.collidepoint(
                        self.rect.midbottom) or self.vel.y < 0 and entity.rect.collidepoint(self.rect.midtop):
                    self.vel.y = 0

    def get_screen_width(self):
        return self.current_map.game_manager.screen.get_size()[0]

    def get_screen_height(self):
        return self.current_map.game_manager.screen.get_size()[1]

    def render(self):
        self.current_map.game_manager.screen.blit(self.surf, self.rect)

    def collides(self, other):
        self.rect.colliderect(other)
