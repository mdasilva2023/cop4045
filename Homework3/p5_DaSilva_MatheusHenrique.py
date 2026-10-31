"""Homework 3, Problem 5 - Matheus Henrique Da Silva - Z23704669"""

from __future__ import annotations

import argparse
import math
from typing import Any

from testif import testif


def draw_leaf_straight(level: int, stem_length: float) -> None:
    """Draw a recursive, straight-branched leaf facing north.

    Preconditions: level >= 1 and stem_length > 0. Requires a graphical
    desktop with tkinter/turtle available. Starts from the turtle's current
    position, preserving its position and heading after drawing.
    """
    if not isinstance(level, int) or level < 1:
        raise ValueError("level must be a positive integer")
    if stem_length <= 0:
        raise ValueError("stem_length must be positive")
    import turtle

    def draw(depth: int, length: float) -> None:
        start = turtle.position()
        heading = turtle.heading()
        turtle.pendown()
        turtle.forward(length)
        tip = turtle.position()
        if depth == 1:
            for angle in (-42, 42):
                turtle.penup()
                turtle.goto(tip)
                turtle.setheading(heading + angle)
                turtle.pendown()
                turtle.forward(length * 0.23)
        else:
            for angle in (-42, 0, 42):
                turtle.penup()
                turtle.goto(tip)
                turtle.setheading(heading + angle)
                draw(depth - 1, length * 0.66)
        turtle.penup()
        turtle.goto(start)
        turtle.setheading(heading)

    draw(level, stem_length)


def draw_leaf_curved(level: int, stem_length: float) -> None:
    """Draw a recursive leaf with curved stems using short turtle segments.

    Preconditions: level >= 1 and stem_length > 0. Requires a graphical
    desktop. The turtle's position and heading are restored afterwards.
    """
    if not isinstance(level, int) or level < 1:
        raise ValueError("level must be a positive integer")
    if stem_length <= 0:
        raise ValueError("stem_length must be positive")
    import turtle

    def draw(depth: int, length: float, bend: float) -> None:
        start = turtle.position()
        heading = turtle.heading()
        turtle.pendown()
        for _ in range(5):
            turtle.left(bend / 5)
            turtle.forward(length / 5)
        tip = turtle.position()
        tip_heading = turtle.heading()
        if depth == 1:
            for angle in (-35, 35):
                turtle.penup()
                turtle.goto(tip)
                turtle.setheading(tip_heading + angle)
                turtle.pendown()
                turtle.forward(length * 0.2)
        else:
            for angle, next_bend in ((-48, -12), (0, 15), (43, 12)):
                turtle.penup()
                turtle.goto(tip)
                turtle.setheading(tip_heading + angle)
                draw(depth - 1, length * 0.67, next_bend)
        turtle.penup()
        turtle.goto(start)
        turtle.setheading(heading)

    draw(level, stem_length, 10)


