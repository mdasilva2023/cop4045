"""Homework 3, Problem 5 - Matheus Henrique Da Silva - Z23704669"""

"""Unit tests for the Homework 3 storage hierarchy problem."""

import unittest

from p6_DaSilva_MatheusHenrique import File, Folder, find_large_files


class StorageHierarchyTests(unittest.TestCase):
    """Verify absolute-path ordering and large-file searches."""

    def setUp(self) -> None:
        """Create a nested folder structure used by the tests."""
        self.root = Folder("root")
        self.academics = Folder("academics")
        self.research = Folder("research")
        self.root.add(self.academics)
        self.academics.add(self.research)

        self.root_file = File("root.txt", 10)
        self.academics_file = File("schedule.pdf", 250)
        self.research_file = File("data.csv", 900)
        self.small_file = File("notes.txt", 80)

        self.root.add(self.root_file)
        self.academics.add(self.academics_file)
        self.research.add(self.research_file)
        self.research.add(self.small_file)

    def test_absolute_path_for_child_file(self) -> None:
        """A file path should start at the file and end at the root entry."""
        expected = [self.research_file, self.research, self.academics, self.root]
        self.assertEqual(self.research_file.absolute_path(), expected)

    def test_absolute_path_for_folder(self) -> None:
        """A folder path should include the folder itself and ancestors in order."""
        expected = [self.research, self.academics, self.root]
        self.assertEqual(self.research.absolute_path(), expected)

    def test_find_large_files_returns_all_matches(self) -> None:
        """Large files should be collected recursively in depth-first traversal order."""
        matches = find_large_files(self.root, 100)
        self.assertEqual(matches, [self.research_file, self.academics_file])

    def test_find_large_files_using_higher_threshold(self) -> None:
        """A higher threshold should filter out smaller files."""
        matches = find_large_files(self.root, 500)
        self.assertEqual(matches, [self.research_file])

    def test_find_large_files_with_empty_result(self) -> None:
        """No qualifying files should return an empty list."""
        matches = find_large_files(self.root, 1000)
        self.assertEqual(matches, [])

    def test_find_large_files_if_starting_entry_is_file(self) -> None:
        """A qualifying file should be returned even when it is the starting entry."""
        self.assertEqual(find_large_files(self.academics_file, 250), [self.academics_file])
        self.assertEqual(find_large_files(self.academics_file, 300), [])

    def test_find_large_files_invalid_inputs(self) -> None:
        """Bad inputs should raise the appropriate exceptions."""
        with self.assertRaises(TypeError):
            find_large_files("not an entry", 10)
        with self.assertRaises(ValueError):
            find_large_files(self.root, -1)


if __name__ == "__main__":
    unittest.main()
