import unittest
from pathlib import Path

from src.courses import Courses


class TestCourses(unittest.TestCase):

    fixtures_folder = Path(__file__).parent / "fixtures"

    def test_no_configs_found(self):
        expected_message = "No courses found."
        with self.assertRaises(ValueError) as e:
            Courses(path=self.fixtures_folder / "folder_without_courses")
        self.assertEqual(str(e.exception)[: len(expected_message)], expected_message)

    def test_duplicate_courses(self):
        expected_message = "Duplicate course names found."
        with self.assertRaises(ValueError) as e:
            Courses(path=self.fixtures_folder / "folder_with_duplicate_courses")
        self.assertEqual(str(e.exception)[: len(expected_message)], expected_message)

    def test_valid_courses(self):
        course_name = "SpanishAdvanced"
        course = Courses(path=self.fixtures_folder).get_course(course_name)
        self.assertEqual(course.name, course_name)

    def test_course_does_not_exist(self):
        course_name = "CourseDoesNotExist"
        expected_message = f"Invalid course: {course_name}. Available courses are: "
        with self.assertRaises(ValueError) as e:
            Courses(path=self.fixtures_folder).get_course(course_name)
        self.assertEqual(str(e.exception)[: len(expected_message)], expected_message)
