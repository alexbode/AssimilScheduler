from datetime import datetime
from dataclasses import dataclass
from heapq import heappush, heappop
from typing import Generator

from src.db import DB
from src.cache import Cache
from src.schema import AssimilCourse, ReviewType, Review


class AssimilScheduler:

    @dataclass
    class PrioritizedLesson:
        priority: float
        lesson: int
        review_type: ReviewType
        wave_index: int

        def __lt__(self, other):
            return self.priority < other.priority

    def __init__(self, course: AssimilCourse, db: DB = DB(), cache=Cache()):
        self.course: AssimilCourse = course
        self.db: DB = db
        self.cache: Cache = cache

    def constuct_priority_queue(self) -> list[tuple[int, int, ReviewType]]:
        if self.cache.has(self.course.name):
            return self.cache.get(self.course.name)
        print(f"Constructing priority queue for course {self.course.name} with {self.course.lesson_count} lessons and {len(self.course.waves)} waves")
        q = []
        for lesson in range(1, self.course.lesson_count + 1):
            for i, wave in enumerate(self.course.waves):
                priority = wave.weights.get_weight(lesson) + i / 10000
                if not wave.filter(lesson):
                    heappush(
                        q,
                        AssimilScheduler.PrioritizedLesson(
                            priority, lesson, wave.type, i
                        ),
                    )
        self.cache.set(self.course.name, q)
        return q

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
                yield Review(
                    course=self.course.name,
                    lesson=prioritized_lesson.lesson,
                    review_type=prioritized_lesson.review_type,
                    review_count=count,
                    total_review_count=total_lessons,
                    percent_complete=(count / total_lessons) * 100,
                    previous_reviews_completed=pratice_counter[key],
                    previous_lesson_reviews_completed=lesson_counter[
                        prioritized_lesson.lesson
                    ],
                    wave_index=prioritized_lesson.wave_index,
                )
                next_n -= 1
        return

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
