"""
Module to pull the latest parkrun json data and save in a local folder
with todays date.
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Union

import requests

from utils import read_toml

CONFIG_DIR = "credentials.toml"

def request_json(url: str) -> dict:
    resp = requests.get(url=url)
    return resp.json()


def save_json(json_file: dict, save_dir:Union[Path,str]) -> None:
    date_today = datetime.today().strftime("%Y-%m-%d")
    jsonpath = Path(save_dir, f"{date_today}.json")
    with open(jsonpath, "w") as f:
        json.dump(json_file, f, ensure_ascii=False)


if __name__ == "__main__":
    config = read_toml(CONFIG_DIR)
    url = config["parkrun_site"]["url"]
    json_save_folder = config["json_directories"]["save_dir"]
    json_dict = request_json(url)
    save_json(json_dict, json_save_folder)
