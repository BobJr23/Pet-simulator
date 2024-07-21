import json
from pets import Pet


class PetManager:
    def __init__(self):
        self.pets = []

    def add_pet(self, pet):
        self.pets.append(pet)

    def save(self, filename):
        pets_data = [pet.__dict__ for pet in self.pets]
        with open(f"{filename}.json", "w") as f:
            json.dump(pets_data, f)

    def load(self, filename):
        with open(f"{filename}.json", "r") as f:
            pets_data = json.load(f)
            self.pets = [Pet(**data) for data in pets_data]
