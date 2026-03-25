from src.schema import (
    AssimilCourseConfig,
    Wave,
    PracticeType,
    Weights,
)

LESSON_COUNT = 60

config = AssimilCourseConfig(
    name="SpanishAdvanced",
    log_file="spanish_advanced_log.txt",
    lesson_count=LESSON_COUNT,
    waves=[
        # LISTEN
        #
        Wave(
            type=PracticeType.LISTEN,
            filter=lambda x: x % 7 == 0,
        ),
        Wave(
            type=PracticeType.LISTEN,
            weights=Weights(offset=1, multiplier=2),
            filter=lambda x: x % 7 == 0,
        ),
        Wave(
            type=PracticeType.LISTEN,
            weights=Weights(offset=50, multiplier=1.5),
            filter=lambda x: x % 7 == 0,
        ),
        Wave(
            type=PracticeType.LISTEN,
            weights=Weights(offset=LESSON_COUNT),
            filter=lambda x: x % 7 == 0,
        ),
        # READ
        #
        Wave(
            type=PracticeType.READ,
            weights=Weights(offset=10),
        ),
        Wave(
            type=PracticeType.READ,
            weights=Weights(offset=11, multiplier=1.75),
            filter=lambda x: x % 7 != 0,
        ),
        # SHADOW
        #
        Wave(
            type=PracticeType.SHADOW,
            weights=Weights(offset=20),
            filter=lambda x: x % 7 == 0,
        ),
        Wave(
            type=PracticeType.SHADOW,
            weights=Weights(offset=70, multiplier=1.5),
            filter=lambda x: x % 7 == 0,
        ),
        # TRANSLATE
        #
        Wave(
            type=PracticeType.TRANSLATE,
            weights=Weights(offset=40),
            filter=lambda x: x % 7 == 0,
        ),
        # REVERSE_TRANSLATE
        #
        Wave(
            type=PracticeType.REVERSE_TRANSLATE,
            weights=Weights(offset=50, multiplier=1.5),
            filter=lambda x: x % 7 == 0,
        ),
        Wave(
            type=PracticeType.REVERSE_TRANSLATE,
            weights=Weights(offset=55, multiplier=1.66),
            filter=lambda x: x % 7 == 0,
        ),
    ],
)
