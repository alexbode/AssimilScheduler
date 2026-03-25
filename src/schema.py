from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Callable


# The different ways to review an Assimil lesson
class PracticeType(Enum):
    # Listen to the audio blind, then while reading the translation,
    # then while reading the target text.
    LISTEN = auto()
    # Shadow the audio blind for 2 passes.
    SHADOW = auto()
    # Read the target text aloud and grammar points.
    READ = auto()
    # Copy the target language text while repeating aloud.
    SCRIPTORIUM = auto()
    # Translate from the target language
    TRANSLATE = auto()
    # Translate to the target language.
    REVERSE_TRANSLATE = auto()


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
    type: PracticeType
    weights: Weights = field(default_factory=Weights)
    # What lessons to ignore
    filter: Callable[[int], bool] = lambda x: True


@dataclass
class AssimilCourseConfig:
    # unique name for the config
    name: str = ""
    # waves of review planned for assimil book ex.
    # first wave listen, second wave shadow, third wave scriptorium, etc.
    waves: list[Wave] = field(default_factory=list)
    # number of lessons in the assimil course
    lesson_count: int = 0
    # where completed lessons are logged
    log_file: str = ""

    def __repr__(self):
        return f"AssimilCourseConfig<{self.name}>"
