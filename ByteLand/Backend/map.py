from utils import *

class GameMap:
    def __init__(self, width, height, tile_size):
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.map_data = [[0 for _ in range(width)] for _ in range(height)]

    def set_tile(self, x, y, tile_value):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.map_data[y][x] = tile_value

    def get_tile(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.map_data[y][x]
        else:
            return None

    def get_nearby_tiles(self, x, y, vision_radius):
        nearby_tiles = []
        for i in range(x - vision_radius, x + vision_radius + 1):
            for j in range(y - vision_radius, y + vision_radius + 1):
                if 0 <= i < self.width and 0 <= j < self.height:
                    nearby_tiles.append((i, j))
        return nearby_tiles

    def set_event(self, x, y, event):
        if 0 <= x < self.width and 0 <= y < self.height:
            # You can store events in a dictionary where the key is the tile coordinates (x, y)
            # and the value is a list of events.
            if (x, y) not in self.events:
                self.events[(x, y)] = [event]
            else:
                self.events[(x, y)].append(event)

    def remove_event(self, x, y, event):
        if (x, y) in self.events and event in self.events[(x, y)]:
            self.events[(x, y)].remove(event)

    def get_events(self, x, y):
        return self.events.get((x, y), [])

    def set_boundaries(self):
            for y in range(self.height):
                for x in range(self.width):
                    if x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1:
                        self.map_data[y][x] = '#'
                    else:
                        self.map_data[y][x] = ' '
            self.map_data[tavern[0]][tavern[1]] = '#'
            self.map_data[towncenter[0]][towncenter[1]] = '#'
            self.map_data[blacksmith[0]][blacksmith[1]] = '#'
            self.map_data[wizard_house[0]][wizard_house[1]] = '#'
            self.map_data[jester_theatre[0]][jester_theatre[1]] = '#'
            self.map_data[gabe_house[0]][gabe_house[1]] = '#'
            self.map_data[miles_house[0]][miles_house[1]] = '#'

    def print_map(self):
        self.set_boundaries()
        for row in self.map_data:
            print(" ".join(map(str, row)))

