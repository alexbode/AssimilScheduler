from importlib import util
from pathlib import Path

from src.schema import AssimilCourse


class Courses:
    """
    Courses class that stores all courses defined in ./courses folder.

    this class automatically imports all courses in the ./courses folder
    if there exists a variable named `course`.
    """

    def __init__(self, path: Path = Path(__file__).parent.parent / "courses"):
        self.path: Path = path
        self.courses: list[AssimilCourse] = self._import_courses()

    def _import_courses(self) -> list[AssimilCourse]:
        courses = []
        for file_path in self.path.glob("*.py"):
            if file_path.name.startswith("__"):
                continue
            spec = util.spec_from_file_location(file_path.stem, file_path)
            if spec and spec.loader:
                module = util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, "course"):
                    courses.append(getattr(module, "course"))
        if not courses:
            raise ValueError("No courses found.")
        if len(set([c.name.lower() for c in courses])) != len(courses):
            raise ValueError("Duplicate course names found.")
        return courses

    def get_course(self, course: str) -> AssimilCourse:
        for c in self.courses:
            if c.name.lower() == course.lower():
                return c
        courses = [c.name for c in self.courses]
        raise ValueError(
            f"Invalid course: {course}. Available courses are: {', '.join(courses)}"
        )

    def list_courses(self):
        output = []
        for course in self.courses:
            output.append(course.name)
        return output
