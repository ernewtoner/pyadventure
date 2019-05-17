from colors import *
import world
from enum import Enum

class direction(Enum):
    NORTH = 1
    SOUTH = 2
    EAST = 3
    WEST = 4

def unpack(list_of_strings):
    return "\n".join(string for string in list_of_strings)

class Room:
    """ A single room's attributes """
    def __init__(self, id, name, description, exits, objects):
        self.id = id
        self.name = name
        self.description = description
        self.exits = exits # Dictionary of exits in the format {'north' : (room_id, "Room Name") } 
        self.objects = objects

    def __repr__(self):
        return (
            f"{WHITE}{self.name}{ENDC}\n"
            f"{self.description}\n" 
            f"Exits: [ {str(*self.exits)} ]\n"
            f"{LCYAN}{unpack(self.objects)}{ENDC}\n"
        )

    def get_id(self): 
        return self.id

    def get_exits(self):
        return self.exits
        
    def enter(self):
        pass

class Player:
    def __init__(self, name, current_room):
        self.name = name
        self.current_room = current_room

    def get_current_room_id(self):
        return self.current_room.get_id()
    
    def move(self, dir):
        current_room_exits = self.current_room.get_exits()

        if dir == direction.NORTH:
            if 'north' in current_room_exits:
                new_room_id = current_room_exits['north'][0]
                self.current_room = world.world_state[new_room_id]
            else:
                print("You can't go that direction!")
        elif dir == direction.SOUTH:
            if 'south' in current_room_exits:
                new_room_id = current_room_exits['south'][0]
                self.current_room = world.world_state[new_room_id]
            else:
                print("You can't go that direction!")
        elif dir == direction.EAST:
            if 'east' in current_room_exits:
                new_room_id = current_room_exits['east'][0]
                self.current_room = world.world_state[new_room_id]
            else:
                print("You can't go that direction!")
        elif dir == direction.WEST:
            if 'west' in current_room_exits:
                new_room_id = current_room_exits['west'][0]
                self.current_room = world.world_state[new_room_id]
            else:
                print("You can't go that direction!")
      
class Item:
    def __init__(self, name, description, weight):
        pass