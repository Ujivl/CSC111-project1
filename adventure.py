from pygame import mixer
from game_data import World, Player, Consumable


def format_and_print(inside_text: str) -> None:
    """
    This function puts everything in between two seperator lines. This improves game readability.
    """
    print(f"------------------------------------------------\n{inside_text}"
          f"\n------------------------------------------------")


if __name__ == "__main__":
    # initializes world object
    w = World(open("map.txt"), open("locations.txt"), open("items.txt"))
    # directions dictionary: contains a vector increment by 1 for all directions
    directions = {"north": (0, -1), "east": (1, 0), "south": (0, 1), "west": (-1, 0)}
    #  list of possible actions
    possible_actions = ["look", "inventory", "score", "quit", "pick up", "drop", "use"]
    # gets the winning location object. (Exam hall)
    winning_location = w.get_location(1, 4)
    #  gets a set of the items required to win (lucky pen, cheat sheet, t-card)
    winning_items = {item for item in w.item_list if item.target_position == winning_location.location_number}
    #  a dictionary of item ids where the keys are items that
    dependent_items = {7: 0, 6: 2, 3: 6, 5: 5}
    items_in_world = [item.name for item in w.item_list]
    choice = ""
    print("\n\n\n\n\n\n\n\n\n\n\n\n")
    format_and_print("HELLO! WELCOME TO OUR GAME, in order to be victorious, you must attain the 3 items needed for\n"
                     "you to pass your exam, travel through campus to find your items before you run out of moves!\n"
                     "You can go to any location using the (go [direction]) command. If you want to know your score,\n"
                     "use the (score) command. You are able to access your inventory at any point in the game using\n"
                     "the (inventory) command. If you want to pick up items, use the (pick up [item name]) command.\n"
                     "But remember, There items you might not be eligible to pick up! There is also the \n"
                     "(drop [item name]) command, which you can use to fulfill npc quests. Some items are usable, so\n"
                     "make sure to take advantage of that by using the (use [item name]) command. Lastly, if you've \n"
                     "had enough of our game, you can use the (quit) command to exit the game. If you are ready to \n"
                     "continue, pick your difficulty: [easy] [medium] [hard] [impossible]")

    while choice not in ["easy", "medium", "hard", "impossible"]:
        choice = input("Enter action: ").lower()
        if choice not in ["easy", "medium", "hard", "impossible"]:
            format_and_print("thats not what we asked you to type!")

    p = Player(2, 1, choice)

    print("\n\n\n\n\n\n\n\n\n\n\n\n")
    format_and_print("LETS BEGIN!")

    mixer.init()
    mixer.music.load('stranger-things-124008.mp3')
    mixer.music.set_volume(0.2)
    mixer.music.play(-1)

    location = w.get_location(p.x, p.y)
    format_and_print(f"YOU ARE CURRENTLY AT {location.name}. (You have {p.max_moves} moves left)"
                     f"\n{location.print_info(items_in_world)}")

    while not p.victory:
        location, past_location = w.get_location(p.x, p.y), location
        if not location.been_here:
            p.score += 5

        if location != past_location:
            format_and_print(f"YOU ARE CURRENTLY AT {location.name}. (You have {p.max_moves} moves left)"
                             f"\n{location.print_info(items_in_world)}")

        if location == winning_location and all(item.item_id in location.item_ids for item in winning_items):
            p.victory = True
            mixer.music.stop()
            break

        if location.location_number == 3 and not location.item_ids:
            location.finished_quest = True

        choice = input("\nEnter action: ").lower()
        print("\n")
        choice_in_possible_actions = any([actions in choice for actions in possible_actions])

        if p.max_moves == 0:
            format_and_print("GAME OVER: You have exceeded the maximum number of moves.")
            mixer.music.stop()
            break

        if "go " in choice and choice[3:] in directions:
            if w.get_location(p.x + directions[choice[3:]][0], p.y + directions[choice[3:]][1]) is None:
                format_and_print("That way is blocked")
            else:
                p.max_moves -= 1
                p.x += directions[choice[3:]][0]
                p.y += directions[choice[3:]][1]

        elif "go " in choice:
            format_and_print("invalid direction")

        elif choice_in_possible_actions and choice == "quit":
            format_and_print("THANK YOU FOR PLAYING!!")
            mixer.music.stop()
            break

        elif choice_in_possible_actions and choice == "look":
            location.been_here = False
            format_and_print(f"YOU ARE CURRENTLY AT {location.name}. (You have {p.max_moves} moves left)"
                             f"\n{location.print_info(items_in_world)}")

        elif choice_in_possible_actions and choice == "inventory":
            format_and_print(p.show_inventory())

        elif choice_in_possible_actions and choice == "score":
            format_and_print(f"SCORE: {p.score}")

        elif choice_in_possible_actions and "pick up" in choice and choice[8:] in items_in_world:
            picked_up_item = False

            for item_id in location.item_ids:
                if item_id == 3 and p.score >= 10:
                    w.item_list[item_id].can_pick_up = True
                    p.score -= 10
                elif item_id == 3:
                    w.item_list[item_id].can_pick_up = False

                if item_id == -1 or picked_up_item:
                    continue

                elif choice[8:] == w.item_list[item_id].name and w.item_list[item_id].can_pick_up:
                    picked_up_item = p.edit_inventory(w.item_list[item_id], "a")
                    format_and_print(f"you have picked up the following item: {choice[8:]}")
                    location.remove_item_id(item_id)

            if not picked_up_item:
                format_and_print("This item is not available to pick up here: you might not be eligible to pick it up")

        elif choice_in_possible_actions and "drop" in choice and choice[5:] in items_in_world:
            item_id = items_in_world.index(choice[5:])
            dropped_item = p.edit_inventory(w.item_list[item_id], "r")

            if dropped_item:
                location.add_item_id(item_id)
                format_and_print(f"you have dropped the following item: {choice[5:]}")

                if location.location_number == w.item_list[item_id].target_position and item_id in dependent_items:
                    location.finished_quest = True
                    w.item_list[dependent_items[item_id]].can_pick_up = True
                    location.remove_item_id(item_id)
                elif location.location_number == w.item_list[item_id].target_position:
                    location.finished_quest = True
                p.score += w.item_list[item_id].return_points(location.location_number)

            else:
                format_and_print("you do not have that item in your inventory")

        elif choice_in_possible_actions and "use" in choice and choice[4:] in items_in_world:
            item_id = items_in_world.index(choice[4:])
            if isinstance(w.item_list[item_id], Consumable) and w.item_list[item_id] in p.inventory:
                format_and_print(w.item_list[item_id].apply_properties(p))
                p.edit_inventory(w.item_list[item_id], "r")
            else:
                format_and_print("This item is not usable")

        elif location.location_number == 6 and not location.finished_quest:
            if choice == "lemon":
                format_and_print("The strange man says: mmmmmm delicious and sour! you really do know my favourite\n"
                                 " fruit i'll leave this concoction here for you, drinking it will take you where you\n"
                                 "need to be!!!!!")
                w.item_list[4].can_pick_up = True
                location.finished_quest = True
            else:
                format_and_print("the strange man says: 'WRONG ANSWER!!!! HEHE HAHA'")

        elif choice_in_possible_actions:
            format_and_print("invalid action: you may have mispelled your action")

        else:
            format_and_print("what are you yappin about bro")

    if p.victory:
        print("\n\n\n\n")
        format_and_print("CONGRATULAIONS!!! you managed to write the exam in time and ace it!")


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
