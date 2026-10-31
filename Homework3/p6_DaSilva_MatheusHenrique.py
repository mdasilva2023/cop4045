"""Homework 3, Problem 6 - Matheus Henrique Da Silva - Z23704669.

This module models a simple university folder storage hierarchy using
inheritance, method overriding, polymorphism, and recursion.
"""

from __future__ import annotations

from typing import Any


class Entry:
    """Represent a single entry in the university storage hierarchy.

    Preconditions:
        - name is a non-empty string.

    Postconditions:
        - Each entry keeps a reference to its parent folder or None for the root.
        - Subclasses implement size() with the appropriate storage semantics.
    """

    def __init__(self, name: str) -> None:
        """Initialize an entry with a name and no parent.

        Args:
            name: The visible name of the entry.

        Raises:
            ValueError: If name is empty or not a string.
        """
        if not isinstance(name, str) or not name:
            raise ValueError("name must be a non-empty string")
        self.name: str = name
        self._parent: Entry | None = None

    def parent(self) -> Entry | None:
        """Return this entry's parent or None if it is the root entry.

        Returns:
            The parent entry for this object, or None when the entry is a root.
        """
        return self._parent

    def absolute_path(self) -> list[Entry]:
        """Return the path from the current entry to the root entry.

        The order is current entry first, followed by its parent, and so on until
        the root entry is last. This matches the specification for the assignment.

        Returns:
            A list of Entry objects representing the path from this object to the
            root entry.
        """
        path: list[Entry] = [self]
        if self._parent is not None:
            path.extend(self._parent.absolute_path())
        return path

    def size(self) -> int:
        """Return the storage size used by this entry.

        This method is intentionally abstract at the base class level and must be
        implemented by subclasses.

        Raises:
            NotImplementedError: If called on the base Entry class.
        """
        raise NotImplementedError("Entry.size() must be implemented by subclasses")


class File(Entry):
    """Represent a file with a fixed number of bytes in use.

    Preconditions:
        - bytes_used is a nonnegative integer.

    Postconditions:
        - The file stores its exact byte count and reports it through size().
    """

    def __init__(self, name: str, bytes_used: int) -> None:
        """Create a file entry.

        Args:
            name: The file's name.
            bytes_used: The amount of storage used by the file, in bytes.

        Raises:
            TypeError: If bytes_used is not an integer.
            ValueError: If bytes_used is negative.
        """
        super().__init__(name)
        if isinstance(bytes_used, bool) or not isinstance(bytes_used, int):
            raise TypeError("bytes_used must be an integer")
        if bytes_used < 0:
            raise ValueError("bytes_used must be nonnegative")
        self.bytes_used: int = bytes_used

    def size(self) -> int:
        """Return the number of bytes used by this file.

        Returns:
            The number of bytes assigned to this file.
        """
        return self.bytes_used


class Folder(Entry):
    """Represent a folder containing child entries.

    Preconditions:
        - Entries added to a folder are valid Entry instances.
        - The folder structure contains no cycles.

    Postconditions:
        - The folder stores its immediate children and calculates the total size
          recursively across nested folders and files.
    """

    def __init__(self, name: str) -> None:
        """Create a folder entry with an empty child list."""
        super().__init__(name)
        self._children: list[Entry] = []

    def add(self, entry: Entry) -> None:
        """Add a child entry to this folder and set its parent reference.

        Args:
            entry: The child object to add.

        Raises:
            TypeError: If entry is not an Entry instance.
            ValueError: If entry is the same object as this folder or already has
                a different parent.
        """
        if not isinstance(entry, Entry):
            raise TypeError("entry must be an Entry instance")
        if entry is self:
            raise ValueError("a folder cannot contain itself")
        if entry.parent() is not None and entry.parent() is not self:
            raise ValueError("entry already belongs to another folder")
        entry._parent = self
        self._children.append(entry)

    def children(self) -> tuple[Entry, ...]:
        """Return the immediate children of this folder.

        Returns:
            A tuple containing the folder's immediate child entries.
        """
        return tuple(self._children)

    def size(self) -> int:
        """Return the total storage used by this folder and all descendants.

        Returns:
            The sum of the size() values for all contained files and folders.
        """
        total = 0
        for child in self._children:
            total += child.size()
        return total


