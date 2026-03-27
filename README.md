# Assimil scheduler

This is a basic program to schedule the sequence of lessons for the [Assimil](www.assimil.com) language learning books.

You can define multiple types of `waves` (listening, shadowing, reading, translation, etc.) to review the Assimil textbook. And this program will keep track of where you are in each wave and which lesson to review next.

## How to run
* `python3 main.py --course=SpanishAdvanced --next=5`
* `uv run uvicorn server:app --reload --port=8080`
* `python3 -m unittest discover -s tests`

## Concepts
### Config
The config defines the review plan. See the src/configs/ folder
### Wave
A wave is type of review.
A wave has 3 fields.
1. type
2. weights
3. filter

#### Weights
A way to manipulate the waves start date and frequency.

#### filter
A way to filter lessons out

#### Examples
Lets say there is an Assimil FakeLanguage course with 10 lessons. Below is a basic starting config

```
LESSON_COUNT=10
config = AssimilCourseConfig(
    name="FakeLanguage",
    lesson_count=LESSON_COUNT,
    waves=[
        Wave(
            type=PracticeType.LISTEN,
        ),
    ],
)
```

When `python3 main.py --course=FakeLanguage --next=5` is run it will return:

```
Lesson: 1, PracticeType.LISTEN
Lesson: 2, PracticeType.LISTEN
Lesson: 3, PracticeType.LISTEN
Lesson: 4, PracticeType.LISTEN
Lesson: 5, PracticeType.LISTEN
```

After doing the listening review for FakeLesson lesson 1, to mark it complete run the command: `python3 main.py --course=FakeLanguage --complete`


Then when `python3 main.py --course=FakeLanguage --next=5` is run again, it will return the below because lesson one was completed:

```
Lesson: 2, PracticeType.LISTEN
Lesson: 3, PracticeType.LISTEN
Lesson: 4, PracticeType.LISTEN
Lesson: 5, PracticeType.LISTEN
Lesson: 6, PracticeType.LISTEN
```

The now lets add a diferent type of review/wave to the config.

```
LESSON_COUNT=10
config = AssimilCourseConfig(
    name="FakeLanguage",
    lesson_count=LESSON_COUNT,
    waves=[
        Wave(
            type=PracticeType.LISTEN,
        ),
        Wave(
            type=PracticeType.READ,
            filter=lambda x: x % 7 == 0,
            weights=Weights(offset=2)
        ),
    ],
)
```

Then when `python3 main.py --course=FakeLanguage --next=16` is run again, it will return the below. Notice how the offset=2 is set for the READ wave in the output below the READ lesson is 2 less than the previous LISTEN lesson. Also note how lesson 7 READ is skipped because of the filter is explicitly skipping every seventh lesson.

```
Lesson: 1, PracticeType.LISTEN
Lesson: 2, PracticeType.LISTEN
Lesson: 3, PracticeType.LISTEN
Lesson: 1, PracticeType.READ
Lesson: 4, PracticeType.LISTEN
Lesson: 2, PracticeType.READ
Lesson: 5, PracticeType.LISTEN
Lesson: 3, PracticeType.READ
Lesson: 6, PracticeType.LISTEN
Lesson: 4, PracticeType.READ
Lesson: 7, PracticeType.LISTEN
Lesson: 5, PracticeType.READ
Lesson: 8, PracticeType.LISTEN
Lesson: 6, PracticeType.READ
Lesson: 9, PracticeType.LISTEN
Lesson: 8, PracticeType.READ
```


