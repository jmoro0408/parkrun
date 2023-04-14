from pathlib import Path
from typing import Union

from utils import read_json, read_toml, save_json

UK_COUNTRY_CODE = 97
UK_JSON_SAVE_DIR = "parsed_json"


def find_latest_n_jsons(json_save_dir: Union[Path, str], n: int = 2) -> list[str]:
    """Finds the latest n jsons saved in the saved json directory.
    Deliberately uses the date in the filename instead of accessing
    file date created data, as it's likely going to be written to a
    data lake in the future.

    Args:
        json_save_dir (Union[Path,str]): folder directory with saved json files
        n (int, optional): Quantity of latest files to return. Defaults to 2.

    Returns:
        list[str]: filenames (dates) of latest files
    """
    files = Path(json_save_dir).glob("**/*")
    file_dates = [x.stem for x in files]
    return sorted(file_dates, reverse=True)[:n]


def read_latest_n_jsons(
    json_save_dir: Union[Path, str], latest_files: list[str]
) -> list[dict]:
    newest_jsons = []
    for filename in latest_files:
        full_filename = Path(json_save_dir, filename + ".json")
        newest_jsons.append(read_json(full_filename))
    return newest_jsons


def filter_uk_parkruns(full_json: dict) -> list[dict]:
    features_dict = full_json["events"]["features"]
    uk_events = []
    for i in features_dict:
        if i["properties"]["countrycode"] == UK_COUNTRY_CODE:
            uk_events.append(i)
    return uk_events


if __name__ == "__main__":
    config = read_toml("credentials.toml")
    json_save_dir = config["json_directories"]["save_dir"]
    latest_json_filenames = find_latest_n_jsons(json_save_dir)
    latest_jsons = read_latest_n_jsons(
        json_save_dir, latest_json_filenames
    )  # get latest 2 jsons to compare
    uk_events: list[dict] = []  # list of dicts -> uk events for each top n jsons
    for json_dict in latest_jsons:
        uk_events.append(filter_uk_parkruns(json_dict))
    for fname, uk_event in zip(latest_json_filenames, uk_events):
        save_json(uk_event, fname, UK_JSON_SAVE_DIR)
