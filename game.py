#!/usr/bin/python3
import world
from world import world_state, load_map_data
from classes import Player, direction

# Clear screen
import os
os.system('cls||clear')

def play():
    print("Escape from Cave Terror!\n")

    # Load rooms into world state
    load_map_data()

    # Init player with starting room (room 1)
    p = world.init_player(world_state[1])

    # Display the starting room
    display_room(1)

    while True:
        action_input = get_player_command()

        if action_input == 'n' or action_input == 'N':
            p.move(direction.NORTH)
        elif action_input == 's' or action_input == 'S':
            p.move(direction.SOUTH)
        elif action_input == 'e' or action_input == 'E':
            p.move(direction.EAST)
        elif action_input == 'w' or action_input == 'W':
            p.move(direction.WEST)
        elif action_input == 'quit' or action_input == 'q':
            exit()
        else:
            print("Invalid action!")

        # Display the room the player has moved to
        display_room(p.get_current_room_id())
    
def display_room(room_id):
    if room_id in world_state:
        print(world_state[room_id])
    else:
        print("Room does not exist!")

def get_player_command():
    return input('Action: ')

play()