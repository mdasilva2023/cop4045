"""Homework 3, Problem 4 - Matheus Henrique Da Silva - Z23704669"""

from pathlib import Path
from tempfile import TemporaryDirectory
from testif import testif


def ed_read(filename: str | Path, from_: int = 0, to: int = -1) -> str:
    """return characters in the half-open interval [from_, to).

    preconditions: from_ and to are integers; from_ >= 0; to is -1
    or at least from_; neither endpoint may exceed the file length.
    postcondition: returns the selected text without changing the file.
    file I/O exceptions propagate to the caller.
    """
    if type(from_) is not int or type(to) is not int:
        raise TypeError("Text positions must be integers")
    if from_ < 0 or to < -1:
        raise ValueError("Invalid text position")

    with open(filename, "r", encoding="utf-8", newline="") as file:
        content = file.read()

    end = len(content) if to == -1 else to
    if from_ > len(content) or end > len(content):
        raise IndexError("Text position exceeds file length")
    if end < from_:
        raise ValueError("End position must not precede start position")
    return content[from_:end]


def ed_find(filename: str | Path, search_str: str) -> list[int]:
    """return the start indices of all matches of search_str in filename.

    precondition: search_str is a nonempty string.
    postcondition: returns a list of indices, or [] if no match exists;
    the file remains unchanged. Overlapping matches are included.
    file I/O exceptions propagate to the caller.
    """
    if not isinstance(search_str, str):
        raise TypeError("Search text must be a string")
    if not search_str:
        raise ValueError("Search text cannot be empty")

    content = ed_read(filename)
    positions = []
    index = content.find(search_str)
    while index != -1:
        positions.append(index)
        index = content.find(search_str, index + 1)
    return positions


def ed_replace(
    filename: str | Path, search_str: str, replace_with: str, occurrence: int = -1
) -> int:
    """replace all matches, or one zero-based occurrence, in a file.

    preconditions: search_str is a nonempty string; replace_with is a
    string; occurrence is an integer >= -1. An occurrence of -1 means
    all matches; 0 means the first match. Out-of-range occurrences do
    not modify the file.
    postcondition: returns the number of replacements performed.
    file I/O exceptions propagate to the caller.
    """
    if not isinstance(search_str, str) or not isinstance(replace_with, str):
        raise TypeError("Search and replacement must be strings")
    if not search_str:
        raise ValueError("Search text cannot be empty")
    if type(occurrence) is not int:
        raise TypeError("Occurrence must be an integer")
    if occurrence < -1:
        raise ValueError("Occurrence must be -1 or nonnegative")

    content = ed_read(filename)
    if occurrence == -1:
        replacements = content.count(search_str)
        new_content = content.replace(search_str, replace_with)
    else:
        locations = []
        start = 0
        while True:
            position = content.find(search_str, start)
            if position == -1:
                break
            locations.append(position)
            start = position + len(search_str)
        if occurrence >= len(locations):
            return 0
        position = locations[occurrence]
        new_content = (content[:position] + replace_with
                       + content[position + len(search_str):])
        replacements = 1

    if replacements:
        with open(filename, "w", encoding="utf-8", newline="") as file:
            file.write(new_content)
    return replacements


def ed_append(filename: str | Path, string: str) -> int:
    """append string to filename, creating the file when necessary.

    precondition: string is a string.
    postcondition: the file ends with string; returns len(string).
    file I/O exceptions propagate to the caller.
    """
    if not isinstance(string, str):
        raise TypeError("Appended text must be a string")
    with open(filename, "a", encoding="utf-8", newline="") as file:
        file.write(string)
    return len(string)


def test_ed_find() -> None:
    """unit-test ed_find using a temporary file and the provided testif."""
    with TemporaryDirectory() as folder:
        filename = Path(folder) / "find_test.txt"
        ed_append(filename, "01234567890123456789")
        testif(ed_find(filename, "345") == [3, 13],
               "ed_find repeated matches", "correct positions", "wrong positions")
        testif(ed_find(filename, "356") == [],
               "ed_find missing text", "empty list", "unexpected match")
        filename.write_text("aaaa", encoding="utf-8")
        testif(ed_find(filename, "aa") == [0, 1, 2],
               "ed_find overlapping matches", "correct positions", "wrong positions")


def test_ed_replace() -> None:
    """unit-test ed_replace and verify both resulting text and counts."""
    with TemporaryDirectory() as folder:
        filename = Path(folder) / "replace_test.txt"
        original = "01234567890123456789"
        filename.write_text(original, encoding="utf-8")
        count = ed_replace(filename, "345", "ABCDE", 1)
        testif(count == 1 and ed_read(filename) == "0123456789012ABCDE6789",
               "ed_replace second match", "correct replacement", "incorrect result")
        filename.write_text(original, encoding="utf-8")
        count = ed_replace(filename, "345", "ABCDE")
        testif(count == 2 and ed_read(filename) == "012ABCDE6789012ABCDE6789",
               "ed_replace all matches", "both replaced", "incorrect result")
        before = ed_read(filename)
        count = ed_replace(filename, "ABCDE", "X", 99)
        testif(count == 0 and ed_read(filename) == before,
               "ed_replace out of range", "file unchanged", "file was changed")


def main() -> None:
    """demonstrate editing commands and run unit tests without touching other files."""
    print("Homework 3 - Problem 4 - Matheus Henrique Da Silva - Z23704669")
    print("\nDemonstration:")
    with TemporaryDirectory() as folder:
        filename = Path(folder) / "file1.txt"
        print("Characters appended:", ed_append(filename, "0123456789"))
        print("Characters appended:", ed_append(filename, "0123456789"))
        print("Read positions 3 to 9:", ed_read(filename, 3, 9))
        print("Read from position 3:", ed_read(filename, 3))
        print("Find '345':", ed_find(filename, "345"))
        print("Find '356':", ed_find(filename, "356"))
        print("Replace second '345':", ed_replace(filename, "345", "ABCDE", 1))
        print("After replacement:", ed_read(filename))
        print("\nUnit tests:")
        test_ed_find()
        test_ed_replace()
    print("\nFinished Problem 4.")


if __name__ == "__main__":
    main()
