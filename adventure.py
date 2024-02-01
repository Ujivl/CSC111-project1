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


if __name__ == "__main__":
    w = World(open("map.txt"), open("locations.txt"), open("items.txt"))
    p = Player(2, 2)  # TODO: file dependent
    directions = {"north": (0, -1), "east": (1, 0), "south": (0, 1), "west": (-1, 0)}
    possible_actions = ["look", "inventory", "score", "quit"]
    winning_location = w.get_location(2, 4)  # TODO: file dependent
    winning_items = {item for item in w.item_list if item.target_position == winning_location.location_number}
    p.edit_inventory(w.item_list[0], "a")
    p.edit_inventory(w.item_list[1], "a")  # TODO: just adding two items to inventory to test stuff
    location = w.get_location(p.x, p.y)
    print("------------------------------------------------")
    print(f"YOU ARE CURRENTLY AT {location.name}. \n")
    location.print_info()
    print("------------------------------------------------")

    while not p.victory:
        location, past_location = w.get_location(p.x, p.y), location
        if location != past_location:
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
        elif choice in possible_actions or choice in location.available_actions():  # TODO: add available_actions()
            if choice == "quit":
                break
            elif choice == "look":
                location.been_here = False
                location.print_info()
            elif choice == "inventory":
                p.show_inventory()
            elif choice == "score":
                print(f"SCORE: {p.score}")
            else:
                w.do_action(p, location, choice)
        else:
            print("what are you yappin about bro\n")
