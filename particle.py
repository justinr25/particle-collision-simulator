import pygame

class Particle():
    def __init__(self, game, pos, vel, mass, radius, color):
        self.game = game
        self.pos = pos
        self.vel = vel
        self.mass = mass
        self.radius = radius
        self.color = color
        
        self.diameter = 2 * radius
        self.size = (self.diameter, self.diameter)
        self.rect = pygame.Rect((0, 0), self.size)
        self.rect.center = pos
    
    def update_radius(self, radius):
        self.radius = radius
        self.diameter = 2 * radius
        self.size = (self.diameter, self.diameter)
        self.rect.size = self.size
        self.rect.center = self.pos
    
    def draw(self, surf):
        pygame.draw.ellipse(surf, self.color, self.rect)
        # pygame.draw.circle(surf, self.color, self.pos, self.radius)
    
    def update(self, surf):
        # update kinematics values
        self.pos += self.vel * self.game.dt

        # handle bouncing off border
        if self.rect.left + self.vel.x + self.game.dt < 0:
            self.vel.x *= -1
            self.rect.left = 0
        if self.rect.right + self.vel.x * self.game.dt > self.game.screen.get_width():
            self.vel.x *= -1
            self.rect.right = self.game.screen.get_width()
        if self.rect.top + self.vel.y + self.game.dt < 0:
            self.vel.y *= -1
            self.rect.top = 0
        if self.rect.bottom + self.vel.y * self.game.dt > self.game.screen.get_height():
            self.vel.y *= -1
            self.rect.bottom = self.game.screen.get_height()

        # sync particle rect
        self.rect.center = self.pos

        # draw particle
        self.draw(surf)