def strB(n: int, base: int = 10) -> str:
    """Recursively convert nonnegative integer n to base 2 through 26.

    Raises TypeError for non-integer arguments; ValueError for n < 0 or
    base outside 2..26. Does not use Python's built-in base formatting.
    """
    if type(n) is not int or type(base) is not int:
        raise TypeError("n and base must be integers")
    if n < 0 or not 2 <= base <= 26:
        raise ValueError("n must be nonnegative and base must be 2..26")
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if n < base:
        return digits[n]
    return strB(n // base, base) + digits[n % base]


def Cnk_m(n: int, k: int) -> int:
    """Compute n choose k using recursion and an explicit memo dictionary.

    Preconditions: n and k are integers with 0 <= k <= n.
    Postcondition: returns the integer binomial coefficient; no decorators.
    """
    if type(n) is not int or type(k) is not int:
        raise TypeError("n and k must be integers")
    if n < 0 or not 0 <= k <= n:
        raise ValueError("require 0 <= k <= n")
    memo: dict[tuple[int, int], int] = {}

    def compute(a: int, b: int) -> int:
        if b == 0 or b == a:
            return 1
        key = (a, b)
        if key not in memo:
            memo[key] = compute(a - 1, b - 1) + compute(a - 1, b)
        return memo[key]

    return compute(n, k)


def run_Cnk() -> None:
    """Print several computed binomial coefficients for console screenshots."""
    print("\nMemoized n-choose-k results:")
    for n, k in ((10, 3), (25, 10), (40, 20), (100, 5)):
        print(f"C({n}, {k}) = {Cnk_m(n, k)}")


def make_pairs(seq1: list[Any], seq2: list[Any]) -> list[tuple[Any, Any]]:
    """Recursively pair matching indices until either sequence ends.

    Preconditions: seq1 and seq2 support len() and integer indexing.
    Uses an accumulator and no loops or comprehensions in the recursion.
    """
    def build(index: int, result: list[tuple[Any, Any]]) -> list[tuple[Any, Any]]:
        if index >= len(seq1) or index >= len(seq2):
            return result
        result.append((seq1[index], seq2[index]))
        return build(index + 1, result)

    return build(0, [])


def test_strB() -> None:
    """Run four unit tests for the recursive base conversion function."""
    testif(strB(0) == "0", "strB zero", "correct", "incorrect")
    testif(strB(42, 2) == "101010", "strB base 2", "correct", "incorrect")
    testif(strB(255, 16) == "FF", "strB base 16", "correct", "incorrect")
    testif(strB(125, 26) == "4L", "strB base 26", "correct", "incorrect")


def test_Cnk_m() -> None:
    """Run four unit tests for memoized binomial coefficients."""
    testif(Cnk_m(0, 0) == 1, "Cnk zero", "correct", "incorrect")
    testif(Cnk_m(7, 0) == 1, "Cnk boundary", "correct", "incorrect")
    testif(Cnk_m(8, 3) == 56, "Cnk 8 choose 3", "correct", "incorrect")
    testif(Cnk_m(30, 15) == math.comb(30, 15), "Cnk 30 choose 15", "correct", "incorrect")


def test_make_pairs() -> None:
    """Run five unit tests, including both empty-sequence boundaries."""
    testif(make_pairs([1, 2, 3], [4, 5, 6]) == [(1, 4), (2, 5), (3, 6)], "pairs equal", "correct", "incorrect")
    testif(make_pairs([1, 2, 3], [4, 5]) == [(1, 4), (2, 5)], "pairs shorter right", "correct", "incorrect")
    testif(make_pairs([1], [4, 5, 6]) == [(1, 4)], "pairs shorter left", "correct", "incorrect")
    testif(make_pairs([], [4, 5]) == [], "pairs empty left", "correct", "incorrect")
    testif(make_pairs([1, 2], []) == [], "pairs empty right", "correct", "incorrect")


def show_leaf(curved: bool = False) -> None:
    """Open the turtle window and draw the required level-6, length-120 leaf."""
    import turtle

    screen = turtle.Screen()
    screen.title("Homework 3 - Problem 5 - " + ("Curved" if curved else "Straight") + " Leaf")
    screen.setup(1000, 900)
    screen.tracer(0, 0)
    turtle.hideturtle()
    turtle.speed(0)
    turtle.pensize(1)
    turtle.penup()
    turtle.goto(0, -380)
    turtle.setheading(90)  # Default is east; turn left by 90 degrees.
    if curved:
        draw_leaf_curved(6, 120)
    else:
        draw_leaf_straight(6, 120)
    screen.update()
    print("Leaf window ready. Take your screenshot before closing it.")
    screen.mainloop()


def main() -> None:
    """Demonstrate and test recursive functions; optionally draw turtle leaves."""
    parser = argparse.ArgumentParser(description="Homework 3 Problem 5")
    parser.add_argument("--leaf", choices=("straight", "curved"), help="open the requested turtle drawing")
    args = parser.parse_args()

    if args.leaf:
        show_leaf(curved=args.leaf == "curved")
        return

    print("Homework 3 - Problem 5 - Matheus Henrique Da Silva - Z23704669")
    print("Base conversion:", strB(2026, 16), strB(31, 2), strB(555, 13))
    test_strB()
    test_Cnk_m()
    test_make_pairs()
    run_Cnk()
    print("\nPairs:", make_pairs([1, 2, 3], [4, 5]))
    print("To draw leaves, run with --leaf straight or --leaf curved")


if __name__ == "__main__":
    main()
