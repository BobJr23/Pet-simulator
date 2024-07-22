import json
from pets import Pet


class PetManager:
    def __init__(self):
        self.pets = []

    def add_pet(self, pet):
        self.pets.append(pet)

    def save(self, filename, money):
        pets_data = [pet.__dict__ for pet in self.pets] + [{"money": money}]
        print(pets_data)
        with open(f"{filename}.json", "w") as f:
            json.dump(pets_data, f)

    def load(self, filename):
        with open(f"{filename}.json", "r") as f:
            pets_data = json.load(f)
            money = pets_data.pop(-1)["money"]
            self.pets = [Pet(**data) for data in pets_data]
            return money


# test manager
if __name__ == "__main__":
    p = PetManager()
    p.add_pet(Pet("Rover", 0, "dog", 100, 100, 100, 100, 100, 100, 100, 100))
    p.add_pet(Pet("Whiskers", 0, "cat", 100, 100, 100, 100, 100, 100, 100, 100))
    p.save("test")
    p.load("test")
    print(p.pets)
    print(p.money)
