from tkinter import Tk, Canvas, Frame, BOTH

import math
import time

import test_cell


WIN_WIDTH = 640
WIN_HEIGHT = 480

FOV = 60
REND_DELAY = 5

R_PRECISION = 64
# what a stupid name
RAY_INC = FOV / WIN_WIDTH

P_SPEED = 0.5

C_COLOR = 'Gainsboro'
W_COLOR = 'LightGoldenrodYellow'
F_COLOR = 'SlateGray'

player = {
    'x': 6,
    'y': 6,
    'angle': 60,
}


# le self
class Stuff:

    def __init__(self):
        self.window = Tk()
        self.canvas = Canvas(self.window, width=WIN_WIDTH, height=WIN_HEIGHT)
        self.window.title('My name is Ray')
        self.window.bind('<Key>', key_pressed)
        self.canvas.pack()

    def run(self):
        raycast(self.canvas)
        
        self.window.after(REND_DELAY, self.update)
        self.window.mainloop()

    def update(self):
        raycast(self.canvas)

        self.window.after_idle(self.update)


def deg_conv(angle):
    angle *= math.pi / 180
    
    return angle


def raycast(canvas): # lol
    canvas.delete('all')

    ray_angle = player['angle'] - FOV/2
    for ray_count in range(WIN_WIDTH):
        ray_x = player['x']
        ray_y = player['y']

        ray_cos = math.cos(deg_conv(ray_angle)) / R_PRECISION
        ray_sin = math.sin(deg_conv(ray_angle)) / R_PRECISION

        wall = 0
        while wall == 0:
            ray_x += ray_cos
            ray_y += ray_sin
            # TODO: change level/map selection method
            wall = test_cell.lvl_map[math.floor(ray_y)][math.floor(ray_x)]

        distance = math.sqrt(math.pow(player['x'] - ray_x, 2) + math.pow(player['y'] - ray_y, 2))
        distance *= math.cos(deg_conv(ray_angle - player['angle']))

        # rename to w_height for consistency?
        wall_height = math.floor((WIN_HEIGHT/2) / distance)

        canvas.create_line((ray_count, 0), (ray_count, WIN_HEIGHT/2 - wall_height), fill=C_COLOR)
        canvas.create_line((ray_count, WIN_HEIGHT/2 - wall_height), (ray_count, WIN_HEIGHT/2 + wall_height), fill=W_COLOR)
        canvas.create_line((ray_count, WIN_HEIGHT/2 + wall_height), (ray_count, WIN_HEIGHT), fill=F_COLOR)

        ray_angle += RAY_INC


def key_pressed(event):
    key = event.char

    # collapse a couple of these together
    match key:
        case 'a' | 'd':
            angle = deg_conv(player['angle']) + math.pi/2
        case _:
            angle = deg_conv(player['angle'])
    
    player_cos = math.cos(angle) * P_SPEED
    player_sin = math.sin(angle) * P_SPEED

    # such a weird way to calculate
    match key:
        case 'w' | 'd':
            x = player['x'] + player_cos
            y = player['y'] + player_sin
        case 's' | 'a':
            x = player['x'] - player_cos
            y = player['y'] - player_sin
        case _:
            x = player['x']
            y = player['y']

    if test_cell.lvl_map[math.floor(y)][math.floor(x)] == 0:
        player['x'] = x
        player['y'] = y


def main():
    stuff = Stuff()
    stuff.run()


if __name__ == '__main__':
    main()