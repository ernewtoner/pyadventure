#!/usr/bin/python3
import os, time
from world_state import * # world_state dictionary and constants
from world import init_player, init_world, load_map_data, load_item_data, save_world_state, load_world_state
from classes import Player, direction
from colors import *

# Clear screen
os.system('cls||clear')

def play():
    print("Escape from Cave Terror!\n")

    # Initialize a world
    w = init_world()

    # Load rooms into world state
    load_map_data(w)
    load_item_data(w)

    # Init player with starting Room
    p = init_player(w.world_state[START_ROOM])

    # Display the starting Room with long description
    display_room(w, START_ROOM, True)

    while True:
        action_input = get_player_command()
        current_room_id = p.get_current_room_id()
        current_room = w.world_state[current_room_id]

        # Transform to lowercase to standardize
        action_input = action_input.lower() 

        # Split string to see if there are multiple arguments
        cmd = action_input.split()

        if len(cmd) == 1:
            process_standalone_cmd(p, w, cmd[0])
        elif len(cmd) == 0: # No input
            continue
        elif len(cmd) > 1 and cmd[0] in ('l', 'look') and cmd[1] in ('at', 'in'):
            process_cmd_with_arg(p, current_room, cmd[2:], "look at")
        elif len(cmd) > 1 and cmd[0] in ('l', 'look'):
            process_cmd_with_arg(p, current_room, cmd[1:], "look at")
        elif len(cmd) > 1 and cmd[0] in ('t', 'take', 'get'):
            process_get_cmd(p, current_room, cmd[1:])
        elif len(cmd) > 1 and cmd[0] == 'pick' and cmd[1] == 'up':
            process_get_cmd(p, current_room, cmd[2:])
        elif len(cmd) > 1 and cmd[0] in ('eq', 'wear', 'equip'):
            process_equip_cmd(p, cmd[1:])
        elif len(cmd) > 1 and cmd[0] in ('remove', 'unequip'):
            process_equip_remove_cmd(p, cmd[1:])       
        elif len(cmd) > 1 and cmd[0] in ('dr', 'drop'):
            process_drop_cmd(p, current_room, cmd[1:])
        elif len(cmd) > 1 and cmd[0] in ('sa', 'say'):
            print(f"{WHITE}You say, '{' '.join(cmd[1:])}'{ENDC}") # converts to lowercase
        elif len(cmd) > 1 and cmd[0] in ('d', 'drink'):
            process_cmd_with_arg(p, current_room, cmd[1:], "drink")
        elif len(cmd) > 1 and cmd[0] in ('ea', 'eat'):
            process_cmd_with_arg(p, current_room, cmd[1:], "eat")
        else:
            print("Invalid action!\n")

def process_standalone_cmd(p, w, action_input):
    update_room_display = False # Flag for whether the room needs to be re-displayed
    display_long_desc = False # Flag for whether the room long desc or short desc should be printed

    if action_input in ('n', 'north'):
        update_room_display, display_long_desc = p.move(w, direction.north)
    elif action_input in ('s', 'south'):
        update_room_display, display_long_desc = p.move(w, direction.south)
    elif action_input in ('e', 'east'):
        update_room_display, display_long_desc = p.move(w, direction.east)
    elif action_input in ('w', 'west'):
        update_room_display, display_long_desc = p.move(w, direction.west)
    elif action_input in ('l', 'look'):
        update_room_display = True
        display_long_desc = True
    elif action_input in ('g', 'get'):
        print("Get what?\n")
    elif action_input in ('t', 'take'):
        print("Take what?\n")
    elif action_input in ('d', 'drop'):
        print("Drop what?\n")
    elif action_input in ('wear'):
        print("Wear what?\n")
    elif action_input in ('i', 'in', 'inv', 'inventory'):
        p.display_inventory()
    elif action_input in ('eq', 'equip', 'equipment'):
        p.display_equipment()
    elif action_input in ('save', 'savegame'):
        save_world_state(w, p)
    elif action_input in ('load', 'loadgame'):
        w.world_state, saved_player = load_world_state(p)
        p.copy(saved_player.name, saved_player.current_room, saved_player.inventory, saved_player.equipment)
        update_room_display = True
    elif action_input in ('h', 'help'):
        display_help()
    elif action_input in ('q', 'quit'):
        exit()
    else:
        print("Invalid action!\n")

    # If the player moved rooms or entered 'look' action re-display room
    if update_room_display:
        display_room(w, p.get_current_room_id(), display_long_desc)

