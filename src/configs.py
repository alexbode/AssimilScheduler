import importlib
from pathlib import Path

from src.schema import AssimilCourseConfig


class Configs:
    """
    Configs class that stores all configs defined in ./configs folder.

    this class automatically imports all configs in the ./configs folder
    if there exists a variable named `config`.
    """

    def __init__(self, path: str = Path(__file__).parent.parent / "configs"):
        self.configs_path: str = path
        self.configs = self._import_configs()

    def _import_configs(self):
        configs = []
        target_dir = Path(self.configs_path)
        for file_path in target_dir.glob("*.py"):
            if file_path.name.startswith("__"):
                continue
            spec = importlib.util.spec_from_file_location(file_path.stem, file_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, "config"):
                    configs.append(getattr(module, "config"))
        if not configs:
            raise ValueError("No configs found.")
        if len(set([c.name for c in configs])) != len(configs):
            raise ValueError("Duplicate config names found.")
        return configs

    def get_config(self, course: str) -> AssimilCourseConfig:
        for config in self.configs:
            if config.name == course:
                return config
        courses = [c.name for c in self.configs]
        raise ValueError(
            f"Invalid course: {course}. Available courses are: {', '.join(courses)}"
        )

    def list_configs(self):
        for config in self.configs:
            print(config.name)
