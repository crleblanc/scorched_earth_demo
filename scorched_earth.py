#!/usr/bin/env python

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
WHITE = (255, 255, 255)
GROUND = (125, 125, 125)
TANK_SIZE = (50, 50)

# Super simple game intended for teaching an 11 year old

def update_bullet(tank_x, tank_y, bullet, v_initial, angle, time_val):
    """ See https://en.wikipedia.org/wiki/Projectile_motion for the equation 'y = ax + bx^2'"""

    x = v_initial * time_val * math.cos(math.radians(angle))
    y = v_initial * time_val * math.sin(math.radians(angle)) - 0.5 * G * time_val**2

    bullet.x = tank_x + x
    bullet.y = tank_y - y

def explosion(screen, bullet, enemy_tank):
    """ Make an explosion if the bullet hits the enemy tank"""
    x_in_range = bullet.x > enemy_tank.left and bullet.x < enemy_tank.right
    y_in_range = bullet.y > enemy_tank.top and bullet.y < enemy_tank.bottom
    if x_in_range and y_in_range:
        pygame.draw.circle(screen, RED, (bullet.x, bullet.y), 100)
        return True

    return False


def main():
    pygame.init()

    screen = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    pygame.display.set_caption('Basic Scorched Earth')

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(WHITE)

    # draw the terrain
    border = 100
    terrain = []
    for x in range(0, WINDOWWIDTH, 75):
        y = randint(0+border, WINDOWHEIGHT-border)
        terrain.append((x, y))
    terrain.append((WINDOWWIDTH, WINDOWHEIGHT))
    terrain.append((0, WINDOWHEIGHT))
    terrain.append(terrain[0])

    pygame.draw.polygon(screen, GROUND, terrain)

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Origin is in the upper left.  These are the starting positions, we can update them later
    my_tank_coord = terrain[randint(0, len(terrain)-4)]
    my_tank_left, my_tank_top, my_tank_width, my_tank_height = (my_tank_coord[0], my_tank_coord[1], TANK_SIZE[0], TANK_SIZE[1])
    #my_tank = pygame.Rect(my_tank_left, my_tank_top, my_tank_width, my_tank_height)
    my_turret = (my_tank_left + my_tank_width/2, my_tank_left + my_tank_height/2)
    my_tank = pygame.image.load('tank1.png')
    screen.blit(my_tank, my_turret)

    enemy_tank_coord = terrain[randint(0, len(terrain)-4)]
    enemy_tank_left, enemy_tank_top, enemy_tank_width, enemy_tank_height = (enemy_tank_coord[0], enemy_tank_coord[1], TANK_SIZE[0], TANK_SIZE[1]) 
    enemy_tank = pygame.Rect(enemy_tank_left, enemy_tank_top, enemy_tank_width, enemy_tank_height)

#    pygame.draw.rect(screen, BLACK, my_tank)
    pygame.draw.rect(screen, BLACK, enemy_tank)
    print(enemy_tank_coord)

    # default values of angle and muzzle velocity
    v_initial = 50 # m/s
    angle = 45 # angle in degrees from a flat plane

    font = pygame.font.Font('freesansbold.ttf', 32)
    text_surface = font.render('Angle: %d, Velocity: %d' % (v_initial, angle), True, BLACK, 0)
    text_rect = text_surface.get_rect()
    text_rect.center = (200, 150)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_KP8]:
            #f angle < 90:
            angle += 1
        elif keys[pygame.K_DOWN] or keys[pygame.K_KP2]:
            if angle > 0:
                angle -= 1
        elif keys[pygame.K_RIGHT]:
            if v_initial < 1000:
                v_initial += 1
        elif keys[pygame.K_LEFT]:
            if v_initial > 0:
                v_initial -= 1                        
        elif keys[pygame.K_SPACE] or keys[pygame.K_KP_ENTER]:
            print('Pew Pew!!')
        
            # TODO: use the keyboard input for angle (up/down) and velocity (+/-), and enter or spacebar to shoot
            start_time = time.time()
            time_step = 0.25 # in seconds
            bullet = pygame.Rect(my_tank_left, my_tank_top, 5, 5)
            while bullet.y < WINDOWHEIGHT:
                time_diff = (time.time() - start_time) * 10
                update_bullet(my_tank_left, my_tank_top, bullet, v_initial, angle, time_diff)

                pygame.draw.rect(screen, RED, bullet)

                exploded = explosion(screen, bullet, enemy_tank)

                pygame.display.update()

                if exploded:
                    break

        screen.blit(background, (0, 0))
        text_surface = font.render('Angle: %d, Velocity: %d' % (angle, v_initial), True, BLACK, 0)
        screen.blit(text_surface, text_rect)
        pygame.draw.polygon(screen, GROUND, terrain)
#        pygame.draw.rect(screen, BLACK, my_tank)
        screen.blit(my_tank, my_turret)
        pygame.draw.rect(screen, BLACK, enemy_tank)
        pygame.time.wait(50)
        pygame.display.update()
    

if __name__ == "__main__":
    main()
