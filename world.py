import json
import pickle
import os
from world_state import * # constants
import classes

def process_room_data(data):
    """ Extracts room data from JSON data and converts into a Room object """
    for key, subdict in data.items():
        name = key
        id = subdict["ID"]
        long_desc = subdict["LONGDESC"]
        short_desc = subdict["SHORTDESC"]

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

        # Dictionary of Items and NPCs (non-player characters) to be populated when item files are processed
        items = {}
        npcs = {}

        room = classes.Room(id, name, long_desc, short_desc, exits, items, npcs)
        return room

def process_item_data(data):
    """ Extracts item data from JSON data and converts into an Item object """
    for key, subdict in data.items():
        key_from_file = key
        room_id = subdict["ROOM_ID"]
        ground_desc = subdict["GROUNDDESC"]
        short_desc = subdict["SHORTDESC"]
        long_desc = subdict["LONGDESC"]
        drink_desc = "You can't drink from that!" # Default description
        hit_desc = "You can't hit that!"
        if subdict.get("DRINKDESC"):
            drink_desc = subdict["DRINKDESC"] # If specified
        eat_desc = "You can't eat that!"
        if subdict.get("EATDESC"):
            eat_desc = subdict["EATDESC"]
        if subdict.get("HITDESC"):
            hit_desc = subdict["HITDESC"]
        talk_desc = "You can't talk to that!"
        if subdict.get("TALKDESC"):
            talk_desc = subdict["TALKDESC"]
        takeable = subdict.get("TAKEABLE")
        equipable = subdict.get("EQUIPABLE")
        enterable = 0
        openable = 0
        destination = None
        if subdict.get("ENTERABLE"):
            enterable = subdict["ENTERABLE"]
        if subdict.get("DESTINATION"):
            destination = subdict["DESTINATION"]
        openable = 0
        locked = 0
        open_desc = "You can't open that!"
        if subdict.get("OPENABLE"):
            openable = 1
            open_desc = subdict["OPENDESC"]
            if subdict.get("LOCKED"):
                locked = 1

        keywords = subdict["KEYWORDS"]
        npc = 0
        if subdict.get("NPC"):
            npc = 1
        hidden = 0
        if subdict.get("HIDDEN"):
            hidden = 1

        item = classes.Object(key_from_file, room_id, ground_desc, short_desc, long_desc, drink_desc, eat_desc, hit_desc, open_desc, talk_desc, takeable, equipable, enterable, openable, locked, destination, npc, hidden, keywords)
        return item

def load_item_data(world):
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
                if item.npc:
                    world.world_state[item_room].npcs.update({item_key: item})
                else:
                    world.world_state[item_room].items.update({item_key: item})

def load_map_data(world):
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
                world.world_state[room_id] = room

def save_world_state(world, player):
    print("Saving game state...\n")
    with open('world/saved_world_state', 'wb') as world_state_file:
        pickle.dump(world.world_state, world_state_file)
    with open('world/saved_player_state', 'wb') as player_state_file:
        pickle.dump(player, player_state_file)

def load_world_state(player):
    os.system('cls||clear')
    print("Loading game state...\n")
    with open('world/saved_world_state', 'rb') as world_state_file:
        saved_world_state = pickle.load(world_state_file)
    with open('world/saved_player_state', 'rb') as player_state_file:
        saved_player = pickle.load(player_state_file)

    return saved_world_state, saved_player

def init_world():
    """ Initializes World object """
    world = classes.World({})
    return world

def init_player(starting_room):
    """ Initializes player object """
    player = classes.Player("Ilswyn", starting_room)
    return player