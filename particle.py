import pygame

class Particle():
    def __init__(self, game, pos, vel, mass, radius, color):
        self.game = game
        self.pos = pos
        self.vel = vel
        self.mass = mass
        self.radius = radius
        self.color = color
        
        self.size = (2*radius, 2*radius)
        self.rect = pygame.Rect((0, 0), self.size)
        self.rect.center = pos
    
    def draw(self, surf):
        pygame.draw.ellipse(surf, self.color, self.rect)
        # pygame.draw.circle(surf, self.color, self.rect.center, self.radius)
    
    def update(self, surf):
        # draw particle
        self.draw(surf)

        # handle bouncing off border
        if self.rect.left + self.vel.x + self.game.dt < 0:
            self.vel.x *= -1
            self.rect.left = 0
        if self.rect.right + self.vel.x * self.game.dt > self.game.screen.get_width():
            self.vel.x *= -1
            self.rect.right = self.game.screen.get_width()
        if self.rect.top + self.vel.y + self.game.dt < 0:
            self.vel.x *= -1
            self.rect.top = 0
        if self.rect.bottom + self.vel.y * self.game.dt > self.game.screen.get_height():
            self.vel.x *= -1
            self.rect.bottom = self.game.screen.get_height()
            
        # update kinematics values
        self.rect.move_ip(self.vel * self.game.dt)