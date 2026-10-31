"""Homework 3, Problem 3 - Matheus Henrique Da Silva - Z23704669

adapted from the professor's code.
"""

from __future__ import annotations

import random
import matplotlib.pyplot as plt


class Island:
    """a square grid of animal objects; empty positions contain zero."""

    def __init__(self, n: int, prey_count: int = 0,
                 predator_count: int = 0, count_humans: int = 0) -> None:
        """create an n-by-n island and randomly place the initial populations.

        preconditions: n > 0; counts are nonnegative and sum to at most n*n.
        postcondition: each animal occupies a distinct grid location.
        """
        if n <= 0 or min(prey_count, predator_count, count_humans) < 0:
            raise ValueError("Grid size must be positive and counts nonnegative")
        if prey_count + predator_count + count_humans > n * n:
            raise ValueError("Too many animals for the island")
        self.grid_size = n
        self.grid: list[list[Animal | int]] = [[0] * n for _ in range(n)]
        self.init_animals(prey_count, predator_count, count_humans)

    def init_animals(self, prey_count: int, predator_count: int,
                     count_humans: int = 0) -> None:
        """place prey, predators, and humans in distinct random empty cells.

        preconditions: counts are nonnegative and enough cells are empty.
        """
        if min(prey_count, predator_count, count_humans) < 0:
            raise ValueError("Counts must be nonnegative")
        available = [(x, y) for x in range(self.grid_size)
                     for y in range(self.grid_size) if self.animal(x, y) == 0]
        if sum((prey_count, predator_count, count_humans)) > len(available):
            raise ValueError("Not enough empty cells")
        random.shuffle(available)
        for animal_type, count in ((Prey, prey_count),
                                   (Predator, predator_count),
                                   (Human, count_humans)):
            for _ in range(count):
                x, y = available.pop()
                self.register(animal_type(self, x=x, y=y))

    def clear_all_moved_flags(self) -> None:
        """reset the movement flags before the next simulation tick."""
        for animal in self.animals():
            animal.clear_moved_flag()

    def size(self) -> int:
        """return the island's width and height."""
        return self.grid_size

    def register(self, animal: Animal) -> None:
        """put an animal in the grid at its current coordinates."""
        self.grid[animal.x][animal.y] = animal

    def remove(self, animal: Animal) -> None:
        """remove an animal from its cell if it still occupies that cell."""
        if self.animal(animal.x, animal.y) is animal:
            self.grid[animal.x][animal.y] = 0

    def animal(self, x: int, y: int) -> Animal | int:
        """return the object at (x,y), zero if empty, or -1 if outside."""
        if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
            return self.grid[x][y]
        return -1

    def animals(self) -> list[Animal]:
        """return a snapshot of all animals currently on the island."""
        return [item for row in self.grid for item in row
                if isinstance(item, Animal)]

    def __str__(self) -> str:
        """return a printable grid with the origin at the bottom left."""
        return "\n".join("  ".join(str(self.animal(x, y))
                            if self.animal(x, y) else "."
                            for x in range(self.grid_size))
                         for y in range(self.grid_size - 1, -1, -1))

    def count_prey(self) -> int:
        """return the number of prey currently on the island."""
        return sum(isinstance(a, Prey) for a in self.animals())

    def count_predators(self) -> int:
        """return the number of predators currently on the island."""
        return sum(isinstance(a, Predator) for a in self.animals())

    def count_humans(self) -> int:
        """return the number of humans currently on the island."""
        return sum(isinstance(a, Human) for a in self.animals())


