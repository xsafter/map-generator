import sys
import random
from collections import deque
from PIL import Image


def printGrid(grid, n: int, m: int):
    img = Image.new('1', (n, m))
    pixels = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            pixels[i, j] = grid[i][j]
    img.save('maze.png')


def makeGrid(width, height):
    newgrid = [[0 for x in range(height)] for y in range(width)]
    for i in range(len(newgrid)):
        for j in range(len(newgrid[i])):
            if i == 0 or j == 0 or i == len(newgrid) - 1 or j == len(newgrid[0]) - 1:
                newgrid[i][j] = 1
    return newgrid


def populateGrid(grid, chance):
    for i in range(len(grid)):  # reminder to test with: for index, value in enumerate(grid)
        for j in range(len(grid[0])):
            if (random.randint(0, 100) <= chance):  # test with list comprehension instead??
                grid[i][j] = 1
    return grid


def automataIteration(grid, minCount, makePillars):
    new_grid = [row[:] for row in grid]
    for i in range(1, len(grid) - 1):
        for j in range(1, len(grid[0]) - 1):
            count = 0
            for k in range(-1, 2):
                for l in range(-1, 2):
                    if grid[i + k][j + l] == 1:
                        count += 1
            if count >= minCount or (count == 0 and makePillars == 1):
                new_grid[i][j] = 1
            else:
                new_grid[i][j] = 0
    return new_grid


def floodFindEmpty(grid, tries, goal):
    times_remade = 0
    percentage = 0

    while times_remade < tries and percentage < goal:
        copy_grid = [row[:] for row in grid]
        open_count = 0
        times_remade += 1
        unvisited = deque([])
        new_grid = [[1 for x in range(len(grid[0]))] for y in range(len(grid))]
        # find a random empty space, hope it's the biggest cave
        randx = random.randint(0, len(grid) - 1)
        randy = random.randint(0, len(grid[0]) - 1)
        while (grid[randx][randy] == 1):
            randx = random.randint(0, len(grid) - 1)
            randy = random.randint(0, len(grid[0]) - 1)
        unvisited.append([randx, randy])
        while len(unvisited) > 0:
            current = unvisited.popleft()
            new_grid[current[0]][current[1]] = 0
            for k in range(-1, 2):
                for l in range(-1, 2):
                    if current[0] + k >= 0 and current[0] + k < len(grid) and current[1] + l >= 0 and current[
                        1] + l < len(grid[0]):  # if we're not out of bounds
                        if copy_grid[current[0] + k][current[1] + l] == 0:  # if it's an empty space
                            copy_grid[current[0] + k][current[1] + l] = 2  # mark visited
                            open_count += 1
                            unvisited.append([current[0] + k, current[1] + l])
        percentage = open_count * 100 / (len(grid) * len(grid[0]))

    return new_grid, percentage


def main():
    #width = int(input("Enter the width: "))
    #height = int(input("Enter the height: "))
    # chance = 100 - int(input("Enter the percentage chance of randomly generating a wall: "))
    # count = int(input("Enter the min count of surrounding walls for the automata rules: "))
    width = 100
    height = 100
    iterations = 2
    chance = 40
    count = 5
    #iterations = int(input("Enter the number of regular iterations: "))
    #pillarIterations = int(input("Enter the number of pillar-generating iterations: "))
    floodTries = 5
    goalPercentage = 30  # above 30% seems to be a good target

    grid = makeGrid(width, height)

    grid = populateGrid(grid, chance)


    for i in range(iterations):
        grid = automataIteration(grid, count, 0)

    grid, percentage = floodFindEmpty(grid, floodTries, goalPercentage)

    # self reminder to try checking map size https://stackoverflow.com/questions/1331471/in-memory-size-of-a-python-structure

    print("")
    printGrid(grid, width, height)

def generate(width: int, height: int, iterations: int):

    chance = 40
    count = 5
    floodTries = 5
    goalPercentage = 30  # above 30% seems to be a good target

    grid = makeGrid(width, height)

    grid = populateGrid(grid, chance)

    for i in range(iterations):
        grid = automataIteration(grid, count, 0)

    grid, percentage = floodFindEmpty(grid, floodTries, goalPercentage)

    printGrid(grid, width, height)

if __name__ == "__main__":
    main()
