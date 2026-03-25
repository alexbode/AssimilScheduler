import unittest
from pathlib import Path
from datetime import datetime

from src.configs import Configs


class TestConfigs(unittest.TestCase):

    fixtures_folder = Path(__file__).parent / "fixtures"

    def test_no_configs_found(self):
        expected_message = "No configs found."
        with self.assertRaises(ValueError) as e:
            Configs(path=self.fixtures_folder / "folder_without_configs")
        self.assertEqual(str(e.exception)[: len(expected_message)], expected_message)

    def test_duplicate_configs(self):
        expected_message = "Duplicate config names found."
        with self.assertRaises(ValueError) as e:
            Configs(path=self.fixtures_folder / "folder_with_duplicate_configs")
        self.assertEqual(str(e.exception)[: len(expected_message)], expected_message)

    def test_valid_configs(self):
        config_name = "SpanishAdvanced"
        config = Configs(path=self.fixtures_folder).get_config(config_name)
        self.assertEqual(config.name, config_name)

    def test_config_does_not_exist(self):
        config_name = "ConfigDoesNotExist"
        expected_message = f"Invalid course: {config_name}. Available courses are: "
        with self.assertRaises(ValueError) as e:
            Configs(path=self.fixtures_folder).get_config(config_name)
        self.assertEqual(str(e.exception)[: len(expected_message)], expected_message)
