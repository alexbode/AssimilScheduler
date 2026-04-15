from datetime import datetime
from typing import Generator

from src.db import DB
from src.priority_queue import PriorityQueue
from src.schema import AssimilCourse, ReviewType, Review, PrioritizedLesson


class AssimilScheduler:

    def __init__(
        self,
        course: AssimilCourse,
        db: DB = DB(),
        priority_queue: PriorityQueue = PriorityQueue(),
    ):
        self.course: AssimilCourse = course
        self.db: DB = db
        ## TODO add a cache layer here to avoid recomputing the priority queue every time
        self.q: PriorityQueue = priority_queue
        self.q.construct_priority_queue(course)
        self.q.update_state(self.db.count_reviews(self.course.name))

    def review_generator(self, next_n: int) -> Generator[Review, int, None]:
        for r in self.q.get_next(next_n):
            yield r
        return

    def mark_as_done(self):
        try:
            l = next(self.review_generator(1))
            self.db.insert_review(
                self.course.name,
                datetime.now(),
                l.review_type,
                l.lesson,
            )
        except Exception as e:
            ValueError("Cannot mark as done the next lesson: {e}")

    def undo_last_review(self):
        self.db.undo_last_review(self.course.name)

    def manual_update(self, lesson: int, review_type: ReviewType):
        review_type = ReviewType[review_type]
        self.db.insert_review(
            self.course.name,
            datetime.now(),
            review_type,
            lesson,
        )

    def get_all_reviews(self, course: str) -> list[int]:
        return self.db.get_all_reviews(course)

    def get_course_percentage(self) -> dict[str, float]:
        return self.q.get_percentaege_complete()

    def get_review_counts_by_date(self) -> list[tuple[datetime, int]]:
        return self.db.get_review_counts_by_date()