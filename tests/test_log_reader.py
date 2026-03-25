import unittest
from pathlib import Path
from datetime import datetime

from src.log_reader import LogReader


class TestLogReader(unittest.TestCase):

    fixtures_folder = Path(__file__).parent / "fixtures"

    def test_file_exists(self):
        expected_message = "Log file not found: "
        with self.assertRaises(ValueError) as e:
            LogReader("does_not_exists_log.txt", path=self.fixtures_folder)
        self.assertEqual(str(e.exception)[: len(expected_message)], expected_message)

    def test_no_headers_in_log_file(self):
        expected_message = "Invalid csv log file, headers: "
        with self.assertRaises(ValueError) as e:
            LogReader("log_file_no_headers_log.txt", path=self.fixtures_folder)
        self.assertEqual(str(e.exception)[: len(expected_message)], expected_message)

    def test_malformed_headers_in_log_file(self):
        expected_message = "Invalid csv log file, headers: "
        with self.assertRaises(ValueError) as e:
            LogReader("log_file_malformed_headers_log.txt", path=self.fixtures_folder)
        self.assertEqual(str(e.exception)[: len(expected_message)], expected_message)

    def test_too_many_values_in_row(self):
        expected_message = "Invalid csv log file, too many or few values in row: "
        with self.assertRaises(ValueError) as e:
            LogReader("log_file_too_many_values_log.txt", path=self.fixtures_folder)
        self.assertEqual(str(e.exception)[: len(expected_message)], expected_message)

    def test_dates_not_in_order(self):
        expected_message = "Invalid csv log file, dates are not in order: "
        with self.assertRaises(ValueError) as e:
            LogReader("log_file_dates_not_in_order_log.txt", path=self.fixtures_folder)
        self.assertEqual(str(e.exception)[: len(expected_message)], expected_message)

    def test_earliest_date(self):
        log_reader = LogReader("valid_log.txt", path=self.fixtures_folder)
        self.assertEqual(
            log_reader.earliest_date(), datetime.strptime("2026-03-14", "%Y-%m-%d")
        )

    def test_latest_date(self):
        log_reader = LogReader("valid_log.txt", path=self.fixtures_folder)
        self.assertEqual(
            log_reader.latest_date(), datetime.strptime("2026-03-16", "%Y-%m-%d")
        )

    def test_log_count(self):
        log_reader = LogReader("valid_log.txt", path=self.fixtures_folder)
        self.assertEqual(log_reader.log_count(), 4)

    def test_counter(self):
        log_reader = LogReader("valid_log.txt", path=self.fixtures_folder)
        counter = log_reader.completed_lessons()
        self.assertEqual(len(counter), 3)
        self.assertEqual(counter[(1, "LISTEN")], 2)
        self.assertEqual(counter[(2, "LISTEN")], 1)
        self.assertEqual(counter[(3, "LISTEN")], 1)
