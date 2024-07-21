import time
from time import strftime, localtime
import json
from plyer import notification
from typing import override
import random
from pets import Dog, Cat, Hamster, Pet, PET_TO_ASCII
from pet_manager import PetManager
from pet_market import PetMarket
import _curses as curses
from _curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN


def process_command(command):

    command, name = command.split(" ")

    pet = next(pet for pet in manager.pets if pet.name.lower() == name.lower())
    # switch
    match int(command):
        case 1:
            pet.feed()
            return f"You have fed {pet.name}.\n{pet.greeting()}"
        case 2:
            pet.play()
            return f"You have played with {pet.name}.\n{pet.greeting()}"
        case 3:
            pet.sleep()
            return f"{pet.name} is now sleeping.\n{pet.greeting()}"
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


def setup():
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
    manager.save()
    manager.load()


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
    key = None
    selected_pet = 0
    selected_command = 0
    color = curses.color_pair(1)
    status = "Press enter to select a command for the selected pet."
    COMMANDS = ["feed", "play", "sleep"]
    while True:
        stdscr.clear()
        stdscr.addstr(1, 0, status)
        height, width = stdscr.getmaxyx()

        pets_per_row = 5

        # Calculate spacing based on the screen width and number of pets per row
        spacing_x = width // pets_per_row

        # Iterate over each pet and its stats
        for index, (pet) in enumerate(manager.pets):
            if index == selected_pet:
                color = curses.color_pair(2)
                stdscr.addstr(0, 0, f"Selected: {pet.name}")

            # Calculate pet's position in the grid
            row = index // pets_per_row
            col = index % pets_per_row
            start_y = (
                row * (height // len(manager.pets)) + 1
            )  # Start a bit down from the top
            start_x = col * spacing_x + 15  # Start a bit in from the left

            # Display the pet ASCII art
            pet_lines = PET_TO_ASCII[pet.species].split("\n")
            for i, line in enumerate(pet_lines):
                stdscr.addstr(start_y + i, start_x, line, color)

            # Display the pet's stats below the ASCII art
            stats_line = f"{pet.name}\nAge: {(pet.age + 0.5) // 1} hours old\nHealth: {pet.health}\nHunger: {pet.hunger}\nHappiness\n{pet.happiness}\nEnergy: {pet.energy}"
            # stdscr.addstr(start_y + len(pet_lines) + 1, start_x, stats_line, color)
            i = 0

            for name, x in pet.__dict__.items():
                i += 1
                stdscr.addstr(
                    start_y + len(pet_lines) + i, start_x, f"{name}: {x}", color
                )
            if index == selected_pet:
                color = curses.color_pair(1)
        for i, command in enumerate(COMMANDS):
            if i == selected_command:
                color = curses.color_pair(3)
            stdscr.addstr(4 + i, 0, command, color)
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
            status = process_command(
                f"{selected_command} {manager.pets[selected_pet].name}"
            )
        elif key == ord("q"):
            break
        stdscr.refresh()

    return height, width


if __name__ == "__main__":
    manager = PetManager()

    r = curses.initscr()
    curses.curs_set(0)
    r.keypad(True)
    curses.start_color()

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    display_pets(r)
    curses.endwin()

    # Use setup if just starting
    # setup()
    exit()

    for pet in manager.pets:
        pet.feed()
        pet.play()
        pet.sleep()
        pet.update()
        print(pet)
        print(PET_TO_ASCII[pet.species])

    while True:

        process_command(
            input(
                'What is your command "(feed, play, sleep, status) + name" or "exit" \n > '
            )
        )
