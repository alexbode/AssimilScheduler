from typing import Generator

from src.schema import PrioritizedLesson, AssimilCourse, Review


class PriorityQueue:
    def __init__(self):
        self.q: list[PrioritizedLesson] = []
        self.index: int = 0
        self.course_name: str = None
        self.completed_lessons: dict[tuple[int, str], int] = {}

    def construct_priority_queue(self, course: AssimilCourse):
        self.reset_state()
        self.course_name = course.name
        for lesson in range(1, course.lesson_count + 1):
            for i, wave in enumerate(course.waves):
                priority = wave.weights.get_weight(lesson) + i / 10000
                if not wave.filter(lesson):
                    self.q.append(
                        PrioritizedLesson(
                            priority=priority,
                            lesson=lesson,
                            review_type=wave.review_type,
                            wave_index=i,
                            review_count=None,
                            lesson_count=None,
                        )
                    )
        self.q.sort(key=lambda x: x.priority)

        review_counter = {}
        lesson_counter = {}
        for pl in self.q:
            key = (pl.lesson, pl.review_type)
            if key not in review_counter:
                review_counter[key] = 0
            review_counter[key] += 1
            if pl.lesson not in lesson_counter:
                lesson_counter[pl.lesson] = 0
            lesson_counter[pl.lesson] += 1
            pl.review_count = review_counter[key]
            pl.lesson_count = lesson_counter[pl.lesson]
        return

    # TODO: state is not update when callingthe get_next method. only the update_state method
    def _increment_completed_lesson(self, lesson: int, review_type: str):
        pass

    def update_state(self, completed_lessons: dict[tuple[int, str], int]):
        self.completed_lessons = completed_lessons
        while self.index < len(self.q):
            prioritized_lesson = self.peek()
            key = (prioritized_lesson.lesson, prioritized_lesson.review_type.name)
            if key in self.completed_lessons:
                self.completed_lessons[key] -= 1
                if self.completed_lessons[key] <= 0:
                    del self.completed_lessons[key]
                self.index += 1
            else:
                break
        return

    def peek(self) -> Review:
        if self.index >= len(self.q):
            raise IndexError("PriorityQueue is empty")
        return self.get_review(self.index)

    def get_next(self, n: int) -> Generator[Review, int, None]:
        index = self.index
        while n > 0 and index < len(self.q):
            yield self.get_review(index)
            n -= 1
            index += 1
        return

    def get_review(self, index: int) -> Review:
        if index >= len(self.q):
            raise IndexError("PriorityQueue is empty")
        prioritized_lesson = self.q[index]
        return Review(
            course=self.course_name,
            lesson=prioritized_lesson.lesson,
            review_type=prioritized_lesson.review_type,
            review_count=index + 1,
            total_review_count=len(self.q),
            percent_complete=((index + 1) / len(self.q)) * 100,
            previous_reviews_completed=prioritized_lesson.review_count,
            previous_lesson_reviews_completed=prioritized_lesson.lesson_count,
            wave_index=prioritized_lesson.wave_index,
        )

    def reset_state(self):
        self.index = 0
        self.q = []
        return
