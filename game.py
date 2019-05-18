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

        # Transform to lowercase to standardize
        action_input = action_input.lower() 

        # Split string to see if there are multiple arguments
        cmd = action_input.split()

        if len(cmd) == 1:
            process_standalone_cmd(p, cmd[0])
        elif len(cmd) > 1 and cmd[0] in ('l', 'look'):
            process_look_cmd(p, cmd[1:])
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
    elif action_input in ('l', 'look'):
        update_room_display = True
    elif action_input in ('get', 'take'):
        print("Get what?")
    elif action_input == 'quit' or action_input == 'q':
        exit()
    else:
        print("Invalid action!")

    # If the player moved rooms or entered 'look' action re-display room
    if update_room_display:
        display_room(p.get_current_room_id())

def process_look_cmd(p, args):
    current_room_id = p.get_current_room_id()
    current_room_items = world_state[current_room_id].get_items()

    # For the Items in the current room, check if the first arg of the command matches any of the Item's keywords
    for item in current_room_items.values():
        if args[0] in item.get_keywords():
            print(item.get_long_desc())
            return # Ignore further command arguments
    else:
        print("There isn't an item with that name here!")

def process_take_cmd():
    pass

def display_room(room_id):
    if room_id in world_state:
        print(world_state[room_id])
    else:
        print("Room does not exist!")

def get_player_command():
    return input('Action: ')

if __name__ == '__main__':
    play()