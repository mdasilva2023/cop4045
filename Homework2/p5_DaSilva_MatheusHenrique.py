"""Weather station observation analysis for Homework 2, Problem 5."""

import csv
import datetime
import sys
from typing import TypeAlias


Observation: TypeAlias = tuple[str, float]
ObservationData: TypeAlias = dict[str, list[Observation]]
Statistics: TypeAlias = dict[str, tuple[float, float, float]]
OutlierData: TypeAlias = dict[str, tuple[str, float, float]]


_DATE_FORMAT = "%I:%M:%S %p %m/%d/%Y"


def read_observations(
        filename: str
) -> tuple[ObservationData, list[tuple[int, str]]]:
    """Read station observations and return valid data and rejected rows.

    Each valid row contains a station, a date in the expected format, and a
    temperature from -100.0 through 150.0. Invalid rows are reported with
    their CSV line number and an explanatory message.
    """
    observations: ObservationData = {}
    errors: list[tuple[int, str]] = []
    seen: set[tuple[str, str]] = set()

    with open(filename, "r", encoding="utf-8", newline="") as file:
        reader = csv.reader(file, strict=True)

        try:
            for row in reader:
                line_number = reader.line_num

                if len(row) != 3:
                    errors.append(
                        (line_number, "expected station, date, temperature")
                    )
                    continue

                station, date_text, temperature_text = row
                if not station:
                    errors.append((line_number, "station cannot be empty"))
                    continue

                try:
                    date_value = datetime.datetime.strptime(
                        date_text,
                        _DATE_FORMAT
                    )
                except ValueError:
                    errors.append((line_number, "invalid date"))
                    continue

                try:
                    temperature = float(temperature_text)
                except ValueError:
                    errors.append((line_number, "temperature is not a number"))
                    continue

                if not -100.0 <= temperature <= 150.0:
                    errors.append(
                        (line_number, "temperature must be between -100.0 and 150.0")
                    )
                    continue

                key = (station, date_text)
                if key in seen:
                    errors.append((line_number, "duplicate station and date"))
                    continue

                seen.add(key)
                observations.setdefault(station, []).append(
                    (date_text, temperature)
                )
        except csv.Error as error:
            errors.append((reader.line_num, f"malformed CSV row: {error}"))

    for station_observations in observations.values():
        station_observations.sort(
            key=lambda observation: datetime.datetime.strptime(
                observation[0],
                _DATE_FORMAT
            )
        )

    return observations, errors


def station_statistics(
        observations: ObservationData
) -> Statistics:
    """Return minimum, maximum, and mean temperature for each station."""
    statistics: Statistics = {}

    for station, station_observations in observations.items():
        temperatures = [temperature for _, temperature in station_observations]
        if temperatures:
            statistics[station] = (
                min(temperatures),
                max(temperatures),
                sum(temperatures) / len(temperatures)
            )

    return statistics


def station_outliers(
        observations: ObservationData
) -> OutlierData:
    """Return stations whose latest temperature exceeds their own mean."""
    statistics = station_statistics(observations)
    return {
        station: (
            station_observations[-1][0],
            station_observations[-1][1],
            statistics[station][2]
        )
        for station, station_observations in observations.items()
        if station_observations
        and station_observations[-1][1] > statistics[station][2]
    }


def write_statistics(
        filename: str,
        statistics: Statistics
) -> None:
    """Write alphabetized station statistics to a CSV file."""
    with open(filename, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        for station in sorted(statistics):
            minimum, maximum, mean = statistics[station]
            writer.writerow(
                [
                    station,
                    f"{minimum:.1f}",
                    f"{maximum:.1f}",
                    f"{mean:.1f}"
                ]
            )


def main() -> None:
    """Run the weather station analyzer from the command line."""
    if len(sys.argv) != 3:
        print(
            "Usage: python p5_DaSilva_MatheusHenrique.py "
            "input_observations.csv output_statistics.csv"
        )
        return

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    try:
        observations, errors = read_observations(input_filename)
        statistics = station_statistics(observations)
        outliers = station_outliers(observations)

        print("Statistics:")
        for station in sorted(statistics):
            minimum, maximum, mean = statistics[station]
            print(
                f"{station}: min={minimum:.1f}, "
                f"max={maximum:.1f}, mean={mean:.1f}"
            )

        print("Outliers:")
        for station in sorted(outliers):
            date_text, temperature, mean = outliers[station]
            print(
                f"{station}: date={date_text}, "
                f"temperature={temperature:.1f}, mean={mean:.1f}"
            )

        print("Rejected lines:")
        if errors:
            for line_number, message in errors:
                print(f"Line {line_number}: {message}")
        else:
            print("None")

        write_statistics(output_filename, statistics)
    except OSError as error:
        print(f"File access error: {error}")


if __name__ == "__main__":
    main()
