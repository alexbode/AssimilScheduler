from datetime import datetime
from dataclasses import dataclass
from heapq import heappush, heappop
from typing import Generator

from src.db import DB
from src.schema import AssimilCourse, ReviewType


class AssimilScheduler:

    @dataclass
    class PrioritizedLesson:
        priority: float
        lesson: int
        review_type: ReviewType

        def __lt__(self, other):
            return self.priority < other.priority

    @dataclass
    class Review:
        lesson_count: int
        lesson_number: int
        total_lessons: int
        review_type: ReviewType

        practice_review_count: int
        lesson_review_count: int

    def __init__(self, course: AssimilCourse, db: DB = DB()):
        self.course: AssimilCourse = course
        self.db: DB = db

    def constuct_priority_queue(self) -> list[tuple[int, int, ReviewType]]:
        q = []
        for lesson in range(1, self.course.lesson_count + 1):
            for i, wave in enumerate(self.course.waves):
                priority = wave.weights.get_weight(lesson) + i / 10000
                if not wave.filter(lesson):
                    heappush(
                        q,
                        AssimilScheduler.PrioritizedLesson(priority, lesson, wave.type),
                    )
        return q

    def calculate_projected_finish_date(self, upcoming_lesson_count: int) -> str:
        # TODO implement projected finish date
        return "Not implemented yet"
        # if len(self.logs.log_file) == 0:
        #     return "INF"
        # now = datetime.now()
        # thirty_days_ago = now - timedelta(days=30)
        # lesson_completed_count_in_last_30_days = len(
        #     [d for d in self.logs.log_file if d[0] > thirty_days_ago]
        # )
        # earliest_date_in_last_30_days = min(
        #     [d[0] for d in self.logs.log_file if d[0] > thirty_days_ago]
        # )
        # date_range = now - earliest_date_in_last_30_days
        # lesson_per_day = lesson_completed_count_in_last_30_days / date_range.days
        # return (now + timedelta(days=upcoming_lesson_count / lesson_per_day)).strftime(
        #     "%Y-%m-%d"
        # )

    def review_generator(self, next_n: int) -> Generator[Review, int, None]:
        count = 0
        lesson_counter = {}
        pratice_counter = {}
        q = self.constuct_priority_queue()
        total_lessons = len(q)
        completed_lessons = self.db.count_reviews(self.course.name)
        while q and next_n > 0:
            count += 1
            prioritized_lesson = heappop(q)
            key = (prioritized_lesson.lesson, prioritized_lesson.review_type.name)
            if prioritized_lesson.lesson not in lesson_counter:
                lesson_counter[prioritized_lesson.lesson] = 0
            lesson_counter[prioritized_lesson.lesson] += 1
            if key not in pratice_counter:
                pratice_counter[key] = 0
            pratice_counter[key] += 1

            if key in completed_lessons:
                completed_lessons[key] -= 1
                if completed_lessons[key] <= 0:
                    del completed_lessons[key]
            else:
                yield AssimilScheduler.Review(
                    count,
                    prioritized_lesson.lesson,
                    total_lessons,
                    prioritized_lesson.review_type,
                    pratice_counter[key],
                    lesson_counter[prioritized_lesson.lesson],
                )
                next_n -= 1
        return

    def get_next_lesson(self, next_n: int):
        idx = 0
        for review in self.review_generator(next_n):
            self.format_review(idx, review)
            idx += 1

    def format_review(self, idx: int, review: Review):
        if idx == 0:
            print(
                f"{self.course.name} - Projected Finish date: {self.calculate_projected_finish_date(review.total_lessons - review.lesson_count)}"
            )
        print(
            f"{idx + 1}. Review {review.lesson_count} of {review.total_lessons} ({(review.lesson_count / review.total_lessons) * 100:.2f}%)"
        )
        print(
            f"Lesson: {review.lesson_number}, {review.review_type.name} ({review.practice_review_count}) [{review.lesson_review_count}]\n"
        )

    def mark_as_done(self):
        try:
            l = next(self.review_generator(1))
            self.db.insert_review(
                self.course.name,
                datetime.now(),
                l.review_type,
                l.lesson_number,
            )
        except Exception as e:
            ValueError("Cannot mark as done the next lesson: {e}")

    def undo_last_review(self):
        self.db.undo_last_review(self.course.name)
