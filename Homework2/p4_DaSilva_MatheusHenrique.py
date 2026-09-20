# -*- coding: utf-8 -*-
"""

Matheus Henrique Bijos Da Silva
"""

import csv


def load_casts(
        filename: str
) -> dict[tuple[str, str], tuple[str, list[str]]]:
    """
    read the cast CSV file and return a dictionary.

    the dictionary key is a tuple containing the movie title
    and year. The value contains the director and actor list.
    """
    try:
        casts = {}

        with open(
                filename,
                "r",
                encoding="utf-8",
                newline=""
        ) as file:

            reader = csv.reader(file)

            for row in reader:

                if len(row) >= 4:

                    title = row[0]
                    year = row[1]
                    director = row[2]
                    actors = row[3:]

                    casts[(title, year)] = (
                        director,
                        actors
                    )

        return casts

    except Exception as error:
        print(
            f"Error while reading cast file "
            f"'{filename}': {error}"
        )
        raise


def load_ranked_movies(
        filename: str
) -> list[dict[str, str]]:
    """
    read a ranked IMDB CSV file that contains a header.

    returns a list of dictionaries representing the rows.
    """
    try:
        movies = []

        with open(
                filename,
                "r",
                encoding="utf-8",
                newline=""
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:
                movies.append(row)

        return movies

    except Exception as error:
        print(
            f"Error while reading movie file "
            f"'{filename}': {error}"
        )
        raise


def display_top_collaborations(
        rated_filename: str,
        casts_filename: str,
        limit: int | None = None
) -> None:
    """
    display director and actor collaboration rankings for
    movies listed in the top-rated movie file.

    rankings are ordered by the number of movies in which
    the director and actor worked together.
    """
    try:
        rated_movies = load_ranked_movies(
            rated_filename
        )

        casts = load_casts(
            casts_filename
        )

        collaborations = {}

        for movie in rated_movies:

            title = movie["Title"]
            year = movie["Year"]

            key = (title, year)

            if key in casts:

                director = casts[key][0]
                actors = casts[key][1]

                for actor in actors:

                    pair = (
                        director,
                        actor
                    )

                    collaborations[pair] = (
                        collaborations.get(pair, 0) + 1
                    )

        ranking = [
            (
                director,
                actor,
                count
            )
            for (director, actor), count
            in collaborations.items()
        ]

        ranking.sort(
            key=lambda item: item[2],
            reverse=True
        )

        if limit is not None:
            ranking = ranking[:limit]

        for rank, item in enumerate(
                ranking,
                start=1
        ):

            director = item[0]
            actor = item[1]
            count = item[2]

            print(
                f"{rank}. "
                f"{director} | "
                f"{actor} | "
                f"{count} movies"
            )

    except Exception as error:
        print(
            f"Error while displaying collaborations: "
            f"{error}"
        )
        raise


def display_top_actors(
        grossing_filename: str,
        casts_filename: str,
        limit: int | None = None
) -> None:
    """
    display actors from the top-grossing movie list ranked
    by the total USA box-office money of their movies.

    the optional limit controls how many actors are displayed.
    """
    try:
        grossing_movies = load_ranked_movies(
            grossing_filename
        )

        casts = load_casts(
            casts_filename
        )

        actor_totals = {}

        for movie in grossing_movies:

            title = movie["Title"]
            year = movie["Year"]

            key = (title, year)

            if key in casts:

                box_office = int(
                    movie["USA Box Office"]
                )

                actors = casts[key][1]

                for actor in actors:

                    actor_totals[actor] = (
                        actor_totals.get(actor, 0)
                        + box_office
                    )

        ranking = [
            (
                actor,
                total
            )
            for actor, total
            in actor_totals.items()
        ]

        ranking.sort(
            key=lambda item: item[1],
            reverse=True
        )

        if limit is not None:
            ranking = ranking[:limit]

        for rank, item in enumerate(
                ranking,
                start=1
        ):

            actor = item[0]
            total = item[1]

            print(
                f"{rank}. "
                f"{actor} | "
                f"${total:,}"
            )

    except Exception as error:
        print(
            f"Error while displaying top actors: "
            f"{error}"
        )
        raise


def main() -> None:
    """
    test the collaboration and actor ranking functions.

    the rankings are limited to 10 entries as required
    for the assignment screenshot.
    """
    try:
        print("Name: Matheus Henrique Da Silva - Z23704669")
        print()

        rated_file = "imdb-top-rated.csv"
        grossing_file = "imdb-top-grossing.csv"
        casts_file = "imdb-top-casts.csv"

        print(
            "PART A - TOP DIRECTOR/ACTOR COLLABORATIONS"
        )
        print()

        display_top_collaborations(
            rated_file,
            casts_file,
            10
        )

        print()

        print(
            "PART B - TOP ACTORS BY USA BOX OFFICE"
        )
        print()

        display_top_actors(
            grossing_file,
            casts_file,
            10
        )

    except Exception as error:
        print(
            f"An error occurred in main: {error}"
        )
        raise


if __name__ == "__main__":
    main()