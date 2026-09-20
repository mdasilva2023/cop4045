# -*- coding: utf-8 -*-
"""

Matheus Henrique Da Silva
"""


def main() -> None:
    """run and display the solutions for parts a through f."""

    print("Name: Matheus Henrique Da Silva - Z23704669")
    print()

    # ---------------------------------------------------------
    # Part A
    # ---------------------------------------------------------
    print("PART A")

    tuples_a = [
        (a, b, c, d)
        for a in range(1, 11)
        for b in range(1, 11)
        for c in range(1, 11)
        for d in range(1, 11)
        if len({a, b, c, d}) == 4
        and a**2 + b**2 == c**2 + d**2
    ]

    print(tuples_a)
    print()

    # ---------------------------------------------------------
    # Part B
    # ---------------------------------------------------------
    print("PART B")

    words_b = ['One', 'SEVEN', 'three', 'two', 'Ten']

    tuples_b = [
        (word.lower(), len(word))
        for word in words_b
        if len(word) <= 3
    ]

    print(tuples_b)
    print()

    # ---------------------------------------------------------
    # Part C
    # ---------------------------------------------------------
    print("PART C")

    names = [
        'Christopher Ashton Kutcher',
        'Elizabeth Stamatina Fey'
    ]

    names_c = [
        f"{parts[0]} {parts[1][0]}. {parts[2]}"
        for name in names
        for parts in [name.split()]
    ]

    print(names_c)
    print()

    # ---------------------------------------------------------
    # Part D
    # ---------------------------------------------------------
    print("PART D")

    lst1 = ["Spam", "Trams", "Elbows", "Tops", "Astral"]
    lst2 = ["Bowels", "Sample", "Altars", "Stop", "Course", "Smart"]

    anagrams_d = [
        (w1, w2)
        for w1 in lst1
        for w2 in lst2
        if sorted(w1.lower()) == sorted(w2.lower())
    ]

    print(anagrams_d)
    print()

    # ---------------------------------------------------------
    # Part E
    # ---------------------------------------------------------
    print("PART E")

    s = ['one', 'two', 'three']

    lengths_e = {
        word: len(word)
        for word in s
    }

    print(lengths_e)
    print()

    # ---------------------------------------------------------
    # Part F
    # ---------------------------------------------------------
    print("PART F")

    text = "Hello world"

    vowels_f = {
        index: char.lower()
        for index, char in enumerate(text)
        if char.lower() in "aeiou"
    }

    print(vowels_f)


if __name__ == "__main__":
    main()