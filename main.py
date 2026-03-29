import sys
import argparse

from src.courses import Courses
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
    help="Unmark the latest lesson as completed.",
)

if __name__ == "__main__":
    args = parser.parse_args()

    courses = Courses()

    if args.list_courses:
        courses.list_courses()
        sys.exit(0)

    if args.course and args.next:
        course = courses.get_course(args.course)
        s = AssimilScheduler(course)
        if args.complete:
            s.complete()
            sys.exit(0)
        if args.undo:
            s.undo_last_review()
            sys.exit(0)
        s.get_next_lesson(next_n=args.next)
        sys.exit(0)
