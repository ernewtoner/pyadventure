import json
import os

import classes

world_state = {}

def process_room_data(data):
    """ Extracts room data from JSON data and converts into a Room object """
    for key, subdict in data.items():
        name = key
        id = subdict["ID"]
        description = subdict["DESC"]

        exits = {}
        # Convert list stored in file to {'north' : (RoomID, "Room Name") } format then add to exits dictionary
        if "NORTH" in subdict:
            exits["north"] = (subdict["NORTH"][0], subdict["NORTH"][1])
        if "EAST" in subdict:
            exits["east"] =  (subdict["EAST"][0], subdict["EAST"][1])
        if "SOUTH" in subdict:
            exits["south"] = (subdict["SOUTH"][0], subdict["SOUTH"][1])
        if "WEST" in subdict:
            exits["west"] = (subdict["WEST"][0], subdict["WEST"][1])

        objects = subdict["OBJECTS"]

        room = classes.Room(id, name, description, exits, objects)
        return room
    
def load_map_data():
    """ Loads data from JSON files in rooms directory and adds Room objects to world state"""
    with os.scandir('world/rooms/') as entries:
        for entry in entries:
            if entry.is_file() and entry.path.endswith(".json"):
                # Process each json file in rooms directory
                data = json.load(open(entry))

                # Create room object
                room = process_room_data(data)
                room_id = room.get_id()

                 # Add to world state
                world_state[room_id] = room

    #print("WORLD STATE")
    #print(world_state)

def init_player(starting_room):
    """ Initializes player object """
    player = classes.Player("Ilswyn", starting_room)
    return player