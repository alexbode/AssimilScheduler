import unittest
from pathlib import Path
from datetime import datetime

from src.db import DB
from src.schema import ReviewType


class TestDb(unittest.TestCase):
    def setUp(self) -> None:
        # set up the db before each test.
        DB.db_path = Path(__file__).parent / "fixtures" / "test.db"
        self.db = DB()

    def tearDown(self):
        # delete the test.db file, ran after each test.
        self.db.db_path.unlink(missing_ok=True)

    def test_insert_review_and_get_all_reviews(self):
        course = "course1"
        date = datetime.fromisoformat("2024-01-01")
        review = ReviewType.READ
        lesson = 1
        self.db.insert_review(course, date, review, lesson)
        reviews = self.db.get_all_reviews(course)
        self.assertEqual(len(reviews), 1)
        self.assertEqual(reviews[0][0], date)
        self.assertEqual(reviews[0][1], lesson)
        self.assertEqual(reviews[0][2], review)

    def test_count_reviews(self):
        course = "course1"
        date = datetime.fromisoformat("2024-01-01")
        self.db.insert_review(course, date, ReviewType.READ, 1)
        self.db.insert_review(course, date, ReviewType.READ, 1)
        self.db.insert_review(course, date, ReviewType.READ, 2)
        self.db.insert_review(course, date, ReviewType.LISTEN, 1)
        self.db.insert_review(course, date, ReviewType.LISTEN, 1)
        self.db.insert_review(course, date, ReviewType.LISTEN, 2)
        self.db.insert_review(course, date, ReviewType.LISTEN, 2)
        reviews_agg = self.db.count_reviews(course)
        self.assertEqual(len(reviews_agg), 4)
        self.assertEqual(reviews_agg[(1, ReviewType.READ.name)], 2)
        self.assertEqual(reviews_agg[(1, ReviewType.LISTEN.name)], 2)
        self.assertEqual(reviews_agg[(2, ReviewType.READ.name)], 1)
        self.assertEqual(reviews_agg[(2, ReviewType.LISTEN.name)], 2)

    def test_count_lessons(self):
        course = "course1"
        date = datetime.fromisoformat("2024-01-01")
        self.db.insert_review(course, date, ReviewType.READ, 1)
        self.db.insert_review(course, date, ReviewType.READ, 1)
        self.db.insert_review(course, date, ReviewType.READ, 2)
        self.db.insert_review(course, date, ReviewType.LISTEN, 1)
        self.db.insert_review(course, date, ReviewType.LISTEN, 1)
        self.db.insert_review(course, date, ReviewType.LISTEN, 2)
        self.db.insert_review(course, date, ReviewType.LISTEN, 2)
        lessons_agg = self.db.count_lessons(course)
        print(lessons_agg)
        self.assertEqual(len(lessons_agg), 2)
        self.assertEqual(lessons_agg[1], 4)
        self.assertEqual(lessons_agg[2], 3)

    def test_undo_last_review(self):
        course = "course1"
        date = datetime.fromisoformat("2024-01-01")
        self.db.insert_review(course, date, ReviewType.READ, 1)
        self.db.insert_review(course, date, ReviewType.READ, 2)
        self.db.insert_review(course, date, ReviewType.READ, 3)
        reviews_before_undo = self.db.get_all_reviews(course)
        self.assertEqual(len(reviews_before_undo), 3)
        self.assertIn((date, 3, ReviewType.READ), reviews_before_undo)
        self.assertIn((date, 2, ReviewType.READ), reviews_before_undo)
        self.assertIn((date, 1, ReviewType.READ), reviews_before_undo)
        self.db.undo_last_review(course)
        reviews_after_undo = self.db.get_all_reviews(course)
        self.assertEqual(len(reviews_after_undo), 2)
        self.assertNotIn((date, 3, ReviewType.READ), reviews_after_undo)
        self.assertIn((date, 2, ReviewType.READ), reviews_after_undo)
        self.assertIn((date, 1, ReviewType.READ), reviews_after_undo)
