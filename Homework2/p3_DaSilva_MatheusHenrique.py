# -*- coding: utf-8 -*-
"""

Matheus Henrique Da Silva
"""

import csv
import os


def testif(
        b: bool,
        testname: str,
        msgOK: str = "",
        msgFailed: str = ""
) -> bool:
    """
    function used for testing.

    param b: Boolean tested condition. True if the test passed,
    False otherwise.
    param testname: The test name.
    param msgOK: Message printed when the test succeeds.
    param msgFailed: Message printed when the test fails.
    returns: The Boolean test result.
    """
    try:
        if b:
            print("Success: " + testname + "; " + msgOK)
        else:
            print("Failed: " + testname + "; " + msgFailed)

        return b

    except Exception as error:
        print(f"Error while running test '{testname}': {error}")
        raise


def add_user(
        sn: dict[str, tuple[str, list[str]]],
        username: str,
        fullname: str
) -> bool:
    """
    add a new user to the social network.

    the new user initially has no friends.
    returns True if the user was added successfully and
    false if the username already exists.
    """
    try:
        if username in sn:
            return False

        sn[username] = (fullname, [])
        return True

    except Exception as error:
        print(f"Error while adding user '{username}': {error}")
        raise


def add_friend(
        sn: dict[str, tuple[str, list[str]]],
        user1: str,
        user2: str
) -> bool:
    """
    add a mutual friend link between user1 and user2.

    returns True if successful and False if either username
    does not exist in the social network.
    """
    try:
        if user1 not in sn or user2 not in sn:
            return False

        if user2 not in sn[user1][1]:
            sn[user1][1].append(user2)

        if user1 not in sn[user2][1]:
            sn[user2][1].append(user1)

        return True

    except Exception as error:
        print(
            f"Error while adding friendship between "
            f"'{user1}' and '{user2}': {error}"
        )
        raise


def get_friends(
        sn: dict[str, tuple[str, list[str]]],
        user1: str,
        distance: int
) -> list[str]:
    """
    return all friends of user1 from distance 1 through
    the specified distance.

    cycles are avoided, users are returned only once, and
    the original user is not included.
    """
    try:
        if user1 not in sn:
            return []

        if distance <= 0:
            return []

        result = []
        visited = {user1}
        current_level = [user1]

        for _ in range(distance):

            next_level = []

            for user in current_level:

                for friend in sn[user][1]:

                    if friend not in visited:
                        visited.add(friend)
                        result.append(friend)
                        next_level.append(friend)

            current_level = next_level

            if not current_level:
                break

        return result

    except Exception as error:
        print(
            f"Error while finding friends for "
            f"'{user1}': {error}"
        )
        raise


