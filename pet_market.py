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
