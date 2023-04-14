from pathlib import Path
from typing import Union

import tomli


def read_toml(toml_dir: Union[Path, str]) -> dict:
    with open(toml_dir, mode="rb") as fp:
        return tomli.load(fp)