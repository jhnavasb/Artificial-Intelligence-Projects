import argparse
from collections import defaultdict, deque
from queue import PriorityQueue

import numpy as np
import pygame

width = 30
height = 30
block_size = 20

Color = [[255, 255, 255], [0, 0, 0], [224, 224, 224], [128, 128, 128], [64, 64, 64], [255, 0, 0], [255, 96, 208],
         [160, 32, 255], [80, 208, 255], [0, 32, 255], [96, 255, 128], [0, 192, 0], [255, 224, 32], [255, 160, 16]]

'''
White = (255,255,255)
Black = (0,0,0)
LightGray = (224,224,224)
Gray = (128,128,128)
DarkGray = (64,64,64)
Red = (255,0,0)
Pink = (255,96,208)
Purple = (160,32,255)
LightBlue = (80,208,255)
Blue = (0,32,255)
LightGreen = (96,255,128)
Green = (0,192,0)
Yellow = (255,224,32)
Orange = (255,160,16)
'''


def read():
    box = np.loadtxt("maze.txt", dtype='i', delimiter=',')
    costs = np.loadtxt("maze_cost.txt", dtype='i', delimiter=',')
    return box, costs


def states(maze, costs):
    status = defaultdict(list)

    for node in {(i, j): [] for j in range(width) for i in range(height) if not maze[i][j]}:
        x, y = node
        if x < height - 1 and not maze[x + 1][y]:
            status[(x, y)].append(("S", (x + 1, y), costs[x + 1, y]))
            status[(x + 1, y)].append(("N", (x, y), costs[x, y]))
        if y < width - 1 and not maze[x][y + 1]:
            status[(x, y)].append(("E", (x, y + 1), costs[x, y + 1]))
            status[(x, y + 1)].append(("W", (x, y), costs[x, y]))
    return status


def DFS(status, screen, start, goal, c1):
    stack, visited = deque([(0, [start], start, "")]), set()

    while stack:
        cost, path, current, actions = stack.pop()
        if current not in visited:
            visited.add(current)
            color_explored(current, screen, c1)
            if current == goal:
                return path, actions, cost, visited.__len__()
            for direction, neighbour, costv in status[current]:
                if neighbour not in visited:
                    stack.append((cost + costv, path + [neighbour, ], neighbour, actions + direction))


def BFS(status, screen, start, goal, c1):
    queue, visited = deque([(0, [start], start, "")]), set()

    while queue:
        cost, path, current, actions = queue.popleft()
        if current not in visited:
            visited.add(current)
            color_explored(current, screen, c1)
            if current == goal:
                return path, actions, cost, visited.__len__()
            for direction, neighbour, costv in status[current]:
                if neighbour not in visited:
                    queue.append((cost + costv, path + [neighbour, ], neighbour, actions + direction))


def UCS(status, screen, start, goal, c1):
    queue, visited = PriorityQueue(), set()
    queue.put((0, [start], start, ""))

    while queue:
        cost, path, current, actions = queue.get()
        if current not in visited:
            visited.add(current)
            color_explored(current, screen, c1)
            if current == goal:
                return path, actions, cost, visited.__len__()
            for direction, neighbour, costv in status[current]:
                if neighbour not in visited:
                    queue.put((cost + costv, path + [neighbour, ], neighbour, actions + direction))


def color_explored(current, screen, c1):
    # pygame.time.wait(100)
    #time.sleep(0.005)
    pygame.draw.rect(screen, Color[c1 + 1],
                     ((current[1] * 20) + 1, (current[0] * 20) + 1, block_size - 1, block_size - 1))
    pygame.display.flip()


def start_goal(start, goal, screen):
    pygame.draw.rect(screen, Color[5], ((start[1] * 20) + 1, (start[0] * 20) + 1, block_size - 1, block_size - 1))
    pygame.draw.rect(screen, Color[11], ((goal[1] * 20) + 1, (goal[0] * 20) + 1, block_size - 1, block_size - 1))
    pygame.display.flip()


