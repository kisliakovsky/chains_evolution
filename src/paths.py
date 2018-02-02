from pathlib import Path
from typing import Iterator, Iterable

IMPORT_DIR = Path("../import")
EXPORT_DIR = Path("../export")
CSV_EXT = "csv"
JSON_EXT = "json"
TXT_EXT = "txt"
LOG_EXT = "log"
PNG_EXT = "png"


# noinspection PyTypeChecker
def collect_subpaths(path: Path) -> Iterator[Path]:
    return path.glob('*')


class PathCleaner(object):

    def __init__(self, paths: Iterator[Path]) -> None:
        self.__paths = paths

    @property
    def paths(self) -> Iterator[Path]:
        return self.__paths

    def process(self) -> None:
        for path in self.paths:
            if path.is_dir():
                subpaths = collect_subpaths(path)
                path_cleaner = PathCleaner(subpaths)
                path_cleaner.process()
                path.rmdir()
            else:
                path.unlink()


if EXPORT_DIR.exists():
    subpaths = collect_subpaths(EXPORT_DIR)
    cleaner = PathCleaner(subpaths)
    cleaner.process()
else:
    EXPORT_DIR.mkdir(exist_ok=False)


def build_input_table_path(file_name: str) -> Path:
    return IMPORT_DIR.joinpath(file_name).with_suffix(".{}".format(CSV_EXT)).resolve()


def build_input_txt_path(file_name: str) -> Path:
    return IMPORT_DIR.joinpath(file_name).with_suffix(".{}".format(TXT_EXT)).resolve()


def build_output_graph_path(output_path: Path, file_name: str) -> Path:
    return output_path.joinpath(file_name).with_suffix(".{}".format(JSON_EXT)).resolve()


def build_output_table_path(output_path: Path, file_name: str) -> Path:
    return output_path.joinpath(file_name).with_suffix(".{}".format(CSV_EXT)).resolve()


def build_output_log_path(output_path: Path, file_name: str) -> Path:
    return output_path.joinpath(file_name).with_suffix(".{}".format(LOG_EXT)).resolve()


def build_output_chart_path(output_path: Path, file_name: str) -> Path:
    return output_path.joinpath(file_name).with_suffix(".{}".format(PNG_EXT)).resolve()


def build_default_output_chart_path(file_name: str) -> Path:
    return EXPORT_DIR.joinpath(file_name).with_suffix(".{}".format(PNG_EXT)).resolve()


def build_subsection_dir_path(section_path: Path, file_name: str) -> Path:
    return section_path.joinpath(file_name).resolve()


def build_section_dir_path(file_name: str) -> Path:
    return EXPORT_DIR.joinpath(file_name).resolve()


def create_section(file_name: str) -> Path:
    path = build_section_dir_path(file_name)
    path.mkdir(exist_ok=True)
    return path


def create_subsection(section_path: Path, file_name: str) -> Path:
    path = build_subsection_dir_path(section_path, file_name)
    path.mkdir(exist_ok=True)
    return path
