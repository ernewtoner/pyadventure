from colors import *
from enum import Enum

class direction(Enum):
    north = 1
    south = 2   
    east = 3
    west = 4

class World:
    """ Wrapper to hold the state of all the rooms and objects in the world (world_state) """
    def __init__(self, world_state):
        self.world_state = world_state # Dictionary in the form { room_id: Room object}

# String helper function to split up items on seperate lines
def unpack(items):
    return "\n".join(str(item.display()) for item in items)

class Room:
    """ A single room's attributes """
    def __init__(self, id, name, long_desc, short_desc, exits, items):
        self.id = id
        self.name = name
        self.long_desc = long_desc
        self.short_desc = short_desc
        self.exits = exits # Dictionary of exits in the format {'north' : (room_id, "Room Name") } 
        self.items = items # Dictionary of Objects in {'key': Object} form

    def display(self, display_long_desc):
        if display_long_desc:
            desc = self.long_desc
        else:
            desc = self.short_desc

        print (
            f"{WHITE}{self.name}{ENDC}\n"
            f"{desc}\n" 
            f"Exits: [ {str(*self.exits)} ]\n"
            f"{unpack(self.items.values())}"
        )

    def get_id(self): 
        return self.id

    def get_exits(self):
        return self.exits

    def get_items(self):
        return self.items

    def add_item(self, item):
        self.items[item.get_key()] = item

    def remove_item(self, item_key):
        del self.items[item_key]

class Player:
    def __init__(self, name, current_room):
        self.name = name
        self.current_room = current_room
        self.visited_rooms = [current_room.get_id()] # List of visited room IDs
        self.inventory = []
        self.equipment = []

    def copy(self, name, current_room, inventory, equipment):
        self.name = name
        self.current_room = current_room
        self.inventory = inventory
        self.equipment = equipment
    
    def display(self):
        print (
            f"{WHITE}{self.name}{ENDC}\n"
            f"Current Room: {self.current_room.get_id()}\n"
            f"Inventory: {self.inventory}"
            f"Equipment: {self.equipment}"
        )

    def get_current_room_id(self):
        return self.current_room.get_id()
    
    def get_inventory(self):
        return self.inventory

    def get_equipment(self):
        return self.equipment
    
    # Returns true if move was successful, false if not
    def move(self, world, dir):
        current_room_exits = self.current_room.get_exits()
        display_long_desc = False

        if dir.name in current_room_exits:
            new_room_id = current_room_exits[dir.name][0]
            self.current_room = world.world_state[new_room_id]
            if new_room_id not in self.visited_rooms:
                display_long_desc = True
                self.visited_rooms.append(new_room_id)

            return True, display_long_desc
        else:
            print("You can't go that direction!")
            return False, False

    def display_inventory(self):
        print("-----Inventory----")
        for item in self.inventory:
            print(item.get_short_desc())
        print()

    def display_equipment(self):
        print("-----Equipment----")
        for item in self.equipment:
            print(item.get_short_desc())
        print()

    def add_item_to_inventory(self, item):
        self.inventory.append(item)
    
    def remove_item_from_inventory(self, item):
        self.inventory.remove(item)

    def add_item_to_equipment(self, item):
        self.equipment.append(item)
    
    def remove_item_from_equipment(self, item):
        self.equipment.remove(item)


class Object:
    def __init__(self, key, room_id, ground_desc, short_desc, long_desc, takeable, keywords):
        self.key = key # The key is the unique identifier defined in the item's JSON file
        self.room_id = room_id # Room item is stored in (0 for inventory)
        self.ground_desc = ground_desc
        self.short_desc = short_desc
        self.long_desc = long_desc
        self.takeable = takeable # Either a 1 or 0
        self.keywords = keywords
    
    def get_key(self):
        return self.key

    def get_room_id(self):
        return self.room_id

    def get_keywords(self):
        return self.keywords
    
    def get_short_desc(self):
        return self.short_desc

    def get_long_desc(self):
        return self.long_desc

    def is_takeable(self):
        return self.takeable

    def display(self):
        return f"{LCYAN}{self.ground_desc}{ENDC}"