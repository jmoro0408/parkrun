import json
from datetime import datetime
from pathlib import Path
from typing import Union

import tomli


def read_toml(toml_dir: Union[Path, str]) -> dict:
    with open(toml_dir, mode="rb") as fp:
        return tomli.load(fp)


def read_json(json_file: Union[Path, str]) -> dict:
    with open(json_file, "r") as f:
        return json.load(f)


def save_json(json_file: dict, fname: str, save_dir: Union[Path, str]) -> None:
    jsonpath = Path(save_dir, f"{fname}.json")
    with open(jsonpath, "w") as f:
        json.dump(json_file, f, ensure_ascii=False)
