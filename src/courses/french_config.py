from src.schema import (
    AssimilCourse,
    Wave,
    ReviewType,
    Weights,
)

LESSON_COUNT = 113

course = AssimilCourse(
    name="French",
    lesson_count=LESSON_COUNT,
    waves=[
        # LISTEN
        #
        Wave(
            type=ReviewType.LISTEN,
            filter=lambda x: x % 7 == 0,
        ),
        Wave(
            type=ReviewType.LISTEN,
            weights=Weights(offset=1, multiplier=1.5),
            filter=lambda x: x % 7 == 0,
        ),
        Wave(
            type=ReviewType.LISTEN,
            weights=Weights(offset=50, multiplier=1.5),
            filter=lambda x: x % 7 == 0,
        ),
        Wave(
            type=ReviewType.LISTEN,
            weights=Weights(offset=LESSON_COUNT),
            filter=lambda x: x % 7 == 0,
        ),
        # READ
        #
        Wave(
            type=ReviewType.READ,
            weights=Weights(offset=10),
        ),
        Wave(
            type=ReviewType.READ,
            weights=Weights(offset=11, multiplier=1.75),
            filter=lambda x: x % 7 != 0,
        ),
        Wave(
            type=ReviewType.READ,
            weights=Weights(offset=LESSON_COUNT),
        ),
        # SHADOW
        #
        Wave(
            type=ReviewType.SHADOW,
            weights=Weights(offset=20),
            filter=lambda x: x % 7 == 0,
        ),
        Wave(
            type=ReviewType.SHADOW,
            weights=Weights(offset=70, multiplier=1.5),
            filter=lambda x: x % 7 == 0,
        ),
        Wave(
            type=ReviewType.SHADOW,
            weights=Weights(offset=80, multiplier=1.5),
            filter=lambda x: x % 7 == 0,
        ),
        Wave(
            type=ReviewType.SHADOW,
            weights=Weights(offset=90, multiplier=1.5),
            filter=lambda x: x % 7 == 0,
        ),
        # SCRIPTORIUM
        #
        Wave(
            type=ReviewType.SCRIPTORIUM,
            weights=Weights(offset=30),
            filter=lambda x: x % 7 == 0,
        ),
        Wave(
            type=ReviewType.SCRIPTORIUM,
            weights=Weights(offset=40, multiplier=1.5),
            filter=lambda x: x % 7 == 0,
        ),
        # TRANSLATE
        #
        Wave(
            type=ReviewType.TRANSLATE,
            weights=Weights(offset=40),
            filter=lambda x: x % 7 == 0,
        ),
        # REVERSE_TRANSLATE
        #
        Wave(
            type=ReviewType.REVERSE_TRANSLATE,
            weights=Weights(offset=50, multiplier=1.5),
            filter=lambda x: x % 7 == 0,
        ),
        Wave(
            type=ReviewType.REVERSE_TRANSLATE,
            weights=Weights(offset=55, multiplier=1.66),
            filter=lambda x: x % 7 == 0,
        ),
        Wave(
            type=ReviewType.REVERSE_TRANSLATE,
            weights=Weights(offset=60, multiplier=1.75),
            filter=lambda x: x % 7 == 0,
        ),
    ],
)
