from pathlib import Path

IMPORT_DIR = "../import"
CSV_EXT = "csv"


def build_input_table_path(file_name: str) -> Path:
    return Path(IMPORT_DIR).joinpath(file_name).with_suffix(".{}".format(CSV_EXT)).resolve()