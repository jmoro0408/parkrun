"""
Common functions used in multiple files.
"""
import json
from pathlib import Path
from typing import Union

import tomli


def read_toml(toml_dir: Union[Path, str]) -> dict:
    """reads in a toml file as a python dict

    Args:
        toml_dir (Union[Path, str]): filepath of toml file

    Returns:
        dict: dictonary representation of data in toml file
    """
    with open(toml_dir, mode="rb") as fp:
        return tomli.load(fp)


def read_json(json_dir: Union[Path, str]) -> dict:
    """reads in a json file as a python dict

    Args:
        json_dir (Union[Path, str]): filepath of json file

    Returns:
        dict: dictonary representation of data in json file
    """
    with open(json_dir, "r") as f:
        return json.load(f)


def save_json(dict_to_save: dict, fname: str, save_dir: Union[Path, str]) -> None:
    """saves python dictonary as a json file.

    Args:
        dict_to_save(dict): dictionary to save
        fname (str): filename of new json file
        save_dir (Union[Path, str]): where to save new json file
    """
    if Path(fname).suffix != ".json":
        fname = fname + ".json"
    jsonpath = Path(save_dir, fname)
    with open(jsonpath, "w") as f:
        json.dump(dict_to_save, f, ensure_ascii=False)
    return None
