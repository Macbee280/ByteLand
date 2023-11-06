""" navigation.py

File containing the Entity Pathfinding functionality

"""

def print_maze(maze):
    for row in maze:
        for item in row:
            print(item, end='')
        print()

def path_finder(maze, start, end, collision_block_char, verbose=False):
    def prepare_maze(maze, start, end):
        maze[start[0]][start[1]] = "S"
        maze[end[0]][end[1]] = "E"
        return maze

    def find_start(maze):
        for row in range(len(maze)):
            for col in range(len(maze[0])):
                if maze[row][col] == 'S':
                    return row, col

    def is_valid_position(maze, pos_r, pos_c):
        if pos_r < 0 or pos_c < 0:
            return False
        if pos_r >= len(maze) or pos_c >= len(maze[0]):
            return False
        if maze[pos_r][pos_c] in ' E':
            return True
        return False

    def solve_maze(maze, start, verbose=False):
        path = []
        stack = []
        stack.append(start)
        while len(stack) > 0:
            pos_r, pos_c = stack.pop()
            if verbose:
                print("Current position", pos_r, pos_c)
            if maze[pos_r][pos_c] == 'E':
                path += [(pos_r, pos_c)]
                return path
            if maze[pos_r][pos_c] == 'X':
                continue
            maze[pos_r][pos_c] = 'X'
            path += [(pos_r, pos_c)]
            if is_valid_position(maze, pos_r - 1, pos_c):
                stack.append((pos_r - 1, pos_c))
            if is_valid_position(maze, pos_r + 1, pos_c):
                stack.append((pos_r + 1, pos_c))
            if is_valid_position(maze, pos_r, pos_c - 1):
                stack.append((pos_r, pos_c - 1))
            if is_valid_position(maze, pos_r, pos_c + 1):
                stack.append((pos_r, pos_c + 1))
            if verbose:
                print('Stack:', stack)
                print_maze(maze)
        return False

    new_maze = []
    for row in maze:
        new_row = []
        for j in row:
            if j == collision_block_char:
                new_row += ["#"]
            else:
                new_row += [" "]
        new_maze += [new_row]

    maze = new_maze
    maze = prepare_maze(maze, start, end)
    start = find_start(maze)
    path = solve_maze(maze, start, verbose)
    return path

def print_maze_with_path(maze, path):
    path_set = set(path)  # Convert the path list into a set for faster membership checks
    for row_index, row in enumerate(maze):
        for col_index, item in enumerate(row):
            if (row_index, col_index) in path_set:
                print('*', end='')  # Print '*' to highlight the path
            else:
                print(item, end='')
        print()

class CollisionMap:
    """ CollisionMap()

    Class which controls the pathfinding of entities on the map

    """
    def __init__(self, maze, collision_block_char):
        self.maze = maze
        self.collision_block_char = collision_block_char

    def find_path(self, start, end):
        pathfinding_maze = self.convert_to_pathfinding_format()
        path = path_finder(pathfinding_maze, start, end, self.collision_block_char)
        return path

    def convert_to_pathfinding_format(self):
        pathfinding_maze = []
        for row in self.maze:
            pathfinding_row = []
            for cell in row:
                if cell == self.collision_block_char:
                    pathfinding_row.append("#")
                else:
                    pathfinding_row.append(" ")
            pathfinding_maze.append(pathfinding_row)
        return pathfinding_maze
