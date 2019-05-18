from colors import *
from world_state import world_state
from enum import Enum

class direction(Enum):
    north = 1
    south = 2   
    east = 3
    west = 4

# String helper function to split up items on seperate lines
def unpack(items):
    return "\n".join(str(item) for item in items)

class Room:
    """ A single room's attributes """
    def __init__(self, id, name, description, exits, items):
        self.id = id
        self.name = name
        self.description = description
        self.exits = exits # Dictionary of exits in the format {'north' : (room_id, "Room Name") } 
        self.items = items # Dictionary of Items in {'key': Item} form

    def __repr__(self):
        return (
            f"{WHITE}{self.name}{ENDC}\n"
            f"{self.description}\n" 
            f"Exits: [ {str(*self.exits)} ]\n"
            f"{unpack(self.items.values())}"
        )

    def get_id(self): 
        return self.id

    def get_exits(self):
        return self.exits

    def get_items(self):
        return self.items

class Player:
    def __init__(self, name, current_room):
        self.name = name
        self.current_room = current_room
        self.inventory = []

    def get_current_room_id(self):
        return self.current_room.get_id()
    
    # Returns true if move was successful, false if not
    def move(self, dir):
        current_room_exits = self.current_room.get_exits()

        if dir.name in current_room_exits:
            new_room_id = current_room_exits[dir.name][0]
            self.current_room = world_state[new_room_id]
            return True
        else:
            print("You can't go that direction!")
            return False

class Item:
    def __init__(self, key, room_id, ground_desc, short_desc, long_desc, takeable, keywords):
        self.key = key # The key is the unique identifier defined in the item's JSON file
        self.room_id = room_id # Room item is stored in (0 for inventory)
        self.ground_desc = ground_desc
        self.short_desc = short_desc
        self.long_desc = long_desc
        self.takeable = takeable
        self.keywords = keywords
    
    def get_key(self):
        return self.key

    def get_room_id(self):
        return self.room_id

    def get_keywords(self):
        return self.keywords
    
    def get_long_desc(self):
        return self.long_desc

    def __repr__(self):
        return f"{LCYAN}{self.ground_desc}{ENDC}"