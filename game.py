#!/usr/bin/python3
import os, time, threading
from world_state import * # world_state dictionary and constants
from world import init_player, init_world, load_map_data, load_item_data, save_world_state, load_world_state
from classes import Player, Object, direction
from colors import *

# Clear screen
os.system('cls||clear')

def play():
    print("Escape from the Astral Plane!\n")

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
            process_cmd_with_arg(p, w, current_room, cmd[2:], "look at")
        elif len(cmd) > 1 and cmd[0] in ('l', 'look'):
            process_cmd_with_arg(p, w, current_room, cmd[1:], "look at")
        elif len(cmd) > 1 and cmd[0] in ('go') and cmd[1] in ('n', 'no', 'nor', 'north', 's', 'so', 'sou', 'south' 'e', 'ea', 'eas', 'east,' 'w', 'we', 'west'):
            process_standalone_cmd(p, w, cmd[1])
        elif len(cmd) > 1 and cmd[0] in ('go'):
            process_cmd_with_arg(p, w, current_room, cmd[1:], "enter")
        elif len(cmd) > 1 and cmd[0] in ('t', 'ta', 'take', 'ge', 'get') and cmd[1] not in ('on','in'):
            process_get_cmd(p, w, current_room, cmd[1:]) # Possible Timer object return
        elif len(cmd) > 1 and cmd[0] == 'pick' and cmd[1] == 'up':
            process_get_cmd(p, w, current_room, cmd[2:])
        elif len(cmd) > 1 and cmd[0] in ('eq', 'wear', 'equip'):
            process_equip_cmd(p, cmd[1:])
        elif len(cmd) > 1 and cmd[0] in ('remove', 'unequip'):
            process_equip_remove_cmd(p, cmd[1:])       
        elif len(cmd) > 1 and cmd[0] in ('dr', 'drop'):
            process_drop_cmd(p, current_room, cmd[1:])
        elif len(cmd) > 1 and cmd[0] in ('sa', 'say'):
            print(f"{WHITE}You say, '{' '.join(cmd[1:])}'{ENDC}") # converts to lowercase
        elif len(cmd) > 1 and cmd[0] in ('tal', 'talk') and cmd[1] in ('to'):
            process_cmd_with_arg(p, w, current_room, cmd[2:], "talk to")
        elif len(cmd) > 1 and cmd[0] in ('tal', 'talk') and cmd[1] in ('abo', 'about'):
            print(f"You talk about the {cmd[2]}")
        elif len(cmd) > 1 and cmd[0] in ('tal', 'talk'):
            process_cmd_with_arg(p, w, current_room, cmd[1:], "talk to")
        elif len(cmd) > 1 and cmd[0] in ('d', 'drink'):
            process_cmd_with_arg(p, w, current_room, cmd[1:], "drink")
        elif len(cmd) > 1 and cmd[0] in ('ea', 'eat'):
            process_cmd_with_arg(p, w, current_room, cmd[1:], "eat")
        elif len(cmd) > 1 and cmd[0] in ('get') and cmd[1] in ('in', 'on'):
            process_cmd_with_arg(p, w, current_room, cmd[2:], "enter")
        elif len(cmd) > 1 and cmd[0] in ('en', 'enter'):
            process_cmd_with_arg(p, w, current_room, cmd[1:], "enter")
        elif len(cmd) > 1 and cmd[0] in ('op', 'open'):
            process_cmd_with_arg(p, w, current_room, cmd[1:], "open")
        elif len(cmd) > 1 and cmd[0] in ('h', 'hit', 'k', 'kill'):
            process_cmd_with_arg(p, w, current_room, cmd[1:], "hit")
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
    elif action_input in ('eat'):
        print("Eat what?\n")
    elif action_input in ('dr', 'dri', 'drin', 'drink'):
        print("Drink what?\n")
    elif action_input in ('hit', 'k', 'kill'):
        print("Hit what?\n")
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
        w.exit()
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

