import turtle
import heapq

# Constants
CELL_SIZE = 20  # Size of each cell in the grid
START_POS = (-160, 160)  # Starting position on the screen
GOAL_POS = (140, -140)  # Goal position on the screen
GRID_SIZE = 15  # Size of the grid (15x15)
MOVE_SPEED = 2  # Turtle movement speed (modified)

class Node:
    def __init__(self, x, y):
        self.x = x  # X-coordinate of the node
        self.y = y  # Y-coordinate of the node
        self.g = float('inf')  # Distance from start node
        self.h = float('inf')  # Distance to end node
        self.parent = None  # Parent node

    def __lt__(self, other):
        # Comparison function for priority queue (min-heap)
        return (self.g + self.h) < (other.g + other.h)

    def __eq__(self, other):
        # Equality check based on coordinates
        return (self.x == other.x) and (self.y == other.y)

    def __hash__(self):
        # Hash function for using Node in sets and dictionaries
        return hash((self.x, self.y))

def euclidean_distance(node1, node2):
    # Calculate Euclidean distance between two nodes
    return ((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2) ** 0.5

def astar(start, goal, grid):
    open_list = []
    closed_set = set()

    heapq.heappush(open_list, start)
    start.g = 0  # Distance from start node to itself is 0
    start.h = euclidean_distance(start, goal)  # Initial heuristic

    while open_list:
        current = heapq.heappop(open_list)  # Get the node with the lowest cost

        if current == goal:
            # Reconstruct the path if goal is reached
            path = []
            while current:
                path.append((current.x, current.y))
                current = current.parent
            return path[::-1]  # Return reversed path

        closed_set.add(current)  # Mark current node as visited

        # Explore neighbors (right, left, down, up)
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_x, new_y = current.x + dx, current.y + dy
            if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE and grid[new_x][new_y] != 1:
                neighbor = Node(new_x, new_y)
                if neighbor in closed_set:
                    continue
                tentative_g = current.g + 1  # Assuming each step cost is 1
                if tentative_g < neighbor.g:
                    neighbor.parent = current
                    neighbor.g = tentative_g
                    neighbor.h = euclidean_distance(neighbor, goal)
                    if neighbor not in open_list:
                        heapq.heappush(open_list, neighbor)

    return None  # No path found

def draw_path(path):
    for x, y in path:
        turtle.goto(START_POS[0] + (x + 0.5) * CELL_SIZE, START_POS[1] - (y + 0.5) * CELL_SIZE)
        turtle.dot(10)  # Draw a dot at each path node

def main():
    # Initialize screen
    screen = turtle.Screen()
    screen.setup(600, 600)
    screen.bgcolor("lightblue")  # Modified background color

    # Initialize turtle
    turtle.shape("turtle")  # Modified shape
    turtle.color("green")  # Modified color
    turtle.penup()

    # Initialize start and goal nodes
    start_node = Node(0, 0)
    goal_node = Node(GRID_SIZE - 1, GRID_SIZE - 1)

    # Initialize maze (0: free space, 1: obstacle)
    maze = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    # Adding more obstacles for challenge
    obstacles = [
        (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6),
        (7, 8), (8, 8), (9, 8), (10, 8),
        (12, 3), (12, 4), (12, 5), (12, 6), (12, 7)
    ]
    for (x, y) in obstacles:
        maze[x][y] = 1

    # Find path using A* algorithm
    path = astar(start_node, goal_node, maze)

    # Draw the path if found
    if path:
        turtle.speed(MOVE_SPEED)
        turtle.goto(START_POS[0] + 0.5 * CELL_SIZE, START_POS[1] - 0.5 * CELL_SIZE)
        turtle.pendown()
        draw_path(path)
        turtle.penup()
        turtle.goto(GOAL_POS)
        turtle.dot(10)  # Mark the goal

    turtle.done()

if __name__ == "__main__":
    main()