class Animal:
    """base class with shared position, movement, and breeding behaviors."""

    def __init__(self, island: Island, x: int = 0, y: int = 0,
                 s: str = "A") -> None:
        """store the animal's island, coordinates, and display character."""
        self.island = island
        self.name = s
        self.x = x
        self.y = y
        self.moved = False
        self.breed_clock = 0

    def position(self) -> tuple[int, int]:
        """return the current (x,y) coordinates."""
        return self.x, self.y

    def __str__(self) -> str:
        """return the symbol displayed on the island grid."""
        return self.name

    def check_grid(self, type_looking_for: type = int) -> tuple[int, int] | int:
        """find the first of eight adjacent cells of the given exact type.

        return (x,y) when found or zero when none are available.
        """
        offsets = [(-1, 1), (0, 1), (1, 1), (-1, 0),
                   (1, 0), (-1, -1), (0, -1), (1, -1)]
        for dx, dy in offsets:
            x, y = self.x + dx, self.y + dy
            if type(self.island.animal(x, y)) is type_looking_for:
                if 0 <= x < self.island.size() and 0 <= y < self.island.size():
                    return x, y
        return 0

    def move(self) -> None:
        """move once into a neighboring empty cell, if one exists."""
        if not self.moved:
            location = self.check_grid(int)
            if location:
                self.island.remove(self)
                self.x, self.y = location
                self.island.register(self)
                self.moved = True

    def breed(self) -> None:
        """produce an animal of the same class in a free neighboring cell.

        breeding occurs when the breed clock reaches zero, if space exists.
        """
        if self.breed_clock <= 0:
            location = self.check_grid(int)
            if location:
                self.breed_clock = self.breed_time
                new_animal = self.__class__(self.island, x=location[0],
                                            y=location[1])
                self.island.register(new_animal)

    def clear_moved_flag(self) -> None:
        """allow movement during the following simulation tick."""
        self.moved = False


class Prey(Animal):
    """an animal that moves and breeds but does not hunt."""

    breed_time: int = 3

    def __init__(self, island: Island, x: int = 0, y: int = 0,
                 s: str = "O") -> None:
        """initialize a prey with its breeding clock."""
        super().__init__(island, x, y, s)
        self.breed_clock = self.breed_time

    def clock_tick(self) -> None:
        """decrease the prey's breeding clock by one tick."""
        self.breed_clock -= 1


class Predator(Animal):
    """an animal that hunts prey and starves if it cannot eat."""

    breed_time: int = 6
    starve_time: int = 3

    def __init__(self, island: Island, x: int = 0, y: int = 0,
                 s: str = "X") -> None:
        """initialize breeding and starvation clocks for a predator."""
        super().__init__(island, x, y, s)
        self.breed_clock = self.breed_time
        self.starve_clock = self.starve_time

    def clock_tick(self) -> None:
        """advance clocks; remove the predator if starvation reaches zero."""
        self.breed_clock -= 1
        self.starve_clock -= 1
        if self.starve_clock <= 0:
            self.island.remove(self)

    def eat(self) -> None:
        """eat neighboring prey, move into its cell, and reset starvation."""
        if not self.moved:
            location = self.check_grid(Prey)
            if location:
                prey = self.island.animal(*location)
                self.island.remove(prey)
                self.island.remove(self)
                self.x, self.y = location
                self.island.register(self)
                self.starve_clock = self.starve_time
                self.moved = True


class Human(Animal):
    """an animal that hunts predators, breeds, and may starve."""

    breed_time: int = 8
    hunt_time: int = 2
    starve_time: int = 5

    def __init__(self, island: Island, x: int = 0, y: int = 0,
                 s: str = "H") -> None:
        """initialize a human's breeding, hunting, and starvation clocks."""
        super().__init__(island, x, y, s)
        self.breed_clock = self.breed_time
        self.hunt_clock = self.hunt_time
        self.starve_clock = self.starve_time

    def clock_tick(self) -> None:
        """advance three clocks; remove a starving human."""
        self.breed_clock -= 1
        self.hunt_clock -= 1
        self.starve_clock -= 1
        if self.starve_clock <= 0:
            self.island.remove(self)

    def eat(self) -> None:
        """at each hunt interval, eat an adjacent predator, if present.

        successful hunting moves the human and resets its starvation clock.
        Humans never eat prey.
        """
        if self.moved or self.hunt_clock > 0:
            return
        self.hunt_clock = self.hunt_time
        location = self.check_grid(Predator)
        if location:
            predator = self.island.animal(*location)
            self.island.remove(predator)
            self.island.remove(self)
            self.x, self.y = location
            self.island.register(self)
            self.starve_clock = self.starve_time
            self.moved = True


