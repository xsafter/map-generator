import random
from collections import deque

from PIL import Image


def print_grid(grid, n: int, m: int):
    img = Image.new('1', (n, m))
    pixels = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            pixels[i, j] = grid[i][j]
    img.save('maze.png')


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


def automata_iteration(grid, min_count, make_pillars):
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
                    if 0 <= current[0] + k < len(grid) and 0 <= current[1] + l_ < len(grid[0]):
                        if copy_grid[current[0] + k][current[1] + l_] == 0:
                            copy_grid[current[0] + k][current[1] + l_] = 2
                            open_count += 1
                            unvisited.append([current[0] + k, current[1] + l_])
        percentage = open_count * 100 / (len(grid) * len(grid[0]))

    return new_grid, percentage


def main():
    width = 100
    height = 100
    iterations = 2
    chance = 40
    count = 5
    flood_tries = 5
    goal_percentage = 30

    grid = make_grid(width, height)

    grid = populate_grid(grid, chance)

    for i in range(iterations):
        grid = automata_iteration(grid, count, 0)

    grid, percentage = flood_find_empty(grid, flood_tries, goal_percentage)

    print_grid(grid, width, height)


def generate(width: int, height: int, iterations: int):
    chance = 40
    count = 5
    flood_tries = 5
    goal_percentage = 30

    grid = make_grid(width, height)

    grid = populate_grid(grid, chance)

    for i in range(iterations):
        grid = automata_iteration(grid, count, 0)

    grid, percentage = flood_find_empty(grid, flood_tries, goal_percentage)

    print_grid(grid, width, height)


if __name__ == "__main__":
    main()
