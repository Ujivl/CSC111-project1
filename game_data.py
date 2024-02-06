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


class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        - name: name of the item
        - start_position: starting location of the item on the map
        - target_position: the location where the item is supposed to end up in on the map
        - target_points: idk what this does uji lol

    Representation Invariants:
        - self.name != ""
    """

    name: str
    item_id: int
    start_position: int
    target_position: int
    target_points: int

    def __init__(self, name: str, item_id: int, start: int, target: int, target_points: int) -> None:
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
        self.item_id = item_id
        self.start_position = start
        self.target_position = target
        self.target_points = target_points


"""
class Character:

    character_name: str
    item_required: Optional[Item] = None
    reward: Optional[Item] = None
    dialogue1: str
    dialogue2: str

    def __init__(self, character_name: str, item_required: Optional[Item], reward: Optional[Item],
                 dialogue1: str, dialogue2: str) -> None:

        self.character_name = character_name
        self.item_required = item_required
        self.reward = reward
        self.dialogue1 = dialogue1
        self.dialogue2 = dialogue2
"""


class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        - name: name of the location
        - characters: characters within the location
         - gold: amount of gold present in the location
        - been_here: a boolean indicating whether the player has visited the location
        - brief_intro: a short introduction to the location
        - long_intro: a more detailed description of the location
        - location_number: a unique identifier for the location
    Representation Invariants:
        - self.gold >= 0
        - location_number >= 0
        - self.name != ""
    """
    name: str
    item_ids: list[int]
    been_here: bool = False
    brief_intro: str
    long_intro: str
    location_number: int

    def __init__(self, name: str, location_number: int, item_ids: list[int],
                 brief_intro: str, long_intro: str) -> None:
        """Initialize a new location.
        """
        self.name = name
        self.item_ids = item_ids
        self.location_number = location_number
        self.brief_intro = brief_intro
        self.long_intro = long_intro

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

    def print_info(self, items) -> str:
        """
        Prints the introduction of the location when the player enters the location, can either print the long
        introduction if the player hasn't been to the location yet, or can print the brief introduction if the player
        has been to the location before.

        """

        items = "items in this location: " + (", ".join([items[x] for x in self.item_ids if x != -1]))

        if items == "items in this location: ":
            items = "There are currently no items in this location"

        if self.been_here:
            return f"{self.brief_intro} \n{items}"
        else:
            self.been_here = True
            return f"{self.long_intro} \n{items}"

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
    def add_item_id(self, item_id: int) -> None:
        """
        adds an item id from a location
        """
        self.item_ids.append(item_id)

    def remove_item_id(self, item_id: int) -> None:
        """
        removes an item id from a location
        """
        self.item_ids.remove(item_id)


class Player:
    """
    A Player in the text advanture game.

    Instance Attributes:
        - x: x-coordinate of the player's position
        - y: y-coordinate of the player's position
        - inventory: a list of items the player is carrying
        - victory: a boolean indicating whether the player has achieved victory
        - score: the player's score in the game, accumulated by collecting items and visiting locations
        - max_moves: the maximum number of moves allowed for the player

    Representation Invariants:
        - self.max_moves > 0
    """

    score: int = 0

    def __init__(self, x: int, y: int) -> None:
        """
        Initializes a new Player at position (x, y).
        """

        self.x = x
        self.y = y
        self.inventory = []
        self.victory = False
        self.score = 0
        self.max_moves = 100

    def edit_inventory(self, item: Item, add_remove: str) -> bool:
        """
        adds or removes an item to the inventory, if the item is not in inventory and add_remove is set as r
        """
        if add_remove == "a":
            self.inventory.append(item)
            return True
        elif item in self.inventory and add_remove == "r":
            self.inventory.remove(item)
            return True
        else:
            return False

    def check_required_items(self, winning_items: set[Item]) -> bool:
        """
        checks to see if the player has reached ending location with all the objects.
        """
        if all([item in self.inventory for item in winning_items]):
            print("items reached end")
            return True
        else:
            return False

    def show_inventory(self) -> str:
        """
        prints out all the items in the inventory in a neat format.
        """
        if not self.inventory:
            return "you currently have no items in your inventory"
        else:
            return "".join([f"[{item.name}]\n" for item in self.inventory])


class World:
    """A text adventure game world storing all location, item and map data.

    Instance Attributes:
        - map: a nested list representation of this world's map
        - locations_list: a list containing instances of Location inside the world

    Representation Invariants:
        - len(self.map) > 0 and all(len(row) == len(map[0]) for row in self.map)
        - all(isinstance(location, Location) for location in self.locations_list)
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
            l1 = self.read_file_line(location_data).split("-")
            detailed_description = ""
            location = Location(l1[1], int(l1[0]),
                                [int(self.read_file_line(location_data))],
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
            l1 = self.read_file_line(items_data).split("_")
            item = Item(l1[0],
                        int(l1[1]),
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


"""
w = World(open("map.txt"), open("locations.txt"), open("items.txt"))
print(w.map)
loc = w.get_location(3, 2)
print(loc.location_number)
print(w.item_list[4].name)
"""
