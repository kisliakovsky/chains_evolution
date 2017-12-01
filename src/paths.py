from pathlib import Path

IMPORT_DIR = Path("../import")
EXPORT_DIR = Path("../export")
CSV_EXT = "csv"
JSON_EXT = "json"

EXPORT_DIR.mkdir(exist_ok=True)


def build_input_table_path(file_name: str) -> Path:
    return IMPORT_DIR.joinpath(file_name).with_suffix(".{}".format(CSV_EXT)).resolve()


def build_output_graph_path(output_path: Path, file_name: str) -> Path:
    return output_path.joinpath(file_name).with_suffix(".{}".format(JSON_EXT)).resolve()


def build_output_table_path(output_path: Path, file_name: str) -> Path:
    return output_path.joinpath(file_name).with_suffix(".{}".format(CSV_EXT)).resolve()


def build_subsection_dir_path(output_path: Path, file_name: str) -> Path:
    return output_path.joinpath(file_name).resolve()


def build_section_dir_path(file_name: str) -> Path:
    return EXPORT_DIR.joinpath(file_name).resolve()
