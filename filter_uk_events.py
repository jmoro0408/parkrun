"""
Module to filter out UK-based parkrun events from the full, global, parkrun
event json data
"""
from pathlib import Path
from typing import Union

from utils import read_json, read_toml, save_json

UK_COUNTRY_CODE = 97
UK_JSON_SAVE_DIR = "uk_json"


def filter_uk_parkruns(full_json: dict) -> list[dict]:
    """filters a full json file to return only those present in the United Kingdom.

    Args:
        full_json (dict): parkrun event json file to filter

    Returns:
        list[dict]: list of UK event json information
    """
    features_dict = full_json["events"]["features"]
    uk_events = []
    for i in features_dict:
        if i["properties"]["countrycode"] == UK_COUNTRY_CODE:
            uk_events.append(i)
    return uk_events


def find_none_filtered_jsons(
    full_json_save_dir: Union[Path, str], filtered_uk_json_save_dir: Union[Path, str]
) -> list[Union[Path,str]]:
    """When filtering for UK events, we don't want to redo any work that has already
    taken place.
    This function compares a folder containing json files with all (global) events, and
    another with previously filtered UK events.
    It returns the filenames of any events (existing in the full events json folder)
    that have not yet been processed for filtering.

    Args:
        full_json_save_dir (Union[Path, str]):
                directory containing full (global) event json data
        filtered_uk_json_save_dir (Union[Path, str]):
                directory containing previously filtered UK event data

    Returns:
        list[str]: list of full json filenames that have not yet been filtered.
    """
    full_jsons = Path(full_json_save_dir).glob("**/*")
    uk_jsons = Path(filtered_uk_json_save_dir).glob("**/*")
    return [x for x in full_jsons if x not in uk_jsons]


def filter_uk_events_main() -> None:
    """Main function to read in the global event jsons, filter out UK events, and
    save these UK event jsons in a different folder.
    """
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
    return None
