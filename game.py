#!/usr/bin/python3
import os
from world_state import * # world_state dictionary and constants
from world import init_player, load_map_data, load_item_data
from classes import Player, direction

# Clear screen
os.system('cls||clear')

def play():
    print("Escape from Cave Terror!\n")

    # Load rooms into world state
    load_map_data()
    load_item_data()

    # Init player with starting room
    p = init_player(world_state[START_ROOM])

    # Display the starting room
    display_room(START_ROOM)

    while True:
        action_input = get_player_command()
        current_room_id = p.get_current_room_id()
        current_room = world_state[current_room_id]

        # Transform to lowercase to standardize
        action_input = action_input.lower() 

        # Split string to see if there are multiple arguments
        cmd = action_input.split()

        if len(cmd) == 1:
            process_standalone_cmd(p, cmd[0])
        elif len(cmd) > 1 and cmd[0] in ('l', 'look'):
            process_look_cmd(p, current_room, cmd[1:])
        elif len(cmd) > 1 and cmd[0] in ('t', 'take', 'get'):
            process_take_cmd(p, current_room, cmd[1:])
        elif len(cmd) > 1 and cmd[0] in ('d', 'drop'):
            process_drop_cmd(p, current_room, cmd[1:])
        else:
            print("Invalid action!")

def process_standalone_cmd(p, action_input):
    update_room_display = False

    if action_input in ('n', 'north'):
        update_room_display = p.move(direction.north)
    elif action_input in ('s', 'south'):
        update_room_display = p.move(direction.south)
    elif action_input in ('e', 'east'):
        update_room_display = p.move(direction.east)
    elif action_input in ('w', 'west'):
        update_room_display = p.move(direction.west)
    elif action_input in ('i', 'inv', 'inventory'):
        p.display_inventory()
    elif action_input in ('l', 'look'):
        update_room_display = True
    elif action_input in ('g', 'get'):
        print("Get what?")
    elif action_input in ('t', 'take'):
        print("Take what?")
    elif action_input == 'quit' or action_input == 'q':
        exit()
    else:
        print("Invalid action!")

    # If the player moved rooms or entered 'look' action re-display room
    if update_room_display:
        display_room(p.get_current_room_id())

def process_look_cmd(p, current_room, args):
    current_room_items = current_room.get_items()

    # For the Items in the current room, check if the first arg of the command matches any of the Item's keywords
    for item in current_room_items.values():
        if args[0] in item.get_keywords():
            print(item.get_long_desc())
            return # Ignore further command arguments
    else:
        print("There isn't an item with that name here!")

def process_take_cmd(p, current_room, args):
    current_room_items = current_room.get_items()

    # For the Items in the current room, check if the first arg of the command matches any of the Item's keywords
    for item in current_room_items.values():
        if args[0] in item.get_keywords():
            if item.is_takeable():
                print("You pick up the {}.".format(item.get_short_desc()))
                p.add_item_to_inventory(item)
                current_room.remove_item(item.get_key())
            else:
                print("You can't pick that up!")
            return # Ignore further command arguments
    else:
        print("There isn't an item with that name here!")

def process_drop_cmd(p, current_room, args):
    inventory_items = p.get_inventory()

    for item in inventory_items:
        if args[0] in item.get_keywords():
            print("You drop the {}.".format(item.get_short_desc()))
            inventory_items.remove(item)
            current_room.add_item(item)
        else:
            print("You can't drop that!")
        return # Ignore further command arguments
    else:
        print("You don't have any item with that name.")

def display_room(room_id):
    if room_id in world_state:
        print(world_state[room_id])
    else:
        print("Room does not exist!")

def get_player_command():
    return input('Action: ')

if __name__ == '__main__':
    play()