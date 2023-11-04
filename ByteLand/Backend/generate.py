from map import *
from navigation import *

width = 13
height = 7
tile_size = 1
game_map = GameMap(width, height, tile_size)

game_map.print_map()

collision_char = '#'  # Character representing collision blocks
collision_map = CollisionMap(game_map.map_data, collision_char)

start_coords = (1, 1)
end_coords = (4, 5)

path = collision_map.find_path(start_coords, end_coords)

print_maze_with_path(game_map.map_data, path)
