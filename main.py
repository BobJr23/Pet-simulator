import time
from pets import Dog, Cat, Hamster, PET_TO_ASCII, localtime, strftime
from pet_manager import PetManager
from pet_market import PetMarket
import _curses as curses
from _curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
import os
import random


def setup():
    # Use to speed up testing
    # new_account = False
    # filename = "pets"

    if "c" in input("Create new account or load saved? (C/L): ").lower():
        new_account = True
        filename = input("Enter a name for your save: ")
        money = 100
    else:
        new_account = False

        filename = input(
            "Enter the name of your save. The options are: "
            + "".join(
                [
                    f'\n> "{x[:-5]}"'
                    + " last save: "
                    + strftime("%Y-%m-%d %I:%M", localtime(os.stat(x).st_mtime))
                    for x in os.listdir()
                    if x.endswith(".json")
                ]
            )
            + "\n > "
        )

    manager = PetManager()
    if new_account:
        dog = Dog(
            "Pedro",
            5,
            100,
            100,
            100,
            100,
            time.time(),
            time.time(),
            time.time(),
            time.time(),
        )
        cat = Cat(
            "Whiskers",
            3,
            100,
            100,
            100,
            100,
            time.time(),
            time.time(),
            time.time(),
            time.time(),
        )
        manager.add_pet(dog)
        manager.add_pet(cat)
        manager.save(filename, 100, time.time() + 86400)
        next_save = time.time() + 86400
        manager.load(filename)
    else:
        money, next_save = manager.load(filename)

    return (manager, filename, money, next_save)


def process_command(command, shop: PetMarket, pet_list: list, stdscr):

    command, name = command.split(" ")

    pet = next(pet for pet in pet_list if pet.name.lower() == name.lower())
    # switch
    match int(command):
        case -2:
            pet = shop.purchase_pet(pet_list.index(pet))
            if pet != None:
                manager.add_pet(pet)
                return "You bought " + pet.name, pet_list
            else:
                return "Not enough money.", pet_list
        case -1:
            shop.refresh()
            pet_list = shop.pets
            return "Refreshed shop.", pet_list
        case 0:
            pet.feed()
            return f"You have fed {pet.name}.\n{pet.greeting()}", pet_list
        case 1:
            pet.play()
            return f"You have played with {pet.name}.\n{pet.greeting()}", pet_list
        case 2:
            pet.sleep()
            return f"{pet.name} is now sleeping.\n{pet.greeting()}", pet_list
        case 3:
            return "SHOP", pet_list
        case 4:
            name = get_user_input(stdscr, "Enter a new pet name: ")
            pet.name = name
            return "Name successfully changed to " + name, pet_list
        case 5:
            change_display_options(stdscr)
            return "UI settings changed", pet_list
        case 6:
            if shop.money >= 15:
                shop.money -= 15
                roll = random.randint(1, 25)
                shop.money += roll
                return f"You rolled a {roll}", pet_list
            else:
                return "Not enough money", pet_list
        case _:
            return (
                "Invalid command, make sure a command and pet name are colored in",
                pet_list,
            )


def get_user_input(stdscr, prompt):
    curses.echo()  # Enable echoing of characters typed by the user
    stdscr.clear()
    stdscr.addstr(0, 0, prompt)
    stdscr.refresh()
    input_str = stdscr.getstr(1, 2)  # Get user input from the second line
    curses.noecho()  # Disable echoing back to the screen
    return input_str.decode("utf-8")


# EDIT UI OPTIONS TODO
def change_display_options(stdscr):
    option = get_user_input(stdscr, "What option do you want to change? (Color, )\n> ")
    match option:

        case "color":

            color_1 = get_user_input(
                stdscr,
                "Enter a foreground color among "
                + ", ".join(COLORS_DICT.keys())
                + "\n> ",
            )

            stdscr.refresh()
            color_2 = get_user_input(
                stdscr,
                "Enter a background color among "
                + ", ".join(COLORS_DICT.keys())
                + "\n> ",
            )
            curses.init_pair(1, COLORS_DICT[color_1], COLORS_DICT[color_2])
            curses.noecho()

        # MORE LATER

    pass