def main(predator_breed_time: int = 6, predator_starve_time: int = 3,
         initial_predators: int = 10, prey_breed_time: int = 3,
         initial_prey: int = 50, size: int = 10, ticks: int = 1000,
         human_breed_time: int = 8, human_hunt_time: int = 2,
         human_starve_time: int = 5, initial_humans: int = 5,
         convergence_ticks: int = 25, show_plot: bool = True) -> tuple[list[int], list[int], list[int]]:
    """run and graph the three populations, stopping at convergence or 1000 ticks.

    preconditions: timing values and island size are positive, counts fit grid.
    returns time histories for prey, predators, and humans (including tick 0).
    convergence is defined as unchanged counts for convergence_ticks ticks.
    """
    if min(predator_breed_time, predator_starve_time, prey_breed_time,
           human_breed_time, human_hunt_time, human_starve_time,
           convergence_ticks) <= 0:
        raise ValueError("Times and convergence interval must be positive")
    Predator.breed_time = predator_breed_time
    Predator.starve_time = predator_starve_time
    Prey.breed_time = prey_breed_time
    Human.breed_time = human_breed_time
    Human.hunt_time = human_hunt_time
    Human.starve_time = human_starve_time

    isle = Island(size, initial_prey, initial_predators, initial_humans)
    prey_list = [isle.count_prey()]
    predator_list = [isle.count_predators()]
    human_list = [isle.count_humans()]
    print("Initial island grid (tick 0):")
    print(isle)
    print(f"Tick 0: Prey={prey_list[-1]}, Predators={predator_list[-1]}, Humans={human_list[-1]}")
    unchanged = 0
    final_tick = 0
    for tick in range(1, min(ticks, 1000) + 1):
        isle.clear_all_moved_flags()
        current_animals = isle.animals()
        for animal in current_animals:
            if isle.animal(animal.x, animal.y) is not animal:
                continue
            if isinstance(animal, (Predator, Human)):
                animal.eat()
            animal.move()
            animal.breed()
            animal.clock_tick()

        prey_list.append(isle.count_prey())
        predator_list.append(isle.count_predators())
        human_list.append(isle.count_humans())
        final_tick = tick
        current = (prey_list[-1], predator_list[-1], human_list[-1])
        previous = (prey_list[-2], predator_list[-2], human_list[-2])
        unchanged = unchanged + 1 if current == previous else 0
        if tick % 10 == 0 or tick == 1:
            print(f"Tick {tick}: Prey={current[0]}, Predators={current[1]}, Humans={current[2]}")
        if unchanged >= convergence_ticks:
            print(f"All three populations stabilized for {convergence_ticks} ticks.")
            break

    print(f"\nFinal island grid (tick {final_tick}):")
    print(isle)
    print(f"Final populations: Prey={prey_list[-1]}, Predators={predator_list[-1]}, Humans={human_list[-1]}")
    print(f"Simulation finished after {final_tick} ticks.")

    times = range(len(prey_list))
    plt.figure(figsize=(10, 6))
    plt.plot(times, prey_list, label="Prey", color="tab:green")
    plt.plot(times, predator_list, label="Predators", color="tab:red")
    plt.plot(times, human_list, label="Humans", color="tab:blue")
    plt.title("Predator-Prey-Human Population Simulation")
    plt.xlabel("Time (clock ticks)")
    plt.ylabel("Population")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    if show_plot:
        plt.show()
    return prey_list, predator_list, human_list


if __name__ == "__main__":
    random.seed(7)  
    main()
