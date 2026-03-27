import sqlite3
from pathlib import Path
from datetime import datetime

from src.schema import PracticeType

CREATE_TABLE_SQL_QUERY = """
CREATE TABLE IF NOT EXISTS Reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course TEXT NOT NULL,
    date TEXT NOT NULL,
    practice_type TEXT NOT NULL,
    lesson INTEGER NOT NULL
)"""

CREATE_INDEX_SQL_QUERY = """
CREATE INDEX IF NOT EXISTS idx_course ON Reviews (course);
"""

INSERT_REVIEW_SQL_QUERY = """
INSERT INTO Reviews (course, date, practice_type, lesson) VALUES (?, ?, ?, ?)
"""

GET_REVIEW_COUNT_SQL_QUERY = """
SELECT practice_type, lesson, COUNT(*) 
FROM Reviews 
WHERE course = ? 
GROUP BY practice_type, lesson;
"""

GET_LESSON_COUNT_SQL_QUERY = """
SELECT lesson, COUNT(*) 
FROM Reviews 
WHERE course = ? 
GROUP BY lesson;
"""

GET_LATEST_REVIEW_SQL_QUERY = """
SELECT id FROM Reviews WHERE course = ? ORDER BY id DESC LIMIT 1
"""

REMOVE_BY_ID_SQL_QUERY = """
DELETE FROM Reviews WHERE id = ?
"""




class DB:
    db_path = Path(__file__).parent / "db" / "assimil_scheduler.db"

    def __init__(self):
        self.create_table()

    def create_table(self):
        with sqlite3.connect(self.db_path) as c:
            cursor = c.cursor()
            cursor.execute(CREATE_TABLE_SQL_QUERY)
            cursor.execute(CREATE_INDEX_SQL_QUERY)

    def insert_review(
        self, course: str, date: datetime, practice_type: PracticeType, lesson: int
    ):
        with sqlite3.connect(self.db_path) as c:
            cursor = c.cursor()
            cursor.execute(
                INSERT_REVIEW_SQL_QUERY,
                (course.lower(), date.strftime("%Y-%m-%d"), practice_type.name, lesson),
            )

    def count_reviews(self, course: str) -> dict[tuple[PracticeType, int], int]:
        with sqlite3.connect(self.db_path) as c:
            cursor = c.cursor()
            cursor.execute(GET_REVIEW_COUNT_SQL_QUERY, (course.lower(),))
            records = cursor.fetchall()
            output = {}
            for row in records:
                # (lesson, ParcticeType): Count
                output[(row[1],row[0])] = row[2]
            return output

    def count_lessons(self, course: str) -> dict[int, int]:
        with sqlite3.connect(self.db_path) as c:
            cursor = c.cursor()
            cursor.execute(GET_REVIEW_COUNT_SQL_QUERY, (course.lower(),))
            records = cursor.fetchall()
            output = {}
            for row in records:
                # lesson: Count
                output[row[0]] = row[1]
            return output

    def undo_last_review(self, course: str):
        with sqlite3.connect(self.db_path) as c:
            cursor = c.cursor()
            most_recent_row = cursor.execute(GET_LATEST_REVIEW_SQL_QUERY, (course.lower(),)).fetchone()
            if most_recent_row:
                cursor.execute(REMOVE_BY_ID_SQL_QUERY, (most_recent_row[0],))