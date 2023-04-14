from pathlib import Path
from typing import Union

from utils import read_json, read_toml, save_json

UK_COUNTRY_CODE = 97
UK_JSON_SAVE_DIR = "uk_json"


def filter_uk_parkruns(full_json: dict) -> list[dict]:
    features_dict = full_json["events"]["features"]
    uk_events = []
    for i in features_dict:
        if i["properties"]["countrycode"] == UK_COUNTRY_CODE:
            uk_events.append(i)
    return uk_events


def find_none_filtered_jsons(
    full_json_save_dir: Union[Path, str], uk_json_save_dir: Union[Path, str]
) -> list[str]:
    full_jsons = Path(full_json_save_dir).glob("**/*")
    uk_jsons = Path(uk_json_save_dir).glob("**/*")
    return [x for x in full_jsons if x not in uk_jsons]


if __name__ == "__main__":
    config = read_toml("credentials.toml")
    json_save_dir = config["json_directories"]["save_dir"]
    uk_json_save_dir = config["json_directories"]["uk_save_dir"]
    none_filtered = find_none_filtered_jsons(json_save_dir, uk_json_save_dir)
    uk_events: list[dict] = []
    for uk_event in none_filtered:
        event = read_json(uk_event)
        uk_events.append(filter_uk_parkruns(event))
    for fname, uk_event in zip(none_filtered, uk_events):
        fname = Path(fname.name)
        save_json(uk_event, fname, UK_JSON_SAVE_DIR)
