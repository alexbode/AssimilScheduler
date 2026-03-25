import csv
from datetime import datetime
from pathlib import Path

from src.schema import PracticeType


class LogReader:
    """
    Reads a log file. Expected format is csv with headers: date,lesson,practice_type
    date: date YYYY-MM-DD
    lesson: lesson number
    practice_type: LISTEN, READ, SHADOW, SCRIPTORIUM, TRANSLATE, REVERSE_TRANSLATE, etc.

    Example log file:
    date,lesson,practice_type
    2026-03-14,1,LISTEN
    2026-03-14,2,LISTEN
    """

    def __init__(
        self, filename: str, path: str = Path(__file__).parent.parent / "logs"
    ):
        self.filename: str = Path(path) / filename
        self.log_file: list[tuple[datetime, int, PracticeType]] = self._read_log_file()

    def _read_log_file(self) -> list[tuple[datetime, int, PracticeType]]:
        if not self.filename.exists():
            raise ValueError(f"Log file not found: {self.filename}")
        output = []
        prev_date = None
        with open(self.filename, newline="", encoding="utf-8") as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=",")
            headers = next(csv_reader, None)
            if (
                len(headers) != 3
                or headers[0] != "date"
                or headers[1] != "lesson"
                or headers[2] != "practice_type"
            ):
                raise ValueError(f"Invalid csv log file, headers: {headers}")
            for row in csv_reader:
                if len(row) != 3:
                    raise ValueError(
                        f"Invalid csv log file, too many or few values in row: {row}"
                    )
                try:
                    lesson = int(row[1])
                    date = datetime.strptime(row[0], "%Y-%m-%d")
                    practice_type = PracticeType[row[2]]
                except ValueError:
                    raise ValueError(
                        f"Invalid csv log file, cannot parse value in row: {row}"
                    )
                output.append((date, lesson, practice_type))
                if prev_date:
                    if date < prev_date:
                        raise ValueError(
                            f"Invalid csv log file, dates are not in order: {prev_date} !< {date}"
                        )
                prev_date = date
        return output

    def completed_lessons(self) -> dict[tuple[int, PracticeType], int]:
        counter = {}
        for row in self.log_file:
            lesson = (
                row[1],
                row[2].name,
            )  # (lesson, partice_type): ex. (3, <PracticeType.LISTEN: 1>)
            if lesson not in counter:
                counter[lesson] = 0
            counter[lesson] += 1
        return counter

    def earliest_date(self) -> datetime:
        return min(self.log_file, key=lambda x: x[0])[0]

    def latest_date(self) -> datetime:
        return max(self.log_file, key=lambda x: x[0])[0]

    def log_count(self) -> int:
        return len(self.log_file)