# Searches for an item keyword in the room, inventory, and equipment
# Returns Object with the matching keyword if found
def find_item(p, current_room, item_keyword):
    current_room_items = current_room.get_items()
    current_room_npcs = current_room.get_npcs()
    inventory_items = p.get_inventory()
    equipped_items = p.get_equipment()

    # Search the Objects and NPCs in the room first
    for item in current_room_items.values():
        if item_keyword in item.get_keywords():
            return item

    for item in current_room_npcs.values():
        if item_keyword in item.get_keywords():
            return item

    # If not in room items, check the player's inventory items
    for item in inventory_items:
        if item_keyword in item.get_keywords():
            return item

    # Lastly check the player's equipped items
    for item in equipped_items:
        if item_keyword in item.get_keywords():
            return item
    else:
        print("There is no item with that name!\n")
        return None

def process_look_at_cmd(p, current_room, args):
    item = find_item(p, current_room, args[0])

    # If item is found, print long description
    if (item):
        print(item.get_long_desc())
    else:
        print("There's no item with that name!\n")

def process_cmd_with_arg(p, current_room, args, action):
    """ Look at <arg>, drink <arg>, eat <arg> """
    item = find_item(p, current_room, args[0])

    # If item is found, process action
    if (item):
        if action == "look at":
            print(item.long_desc)
        elif action == 'drink':
            print(item.drink_desc)
            if item in p.inventory:
                p.remove_item_from_inventory(item)
        elif action == 'eat':
            if item in p.inventory:
                if item.key == "Dagger":
                    print(item.eat_desc)
                    time.sleep(1)
                    p.death()
                    return
                print(item.eat_desc)
                p.remove_item_from_inventory(item)
            elif item.key in current_room.items:
                print("You don't have that in your inventory!\n")
        else:
            print("Action not found!\n")

def process_get_cmd(p, current_room, args):
    current_room_items = current_room.get_items()

    # For the Items in the current room, check if the first arg of the command matches any of the Item's keywords
    for item in current_room_items.values():
        if args[0] in item.get_keywords():
            if item.is_takeable():
                print(f"You pick up the {item.get_short_desc()}.\n")
                p.add_item_to_inventory(item)
                current_room.remove_item(item.get_key())
            else:
                print("You can't pick that up!\n")
            return # Ignore further command arguments
    else:
        print("There isn't an item with that name here!\n")

def process_equip_cmd(p, args):
    inventory_items = p.get_inventory()

    for item in inventory_items:
        if args[0] in item.get_keywords():
            if item.equipable:
                print(f"You equip the {item.get_short_desc()}.\n")
                p.add_item_to_equipment(item)
                p.remove_item_from_inventory(item)
                return # Ignore further command arguments
            else:
                print("You cannot equip that item!\n")
                return
    else:
        print("You do not have that item!\n")

def process_equip_remove_cmd(p, args):
    equipment_items = p.get_equipment()

    for item in equipment_items:
        if args[0] in item.get_keywords():
            print(f"You remove the {item.get_short_desc()}.")
            p.add_item_to_inventory(item)
            p.remove_item_from_equipment(item)
            return # Ignore further command arguments
    else:
        print("You do not have that item equipped!\n")

def process_drop_cmd(p, current_room, args):
    inventory_items = p.get_inventory()

    for item in inventory_items:
        if args[0] in item.get_keywords():
            print("You drop the {}.".format(item.get_short_desc()))
            current_room.add_item(item)
            p.remove_item_from_inventory(item)
            return # Ignore further command arguments
    else:
        print("You don't have that to drop!\n")

def display_help():
    print("-----Available Commands----")
    print("Directional: north, south, east, west")
    print("World actions: get <arg>, drop <arg>, look <arg>")
    print("Player actions: inventory, equipment, wear <arg>, remove <arg>, say <arg>\n")

def display_room(w, room_id, display_long_desc_flag):
    room = w.world_state[room_id]

    if room_id in w.world_state:
        room.display(display_long_desc_flag)
    else:
        print("Room does not exist!")

def get_player_command():
    return input('Action: ')

if __name__ == '__main__':
    play()