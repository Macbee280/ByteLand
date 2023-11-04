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
