import time
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
        self.timer = None # Possible Timer object

    def exit(self):
        if self.timer:
            self.timer.cancel()
        exit()

# String helper function to split up items on seperate lines
def unpack(items):
    return "\n".join(str(item.display()) for item in items)

class Room:
    """ A single room's attributes """
    def __init__(self, id, name, long_desc, short_desc, exits, items, npcs):
        self.id = id
        self.name = name
        self.long_desc = long_desc
        self.short_desc = short_desc
        self.exits = exits # Dictionary of exits in the format {'north' : (room_id, "Room Name") } 
        self.items = items # Dictionary of Objects in {'key': Object} form
        self.npcs = npcs

    def display(self, display_long_desc):
        if display_long_desc:
            desc = self.long_desc
        else:
            desc = self.short_desc

        print (
            f"{WHITE}{self.name}{ENDC}\n"
            f"{desc}\n" 
        )
        if len(self.exits) > 0:
            print("Exits: [", f"{', '.join(key for key in self.exits.keys())}", "]")
        else:
            print(f"Exits: [ none ]")

        if len(self.npcs) > 0:
            print(f"{unpack(self.npcs.values())}")
        
        print (f"{unpack(self.items.values())}")

    def get_id(self): 
        return self.id

    def get_exits(self):
        return self.exits

    def get_items(self):
        return self.items

    def get_npcs(self):
        return self.npcs

    def add_item(self, item):
        self.items[item.get_key()] = item

    def remove_item(self, item_key):
        del self.items[item_key]
    
    def remove_npc(self, npc_key):
        del self.npcs[npc_key]

class Player:
    def __init__(self, name, current_room):
        self.name = name
        self.current_room = current_room
        self.visited_rooms = [current_room.get_id()] # List of visited room IDs
        self.inventory = []
        self.equipment = []
        self.counter = 0 # Counter for calculating plain rooms
        self.fountain_trigger = 0 # Trigger if the player has bathed in the fountain
        self.endgame_trigger = 0 # Trigger if player has bathed in the fountain and eats the magical wafer

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
    
    def set_current_room(self, world, room_id):
        self.current_room = world.world_state[room_id]
        if room_id not in self.visited_rooms:
            display_long_desc = True # Flag for displaying long desc or not
            self.visited_rooms.append(room_id)
        else:
            display_long_desc = False
                

        return display_long_desc

    # Returns true if move was successful, false if not
    def move(self, world, dir):
        current_room_exits = self.current_room.get_exits()
        display_long_desc = False

        if dir.name in current_room_exits:
            old_room_id = self.get_current_room_id()
            # If direction is a valid exit, get new room id and set current room
            new_room_id = current_room_exits[dir.name][0]
            display_long_desc = self.set_current_room(world, new_room_id)

            if new_room_id == 3 and dir.name == 'north':
                self.counter += 1
            
            if self.counter >= 5:
                new_room_id = 4 # Escaping the plains
                display_long_desc = self.set_current_room(world, new_room_id)
                self.counter = 0

            if old_room_id == 4 and new_room_id == 2:
                print("What the? You scratch your head wondering how you got back here..\n")    

            return True, display_long_desc
        else:
            print("You can't go that direction!")
            return False, False

    def death(self, world):
        print("You are in excrutiating pain from your injuries!")
        time.sleep(3)
        print("You feel critically weak!")
        time.sleep(2)
        print("You have died.")
        world.exit()

    def sudden_death(self, world):
        print("You have died.")
        world.exit()

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
    def __init__(self, key, room_id, ground_desc, short_desc, long_desc, drink_desc, eat_desc, hit_desc, open_desc, talk_desc, 
                 takeable, equipable, enterable, openable, destination, npc, hidden, keywords):
        self.key = key # The key is the unique identifier defined in the item's JSON file
        self.room_id = room_id # Room item is stored in (0 for inventory)
        self.ground_desc = ground_desc
        self.short_desc = short_desc
        self.long_desc = long_desc
        self.drink_desc = drink_desc
        self.eat_desc = eat_desc
        self.hit_desc = hit_desc
        self.open_desc = open_desc  
        self.talk_desc = talk_desc
        self.takeable = takeable # Either a 1 or 0
        self.equipable = equipable
        self.enterable = enterable
        self.openable = openable
        self.destination = destination
        self.npc = npc # Is non-player character?
        self.hidden = hidden # Is object hidden?
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
        if self.hidden: # If hidden object, do not display
            return f""

        if not self.npc:
            return f"{LCYAN}{self.ground_desc}{ENDC}"
        else:
            return f"{CYAN}{self.ground_desc}{ENDC}"