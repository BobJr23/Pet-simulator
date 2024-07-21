import time
import json
from plyer import notification
from typing import override
import random
import _curses as curses

PET_TO_ASCII = {
    "dog": r"""
    / \__
   (    @\___
   /         O
  /   (_____/
 /_____/   U
""",
    "cat": r"""
 /\_/\  
( o.o ) 
 > ^ <
""",
    "bird": r"""
   __
 <(o )___
   (  ._>
   """,
    "sick": r"""
    
    """,
}


class Pet:
    def __init__(
        self,
        name,
        age,
        species,
        health,
        hunger,
        happiness,
        energy,
        last_fed,
        last_played,
        last_slept,
        birth_time,
    ):
        self.name = name
        self.age = age
        self.species = species
        self.health = health
        self.hunger = hunger
        self.happiness = happiness
        self.energy = energy
        self.last_fed = last_fed
        self.last_played = last_played
        self.last_slept = last_slept
        self.birth_time = birth_time

    def feed(self):
        self.hunger = 100
        self.last_fed = time.time()
        print("Thanks for the food!")

    def play(self):
        self.happiness = 100
        self.energy -= 10
        self.last_played = time.time()

    def sleep(self):
        self.energy = 100
        self.last_slept = time.time()

    def greeting(self):
        print("Hello! My name is " + self.name + ".")

    def update(self):
        self.hunger -= (time.time() - self.last_fed) / 1000
        self.happiness -= (time.time() - self.last_played) / 1000
        self.energy -= (time.time() - self.last_slept) / 1000
        # age in hours
        self.age = (time.time() - self.birth_time) / 3600  # Age in hours
        if self.hunger < 50 or self.happiness < 50 or self.energy < 50:
            self.health -= 1  # Health degrades if basic needs are not met
            self.notify_unwell()
            self.check_health()

    def check_health(self):

        if self.health <= 75:
            print(f"{self.name} is sick.")
            self.notify_unwell()
        else:
            print("Your pet is healthy. 😊")
            print(PET_TO_ASCII[pet.species])

    def notify_unwell(self):
        notification.notify(
            title="Pet Simulator",
            message=f"{self.name} is hungry, unhappy, or tired!",
            app_name="Pet Simulator",
            timeout=10,
        )

    def __str__(self):
        return f"{self.name} is a {self.species} that is {str(int(self.age))} hours old. It has {self.health} health, {self.hunger} hunger, {self.happiness} happiness, and {self.energy} energy."


class Dog(Pet):
    def __init__(
        self,
        name,
        age,
        health,
        hunger,
        happiness,
        energy,
        last_fed,
        last_played,
        last_slept,
        birth_time,
    ):
        super().__init__(
            name,
            age,
            "dog",
            health,
            hunger,
            happiness,
            energy,
            last_fed,
            last_played,
            last_slept,
            birth_time,
        )

    @override
    def greeting(self):
        print(f"{self.name} says: Woof!")


class Cat(Pet):
    def __init__(
        self,
        name,
        age,
        health,
        hunger,
        happiness,
        energy,
        last_fed,
        last_played,
        last_slept,
        birth_time,
    ):
        super().__init__(
            name,
            age,
            "cat",
            health,
            hunger,
            happiness,
            energy,
            last_fed,
            last_played,
            last_slept,
            birth_time,
        )

    @override
    def greeting(self):
        print(f"{self.name} says: Meow!")


class Hamster(Pet):
    def __init__(
        self,
        name,
        age,
        health,
        hunger,
        happiness,
        energy,
        last_fed,
        last_played,
        last_slept,
        birth_time,
    ):
        super().__init__(
            name,
            age,
            "hamster",
            health,
            hunger,
            happiness,
            energy,
            last_fed,
            last_played,
            last_slept,
            birth_time,
        )

    @override
    def greeting(self):
        print(f"{self.name} says: Squeak!")


class PetManager:
    def __init__(self):
        self.pets = []
        self.load()

    def add_pet(self, pet):
        self.pets.append(pet)

    def save(self):
        pets_data = [pet.__dict__ for pet in self.pets]
        with open("pets.json", "w") as f:
            json.dump(pets_data, f)

    def load(self):
        with open("pets.json", "r") as f:
            pets_data = json.load(f)
            self.pets = [Pet(**data) for data in pets_data]


# Able to purchase pets
class PetMarket:
    def __init__(self):
        self.pets = []

    def add_pet(self, pet):
        self.pets.append(pet)

    def list_pets(self):
        for i, pet in enumerate(self.pets):
            print(f"{i + 1}: {pet.name} the {pet.species}")

    def purchase_pet(self, index: int):
        if 0 < index <= len(self.pets):
            return self.pets.pop(index + 1)
        else:
            print("Invalid selection.")
            return None

    def refresh(self):
        pass


def process_command(command):
    if command == "exit":
        manager.save()
        exit()
    command, name = command.split(" ")

    pet = next(pet for pet in manager.pets if pet.name.lower() == name.lower())
    if command == "feed":
        pet.feed()
        print(f"You have fed {pet.name}.")
    elif command == "play":
        pet.play()
        print(f"You played with {pet.name}.")
    elif command == "sleep":
        pet.sleep()
        print(f"{pet.name} is now sleeping.")
    elif command == "status":
        print(pet)
    else:
        print("Unknown command. Try 'feed', 'play', 'sleep', or 'status'.")


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


def display_pets(stdscr):

    stdscr.clear()

    # Get the height and width of the screen
    height, width = stdscr.getmaxyx()

    pets_per_row = 2

    # Calculate spacing based on the screen width and number of pets per row
    spacing_x = width // pets_per_row

    # Iterate over each pet and its stats
    for index, (pet) in enumerate(manager.pets):
        # Calculate pet's position in the grid
        row = index // pets_per_row
        col = index % pets_per_row
        start_y = (
            row * (height // len(manager.pets)) + 1
        )  # Start a bit down from the top
        start_x = col * spacing_x + 1  # Start a bit in from the left

        # Display the pet ASCII art
        pet_lines = PET_TO_ASCII[pet.species].split("\n")
        for i, line in enumerate(pet_lines):
            stdscr.addstr(start_y + i, start_x, line)

        # Display the pet's stats below the ASCII art
        stats_line = f"{pet.name}, Age: {pet.age}, Health: {pet.health}, Hunger: {pet.hunger}, Happiness: {pet.happiness}, Energy: {pet.energy}"
        stdscr.addstr(start_y + len(pet_lines) + 1, start_x, stats_line)

    # stdscr.refresh()
    stdscr.getch()
    return height, width


if __name__ == "__main__":
    manager = PetManager()

    print(manager.pets)
    r = curses.initscr()
    h, w = display_pets(r)
    curses.endwin()
    print(h, w)
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
