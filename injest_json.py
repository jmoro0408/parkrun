"""
Module to pull the latest parkrun json data and save in a local folder
with todays date.
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Union

import requests

from utils import read_toml, save_json

CONFIG_DIR = "credentials.toml"


def request_json(url: str) -> dict:
    resp = requests.get(url=url)
    return resp.json()


def injest_main():
    config = read_toml(CONFIG_DIR)
    url = config["parkrun_site"]["url"]
    json_save_folder = config["json_directories"]["save_dir"]
    json_dict = request_json(url)
    date_today = datetime.today().strftime("%Y-%m-%d")
    save_json(json_dict, date_today, json_save_folder)
