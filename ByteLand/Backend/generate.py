from map import *
from navigation import *

width = 13
height = 7
tile_size = 1
game_map = GameMap(width, height, tile_size)

game_map.print_map()

# for y in range(height):
#     for x in range(width):
#         if game_map[y][x] == ' ':
#             game_map.set_tile(x, y, 0)  # 0 represents an open space
#         else:
#             game_map.set_tile(x, y, 1)  # 1 represents a boundary/collision

# collision_char = 1  # Character representing collision blocks
# collision_map = CollisionMap(game_map.map_data, collision_char)

# start_coords = (0, 0)
# end_coords = (6, 12)

# path = collision_map.find_path(start_coords, end_coords)

# print_maze_with_path(game_map.map_data, path)
