import random
from pets import Pet
from time import time


class PetMarket:
    def __init__(self, money):
        self.pets = []
        self.money = money

    def add_pet(self, pet):
        self.pets.append(pet)

    def list_pets(self):
        for i, pet in enumerate(self.pets):
            print(f"{i + 1}: {pet.name} the {pet.species}")

    def purchase_pet(self, index: int):

        if self.money >= 20:
            self.money -= 20
            return self.pets.pop(index)
        else:
            print("Invalid selection.")
            return None

    def refresh(self):
        self.pets = []
        for x in range(5):
            self.add_pet(
                Pet(
                    random.choice(
                        [
                            "Rover",
                            "Chip",
                            "Fluffy",
                            "Nibbles",
                            "Whiskers",
                            "Fido",
                            "Mittens",
                            "Buddy",
                        ]
                    ),
                    0,
                    random.choice(["dog", "cat", "hamster", "bird"]),
                    100,
                    100,
                    100,
                    100,
                    time(),
                    time(),
                    time(),
                    time(),
                )
            )
