from pathlib import Path
from typing import Union

from utils import read_json, read_toml


def find_latest_n_jsons(uk_jsons: Union[Path, str], n: int = 2) -> list[str]:
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
    files = Path(uk_jsons).glob("**/*")
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


def find_new_parkruns(new_json: dict, prev_json: dict) -> list[str]:
    new_event_names = []
    for event in new_json:
        new_event_names.append(event["properties"]["EventLongName"])
    prev_event_names = []
    for event in prev_json:
        prev_event_names.append(event["properties"]["EventLongName"])
    return [i for i in new_event_names if i not in prev_event_names]


def find_new_parkun_locations(
    new_json: dict, event_name: str
) -> tuple[str, list[float]]:
    for i in range(len(new_json)):
        if new_json[i]["properties"]["EventLongName"] == event_name:
            return event_name, new_json[i]["geometry"]["coordinates"]


if __name__ == "__main__":
    config = read_toml("credentials.toml")
    uk_json_save_dir = config["json_directories"]["uk_save_dir"]
    latest_jsons_fnames = find_latest_n_jsons(uk_json_save_dir)
    latest_jsons = read_latest_n_jsons(uk_json_save_dir, latest_jsons_fnames)
    new_json = latest_jsons[0]
    prev_json = latest_jsons[1]
    new_parkruns = find_new_parkruns(new_json, prev_json)
    new_parkrun_loc_dict = {}
    for run in new_parkruns:
        new_parkrun_loc_dict[run] = find_new_parkun_locations(new_json, run)[1]
    print(new_parkrun_loc_dict)
