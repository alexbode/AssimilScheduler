from datetime import datetime, timedelta
from dataclasses import dataclass
from heapq import heappush, heappop
from typing import Generator

from src.log_reader import LogReader
from src.schema import AssimilCourseConfig, PracticeType


class AssimilScheduler:

    @dataclass
    class PrioritizedLesson:
        priority: float
        lesson: int
        practice_type: PracticeType

        def __lt__(self, other):
            return self.priority < other.priority

    @dataclass
    class Review:
        lesson_count: int
        lesson_number: int
        total_lessons: int
        practice_type: PracticeType
        practice_review_count: int
        lesson_review_count: int

    def __init__(self, course: str, logs: LogReader, config: AssimilCourseConfig):
        self.course = course
        self.logs: LogReader = logs
        self.config: AssimilCourseConfig = config

    def constuct_priority_queue(self) -> list[tuple[int, int, PracticeType]]:
        q = []
        for lesson in range(1, self.config.lesson_count + 1):
            for i, wave in enumerate(self.config.waves):
                priority = wave.weights.get_weight(lesson) + i / 10000
                if not wave.filter(lesson):
                    heappush(
                        q,
                        AssimilScheduler.PrioritizedLesson(priority, lesson, wave.type),
                    )
        return q

    def calculate_projected_finish_date(self, upcoming_lesson_count: int) -> str:
        now = datetime.now()
        thirty_days_ago = now - timedelta(days=30)
        lesson_completed_count_in_last_30_days = len(
            [d for d in self.logs.log_file if d[0] > thirty_days_ago]
        )
        earliest_date_in_last_30_days = min(
            [d[0] for d in self.logs.log_file if d[0] > thirty_days_ago]
        )
        date_range = now - earliest_date_in_last_30_days
        lesson_per_day = lesson_completed_count_in_last_30_days / date_range.days
        return (now + timedelta(days=upcoming_lesson_count / lesson_per_day)).strftime(
            "%Y-%m-%d"
        )

    def review_generator(self, next_n: int) -> Generator[Review, int, None]:
        count = 0
        lesson_counter = {}
        pratice_counter = {}
        q = self.constuct_priority_queue()
        total_lessons = len(q)
        completed_lessons = self.logs.completed_lessons()
        while q and next_n > 0:
            count += 1
            prioritized_lesson = heappop(q)
            key = (prioritized_lesson.lesson, prioritized_lesson.practice_type.name)
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
                    prioritized_lesson.practice_type,
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
                f"{self.config.name} - Projected Finish date: {self.calculate_projected_finish_date(review.total_lessons - review.lesson_count)}"
            )
        print(
            f"{idx + 1}. Review {review.lesson_count} of {review.total_lessons} ({(review.lesson_count / review.total_lessons) * 100:.2f}%)"
        )
        print(
            f"Lesson: {review.lesson_number}, {review.practice_type} ({review.practice_review_count}) [{review.lesson_review_count}]\n"
        )
