"""CSC111 Project 1: Text Adventure Game Classes

Instructions (READ THIS FIRST!)
===============================

This Python module contains the main classes for Project 1, to be imported and used by
 the `adventure` module.
 Please consult the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2024 CSC111 Teaching Team
"""
from typing import Optional, TextIO


class Character:
    """
    Class representing a character
    """
    character_name: str
    character_file: str

    def __init__(self, character_file: str) -> None:
        self.character_file = character_file


class HostileCharacter(Character):
    """
    Subclass represenrting a hostile character
    """


class DocileCharacter(Character):
    """
    Subclass represenrting a hostile character
    """


class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        - coordinate: an x and y position the player is currently at

    Representation Invariants:
        - # TODO
    """
    name: str
    characters: list[Character]
    gold: int
    been_here: bool = False
    brief_intro: str
    long_intro: str
    location_number: int

    def __init__(self, name: str, location_number: int, character_files: list[str], gold: int,
                 brief_intro: str, long_intro: str) -> None:
        """Initialize a new location.
        """
        self.name = name
        self.location_number = location_number
        self.gold = gold
        self.brief_intro = brief_intro
        self.long_intro = long_intro

        for file in character_files:
            with open(file) as f:
                for line_n in f:
                    line = line_n.strip()
                    if line.isdigit() and line == 0:
                        self.character = DocileCharacter(file)
                    elif line.isdigit() and line == 1:
                        self.character = HostileCharacter(file)
        # NOTES:
        # Data that could be associated with each Location object:
        # a position in the world map,
        # a brief description,
        # a long description,
        # a list of available commands/directions to move,
        # items that are available in the location,
        # and whether the location has been visited before.
        # Store these as you see fit, using appropriate data types.
        #
        # This is just a suggested starter class for Location.
        # You may change/add parameters and the data available for each Location object as you see fit.
        #
        # The only thing you must NOT change is the name of this class: Location.
        # All locations in your game MUST be represented as an instance of this class.

        # TODO: Complete this method

    def print_info(self) -> None:
        """
        Prints the introduction of the location when the player enters the location, can either print the long
        introduction if the player hasn't been to the location yet, or can print the brief introduction if the player
        has been to the location before.

        """
        if self.been_here:
            print(self.brief_intro)
        else:
            print(self.long_intro)
            self.been_here = True

    def available_actions(self):
        """
        Return the available actions in this location.
        The actions should depend on the items available in the location
        and the x,y position of this location on the world map.
        """

        # NOTE: This is just a suggested method
        # i.e. You may remove/modify/rename this as you like, and complete the
        # function header (e.g. add in parameters, complete the type contract) as needed

        # TODO: Complete this method, if you'd like or remove/replace it if you're not using it


class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        - # TODO

    Representation Invariants:
        - # TODO
    """

    def __init__(self, name: str, start: int, target: int, target_points: int) -> None:
        """Initialize a new item.
        """

        # NOTES:
        # This is just a suggested starter class for Item.
        # You may change these parameters and the data available for each Item object as you see fit.
        # (The current parameters correspond to the example in the handout).
        # Consider every method in this Item class as a "suggested method".
        #
        # The only thing you must NOT change is the name of this class: Item.
        # All item objects in your game MUST be represented as an instance of this class.

        self.name = name
        self.start_position = start
        self.target_position = target
        self.target_points = target_points


class Player:
    """
    A Player in the text advanture game.

    Instance Attributes:
        - # TODO

    Representation Invariants:
        - # TODO
    """

    def __init__(self, x: int, y: int) -> None:
        """
        Initializes a new Player at position (x, y).
        """

        # NOTES:
        # This is a suggested starter class for Player.
        # You may change these parameters and the data available for the Player object as you see fit.

        self.x = x
        self.y = y
        self.inventory = []
        self.victory = False

    def edit_inventory(self, item: Item, add_remove: str) -> None:
        """
        adds or removes an item to the inventory, if the item is not in inventory and add_remove is set as r,
        raise index error
        """
        if add_remove == "a":
            self.inventory.append(item)
        elif item in self.inventory and add_remove == "r":
            self.inventory.remove(item)
        else:
            raise IndexError

    def check_required_items(self, winning_items: set[Item]) -> bool:
        """
        checks to see if the player has reached ending location with all the objects.
        """
        if all([item in self.inventory for item in winning_items]):
            print("items reached end")
            return True
        else:
            return False



class World:
    """A text adventure game world storing all location, item and map data.

    Instance Attributes:
        - map: a nested list representation of this world's map
        - # TODO add more instance attributes as needed; do NOT remove the map attribute

    Representation Invariants:
        - # TODO
    """
    map: list[list]
    locations_list: list[Location]

    def __init__(self, map_data: TextIO, location_data: TextIO, items_data: TextIO) -> None:
        """
        Initialize a new World for a text adventure game, based on the data in the given open files.

        - location_data: name of text file containing location data (format left up to you)
        - items_data: name of text file containing item data (format left up to you)
        """

        self.map = self.load_map(map_data)
        self.locations_list = []
        self.item_list = []
        ending_line = ""

        while ending_line != "locations end":
            l1 = self.read_file_line(location_data).split()
            detailed_description = ""
            location = Location(l1[1], int(l1[0]),
                                self.read_file_line(location_data).split(),
                                int(self.read_file_line(location_data)),
                                self.read_file_line(location_data),
                                "")

            line = location_data.readline()

            while line != "descriptions end\n":
                detailed_description += line
                line = location_data.readline()
            location.long_intro = detailed_description

            self.locations_list.append(location)
            ending_line = self.read_file_line(location_data)

        while ending_line != "items end":
            item = Item(self.read_file_line(items_data),
                        int(self.read_file_line(items_data)),
                        int(self.read_file_line(items_data)),
                        int(self.read_file_line(items_data)))
            self.item_list.append(item)
            ending_line = self.read_file_line(items_data)

    def read_file_line(self, data: TextIO) -> str:
        """
        returns a line of the data file without the newline (made for more neat code).
        """
        return data.readline().strip()

    def load_map(self, map_data: TextIO) -> list[list[int]]:
        """
        Store map from open file map_data as the map attribute of this object, as a nested list of integers like so:

        If map_data is a file containing the following text:
            1 2 5
            3 -1 4
        then load_map should assign this World object's map to be [[1, 2, 5], [3, -1, 4]].

        Return this list representation of the map.
        """
        final_list = []
        for line in map_data:
            final_list.append([int(x) for x in line.strip().split()])

        return final_list

    def get_location(self, x: int, y: int) -> Optional[Location]:
        """Return Location object associated with the coordinates (x, y) in the world map, if a valid location exists at
         that position. Otherwise, return None. (Remember, locations represented by the number -1 on the map should
         return None.)
        """

        location_number = self.map[y][x]
        for i in self.locations_list:
            if location_number == i.location_number:
                return i
        return None

    def do_action(self, p: Player, location: Location, choice: str):
        """
        Does an action
        """
        if choice == "quit":




"""
w = World(open("map.txt"), open("locations.txt"), open("items.txt"))
print(w.map)
loc = w.get_location(3, 2)
print(loc.location_number)
print(w.item_list[4].name)
"""