def color_path(final, screen, c2):
    final = np.asarray(final)

    for i in range(0, len(final)):
        a = final[i]
        pygame.draw.rect(screen, Color[c2 + 1], ((a[1] * 20) + 1, (a[0] * 20) + 1, block_size - 1, block_size - 1))
        pygame.display.flip()


def draw_maze(screen, box):
    for h in range(width):
        for w in range(height):
            pygame.draw.rect(screen, Color[box[h, w]], ((w * 20) + 1, (h * 20) + 1, block_size - 1, block_size - 1))
    pygame.display.flip()


def search(s, start, goal, c1, c2, box, costs):
    screen = pygame.display.set_mode((width * block_size, height * block_size))
    pygame.display.set_caption("Maze Runner")
    screen.fill(Color[1])

    switcher = {
        "dfs": DFS,
        "bfs": BFS,
        "ucs": UCS,
    }
    func = switcher.get(s, lambda: "Invalid Arguments")

    draw_maze(screen, box)
    status = states(box, costs)

    start_goal(start, goal, screen)
    start_time = pygame.time.get_ticks()
    final_path, final_actions, final_cost, explored = func(status, screen, start, goal, c1)
    time_search = pygame.time.get_ticks() - start_time
    color_path(final_path, screen, c2)
    start_goal(start, goal, screen)

    print("The sequence of actions for the solution is: \n", list(final_actions))
    print("The amount of explored states is: ", explored)
    print("The cost of the path is: ", final_cost)
    print("The elapse time until a solution was found, is: ", time_search / 1000, "s")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--type", required=True,
                    help="could be: standard or custom")
    ap.add_argument("-s", "--search", required=True,
                    help="could be: dfs, bfs or ucs")
    ap.add_argument("-r", "--start", default=0,
                    help="start point, i.e. 0,1 . If the start point is invalid, the standard start point will be used instead")
    ap.add_argument("-g", "--goal", default=0,
                    help="goal point, i.e. 28,29 . If the goal point is invalid, the standard goal point will be used instead")
    ap.add_argument("-f", "--color_1", type=int, default=0,
                    help="the color of the visited nodes, could be: LightGray (1), Gray (2), DarkGray (3), Red (4)"
                         "Pink (5), Purple (6), LightBlue (7), Blue (8), LightGreen (9), Green (10), Yellow (11), "
                         "Orange (12)")
    ap.add_argument("-p", "--color_2", type=int, default=0,
                    help="the color of the path, could be: LightGray (1), Gray (2), DarkGray (3), Red (4)"
                         "Pink (5), Purple (6), LightBlue (7), Blue (8), LightGreen (9), Green (10), Yellow (11), "
                         "Orange (12)")
    arg = ap.parse_args()
    args = vars(arg)

    k, c1, c2 = 0, 8, 11
    if arg.type == "custom" and (arg.start or arg.goal or arg.color_1 or arg.color_2) is None:
        ap.error("--type: custom requires --start --goal --color_1 --color_2.")

    if arg.type == "custom":
        k = 1
        if arg.color_1 < 1 or arg.color_1 > 12:
            ap.error("--color_1: invalid arguments.")
        else:
            c1 = args["color_1"]
        if arg.color_2 < 1 or arg.color_2 > 12:
            ap.error("--color_2: invalid arguments.")
        else:
            c2 = args["color_2"]

    pygame.init()

    box, costs = read()
    start = [0, 1]
    goal = [28, 29]

    if k == 1:
        start[0], start[1] = map(int, args["start"].split(","))
        goal[0], goal[1] = map(int, args["goal"].split(","))

    if box[start[0], start[1]] == 1:
        start = (0, 1)
    else:
        start = (start[0], start[1])

    if box[goal[0], goal[1]] == 1:
        goal = (28, 29)
    else:
        goal = (goal[0], goal[1])

    search(args["search"], start, goal, c1, c2, box, costs)

    ok = True
    clock = pygame.time.Clock()

    while ok:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ok = False

    pygame.quit()


if __name__ == "__main__":
    main()
