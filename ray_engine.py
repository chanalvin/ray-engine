import pygame
import math
import time

import settings
import ray
import player
# import game_data
import test_cell

pygame.init()

pygame.display.set_caption('Ray')
window = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))

background = pygame.Surface((settings.WIDTH, settings.HEIGHT))
background.fill(pygame.Color('#000000'))

def degToRad(degree):
    degree *= math.pi / 180

    return degree


def rayCasting():
    ray_angle = player.angle - settings.HALF_FOV

    for ray_count in range(settings.WIDTH):
        ray.x = player.x
        ray.y = player.y    

        ray_cos = math.cos(degToRad(ray_angle)) / ray.PRECISION
        ray_sin = math.sin(degToRad(ray_angle)) / ray.PRECISION

        # checking for wall collisions (simpler than dda)
        wall = 0
        while wall == 0:
            ray.x += ray_cos
            ray.y += ray_sin
            wall = test_cell.lvl_map[math.floor(ray.y)][math.floor(ray.x)]

        # normalizes the ray vector and finds its magnitude (distance) w/ Pythagorean Theorem
        distance = math.sqrt(math.pow(player.x - ray.x, 2) + math.pow(player.y - ray.y, 2))
        distance *= math.cos(degToRad(ray_angle - player.angle)) # fisheye fix

        wall_height = math.floor(settings.HALF_H / distance)

        ceiling_colour = 'black'
        #wall_colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        match wall:
            case 1:
                wall_colour = 'brown'
            case default:
                wall_colour = 'red'
        floor_colour = 'grey'

        # Draw
        pygame.draw.line(window, ceiling_colour, (ray_count, 0), (ray_count, settings.HALF_H - wall_height)) # ceiling
        pygame.draw.line(window, wall_colour, (ray_count, settings.HALF_H - wall_height), (ray_count, settings.HALF_H + wall_height)) # wall
        pygame.draw.line(window, floor_colour, (ray_count, settings.HALF_H + wall_height), (ray_count, settings.HEIGHT)) # floor

        ray_angle += ray.INCREMENT


def keyControls():
    match event.key:
        case pygame.K_UP:
            player_cos = math.cos(degToRad(player.angle)) * settings.SPEED
            player_sin = math.sin(degToRad(player.angle)) * settings.SPEED
            new_x = player.x + player_cos
            new_y = player.y + player_sin

            if test_cell.lvl_map[math.floor(new_y)][math.floor(new_x)] == 0:
                player.x = new_x
                player.y = new_y

        case pygame.K_DOWN:
            player_cos = math.cos(degToRad(player.angle)) * settings.SPEED
            player_sin = math.sin(degToRad(player.angle)) * settings.SPEED
            new_x = player.x - player_cos
            new_y = player.y - player_sin

            if test_cell.lvl_map[math.floor(new_y)][math.floor(new_x)] == 0:
                player.x = new_x
                player.y = new_y

        case pygame.K_LEFT:
            player.angle -= settings.TURNRATE

        case pygame.K_RIGHT:
            player.angle += settings.TURNRATE


running = True
while running:
    events = pygame.event.get()
    for event in events:
        match event.type:
            case pygame.QUIT:
                running = False
            case pygame.KEYDOWN:
                keyControls()

    window.blit(background, (0, 0))

    rayCasting()

    time.sleep(settings.RENDER_DELAY)

    pygame.display.update()