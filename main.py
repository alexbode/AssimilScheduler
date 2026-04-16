import sys
import argparse

from src.courses import Courses
from src.db import DB
from src.scheduler import AssimilScheduler

parser = argparse.ArgumentParser(description="CLI script for the Assimil scheduler.")
parser.add_argument(
    "--course",
    "-c",
    type=str,
    help="The name of the Assimil course. Use list configs to see available courses.",
)
parser.add_argument(
    "--list_courses",
    "-l",
    action="store_true",
    help="List all courses in the courses folder.",
)
parser.add_argument(
    "--next", "-n", type=int, default=4, help="Return next n lessons, default is 4."
)
parser.add_argument(
    "--done",
    "-d",
    action="store_true",
    help="Mark the next lesson as done.",
)
parser.add_argument(
    "--undo",
    "-u",
    action="store_true",
    help="Unmark the latest lesson as done.",
)
parser.add_argument(
    "--manual_update",
    "-m",
    nargs=2,
    metavar=("LESSON", "REVIEW_TYPE"),
    help="Manually update the review count for a specific lesson and review type. Example: --manual_update 5 LISTEN",
)

parser.add_argument(
    "--query",
    "-q",
    type=str,
    help="Query the sqlite3 db"
)

if __name__ == "__main__":
    args = parser.parse_args()

    courses = Courses()

    if args.list_courses:
        for c in courses.list_courses():
            print(c)
        sys.exit(0)

    if args.query:
        db = DB()
        print(db.query(args.query))
        sys.exit(0)


    if args.course and args.next:
        course = courses.get_course(args.course)
        if args.done and not args.manual_update:
            s.mark_as_done()
            sys.exit(0)
        if args.done and args.manual_update:
            lesson = int(args.manual_update[0])
            review_type = args.manual_update[1]
            s.manual_update(lesson, review_type)
            sys.exit(0)
        if args.undo:
            s.undo_last_review()
            sys.exit(0)
        idx = 0
        for review in s.review_generator(args.next):
            idx += 1
            print(f"{idx}.")
            print(review)
        sys.exit(0)
