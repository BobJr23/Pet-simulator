import json
from pets import Pet
from time import time


class PetManager:
    def __init__(self):
        self.pets = []

    def add_pet(self, pet):
        self.pets.append(pet)

    def save(self, filename, money, next_save):
        pets_data = [pet.__dict__ for pet in self.pets] + [
            {"money": money, "next_save": next_save}
        ]
        print(pets_data)
        with open(f"{filename}.json", "w") as f:
            json.dump(pets_data, f)

    def load(self, filename):
        with open(f"{filename}.json", "r") as f:
            pets_data = json.load(f)
            info = pets_data.pop(-1)
            money = info["money"]
            next_save = info["next_save"]
            self.pets = [Pet(**data) for data in pets_data]
            return money, next_save


# test manager
if __name__ == "__main__":
    p = PetManager()
    p.add_pet(Pet("Rover", 0, "dog", 100, 100, 100, 100, 100, 100, 100, 100))
    p.add_pet(Pet("Whiskers", 0, "cat", 100, 100, 100, 100, 100, 100, 100, 100))
    p.save("test")
    p.load("test")
    print(p.pets)
    print(p.money)