def process_cmd_with_arg(p, w, current_room, args, action):
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
                    p.death(w)
                    return

                print(item.eat_desc)

                if item.key == "Wafer":
                    if p.fountain_trigger:
                        time.sleep(1)
                        print(f"You feel very {CYAN}d{ENDC}i{WHITE}ff{ENDC}ere{CYAN}nt{ENDC}.")
                        p.endgame_trigger = 1
                p.remove_item_from_inventory(item)
            elif item.key in current_room.items:
                print("You don't have that in your inventory!\n")
        elif action == 'enter':
            if item.key == "Fountain":
                print("You bathe in the fountain.")
                p.fountain_trigger = 1
                time.sleep(1)
                print(f"You feel {WHITE}f{ENDC}u{WHITE}n{ENDC}n{WHITE}y{ENDC}.")
                return
            if item.enterable:
                new_room_id = item.destination
                display_long_desc_flag = p.set_current_room(w, new_room_id)
                display_room(w, new_room_id, display_long_desc_flag)
            else:
                print("You can't enter that!\n")
        elif action == 'open':
            print(item.open_desc)
            if item.key == "Doors":
                # Modify room with east exit {'north' : (room_id, "Room Name")
                item.long_desc = "The plain wooden doors are open."
                current_room.exits.update({'east': (7, "Inside the Wizard's Tower")})
                current_room.display(True)
            else:
                print("You can't open that!\n")
        elif action == 'hit':
            if item.hit_desc:
                print(item.hit_desc)

                weapon_action = "punch"
                for eq in p.equipment:
                    if eq.key == "Dagger":
                        weapon_action = "stab"

                if item.key == "Tired Mage":
                    if p.endgame_trigger:
                        print("\nYou <-< AnnihilatE >-> a tired mage.")
                        current_room.remove_npc(item.key)
                        return
                    
                    print(f"You barely {weapon_action} a tired mage.\n")
                    print(f"{WHITE}A tired mage says, 'What are you doing?!'{ENDC}")
                    time.sleep(3)
                    print(f"You barely {weapon_action} a tired mage.\n")
                    print(f"{WHITE}A tired mage says, 'Stop at once!'{ENDC}")
                    print("A tired mage starts uttering some strange incantations..")
                    time.sleep(4)
                    print(f"You barely {weapon_action} a tired mage.\n")
                    print(f"{WHITE}A tired mage [ [ [ ERADICATES ] ] ] you with his deadly Falling Star!{ENDC}")
                    p.death(w)
                # [0mBl[1;37mi[0mnd[1;37mi[0mng [31mO[1;31mR[0;31mB[1;35m![0m

                if item.key == "Resident Mage":
                    if p.endgame_trigger:
                        print("\nYou <-< AnnihilatE >-> the resident mage.")
                        current_room.remove_npc(item.key)
                        print ("You have won the game!")
                        w.exit()
                        return

                    print(f"You barely {weapon_action} the resident mage.\n")
                    print(f"{WHITE}The resident mage says, 'Do you think you can fight your way out of this?'{ENDC}")
                    time.sleep(3)
                    print(f"You barely {weapon_action} the resident mage.\n")
                    print(f"{WHITE}A tired mage says, 'Foolish.'{ENDC}")
                    print("A tired mage starts uttering some strange incantations..")
                    time.sleep(4)
                    print(f"You barely {weapon_action} the resident mage.\n")
                    print(f"{WHITE}The resident mage . ._ ..__a T o M i Z e S__.. _. . you with his inconceivable Fireball!{ENDC}\n")
                    p.sudden_death(w)
            else:
                print("You can't hit that!\n")
        elif action == 'talk to':
            if item.talk_desc:
                print(item.talk_desc)
            if item.key == "Resident Mage":
                print(f"{WHITE}A resident mage says 'You still haven't figured it out have you?{ENDC}")
        else:
            print("Action not found!\n")

def createWafer(room, wafer):
    room.add_item(wafer)

def process_get_cmd(p, w, current_room, args):
    current_room_items = current_room.get_items()
    current_room_npcs = current_room.get_npcs()

    # For the Items in the current room, check if the first arg of the command matches any of the Item's keywords
    for item in current_room_items.values():
        if args[0] in item.get_keywords():
            if item.is_takeable():
                print(f"You pick up the {item.get_short_desc()}.\n")
                p.add_item_to_inventory(item)

                if item.key == "Wafer":
                    wafer_copy = Object(item.key, item.room_id, item.ground_desc, item.short_desc, item.long_desc, item.drink_desc, item.eat_desc, item.hit_desc, item.open_desc, item.hit_desc, item.takeable, item.equipable, item.enterable, item.openable, item.destination, item.npc, item.hidden, item.keywords)
                    w.timer = threading.Timer(60, createWafer, [current_room, wafer_copy])
                    w.timer.start()

                current_room.remove_item(item.get_key())
            else:
                print(f"You can't pick up {item.short_desc}!\n")
            return # Ignore further command arguments

    for npc in current_room_npcs.values():
        if args[0] in npc.get_keywords():
            print(f"How do you propose to pick up {npc.get_short_desc()}?")
            return
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
    print("Directional: (optional 'go') north, south, east, west")
    print("World actions: get <arg>, drop <arg>, look <arg>, enter <arg>, eat <arg>, drink <arg>")
    print("Player actions: inventory, equipment, wear <arg>, remove <arg>, say <arg>")
    print("NPC interactions: talk (to) <arg>, hit <arg>")
    print("Game actions: loadgame, savegame\n")

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