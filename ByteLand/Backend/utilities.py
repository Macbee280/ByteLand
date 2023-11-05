# utilities.py
def configure_opt(opt):
    # Map dimensions
    MAP_WIDTH = 13
    MAP_HEIGHT = 7
    TILE_SIZE = 1

    # Collision character
    COLLISION_CHAR = '#'

    # Coordinates
    COORDINATES = {
        'TAVERN': (2, 2),
        'TOWNSQUARE': (4, 2),
        'SMITHERY': (3, 6),
        'WIZARD_HOUSE': (4, 10),
        'JESTER_THEATRE': (2, 9),
        'GABE_HOUSE': (1, 7),
        'MARKET': (5, 4)
    }

    CHARACTERS = {
        'Ancient Aiden',
        'Galliant Gabe',
        'Magical Miles',
        'Ye Olde Izzy'
    }

    # Create the opt variable
    opt = {
        'map_width': MAP_WIDTH,
        'map_height': MAP_HEIGHT,
        'tile_size' : TILE_SIZE,
        'collision_char' : COLLISION_CHAR,
        'coordinates': COORDINATES,
        'characters' : CHARACTERS
    }

    return opt