from typing import override
from time import strftime, localtime, time
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
        birth_date=None,
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
        self.birth_date = strftime("%Y-%m-%d %I:%M", localtime(self.birth_time))

    def feed(self):
        self.hunger = 100
        self.last_fed = time()
        print("Thanks for the food!")

    def play(self):
        self.happiness = 100
        self.energy -= 10
        self.last_played = time()

    def sleep(self):
        self.energy = 100
        self.last_slept = time()

    def greeting(self):
        return "Hello! My name is " + self.name + "."

    def update(self):
        self.hunger -= (time() - self.last_fed) / 1000
        self.happiness -= (time() - self.last_played) / 1000
        self.energy -= (time() - self.last_slept) / 1000
        # age in hours
        self.age = (time() - self.birth_time) / 3600  # Age in hours
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
            print(PET_TO_ASCII[self.species])

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
        return f"{self.name} says: Woof!"


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
        return f"{self.name} says: Meow!"


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
        return f"{self.name} says: Squeak!"