def find_large_files(entry: Entry, minimum_size: int) -> list[File]:
    """Return all files with size greater than or equal to a threshold.

    The search is recursive and explores every nested folder beneath the given
    entry. If the starting entry itself is a qualifying file, it is returned in a
    single-element list.

    Args:
        entry: A File or Folder to search.
        minimum_size: The minimum file size to include.

    Returns:
        A list of File objects meeting or exceeding the threshold.

    Raises:
        TypeError: If entry is not a File or Folder, or if minimum_size is not an
            integer.
        ValueError: If minimum_size is negative.
    """
    if not isinstance(entry, (File, Folder)):
        raise TypeError("entry must be a File or Folder instance")
    if isinstance(minimum_size, bool) or not isinstance(minimum_size, int):
        raise TypeError("minimum_size must be an integer")
    if minimum_size < 0:
        raise ValueError("minimum_size must be nonnegative")

    if isinstance(entry, File):
        return [entry] if entry.size() >= minimum_size else []

    matches: list[File] = []
    for child in entry.children():
        matches.extend(find_large_files(child, minimum_size))
    return matches


def build_demo_hierarchy() -> Folder:
    """Create a three-level folder hierarchy for demonstration and testing.

    Returns:
        A root folder containing nested folders and files with different sizes.
    """
    root = Folder("root")
    academics = Folder("academics")
    research = Folder("research")
    library = Folder("library")

    root.add(academics)
    root.add(library)
    academics.add(research)

    root.add(File("root_notes.txt", 150))
    academics.add(File("schedule.pdf", 325))
    research.add(File("experiment_data.csv", 980))
    research.add(File("lab_notes.txt", 120))
    library.add(File("book_index.db", 640))
    library.add(File("manual.pdf", 210))

    return root


def print_hierarchy(entry: Entry, indent: str = "") -> None:
    """Print the storage hierarchy in a readable, indented form."""
    label = f"{indent}{entry.name} [{type(entry).__name__}] -> {entry.size()} bytes"
    print(label)
    if isinstance(entry, Folder):
        for child in entry.children():
            print_hierarchy(child, indent + "  ")


def main() -> None:
    """Demonstrate the folder hierarchy, size calculations, and path lookup."""
    root = build_demo_hierarchy()

    print("Homework 3 - Problem 6 - Matheus Henrique Da Silva - Z23704669")
    print("\nStorage hierarchy:")
    print_hierarchy(root)

    print("\nOutermost folder size:")
    print(f"{root.name} total size = {root.size()} bytes")

    print("\nLarge files using threshold 300 bytes:")
    large_300 = find_large_files(root, 300)
    for file_entry in large_300:
        print(f"- {file_entry.name}: {file_entry.size()} bytes")

    print("\nLarge files using threshold 500 bytes:")
    large_500 = find_large_files(root, 500)
    for file_entry in large_500:
        print(f"- {file_entry.name}: {file_entry.size()} bytes")

    print("\nPolymorphism through the shared Entry interface:")
    entries: list[Entry] = [root, root.children()[0], root.children()[1], root.children()[0].children()[0]]
    for entry in entries:
        print(f"{entry.name} -> size() = {entry.size()} bytes")

    print("\nAbsolute path demonstrations:")
    target_file = root.children()[0].children()[0].children()[0]
    target_folder = root.children()[1]
    for target in (target_file, target_folder):
        path = target.absolute_path()
        print(f"{target.name}: {' -> '.join(item.name for item in path)}")


if __name__ == "__main__":
    main()
