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
    type: ReviewType
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
