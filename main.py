import sys
import argparse

from src.configs import Configs
from src.scheduler import AssimilScheduler

parser = argparse.ArgumentParser(description="CLI script for the Assimil scheduler.")
parser.add_argument("--course", help="The name of the Assimil course. Use list configs to see available courses.")
parser.add_argument(
    "--list_configs",
    action="store_true",
    help="List all configs in the configs folder.",
)
parser.add_argument(
    "--next", type=int, default=4, help="Return next n lessons, default is 4."
)
parser.add_argument(
    "--complete",
    action="store_true",
    help="Mark the next lesson as completed.",
)
parser.add_argument(
    "--undo",
    action="store_true",
    help="Unmark the latest lesson as completed.",
)

if __name__ == "__main__":
    args = parser.parse_args()

    configs = Configs()

    if args.list_configs:
        configs.list_configs()
        sys.exit(0)

    if args.course and args.next:
        config = configs.get_config(args.course)
        s = AssimilScheduler(config.name, config)
        if args.complete:
            s.complete()
            sys.exit(0)
        if args.undo:
            s.undo_last_review()
            sys.exit(0)
        s.get_next_lesson(next_n=args.next)
        sys.exit(0)
