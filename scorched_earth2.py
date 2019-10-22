import pygame
import sys
import time
import math
from random import randint

G = 9.8 # gravitational constant, in m/s^2
WINDOWWIDTH = 1024
WINDOWHEIGHT = 768
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
GROUND = (125, 125, 125)


class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, left_or_right):
        super().__init__()

        if left_or_right == 'right':
            self.image = pygame.image.load('tank_facing_right.png')
        else:
            self.image = pygame.image.load('tank_facing_left.png')

        self.rect = self.image.get_rect()
        self.rect.x = x - self.rect[2] // 2
        self.rect.y = y - self.rect[3]

class Terrain(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([WINDOWWIDTH, WINDOWHEIGHT])
        self.image.fill(BLUE)
 
        border = 100
        self.points = []
        for x in range(0, WINDOWWIDTH, 75):
            y = randint(200, WINDOWHEIGHT-border)
            self.points.append((x, y))

        self.points.append((WINDOWWIDTH, WINDOWHEIGHT))
        self.points.append((0, WINDOWHEIGHT))
        self.points.append(self.points[0])

        pygame.draw.polygon(self.image, GROUND, self.points)
        self.rect = self.image.get_rect()
        

class Main:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
        self.default_velocity = 50 # m/s
        self.default_angle = 45 # angle in degrees from a flat plane
        self.velocity = self.default_velocity
        self.angle = self.default_angle
        self.bg_group = pygame.sprite.Group()
        self.fg_group = pygame.sprite.Group()

        pygame.display.set_caption('Basic Scorched Earth')
    
    def keyboard_input(self):
        shoot = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_KP8]:
            self.angle += 1
        elif keys[pygame.K_DOWN] or keys[pygame.K_KP2]:
            if self.angle > 0:
                self.angle -= 1
        elif keys[pygame.K_RIGHT]:
            if self.velocity < 1000:
                self.velocity += 1
        elif keys[pygame.K_LEFT]:
            if self.velocity > 0:
                self.velocity -= 1                        
        elif keys[pygame.K_SPACE] or keys[pygame.K_KP_ENTER]:
            shoot = True
        
        return shoot

    def game(self):
        # reset angle and velocity to defaults
        self.angle = self.default_angle
        self.velocity = self.default_velocity

        self.make_background()

        terrain = Terrain()
        my_tank_x, my_tank_y = terrain.points[randint(0, len(terrain.points)//2)]
        my_tank = Tank(my_tank_x, my_tank_y, 'right')

        enemy_tank_x, enemy_tank_y = terrain.points[randint(len(terrain.points)//2, len(terrain.points)-3)]
        enemy_tank = Tank(enemy_tank_x, enemy_tank_y, 'left')

        self.bg_group.empty()
        self.bg_group.add(terrain)
        self.bg_group.draw(self.screen)

        # Hmm, sometimes the tanks are drawn behind the background so remove the terrain from the group
        self.bg_group.empty()
        self.fg_group.add(my_tank)
        self.fg_group.add(enemy_tank)
        self.update()

        run = True
        while run:
            shoot = self.keyboard_input()
            if shoot:
                # my_tank.rect.x += 10
                self.update()
            else:
                time.sleep(0.1)

        return run

    def make_background(self):
        # Fill background
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill(WHITE)
        self.screen.blit(background, (0, 0))

    def update(self):
        self.fg_group.draw(self.screen)
        pygame.display.flip()
    
    def play(self):
        run = True
        while run:
            run = self.game()


main = Main()
main.play()
