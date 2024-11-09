import pygame
import math
from queue import PriorityQueue
import random
import timeit
import matplotlib.pyplot as plt

CLOSED = (227, 148, 155)
GOAL = (232, 184, 132)
PATH = (88, 219, 127)
OPEN = (237, 233, 126)
CLEAN = (255, 255, 255)
OBSTACLES = (0, 0, 0)
START = (165, 232, 185)
LINES = (128, 128, 128)

class node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = CLEAN
        self.adjacents = []
        self.width = width
        self.total_rows = total_rows

    def reset(self):
        self.color = CLEAN

    def set_start(self):
        self.color = START

    def set_closed(self):
        self.color = CLOSED

    def set_open(self):
        self.color = OPEN

    def set_obtacle(self):
        self.color = OBSTACLES

    def set_goal(self):
        self.color = GOAL

    def set_path(self):
        self.color = PATH

    def get_pos(self):
        x = self.row
        y = self.col
        return x, y

    def is_closed(self):
        return self.color == CLOSED

    def is_open(self):
        return self.color == OPEN

    def is_path(self):
        return self.color == PATH

    def is_obstacle(self):
        return self.color == OBSTACLES

    def is_start(self):
        return self.color == START

    def is_end(self):
        return self.color == GOAL

    def init_map(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
        font_size = int(self.width / 4)
        if self.is_start():
            font = pygame.font.SysFont('georgia', font_size)
            text = font.render("START", True, OBSTACLES)
            text_rect = text.get_rect(center=(self.x + self.width / 2, self.y + self.width / 2))
            win.blit(text, text_rect)
        elif self.is_end():
            font = pygame.font.SysFont('georgia', font_size)
            text = font.render("END", True, OBSTACLES)
            text_rect = text.get_rect(center=(self.x + self.width / 2, self.y + self.width / 2))
            win.blit(text, text_rect)
        else:
            font = pygame.font.SysFont('leelawadeeui', font_size)
            if self.is_obstacle():
                text = font.render(f"({self.row}, {self.col})", True, CLEAN)
            else:
                text = font.render(f"({self.row}, {self.col})", True, OBSTACLES)

            text_rect = text.get_rect(center=(self.x + self.width / 2, self.y + self.width / 2))
            win.blit(text, text_rect)

    def adjacent(self, grid):
        self.adjacents = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                row = self.row + i
                col = self.col + j
                if 0 <= row < self.total_rows and 0 <= col < self.total_rows and not grid[row][col].is_obstacle():
                    self.adjacents.append(grid[row][col])

    def __lt__(self, other):
        return False

def heuristic(p1, p2):  # Euclidean
    x1, y1 = p1
    x2, y2 = p2
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    return math.sqrt(dx**2 + dy**2)

def path(previous_nodes, current, start):
    path = []
    while current in previous_nodes:
        path.append(current)
        current = previous_nodes[current]
    path.append(start)
    path_cost = sum([math.sqrt(2) if abs(path[i].row - path[i - 1].row) == 1 and abs(path[i].col - path[i - 1].col) == 1 else 1 for i in range(1, len(path))])
    path.reverse()
    for cell in path:
        cell.set_path()
    print([cell.get_pos() for cell in path])
    print("Path cost: {:.5f}".format(path_cost))
    return path

def A_star(grid, start, end):
    counter = 0
    open_queue = PriorityQueue()
    open_queue.put((0, counter, start))
    previous_nodes = {}
    open_list = {start}
    g_score = {tnode: float("inf") for row in grid for tnode in row}
    g_score[start] = 0
    f_score = {tnode: float("inf") for row in grid for tnode in row}
    f_score[start] = 0

    while not open_queue.empty():
        on_going = open_queue.get()[2]
        open_list.remove(on_going)

        if on_going == end:
            path(previous_nodes, end, start)
            start.set_start()
            end.set_goal()
            return True

        if on_going != start:
            on_going.set_closed()

        for neighbor in on_going.adjacents:
            if neighbor.row == on_going.row or neighbor.col == on_going.col:
                temp_g_score = g_score[on_going] + 1
            else:
                temp_g_score = g_score[on_going] + math.sqrt(2)

            if temp_g_score < g_score[neighbor]:
                previous_nodes[neighbor] = on_going
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_list:
                    counter += 1
                    open_queue.put((f_score[neighbor], counter, neighbor))
                    open_list.add(neighbor)
                    neighbor.set_open()

    if open_queue.empty():
        print("Path does not exist !")
        return False

def map(rows, width, obstacles_percentage):
    grid = []
    gap = width // rows
    num_cells = rows ** 2
    num_obstacles = int(num_cells * obstacles_percentage)
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            tnode = node(i, j, gap, rows)
            grid[i].append(tnode)

    start = grid[1][1]
    end = grid[rows-2][rows-2]

    start.set_start()
    end.set_goal()

    for i in range(num_obstacles):
        while True:
            row = random.randint(0, rows - 1)
            col = random.randint(0, rows - 1)
            tnode = grid[row][col]
            if tnode != start and tnode != end and not tnode.is_obstacle():
                tnode.set_obtacle()
                break

    return grid, start, end

def matrix(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, LINES, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, LINES, (j * gap, 0), (j * gap, width))

def produce(win, grid, rows, width):
    win.fill(CLEAN)
    for row in grid:
        for tnode in row:
            tnode.init_map(win)
    matrix(win, rows, width)
    pygame.display.update()

def run_tests():
    results = {}
    for obstacles in range(10, 100, 10):
        times = []
        for _ in range(20):
            grid, start, end = map(100, 600, obstacles / 100)
            for row in grid:
                for tnode in row:
                    tnode.adjacent(grid)
            start_time = timeit.default_timer()
            A_star(grid, start, end)
            end_time = timeit.default_timer()
            times.append(end_time - start_time)
        results[obstacles] = {
            'average': sum(times) / len(times),
            'worst': max(times),
            'best': min(times)
        }
    return results

def main():
    pygame.init()
    WINDOW_SIZE = 600
    WINDOW = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("A* Path Finding (Robot)")

    results = run_tests()
    for obstacles, data in results.items():
        print(f"Obstacles: {obstacles}% - Average: {data['average']*1000:.2f} ms, Worst: {data['worst']*1000:.2f} ms, Best: {data['best']*1000:.2f} ms")

    obstacle_percentages = list(results.keys())
    average_times = [data['average']*1000 for data in results.values()]
    worst_times = [data['worst']*1000 for data in results.values()]
    best_times = [data['best']*1000 for data in results.values()]

    plt.plot(obstacle_percentages, average_times, label='Average Time')
    plt.plot(obstacle_percentages, worst_times, label='Worst Time')
    plt.plot(obstacle_percentages, best_times, label='Best Time')
    plt.xlabel('Percentage of Obstacles')
    plt.ylabel('Time (ms)')
    plt.title('A* Performance with Varying Obstacles')
    plt.legend()
    plt.show()

    # Displaying GUI for specific cases
    for obstacles in [20, 50, 80]:
        grid, start, end = map(20, 600, obstacles / 100)
        for row in grid:
            for tnode in row:
                tnode.adjacent(grid)
        A_star(grid, start, end)
        produce(WINDOW, grid, 20, 600)
        pygame.time.wait(2000)  # Display each case for 2 seconds

        selected_obstacles = int(input("Enter the percentage of obstacles for the path you want to visualize: "))

    grid, start, end = map(100, 600, selected_obstacles / 100)
    for row in grid:
        for tnode in row:
            tnode.adjacent(grid)

    # Find the path using A*
    A_star(grid, start, end)

    # Visualize the path on GUI
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        produce(WINDOW, grid, 100, 600)
        pygame.display.update()

main()