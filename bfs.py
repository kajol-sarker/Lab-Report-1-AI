from collections import deque

class Node:
    def __init__(self, x, y, level):
        self.x = x  
        self.y = y  
        self.level = level

class BFS:
    def __init__(self, grid, start, goal):
        self.directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Movement directions
        self.found = False 
        self.goal_level = 0 
        self.N = len(grid)  
        self.grid = [row[:] for row in grid] 
        self.source = Node(start[0], start[1], 0) 
        self.goal = Node(goal[0], goal[1], float('inf')) 
        self.parents = {} 
        self.visited = set() 

    def st_bfs(self):
        queue = deque()
        queue.append(self.source)
        self.parents[(self.source.x, self.source.y)] = None  # Start node has no parent
        self.visited.add((self.source.x, self.source.y))  # Mark start node as visited

        while queue:
            u = queue.popleft() 

            for dx, dy in self.directions:
                v_x, v_y = u.x + dx, u.y + dy

                if 0 <= v_x < self.N and 0 <= v_y < self.N and self.grid[v_x][v_y] == 0 and (v_x, v_y) not in self.visited:
                    v_level = u.level + 1  # Increment level

                    if v_x == self.goal.x and v_y == self.goal.y:
                        self.found = True
                        self.goal_level = v_level
                        self.goal.level = v_level
                        self.parents[(v_x, v_y)] = (u.x, u.y)
                        return

                    self.visited.add((v_x, v_y))  # Mark node as visited
                    child = Node(v_x, v_y, v_level)
                    queue.append(child)
                    self.parents[(v_x, v_y)] = (u.x, u.y)

    def reconstruct_path(self):
        """ Reconstructs the path from goal to start using the parent dictionary """
        if not self.found:
            return []

        path = []
        current = (self.goal.x, self.goal.y)

        while current is not None:
            path.append(current)
            current = self.parents.get(current)

        return path[::-1]  

    def print_grid(self, path):
        grid_copy = [row[:] for row in self.grid] 
        path_set = set(path)

        for i in range(len(grid_copy)):
            for j in range(len(grid_copy[0])):
                if (i, j) in path_set:
                    print('*', end=' ')
                elif grid_copy[i][j] == 1:
                    print('#', end=' ')  # Obstacle
                else:
                    print('.', end=' ')  # Open space
            print()

def get_user_input():
    N = int(input("Enter grid size (N x N): "))

    # Initialize grid
    grid = []
    print(f"Enter the grid row-wise ({N}x{N}) with 0 for open space & 1 for obstacles:")
    for _ in range(N):
        row = list(map(int, input().split()))
        grid.append(row)

    start_x, start_y = map(int, input("Enter start position (row column): ").split())
    goal_x, goal_y = map(int, input("Enter goal position (row column): ").split())

    return grid, (start_x, start_y), (goal_x, goal_y)

if __name__ == "__main__":
    grid, start, goal = get_user_input()
    bfs = BFS(grid, start, goal)
    bfs.st_bfs()

    if bfs.found:
        print("\nGoal found")
        print("Number of moves required =", bfs.goal_level)
        path = bfs.reconstruct_path()
        print("Path Traversed by Robot:", path)
        print("\nGrid with Path:")
        bfs.print_grid(path)
    else:
        print("Goal cannot be reached from starting block")