# Main method
def display_pets(stdscr: curses.window, money, next_save):
    # Daily login bonus coins
    if next_save < time.time():
        money += 50
        next_save = time.time() + 86400
    shop = PetMarket(money)
    shopping = False
    key = None
    selected_pet = 0
    selected_command = 0
    color = curses.color_pair(1)
    status = "Press enter to select a command for the selected pet Up-down arrow keys for commands, Left-right arrow keys for pet selection."
    command_list = ["feed", "play", "sleep", "shop", "rename", "UI settings", "roll"]
    command_offset = 0
    pets_per_row = 5
    height, width = stdscr.getmaxyx()
    spacing_x = width // pets_per_row
    pet_list = manager.pets
    while True:
        stdscr.clear()

        stdscr.addstr(1, 0, status)
        stdscr.addstr(2, width // 2 - 4, f"Money: ${shop.money}")

        if next_save < time.time():
            money += 50
            next_save = time.time() + 86400
        diff = next_save - time.time()
        stdscr.addstr(
            2,
            width // 2 + 10,
            f"Next login bonus in: {int(diff // 3600)}:{int(diff % 3600 // 60)}:{int(diff % 60)}",
        )
        # Iterate over each pet and its stats
        i = 0
        color = curses.color_pair(1)
        for i, command in enumerate(command_list):
            if i == selected_command:
                color = curses.color_pair(3)
            stdscr.addstr(5 + i, 0, command, color)
            color = curses.color_pair(1)

        for index, (pet) in enumerate(pet_list):
            if index == selected_pet:
                color = curses.color_pair(2)
                stdscr.addstr(0, 0, f"Selected: {pet.name}")

            # Calculate pet's position in the grid
            row = index // pets_per_row
            col = index % pets_per_row
            start_y = (
                row * (height // len(pet_list)) * 2 + 5
            )  # Start a bit down from the top
            start_x = col * spacing_x + 15  # Start a bit in from the left

            # Display the pet ASCII art

            pet_lines = PET_TO_ASCII[pet.species].split("\n")

            for i, line in enumerate(pet_lines):
                stdscr.addstr(start_y + i, start_x, line, color)

            for name, x in pet.__dict__.items():
                if index == selected_pet:
                    color = curses.color_pair(1)
                i += 1
                stdscr.addstr(
                    start_y + len(pet_lines) + i, start_x, f"{name}: {x}", color
                )

        key = stdscr.getch()

        if key == KEY_LEFT:
            selected_pet = max(0, selected_pet - 1)
        elif key == KEY_RIGHT:
            selected_pet = min(len(pet_list) - 1, selected_pet + 1)
        elif key == KEY_UP:
            selected_command = max(0, selected_command - 1)
        elif key == KEY_DOWN:
            selected_command = min(len(command_list) - 1, selected_command + 1)
        # ENTER KEY
        elif key == 10:

            if selected_command == 3 and not shopping:
                selected_command = 0
                shopping = True
                shop.refresh()
                command_offset = -3
                command_list = ["return", "buy", "refresh"]
                pet_list = shop.pets
            elif selected_command == 0 and shopping:
                selected_command = 0
                shopping = False
                pet_list = manager.pets
                command_offset = 0
                command_list = [
                    "feed",
                    "play",
                    "sleep",
                    "shop",
                    "rename",
                    "UI settings",
                    "roll",
                ]
            else:
                status, pet_list = process_command(
                    f"{selected_command + command_offset} {pet_list[selected_pet].name}",
                    shop,
                    pet_list,
                    stdscr,
                )
        elif key == ord("q"):
            break
        stdscr.refresh()

    return shop.money, next_save


if __name__ == "__main__":
    COLORS_DICT = {
        "red": curses.COLOR_RED,
        "green": curses.COLOR_GREEN,
        "blue": curses.COLOR_BLUE,
        "black": curses.COLOR_BLACK,
        "white": curses.COLOR_WHITE,
        "cyan": curses.COLOR_CYAN,
        "magenta": curses.COLOR_MAGENTA,
        "yellow": curses.COLOR_YELLOW,
    }
    manager, file, money_1, ns = setup()

    r = curses.initscr()
    curses.curs_set(0)
    r.keypad(True)
    curses.start_color()

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_WHITE)
    money_1, ns = display_pets(r, money_1, ns)
    manager.save(file, money_1, ns)
    print(money_1)
    curses.endwin()

    # Use setup if just starting
    # setup()
    exit()
