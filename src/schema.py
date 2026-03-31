from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Callable


class ReviewType(Enum):
    """
    Different ways to review an Assimil lesson

    Ideal order of review:
    1. Listen
    2. Read
    3. Translate
    4. Grammar
    5. Shadow with text
    6. Scriptorium
    ---
    7. Transcribe
    8. Shadow blind
    9. Reverse translate
    """

    # Listen to the audio blind, then while reading the translation,
    # then while reading the target text.
    LISTEN = auto()
    # Shadow the audio while reading the target text for 2 passes.
    SHADOW = auto()
    # Shadow the audio blind for 2 passes.
    SHADOW_BLIND = auto()
    # Read the target text aloud and grammar points.
    READ = auto()
    # Copy the target language text while repeating aloud.
    SCRIPTORIUM = auto()
    # Translate from the target language (text to text).
    TRANSLATE = auto()
    # Translate to the target language (text to text).
    REVERSE_TRANSLATE = auto()
    # Listen to audio and write what you hear in the target language.
    TRANSCRIBE = auto()
    # Review grammar points without looking at the text.
    GRAMMAR_POINTS = auto()


@dataclass
class Weights:
    """
    Used when calculating priority/scheduling lessons.
    multiplier(lesson_num) + offset
    multiplier = 2, offset = 3
    lesson = 1, 2, 3 -> 2(1)+3, 2(2)+3, 2(3)+3 = 5, 7, 9
    """

    offset: int = 0
    multiplier: int = 1

    def get_weight(self, lesson: int) -> int:
        return self.multiplier * lesson + self.offset


@dataclass
class Wave:
    review_type: ReviewType
    weights: Weights = field(default_factory=Weights)
    # What lessons to ignore
    filter: Callable[[int], bool] = lambda x: False


@dataclass
class AssimilCourse:
    # unique name for the course
    name: str = ""
    # waves of review planned for assimil book ex.
    # first wave listen, second wave shadow, third wave scriptorium, etc.
    waves: list[Wave] = field(default_factory=list)
    # number of lessons in the assimil course
    lesson_count: int = 0

    def __repr__(self):
        return f"AssimilCourse<{self.name}>"

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


@dataclass
class Review:
    """
    Example output:
    Review 34 of 536 (6.34%)
    Lesson: 9, READ (1) [3]

    course: "French"
    lesson: 9
    review_type: ReviewType.READ
    review_count: 34
    total_review_count: 536
    percent_complete: 6.34
    previous_reviews_completed: 1
    previous_lesson_reviews_completed: 3
    """

    course: str
    lesson: int
    review_type: ReviewType
    review_count: int
    total_review_count: int
    percent_complete: float
    previous_reviews_completed: int
    previous_lesson_reviews_completed: int
    wave_index: int

    def __repr__(self):
        return f"Review {self.review_count} of {self.total_review_count} ({self.percent_complete:.2f}%) \nLesson: {self.lesson}, {self.review_type.name} ({self.previous_reviews_completed}) [{self.previous_lesson_reviews_completed}]\n"

    def to_dict(self):
        return {
            "course": self.course,
            "lesson": self.lesson,
            "review_type": self.review_type.name,
            "review_count": self.review_count,
            "total_review_count": self.total_review_count,
            "percent_complete": self.percent_complete,
            "previous_reviews_completed": self.previous_reviews_completed,
            "previous_lesson_reviews_completed": self.previous_lesson_reviews_completed,
            "wave_index": self.wave_index,
        }


@dataclass
class PrioritizedLesson:
    priority: float
    lesson: int
    review_type: ReviewType
    wave_index: int
    review_count: int = 0
    lesson_count: int = 0

    def __lt__(self, other):
        return self.priority < other.priority
