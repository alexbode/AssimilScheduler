from datetime import datetime
from dataclasses import dataclass
from heapq import heappush, heappop
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
        self.q: PriorityQueue = priority_queue
        print(f"Constructing priority queue for course {course.name}...")
        self.q.construct_priority_queue(course)
        print(f"Priority queue constructed with {len(self.q.q)} lessons.")
        self.q.update_state(self.db.count_reviews(self.course.name))
        print(f"Priority queue state updated with completed reviews from DB.")

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
