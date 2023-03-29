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

        ceiling_colour = 'Gainsboro'
        #wall_colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        match wall:
            case 1:
                wall_colour = 'LightGoldenrodYellow'
            case default:
                wall_colour = 'Fuchsia'
        floor_colour = 'SlateGray'

        # Draw
        pygame.draw.line(window, ceiling_colour, (ray_count, 0), (ray_count, settings.HALF_H - wall_height)) # ceiling
        pygame.draw.line(window, wall_colour, (ray_count, settings.HALF_H - wall_height), (ray_count, settings.HALF_H + wall_height)) # wall
        pygame.draw.line(window, floor_colour, (ray_count, settings.HALF_H + wall_height), (ray_count, settings.HEIGHT)) # floor

        ray_angle += ray.INCREMENT


def posCalc(key):
    if key == pygame.K_a or key == pygame.K_d:
        angle = degToRad(player.angle) + math.pi/2
    else:
        angle = degToRad(player.angle)

    player_cos = math.cos(angle) * settings.SPEED #*sidestrafe 0.5 mod
    player_sin = math.sin(angle) * settings.SPEED

    if key == pygame.K_w or key == pygame.K_d:
        x = player.x + player_cos
        y = player.y + player_sin
    elif key == pygame.K_s or key == pygame.K_a:
        x = player.x - player_cos
        y = player.y - player_sin
    else:
        x = player.x
        y = player.y

    if test_cell.lvl_map[math.floor(y)][math.floor(x)] == 0:
        player.x = x
        player.y = y


def keyControls():
    rel_mouse = pygame.mouse.get_rel()
    rel_x = rel_mouse[0]
    rel_y = rel_mouse[1]

    match event.type:
        case pygame.KEYDOWN:
            posCalc(event.key)


        case pygame.MOUSEMOTION:
            player.angle += settings.TURNRATE * rel_x


pygame.mouse.set_visible(False)    # hides mouse cursor ingame
pygame.event.set_grab(True)    # locks mouse in window

running = True
while running:
    events = pygame.event.get()
    for event in events:
        match event.type:
            case pygame.QUIT:
                running = False
            case pygame.KEYDOWN:
                keyControls()
            case pygame.MOUSEMOTION:
                pygame.mouse.set_pos([settings.WIDTH/2, settings.HEIGHT/2])
                keyControls()

    window.blit(background, (0, 0))

    rayCasting()

    time.sleep(settings.RENDER_DELAY)

    pygame.display.update()