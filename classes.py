from colors import *
import world
from enum import Enum

class direction(Enum):
    north = 1
    south = 2
    east = 3
    west = 4

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

        if dir.name in current_room_exits:
            new_room_id = current_room_exits[dir.name][0]
            self.current_room = world.world_state[new_room_id]
        else:
            print("You can't go that direction!")
      
class Item:
    def __init__(self, name, description, weight):
        pass