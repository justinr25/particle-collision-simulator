import sys
import time

import pygame

from utils import display_text
from particle import Particle

class Game:
    def __init__(self):
        #setup pygame
        pygame.init()
        pygame.display.set_caption('pygame-elastic-collision-test')
        self.monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
        self.is_fullscreen = False
        self.screen_size = (1280, 720)
        self.max_fps = 60
        self.screen = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()
        self.last_time = time.perf_counter()
        self.screen_bg_color = (255, 255, 255)

        # initialize particles
        self.particle1 = Particle(
            game = self,
            pos = pygame.math.Vector2(200, self.screen.get_height() // 2 + 100),
            vel = pygame.math.Vector2(5, 0),
            mass = 2000,
            radius = 200,
            color = (255, 0, 0)
        )
        self.particle2 = Particle(
            game = self,
            pos = pygame.math.Vector2(self.screen.get_width() - 300, self.screen.get_height() // 2 + 100),
            vel = pygame.math.Vector2(-5, 0),
            mass = 5,
            radius = 25,
            color = (0, 255, 0)
        )

    def run(self):
        # game loop
        while True:
            # update delta time
            self.dt = time.perf_counter() - self.last_time
            self.dt *= 60
            self.last_time = time.perf_counter()

            # event loop
            for event in pygame.event.get():
                # handle closing window
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                # handle resizing
                if event.type == pygame.VIDEORESIZE:
                    if not self.is_fullscreen:
                        self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                
                # handle toggling fullscreen with f
                if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                    self.is_fullscreen = not self.is_fullscreen
                    if self.is_fullscreen:
                        self.screen = pygame.display.set_mode(self.monitor_size, pygame.FULLSCREEN)
                    else:
                        self.screen = pygame.display.set_mode((self.screen.get_width(), self.screen.get_height()), pygame.RESIZABLE)

                # handle resetting display size with r
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.screen = pygame.display.set_mode(self.screen_size, pygame.RESIZABLE)
                
                # * DEBUG: toggle framerate with e
                if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                    if self.max_fps == 60:
                        self.max_fps = 10
                    else:
                        self.max_fps = 60

                # reset simulation with space
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.__init__()

            # clear screen
            self.screen.fill(self.screen_bg_color)

            # handle particle collision
            # if pygame.Rect.colliderect(self.particle1.rect, self.particle2.rect):
            if self.particle1.rect.right + self.particle1.vel.x * self.dt > self.particle2.rect.left + self.particle2.vel.x * self.dt:
                # # resolve overlap by moving the particles apart
                # overlap = self.particle1.rect.right - self.particle2.rect.left
                # self.particle1.rect.right -= overlap / 2
                # self.particle2.rect.left += overlap / 2

                # update velocities with elastic collision formula
                m1 = self.particle1.mass
                v1i = self.particle1.vel.x
                m2 = self.particle2.mass
                v2i = self.particle2.vel.x

                self.particle1.vel.x = (m1-m2)/(m1+m2)*v1i + 2*m2/(m1+m2)*v2i
                self.particle2.vel.x = 2*m1/(m1+m2)*v1i + (m2-m1)/(m1+m2)*v2i

            # update particles
            self.particle1.update(self.screen)
            self.particle2.update(self.screen)

            # display particle1 velocity
            display_text(
                surf = self.screen,
                text = f'v1: {self.particle1.vel.x:.2f}',
                size = 70,
                pos = (20, 20),
                color = self.particle1.color
            )

            # display particle 1 mass
            display_text(
                surf = self.screen,
                text = f'm1: {self.particle1.mass:.2f}',
                size = 70,
                pos = (20, 100),
                color = self.particle1.color
            )

            # display particle 2 velocity
            display_text(
                surf = self.screen,
                text = f'v2: {self.particle2.vel.x:.2f}',
                size = 70,
                pos = (self.screen.get_width()-250, 20),
                color = self.particle2.color
            )

            # display particle 2 mass
            display_text(
                surf = self.screen,
                text = f'm1: {self.particle2.mass:.2f}',
                size = 70,
                pos = (self.screen.get_width()-250, 100),
                color = self.particle2.color
            )

            # update pygame window
            pygame.display.update()
            self.clock.tick(self.max_fps)

if __name__ == '__main__':
    game = Game()
    game.run()