import json
from pets import Pet


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
