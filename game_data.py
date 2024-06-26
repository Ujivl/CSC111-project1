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
        - start_position: starting location id of the item on the map
        - target_position: the location id where the item is supposed to end up in on the map
        - target_points: The amount of points you will get when u get the item to the target location
        - can_pick_up: a boolean indicating whether you can pick up an item or not

    Representation Invariants:
        - self.name != ""
    """

    name: str
    item_id: int
    start_position: int
    target_position: int
    target_points: int
    can_pick_up: bool = False

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
        if item_id in {1, 5, 7}:
            self.can_pick_up = True

    def return_points(self, location_id: int) -> int:
        """
        Returns the points in if the item reached its target location, then makes the points 0.

        >>> item = Item('book', 2, 1, 4, 50 )
        >>> samp_location_id = 4
        >>> Item.return_points(item, samp_location_id)
        50
        >>> item = Item('cheat sheet', 2, 1, 4, 50 )
        >>> test_location_id = 3
        >>> Item.return_points(item, test_location_id)
        0
        """
        if self.target_position == location_id:
            self.target_points, points = 0, self.target_points
            return points
        else:
            return 0


class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        - name: name of the location
        - item_ids: list of item ids in the location
        - brief_intro: a short introduction to the location
        - long_intro: a more detailed description of the location
        - location_number: a unique identifier for the location
        - been_here: a boolean indicating whether the player has visited the location
        - finished_quest: a boolean indicating whether the player has completed the quest in the location
    Representation Invariants:
        - location_number >= 0
        - self.name != ""
    """

    name: str
    item_ids: list[int]
    location_number: int
    brief_intro: str
    long_intro: str
    starting_dialogue: str
    ending_dialogue: str
    been_here: bool = False
    finished_quest: bool = False

    def __init__(self, name: str, location_number: int, item_ids: list[str], starting_dialogue: str,
                 ending_dialogue: str, brief_intro: str, long_intro: str) -> None:
        """Initialize a new location.
        """
        self.name = name
        self.item_ids = [int(x) for x in item_ids]
        self.location_number = location_number
        self.brief_intro = brief_intro
        self.long_intro = long_intro
        self.starting_dialogue = starting_dialogue
        self.ending_dialogue = ending_dialogue

    def print_info(self, items: list[str]) -> str:
        """
        Prints the introduction of the location when the player enters the location, can either print the long
        introduction if the player hasn't been to the location yet, or can print the brief introduction if the player
        has been to the location before. Also prints the npc text based on if the player has completed the quest and
        also prints the items in the location.

        """
        if self.finished_quest:
            dialogue = self.ending_dialogue
        else:
            dialogue = self.starting_dialogue

        items = "items in this location: " + (", ".join([items[x] for x in self.item_ids if x != -1]))

        if items == "items in this location: ":
            items = "There are currently no items in this location"

        if self.been_here:
            return f"{self.brief_intro} \n\n{dialogue} \n\n{items}"
        else:
            self.been_here = True
            return f"{self.long_intro} \n{dialogue} \n\n{items}"

    def add_item_id(self, item_id: int) -> None:
        """
        adds an item id to the location

        >>> location = Location('bahen', 6, ["5", "6"], "random brief intro", "random long intro", "", "")
        >>> location.add_item_id(3)
        >>> location.item_ids == [5, 6] + [3]
        True
        """
        self.item_ids.append(item_id)

    def remove_item_id(self, item_id: int) -> None:
        """
        removes an item id from a location, if the item exists

        >>> location = Location('bahen', 6, ["5", "6"], "random brief intro", "random long intro", "", "")
        >>> location.remove_item_id(3)
        >>> location.item_ids == [5, 6]
        True

        >>> location = Location('bahen', 6, ["5", "6"], "random brief intro", "random long intro", "", "")
        >>> location.remove_item_id(5)
        >>> location.item_ids == [6]
        True
        """
        if item_id in self.item_ids:
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
        - difficulty: a string value that determines the difficulty

    Representation Invariants:
        - self.max_moves > 0
    """
    x: int
    y: int
    victory: bool
    inventory: list[Item] = []
    score: int = 0
    difficulty: str = "easy"
    max_moves: int

    def __init__(self, x: int, y: int, difficulty: str) -> None:
        """
        Initializes a new Player at position (x, y).
        """

        self.x = x
        self.y = y
        self.inventory = []
        self.victory = False
        self.score = 0
        self.difficulty = difficulty
        if difficulty == "easy":
            self.max_moves = 50
        elif difficulty == "medium":
            self.max_moves = 30
        elif difficulty == "hard":
            self.max_moves = 15
        else:
            self.max_moves = 10

    def edit_inventory(self, item: Item, add_remove: str) -> bool:
        """
        adds or removes an item to the inventory, based on whether we want to remove the item "r" or add an item "a"
        returns false if the item was removed or added, else returns True.

        >>> player = Player(0, 0, 'easy')
        >>> itemss = Item('book', 2, 1, 4, 50)
        >>> player.edit_inventory(itemss, 'a')
        True
        >>> player.edit_inventory(itemss, 'r')
        True
        >>> player.inventory
        []
        >>> player.edit_inventory(itemss, 'r')
        False
        """
        if add_remove == "a":
            self.inventory.append(item)
            return True
        elif item in self.inventory and add_remove == "r":
            self.inventory.remove(item)
            return True
        else:
            return False

    def show_inventory(self) -> str:
        """
        prints out all the items in the inventory in a neat format.

        >>> player = Player(0, 0, 'easy')
        >>> item1 = Item('book', 2, 1, 4, 50)
        >>> item2 = Item('choco', 2, 1, 4, 50)
        >>> item3 = Item('cheat', 2, 1, 4, 50)
        >>> player.edit_inventory(item1, 'a')
        True
        >>> player.edit_inventory(item2, 'a')
        True
        >>> print(player.show_inventory())
        [book]
        [choco]
        <BLANKLINE>
        >>> player = Player(0, 0, 'easy')
        >>> player.show_inventory()
        'you currently have no items in your inventory'
        """
        if not self.inventory:
            return "you currently have no items in your inventory"
        else:
            return "".join([f"[{item.name}]\n" for item in self.inventory])


class Consumable(Item):
    """
    Sub-Class for the consumable items

    Instance Attributes:
        - properties: property of the consumable item
    Representation Invariants:
        - self.properties != []
    """
    properties: list[str]

    def __init__(self, name: str, item_id: int, properties: list[str],
                 start: int, target: int, target_points: int) -> None:
        """Initialize a new item.
        """

        super().__init__(name, item_id, start, target, target_points)
        self.properties = properties

    def apply_properties(self, p: Player) -> str:
        """
        Applies the properties of the item
        """
        if self.properties[0] == "moves":
            p.max_moves += int(self.properties[2])
            return self.properties[1]
        else:
            p.x = int(self.properties[2])
            p.y = int(self.properties[3])
            return self.properties[1]


class World:
    """A text adventure game world storing all location, item and map data.

    Instance Attributes:
        - map: a nested list representation of this world's map
        - locations_list: a list containing instances of Location inside the world
        - item_list: a list of items that is in the world.

    Representation Invariants:
        - len(self.map) > 0 and all(len(row) == len(map[0]) for row in self.map)
        - all(isinstance(location, Location) for location in self.locations_list)
    """
    map: list[list]
    locations_list: list[Location]
    item_list: list

    def __init__(self, map_data: TextIO, location_data: TextIO, items_data: TextIO) -> None:
        """
        Initialize a new World for a text adventure game, based on the data in the given open files.

        First while loop:
        parses through the locations.txt file and creates a location object for every location.
        the format for the location.txt file goes:

        [location number]-[location name]
        [list of items in location]
        [Starting quest dialogue]
        [Ending quest dialogue]
        [short description for location]
        [long description for location (can be multiple lines)]
        [descriptions end]      <---- This is to signify long descriptions end
        [----------]            <----- if this is locations end, the while loop breaks

        Second while loop:
        parses through the items.txt file and creates a item/consumable object for every item.
        the format for the items.txt file goes:

        [name of item]_[item id]
        [type of effect]_[effect application text]_[effect change value]  <-- This will just be - if its not consumable
        [Starting location id]
        [Ending location id]
        [----------]            <----- if this is items end, the while loop breaks
        """

        self.map = self.load_map(map_data)
        self.locations_list = []
        self.item_list = []
        ending_line = ""

        while ending_line != "locations end":
            l1 = self.read_file_line(location_data).split("-")
            detailed_description = ""
            location = Location(l1[1], int(l1[0]),
                                self.read_file_line(location_data).split(" "),
                                self.read_file_line(location_data),
                                self.read_file_line(location_data),
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
            consumable = self.read_file_line(items_data)
            if consumable == "-":
                item = Item(l1[0],
                            int(l1[1]),
                            int(self.read_file_line(items_data)),
                            int(self.read_file_line(items_data)),
                            int(self.read_file_line(items_data)))
            else:
                item = Consumable(l1[0],
                                  int(l1[1]),
                                  consumable.split("_"),
                                  int(self.read_file_line(items_data)),
                                  int(self.read_file_line(items_data)),
                                  int(self.read_file_line(items_data)))
            self.item_list.append(item)
            ending_line = self.read_file_line(items_data)

        map_data.close()
        location_data.close()
        items_data.close()

    def read_file_line(self, data: TextIO) -> str:
        """
        Returns a line of the data file without the newline (made for more neat code).
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


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (In PyCharm, select the lines below and press Ctrl/Cmd + / to toggle comments.)
    # You can use "Run file in Python Console" to run both pytest and PythonTA,
    # and then also test your methods manually in the console.
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120
    })
