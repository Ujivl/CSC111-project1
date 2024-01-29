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

# Note: You may add helper functions, classes, etc. here as needed

# Note: You may modify the code below as needed; the following starter template are just suggestions
if __name__ == "__main__":
    w = World(open("map.txt"), open("locations.txt"), open("map.txt"))
    p = Player(3, 2)  # set starting location of player; you may change the x, y coordinates here as appropriate
    directions = {"north": (0, -1), "east": (1, 0), "south": (0, 1), "west": (-1, 0)}

    while not p.victory:
        location = w.get_location(p.x, p.y)
        location.print_info()

        for action in location.available_actions():
            print(action)
        choice = input("\nEnter action: ")

        if "go " in choice:
            if w.get_location(p.x + directions[choice[3:0]][0], p.y + directions[choice[3:0]][1]) is None:
                print("invalid")
            else:
                p.x += directions[choice[3:0]][0]
                p.y += directions[choice[3:0]][1]


        # TODO: CALL A FUNCTION HERE TO HANDLE WHAT HAPPENS UPON THE PLAYER'S CHOICE
        #  REMEMBER: the location = w.get_location(p.x, p.y) at the top of this loop will update the location if
        #  the choice the player made was just a movement, so only updating player's position is enough to change the
        #  location to the next appropriate location
        #  Possibilities:
        #  A helper function such as do_action(w, p, location, choice)
        #  OR A method in World class w.do_action(p, location, choice)
        #  OR Check what type of action it is, then modify only player or location accordingly
        #  OR Method in Player class for move or updating inventory
        #  OR Method in Location class for updating location item info, or other location data etc....
