"""

TO DO LIST:

- dropping items and picking up items (BASE GAME)
    - when giving descriptions there should also be a line that says what items are in that location
- score addition, when visiting a new place score should be increased by some value (BASE GAME)
    - this should also include the fetch quest rewards (we might have to change gold to score just to simplify)
- limited amount of moves, this should go down by one when the player changes location (BASE GAME)
    - maybe add a time command that translates amount of moves to time to tell the player how long they have
- lose when amount of moves reach zero, break out of while loop (BASE GAME)

- Music (enchancements)
- characters (enhancements)
    - each character should have a quest they can give u (maybe we can add a character that gives u an item that's fake)
    - add talk command to each character in the location that will activate the quest line
    - add a quests command that tracks all quests (optional)
- consumables (enchancements)


"""

from game_data import World, Player  # , Item, Location,
# from pygame import mixer

if __name__ == "__main__":
    w = World(open("map.txt"), open("locations.txt"), open("items.txt"))
    p = Player(2, 2)  # TODO: file dependent
    directions = {"north": (0, -1), "east": (1, 0), "south": (0, 1), "west": (-1, 0)}
    possible_actions = ["look", "inventory", "score", "quit"]
    winning_location = w.get_location(2, 4)  # TODO: file dependent
    winning_items = {item for item in w.item_list if item.target_position == winning_location.location_number}
    p.edit_inventory(w.item_list[0], "a")
    p.edit_inventory(w.item_list[1], "a")  # just adding two items to inventory to test stuff
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
            check_been_here = location.print_info()
            print("------------------------------------------------")
        if not location.been_here:
            location.been_here = True
            p.score += 1
        if location == winning_location and p.check_required_items(winning_items):  # TODO: change this so it checks item location once the player drops
            p.victory = True
            break
        choice = input("\nEnter action: ").lower()
        print("\n")

        if p.max_moves == 0:
            print("You have exceeded the maximum number of moves.")
            break

        if "go " in choice and choice[3:] in directions.keys():
            if w.get_location(p.x + directions[choice[3:]][0], p.y + directions[choice[3:]][1]) is None:
                print("That way is blocked \n")
            else:
                p.max_moves -= 1
                p.x += directions[choice[3:]][0]
                p.y += directions[choice[3:]][1]
        elif "go " in choice:
            print("invalid direction\n")
        elif choice in possible_actions or choice in location.available_actions():  # TODO: add available_actions()
            p.max_moves -= 1
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
