import time
import json

class Pet:
    def __init__(self, name, age, species, health, hunger, happiness, energy, last_fed, last_played, last_slept):
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

    def __str__(self):
        return f"{self.name} is a {self.species} that is {self.age} years old. It has {self.health} health, {self.hunger} hunger, {self.happiness} happiness, and {self.energy} energy."

    def save(self):
        with open("pet.json", "w") as f:
            json.dump(self.__dict__, f)

    def load(self):
        with open("pet.json", "r") as f:
            data = json.load(f)
            self.name = data["name"]
            self.age = data["age"]
            self.species = data["species"]
            self.health = data["health"]
            self.hunger = data["hunger"]
            self.happiness = data["happiness"]
            self.energy = data["energy"]
            self.last_fed = data["last_fed"]
            self.last_played = data["last_played"]
            self.last_slept = data["last_slept"]