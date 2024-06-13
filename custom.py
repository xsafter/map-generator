"""
EN:
This version of the algorithm is used in The Maze Game Telegram bot (by @whynotlol1)
RU:
Эта версия алгоритма используется в телеграм боте The Maze Game (от @whynotlol1)
"""


# Credit: @xsafter

from collections import deque
from PIL import Image
import random


def make_grid(width, height):
    newgrid = [[0 for _ in range(height)] for _ in range(width)]
    for i in range(len(newgrid)):
        for j in range(len(newgrid[i])):
            if i == 0 or j == 0 or i == len(newgrid) - 1 or j == len(newgrid[0]) - 1:
                newgrid[i][j] = 1
    return newgrid


def populate_grid(grid, chance):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if random.randint(0, 100) <= chance:
                grid[i][j] = 1
    return grid


def automate_iteration(grid, min_count, make_pillars):
    new_grid = [row[:] for row in grid]
    for i in range(1, len(grid) - 1):
        for j in range(1, len(grid[0]) - 1):
            count = 0
            for k in range(-1, 2):
                for l_ in range(-1, 2):
                    if grid[i + k][j + l_] == 1:
                        count += 1
            if count >= min_count or (count == 0 and make_pillars == 1):
                new_grid[i][j] = 1
            else:
                new_grid[i][j] = 0
    return new_grid


def flood_find_empty(grid, tries, goal):
    times_remade = 0
    percentage = 0
    new_grid = []

    while times_remade < tries and percentage < goal:
        copy_grid = [row[:] for row in grid]
        open_count = 0
        times_remade += 1
        unvisited = deque([])
        new_grid = [[1 for _ in range(len(grid[0]))] for _ in range(len(grid))]
        # find a random empty space, hope it's the biggest cave
        randx = random.randint(0, len(grid) - 1)
        randy = random.randint(0, len(grid[0]) - 1)
        while grid[randx][randy] == 1:
            randx = random.randint(0, len(grid) - 1)
            randy = random.randint(0, len(grid[0]) - 1)
        unvisited.append([randx, randy])
        while len(unvisited) > 0:
            current = unvisited.popleft()
            new_grid[current[0]][current[1]] = 0
            for k in range(-1, 2):
                for l_ in range(-1, 2):
                    if 0 <= current[0] + k < len(grid) and 0 <= current[1] + l_ < len(grid[0]):  # if we're not out of bounds
                        if copy_grid[current[0] + k][current[1] + l_] == 0:  # if it's an empty space
                            copy_grid[current[0] + k][current[1] + l_] = 2  # mark visited
                            open_count += 1
                            unvisited.append([current[0] + k, current[1] + l_])
        percentage = open_count * 100 / (len(grid) * len(grid[0]))

    return new_grid, percentage


def generate(*, width: int, height: int, iterations: int):
    chance = 40
    count = 5
    flood_tries = 5
    goal_percentage = 30  # above 30% seems to be a good target

    grid = make_grid(width, height)

    grid = populate_grid(grid, chance)

    for i in range(iterations):
        grid = automate_iteration(grid, count, 0)

    grid, percentage = flood_find_empty(grid, flood_tries, goal_percentage)
    exit_side = random.randint(1, 4)
    player_coords = [0, 0]

    def check_for_valid_pos(coords: list) -> bool:
        values = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                try:
                    values.append(grid[coords[0]+i][coords[1]+j] == 0)
                except IndexError:
                    pass
        return False not in values

    match exit_side:
        case 1:  # left, right
            starting_coords = [0, random.randint(10, len(grid) - 20)]
            for i in range(3):
                for y in range(starting_coords[1], starting_coords[1] + 10):
                    grid[starting_coords[0] + i][y] = 2
            while not check_for_valid_pos(player_coords):
                player_coords = [random.randint(len(grid[0]) // 2, len(grid[0]) - 1), random.randint(0, len(grid) - 1)]
        case 2:  # right, left
            starting_coords = [len(grid[0]) - 1, random.randint(10, len(grid) - 20)]
            for i in range(3):
                for y in range(starting_coords[1], starting_coords[1] + 10):
                    grid[starting_coords[0] - i][y] = 2
            while not check_for_valid_pos(player_coords):
                player_coords = [random.randint(0, len(grid[0]) // 2), random.randint(0, len(grid) - 1)]
        case 3:  # top, bottom
            starting_coords = [random.randint(10, len(grid[0]) - 20), 0]
            for i in range(3):
                for x in range(starting_coords[0], starting_coords[0] + 10):
                    grid[x][starting_coords[1] + i] = 2
            while not check_for_valid_pos(player_coords):
                player_coords = [random.randint(0, len(grid[0]) - 1), random.randint(len(grid) // 2, len(grid) - 1)]
        case 4:  # bottom, top
            starting_coords = [random.randint(10, len(grid[0]) - 20), len(grid) - 1]
            for i in range(3):
                for x in range(starting_coords[0], starting_coords[0] + 10):
                    grid[x][starting_coords[1] - i] = 2
            while not check_for_valid_pos(player_coords):
                player_coords = [random.randint(0, len(grid[0]) - 1), random.randint(0, len(grid) // 2)]

    grid[player_coords[0]][player_coords[1]] = 3

    coords_list = []
    while len(coords_list) != random.randint(30, 40):
        coords = [0, 0]
        while not check_for_valid_pos(coords):
            coords = [random.randint(0, len(grid[0])-1), random.randint(0, len(grid)-1)]
        if coords not in coords_list and coords != player_coords:
            coords_list.append(coords)

    for coords in coords_list:
        grid[coords[0]][coords[1]] = 4

    return player_coords, grid


def draw_small(grid, n, m, user_id):
    color_map = {
        0: (0, 0, 0),  # Black
        1: (255, 255, 255),  # White
        2: (255, 255, 0),  # Yellow
        3: (0, 50, 250),  # Blue
        4: (250, 50, 0)  # Red
    }
    img = Image.new('RGB', (10*n, 10*m))
    pixels = img.load()
    for i in range(n):
        for j in range(m):
            for l_ in range(10):
                for k_ in range(10):
                    rgb_color = color_map.get(grid[i][j], (0, 0, 0))
                    pixels[10*i+l_, 10*j+k_] = rgb_color
    img.save(f'maze_game/data/temp_files/temp_maze_{user_id}.png')
