from map import *
from navigation import *
from general import *

game_map = GameMap(MAP_WIDTH, MAP_HEIGHT, TILE_SIZE)

game_map.print_map()

collision_map = CollisionMap(game_map.map_data, COLLISION_CHAR)

run_command(gabe, command, variable, collision_map)

start_coords = (1, 1)
end_coords = (4, 5)

path = collision_map.find_path(start_coords, end_coords)
print(path)

print_maze_with_path(game_map.map_data, path)

