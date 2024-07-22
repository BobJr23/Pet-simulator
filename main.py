import time
from pets import Dog, Cat, Hamster, PET_TO_ASCII, localtime, strftime
from pet_manager import PetManager
from pet_market import PetMarket
import _curses as curses
from _curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
import os


def setup():
    # Use to speed up testing
    # new_account = False
    # filename = "pets"
    if "c" in input("Create new account or load saved? (C/L): ").lower():
        new_account = True
        filename = input("Enter a name for your save: ")
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
        manager.save(filename)
        manager.load(filename)
    else:
        manager.load(filename)

    return manager, filename


def process_command(command):

    command, name = command.split(" ")

    pet = next(pet for pet in manager.pets if pet.name.lower() == name.lower())
    # switch
    match int(command):
        case 0:
            pet.feed()
            return f"You have fed {pet.name}.\n{pet.greeting()}"
        case 1:
            pet.play()
            return f"You have played with {pet.name}.\n{pet.greeting()}"
        case 2:
            pet.sleep()
            return f"{pet.name} is now sleeping.\n{pet.greeting()}"
        case 3:
            return "SHOP"
        case _:
            return "Invalid command, make sure a command and pet name are colored in"
    # if command == "feed":
    #     pet.feed()
    #     print(f"You have fed {pet.name}.")
    # elif command == "play":
    #     pet.play()
    #     print(f"You played with {pet.name}.")
    # elif command == "sleep":
    #     pet.sleep()
    #     print(f"{pet.name} is now sleeping.")
    # elif command == "status":
    #     print(pet)
    # else:
    #     print("Unknown command. Try 'feed', 'play', 'sleep', or 'status'.")


# TODO: implement curses for better UI


def add_pet(name, species):
    if species == "dog":
        pet = Dog(
            name,
            0,
            100,
            100,
            100,
            100,
            time.time(),
            time.time(),
            time.time(),
            time.time(),
        )
    elif species == "cat":
        pet = Cat(
            name,
            0,
            100,
            100,
            100,
            100,
            time.time(),
            time.time(),
            time.time(),
            time.time(),
        )
    elif species == "hamster":
        pet = Hamster(
            name,
            0,
            100,
            100,
            100,
            100,
            time.time(),
            time.time(),
            time.time(),
            time.time(),
        )
    else:
        print("Unknown species.")
        return
    manager.add_pet(pet)
    print(f"Added {name} the {species} to your pets.")
    manager.save()


def display_pets(stdscr: curses.window):
    shop = PetMarket()
    shopping = False
    key = None
    selected_pet = 0
    selected_command = 0
    color = curses.color_pair(1)
    status = "Press enter to select a command for the selected pet Up-down arrow keys for commands, Left-right arrow keys for pet selection."
    COMMANDS = ["feed", "play", "sleep", "shop"]
    COMMANDS_SHOP = ["buy", "refresh"]
    pets_per_row = 5
    height, width = stdscr.getmaxyx()
    spacing_x = width // pets_per_row
    pet_list = manager.pets
    while True:
        stdscr.clear()

        # Calculate spacing based on the screen width and number of pets per row
        stdscr.addstr(1, 0, status)

        # Iterate over each pet and its stats
        for index, (pet) in enumerate(pet_list):
            if index == selected_pet:
                color = curses.color_pair(2)
                stdscr.addstr(0, 0, f"Selected: {pet.name}")

            # Calculate pet's position in the grid
            row = index // pets_per_row
            col = index % pets_per_row
            start_y = (
                row * (height // len(pet_list)) + 5
            )  # Start a bit down from the top
            start_x = col * spacing_x + 15  # Start a bit in from the left

            # Display the pet ASCII art
            pet_lines = PET_TO_ASCII[pet.species].split("\n")
            for i, line in enumerate(pet_lines):
                stdscr.addstr(start_y + i, start_x, line, color)

        if shopping:
            ...
        else:

            i = 0

            for name, x in pet.__dict__.items():
                if index == selected_pet:
                    color = curses.color_pair(1)
                i += 1
                stdscr.addstr(
                    start_y + len(pet_lines) + i, start_x, f"{name}: {x}", color
                )
            color = curses.color_pair(1)
            for i, command in enumerate(COMMANDS):
                if i == selected_command:
                    color = curses.color_pair(3)
                stdscr.addstr(start_y + i, 0, command, color)
                color = curses.color_pair(1)
        key = stdscr.getch()

        if key == KEY_LEFT:
            selected_pet -= 1
        elif key == KEY_RIGHT:
            selected_pet += 1
        elif key == KEY_UP:
            selected_command -= 1
        elif key == KEY_DOWN:
            selected_command += 1
        # ENTER KEY
        elif key == 10:
            if selected_command == 3:
                shopping = True
                shop.refresh()
                pet_list = shop.pets
            if selected_command == 4:
                shopping = False
                pet_list = manager.pets

            status = process_command(
                f"{selected_command} {manager.pets[selected_pet].name}"
            )
        elif key == ord("q"):
            break
        stdscr.refresh()

    return height, width


if __name__ == "__main__":

    manager, file = setup()

    r = curses.initscr()
    curses.curs_set(0)
    r.keypad(True)
    curses.start_color()

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    display_pets(r)
    manager.save(file)
    curses.endwin()

    # Use setup if just starting
    # setup()
    exit()
