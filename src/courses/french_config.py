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
            review_type=ReviewType.LISTEN,
            filter=lambda x: x % 7 == 0,
        ),
        Wave(
            review_type=ReviewType.LISTEN,
            weights=Weights(offset=1, multiplier=1.5),
            filter=lambda x: x % 7 == 0,
        ),
        Wave(
            review_type=ReviewType.LISTEN,
            weights=Weights(offset=50, multiplier=1.5),
            filter=lambda x: x % 7 == 0,
        ),
        Wave(
            review_type=ReviewType.LISTEN,
            weights=Weights(offset=LESSON_COUNT),
            filter=lambda x: x % 7 == 0,
        ),
        # READ
        #
        Wave(
            review_type=ReviewType.READ,
            weights=Weights(offset=10),
        ),
        Wave(
            review_type=ReviewType.READ,
            weights=Weights(offset=11, multiplier=1.75),
            filter=lambda x: x % 7 != 0,
        ),
        Wave(
            review_type=ReviewType.READ,
            weights=Weights(offset=LESSON_COUNT),
        ),
        # SHADOW
        #
        Wave(
            review_type=ReviewType.SHADOW,
            weights=Weights(offset=20),
            filter=lambda x: x % 7 == 0,
        ),
        Wave(
            review_type=ReviewType.SHADOW,
            weights=Weights(offset=70, multiplier=1.5),
            filter=lambda x: x % 7 == 0,
        ),
        Wave(
            review_type=ReviewType.SHADOW_BLIND,
            weights=Weights(offset=80, multiplier=1.5),
            filter=lambda x: x % 7 == 0,
        ),
        Wave(
            review_type=ReviewType.SHADOW_BLIND,
            weights=Weights(offset=90, multiplier=1.5),
            filter=lambda x: x % 7 == 0,
        ),
        # SCRIPTORIUM
        #
        Wave(
            review_type=ReviewType.SCRIPTORIUM,
            weights=Weights(offset=30),
            filter=lambda x: x % 7 == 0,
        ),
        # TRANSCRIBE
        #
        Wave(
            review_type=ReviewType.TRANSCRIBE,
            weights=Weights(offset=35, multiplier=1.5),
            filter=lambda x: x % 7 == 0,
        ),
        # TRANSLATE
        #
        Wave(
            review_type=ReviewType.TRANSLATE,
            weights=Weights(offset=40),
            filter=lambda x: x % 7 == 0,
        ),
        # REVERSE_TRANSLATE
        #
        Wave(
            review_type=ReviewType.REVERSE_TRANSLATE,
            weights=Weights(offset=50, multiplier=1.5),
            filter=lambda x: x % 7 == 0,
        ),
        Wave(
            review_type=ReviewType.REVERSE_TRANSLATE,
            weights=Weights(offset=55, multiplier=1.66),
            filter=lambda x: x % 7 == 0,
        ),
        Wave(
            review_type=ReviewType.REVERSE_TRANSLATE,
            weights=Weights(offset=60, multiplier=1.75),
            filter=lambda x: x % 7 == 0,
        ),
    ],
)
