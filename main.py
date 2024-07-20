import time
import json
from plyer import notification

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
   """}


class Pet:
    def __init__(self, name, age, species, health, hunger, happiness, energy, last_fed, last_played, last_slept,
                 birth_time):
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

    def play(self):
        self.happiness = 100
        self.energy -= 10
        self.last_played = time.time()

    def sleep(self):
        self.energy = 100
        self.last_slept = time.time()

    def update(self):
        self.hunger -= (time.time() - self.last_fed) / 1000
        self.happiness -= (time.time() - self.last_played) / 1000
        self.energy -= (time.time() - self.last_slept) / 1000

        self.age = (time.time() - self.birth_time) / 31536000  # Age in years
        if self.hunger < 50 or self.happiness < 50 or self.energy < 50:
            self.health -= 1  # Health degrades if basic needs are not met
            self.notify()

    def notify(self):
        notification.notify(
            title="Pet Simulator",
            message=f"{self.name} is hungry, unhappy, or tired!",
            app_name="Pet Simulator",
            timeout=10
        )

    def __str__(self):
        return f"{self.name} is a {self.species} that is {self.age} years old. It has {self.health} health, {self.hunger} hunger, {self.happiness} happiness, and {self.energy} energy."


class PetManager:
    def __init__(self):
        self.pets = []

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


def process_command(command):
    pass


if __name__ == "__main__":
    manager = PetManager()
    dog = Pet("Pedro", 5, "dog", 100, 100, 100, 100, time.time(), time.time(), time.time(), time.time())
    cat = Pet("Whiskers", 3, "cat", 100, 100, 100, 100, time.time(), time.time(), time.time(), time.time())
    manager.add_pet(dog)
    manager.add_pet(cat)
    manager.save()
    manager.load()
    for pet in manager.pets:
        pet.feed()
        pet.play()
        pet.sleep()
        pet.update()
        print(pet)
        print(PET_TO_ASCII[pet.species])

    while True:

        for pet in manager.pets:
            command = input("What is your command?")
            process_command(command)
            pet.update()
            print(pet)
            print(PET_TO_ASCII[pet.species])
            manager.save()
