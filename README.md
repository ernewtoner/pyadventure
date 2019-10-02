# pyadventure
Text-based adventure game in Python 3

----Game Usage Instructions----

* To run the program it is necessary to have access to a UNIX-based terminal, which is available on every popular operating system these days (Linux, Mac OS X terminal, Windows Linux Subsystem). The program is a Python 3 script so it is necessary to have Python 3.6 or greater installed (see https://realpython.com/installing-python/ for installation instructions for each major operating system) and run the program as follows:

'python3 game.py'

The user will then see the welcome screen and the display of the starting room of the world and will be presented with an action input prompt. To navigate around the world you can type a direction (north, south, east, west) according to the available exits in a room. One can also ‘look’ to see a description of the room or an object. The ‘help’ command shows additional verbs you can use to interact with the world. 

----Game Playthrough Instructions----

1. You start in the Eternal Void room and enter the portal with this or a similar command: 'en portal'
2. The Edge of the Cliff Face room--two items can be picked up here, both of which are needed: 'pick up dagger' and 'get wafer'
3. Before toggling the win condition, if you choose to fight the mage in the room or the other mage in the tower to the north you will die. Triggering the win condition makes you all-powerful.
4. The win condition involves two triggers that must be done in order, bathing in the fountain and eating the wafer which puts your character into the win-state: 'bathe in fountain' and 'eat wafer'
5. If you accidentally have already eaten the wafer it will regenerate in the room in 60 seconds.
6. In this all-powerful state you can feel free to: 'hit mage'
7. Go 'north' to A Barren Plain.
8. Go 'north' to More Barren Plain. This is an room that seems infinite where there is more More Barren Plain in any direction you go besides where you came from.
9. It’s not actually infinite as the description suggests, you can go 'north' 10 times and arrive at Approaching a Dark Citadel.
10. Go 'north' to The Path to the Citadel.
11. Go 'north' to Inside the Citadel.
12. There is a hidden feature in this room ‘doors’ which can be unlocked like so: 'use dagger on doors' they can then be opened by 'open doors'.
13. There is now an east exit to the room. Go 'east' to The Wizard's Tower.
14. Kill the resident mage to win the game: 'kill mage'
