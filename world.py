import json
import os
from world_state import * # world_state dictionary and constants
import classes

def process_room_data(data):
    """ Extracts room data from JSON data and converts into a Room object """
    for key, subdict in data.items():
        name = key
        id = subdict["ID"]
        description = subdict["DESC"]

        exits = {}
        # Convert list stored in file to {'north' : (RoomID, "Room Name") } format then add to exits dictionary
        if "NORTH" in subdict:
            exits[NORTH] = (subdict["NORTH"][0], subdict["NORTH"][1])
        if "EAST" in subdict:
            exits[EAST] =  (subdict["EAST"][0], subdict["EAST"][1])
        if "SOUTH" in subdict:
            exits[SOUTH] = (subdict["SOUTH"][0], subdict["SOUTH"][1])
        if "WEST" in subdict:
            exits[WEST] = (subdict["WEST"][0], subdict["WEST"][1])

        # Dictionary of Items to be populated when item files are processed
        items = {}

        room = classes.Room(id, name, description, exits, items)
        return room

def process_item_data(data):
    """ Extracts item data from JSON data and converts into an Item object """
    for key, subdict in data.items():
        key_from_file = key
        room_id = subdict["ROOM_ID"]
        ground_desc = subdict["GROUNDDESC"]
        short_desc = subdict["SHORTDESC"]
        long_desc = subdict["LONGDESC"]
        takeable = subdict["TAKEABLE"]
        keywords = subdict["KEYWORDS"]

        item = classes.Item(key_from_file, room_id, ground_desc, short_desc, long_desc, takeable, keywords)
        return item

def load_item_data():
    """ Loads data from JSON files in items directory and adds Item objects to world state"""
    with os.scandir('world/items/') as entries:
        for entry in entries:
            if entry.is_file() and entry.path.endswith(".json"):
                # Process each json file in rooms directory
                data = json.load(open(entry))

                # Create Item object
                item = process_item_data(data)
                item_key = item.get_key()
                item_room = item.get_room_id()

                # Add to world state under a Room's items dictionary
                world_state[item_room].items.update({item_key: item})

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
    #print("--------------------------------------------")

def init_player(starting_room):
    """ Initializes player object """
    player = classes.Player("Ilswyn", starting_room)
    return player