"""CSC111 Project 1: Text Adventure Game

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.
This file is Copyright (c) 2024 CSC111 Teaching Team
"""

# Note: You may add in other import statements here as needed
from game_data import World, Item, Location, Player
from pygame import mixer
# Note: You may add helper functions, classes, etc. here as needed

# Note: You may modify the code below as needed; the following starter template are just suggestions
if __name__ == "__main__":
    w = World(open("map.txt"), open("locations.txt"), open("items.txt"))
    p = Player(2, 2)  # TODO: file dependent
    directions = {"north": (0, -1), "east": (1, 0), "south": (0, 1), "west": (-1, 0)}
    possible_actions = ["look", "inventory", "score", "quit"]
    winning_location = w.get_location(2, 4)  # TODO: file dependent
    winning_items = {item for item in w.item_list if item.target_position == winning_location.location_number}
    print([x.name for x in winning_items])
<<<<<<< HEAD
=======
    mixer.init()

    # # Load audio file
    # mixer.music.load('stranger-things-124008.mp3')
    # mixer.music.set_volume(0.5)
    #
    # # Play the music
    # mixer.music.play()
>>>>>>> 1836f7689e33dfbc8de655c330182393f62b2866

    while not p.victory:
        location = w.get_location(p.x, p.y)
        print("------------------------------------------------")
        print(f"YOU ARE CURRENTLY AT {location.name}. \n")
        location.print_info()
        print("------------------------------------------------")
        if location == winning_location and p.check_required_items(winning_items):
            p.victory = True
            break
        choice = input("\nEnter action: ").lower()
        print("\n")

        if "go " in choice and choice[3:] in directions.keys():
            if w.get_location(p.x + directions[choice[3:]][0], p.y + directions[choice[3:]][1]) is None:
                print("That way is blocked \n")
            else:
                p.x += directions[choice[3:]][0]
                p.y += directions[choice[3:]][1]
        elif "go " in choice:
            print("invalid direction\n")
        elif choice in possible_actions:
            if choice == "quit":
                break
            w.do_action(p, location, choice)
        else:  # runs when the program does not recognize what the player wants to do
            print("what are you yappin about bro\n")
