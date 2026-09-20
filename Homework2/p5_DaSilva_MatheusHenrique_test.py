"""Unit tests for the Homework 2 weather station analyzer."""

import csv
import tempfile
import unittest
from pathlib import Path

from p5_DaSilva_MatheusHenrique import (
    read_observations,
    station_outliers,
    station_statistics,
    write_statistics,
)


class TestWeatherStationAnalyzer(unittest.TestCase):
    """Test the weather station analyzer functions."""

    def setUp(self) -> None:
        """Create a temporary directory for test input and output files."""
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.directory = Path(self.temporary_directory.name)

    def tearDown(self) -> None:
        """Remove the temporary directory used by the test."""
        self.temporary_directory.cleanup()

    def write_rows(self, rows: list[list[str]], filename: str = "input.csv") -> Path:
        """Write CSV rows to a temporary file and return its path."""
        path = self.directory / filename
        with path.open("w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(rows)
        return path

    def test_read_multiple_stations_and_negative_temperatures(self) -> None:
        """Read several stations, including a valid negative temperature."""
        path = self.write_rows([
            ["North", "09:00:00 AM 04/20/2026", "-12.5"],
            ["South", "09:30:00 AM 04/20/2026", "25.0"],
            ["North", "10:00:00 AM 04/20/2026", "-5.0"],
        ])

        observations, errors = read_observations(str(path))

        self.assertEqual(set(observations), {"North", "South"})
        self.assertEqual(observations["North"][0][1], -12.5)
        self.assertEqual(errors, [])

    def test_duplicate_station_date_is_rejected(self) -> None:
        """Reject a repeated station and date combination."""
        path = self.write_rows([
            ["North", "09:00:00 AM 04/20/2026", "10.0"],
            ["North", "09:00:00 AM 04/20/2026", "11.0"],
        ])

        observations, errors = read_observations(str(path))

        self.assertEqual(len(observations["North"]), 1)
        self.assertEqual(len(errors), 1)
        self.assertIn("duplicate", errors[0][1])

    def test_temperatures_outside_range_are_rejected(self) -> None:
        """Reject temperatures below -100.0 and above 150.0."""
        path = self.write_rows([
            ["Cold", "09:00:00 AM 04/20/2026", "-100.1"],
            ["Hot", "09:00:00 AM 04/20/2026", "150.1"],
        ])

        observations, errors = read_observations(str(path))

        self.assertEqual(observations, {})
        self.assertEqual(len(errors), 2)
        self.assertTrue(all("between" in message for _, message in errors))

    def test_nonnumeric_temperature_is_rejected(self) -> None:
        """Reject a temperature that cannot be converted to a float."""
        path = self.write_rows([
            ["North", "09:00:00 AM 04/20/2026", "not-a-number"],
        ])

        observations, errors = read_observations(str(path))

        self.assertEqual(observations, {})
        self.assertEqual(len(errors), 1)
        self.assertIn("not a number", errors[0][1])

    def test_malformed_csv_line_is_reported(self) -> None:
        """Place a row with the wrong number of fields in the errors list."""
        path = self.write_rows([
            ["North", "09:00:00 AM 04/20/2026", "10.0"],
            ["malformed", "row"],
        ])

        observations, errors = read_observations(str(path))

        self.assertEqual(len(observations["North"]), 1)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0][0], 2)
        self.assertIn("expected", errors[0][1])

    def test_observations_are_sorted_chronologically(self) -> None:
        """Sort each station's observations by parsed datetime."""
        path = self.write_rows([
            ["North", "11:00:00 AM 04/20/2026", "20.0"],
            ["North", "09:00:00 AM 04/20/2026", "10.0"],
            ["North", "10:00:00 AM 04/20/2026", "15.0"],
        ])

        observations, errors = read_observations(str(path))

        self.assertEqual(errors, [])
        self.assertEqual(
            [temperature for _, temperature in observations["North"]],
            [10.0, 15.0, 20.0],
        )

    def test_station_statistics_calculates_min_max_and_mean(self) -> None:
        """Calculate minimum, maximum, and mean for every station."""
        observations = {
            "North": [("date 1", -10.0), ("date 2", 20.0), ("date 3", 0.0)],
            "South": [("date 1", 7.5), ("date 2", 12.5)],
        }

        statistics = station_statistics(observations)

        self.assertEqual(statistics["North"], (-10.0, 20.0, 10.0 / 3))
        self.assertEqual(statistics["South"], (7.5, 12.5, 10.0))

    def test_station_outliers_uses_latest_temperature(self) -> None:
        """Return only stations whose latest temperature exceeds their mean."""
        observations = {
            "North": [
                ("09:00:00 AM 04/20/2026", 10.0),
                ("10:00:00 AM 04/20/2026", 20.0),
            ],
            "South": [
                ("09:00:00 AM 04/20/2026", 20.0),
                ("10:00:00 AM 04/20/2026", 10.0),
            ],
        }

        outliers = station_outliers(observations)

        self.assertEqual(
            outliers,
            {"North": ("10:00:00 AM 04/20/2026", 20.0, 15.0)},
        )

    def test_write_statistics_sorts_and_formats_values(self) -> None:
        """Write alphabetized stations with exactly one decimal place."""
        path = self.directory / "statistics.csv"
        statistics = {
            "Zulu": (-1.25, 9.99, 4.375),
            "Alpha": (2.0, 12.0, 7.5),
        }

        write_statistics(str(path), statistics)

        self.assertEqual(
            path.read_text(encoding="utf-8").splitlines(),
            ["Alpha,2.0,12.0,7.5", "Zulu,-1.2,10.0,4.4"],
        )

    def test_missing_input_file_raises_file_not_found_error(self) -> None:
        """Allow a missing input file error to propagate from the reader."""
        missing_path = self.directory / "does-not-exist.csv"

        with self.assertRaises(FileNotFoundError):
            read_observations(str(missing_path))


if __name__ == "__main__":
    unittest.main()