def save_network(
        filename: str,
        sn: dict[str, tuple[str, list[str]]]
) -> None:
    """
    save the social network dictionary to a CSV file.

    each CSV row contains the username, full name,
    and the user's friends.
    """
    try:
        with open(
                filename,
                "w",
                newline="",
                encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            for username, data in sn.items():

                fullname = data[0]
                friends = data[1]

                writer.writerow(
                    [username, fullname] + friends
                )

    except Exception as error:
        print(
            f"Error while saving network to "
            f"'{filename}': {error}"
        )
        raise


def load_network(
        filename: str
) -> dict[str, tuple[str, list[str]]]:
    """
    load a social network from a CSV file produced by
    save_network and return the reconstructed dictionary.
    """
    try:
        sn = {}

        with open(
                filename,
                "r",
                newline="",
                encoding="utf-8"
        ) as file:

            reader = csv.reader(file)

            for row in reader:

                if len(row) >= 2:

                    username = row[0]
                    fullname = row[1]
                    friends = row[2:]

                    sn[username] = (
                        fullname,
                        friends
                    )

        return sn

    except Exception as error:
        print(
            f"Error while loading network from "
            f"'{filename}': {error}"
        )
        raise


def test() -> None:
    """
    test the functions from parts a through e using testif.
    """
    try:
        print("PART G - EXTRA CREDIT TESTS")
        print()

        sn_test = {
            'alice': ('Alice Smith', ['maria']),
            'maria': (
                'Maria Cortez',
                ['alice', 'joe', 'david']
            ),
            'joe': (
                'Joseph Adams',
                ['maria', 'eve']
            ),
            'eve': (
                'Evelyn Cooper',
                ['joe']
            ),
            'david': (
                'David Benson',
                ['maria']
            )
        }

        # Test Part A - add_user
        result = add_user(
            sn_test,
            "john",
            "John Williams"
        )

        testif(
            result is True
            and "john" in sn_test
            and sn_test["john"] == ("John Williams", []),
            "add_user new user",
            "John was added correctly.",
            "John was not added correctly."
        )

        result = add_user(
            sn_test,
            "alice",
            "Another Alice"
        )

        testif(
            result is False,
            "add_user existing user",
            "Existing username correctly rejected.",
            "Existing username was incorrectly added."
        )

        # Test Part B - add_friend
        result = add_friend(
            sn_test,
            "john",
            "eve"
        )

        testif(
            result is True
            and "eve" in sn_test["john"][1]
            and "john" in sn_test["eve"][1],
            "add_friend valid users",
            "Mutual friendship was added.",
            "Mutual friendship was not added correctly."
        )

        result = add_friend(
            sn_test,
            "john",
            "unknown"
        )

        testif(
            result is False,
            "add_friend invalid user",
            "Invalid username correctly rejected.",
            "Invalid username was not handled correctly."
        )

        # Test Part C - get_friends
        testif(
            get_friends(sn_test, "alice", 1)
            == ["maria"],
            "get_friends distance 1",
            "Correct friends returned.",
            "Incorrect friends returned."
        )

        testif(
            get_friends(sn_test, "alice", 2)
            == ["maria", "joe", "david"],
            "get_friends distance 2",
            "Correct friends returned.",
            "Incorrect friends returned."
        )

        testif(
            get_friends(sn_test, "unknown", 2)
            == [],
            "get_friends invalid user",
            "Empty list correctly returned.",
            "Invalid username was not handled correctly."
        )

        # Test Parts D and E - save_network and load_network
        test_filename = "test_social_network.csv"

        save_network(
            test_filename,
            sn_test
        )

        testif(
            os.path.exists(test_filename),
            "save_network",
            "CSV file was created successfully.",
            "CSV file was not created."
        )

        loaded_test = load_network(
            test_filename
        )

        testif(
            loaded_test == sn_test,
            "load_network",
            "Saved network was loaded correctly.",
            "Loaded network does not match original."
        )

        if os.path.exists(test_filename):
            os.remove(test_filename)

        print()

    except Exception as error:
        print(f"Error while running tests: {error}")
        raise


def main() -> None:
    """
    test and display all social network functions
    from parts a through g.
    """
    try:
        print("Name: Matheus Henrique Da Silva - Z23704669")
        print()

        sn = {
            'alice': ('Alice Smith', ['maria']),
            'maria': (
                'Maria Cortez',
                ['alice', 'joe', 'david']
            ),
            'joe': (
                'Joseph Adams',
                ['maria', 'eve']
            ),
            'eve': (
                'Evelyn Cooper',
                ['joe']
            ),
            'david': (
                'David Benson',
                ['maria']
            )
        }

        # -------------------------------------------------
        # Part A
        # -------------------------------------------------
        print("PART A - add_user")

        added = add_user(
            sn,
            "john",
            "John Williams"
        )

        print("Add john:", added)
        print("John's information:", sn["john"])

        duplicate = add_user(
            sn,
            "alice",
            "Another Alice"
        )

        print("Add existing user alice:", duplicate)
        print()

        # -------------------------------------------------
        # Part B
        # -------------------------------------------------
        print("PART B - add_friend")

        friendship = add_friend(
            sn,
            "john",
            "eve"
        )

        print("Add friendship john/eve:", friendship)
        print("John's friends:", sn["john"][1])
        print("Eve's friends:", sn["eve"][1])

        invalid_friendship = add_friend(
            sn,
            "john",
            "unknown"
        )

        print(
            "Add friendship with unknown user:",
            invalid_friendship
        )
        print()

        # -------------------------------------------------
        # Part C
        # -------------------------------------------------
        print("PART C - get_friends")

        friends1 = get_friends(
            sn,
            "alice",
            1
        )

        friends2 = get_friends(
            sn,
            "alice",
            2
        )

        print(
            'get_friends(sn, "alice", 1):',
            friends1
        )

        print(
            'get_friends(sn, "alice", 2):',
            friends2
        )

        print()

        # -------------------------------------------------
        # Part D
        # -------------------------------------------------
        print("PART D - save_network")

        filename = "social_network.csv"

        save_network(
            filename,
            sn
        )

        print(
            f"Network successfully saved to {filename}"
        )
        print()

        # -------------------------------------------------
        # Part E
        # -------------------------------------------------
        print("PART E - load_network")

        loaded_sn = load_network(
            filename
        )

        print("Loaded network:")
        print(loaded_sn)
        print()

        # -------------------------------------------------
        # Part G - Extra Credit
        # -------------------------------------------------
        test()

    except Exception as error:
        print(
            f"An error occurred in main: {error}"
        )
        raise


if __name__ == "__main__":
    main()