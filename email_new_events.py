import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Union

import pandas as pd
import plotly.express as px

from utils import read_json, read_toml

MAP_SAVE_FNAME = Path("maps", datetime.today().strftime('%Y-%m-%d') + ".html")

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

def create_map(new_parkun_dict:dict,
               mapbox_token:str,
               save_fname:Union[Path,str])->None:
    df = (pd.DataFrame.from_dict(new_parkun_dict)
      .T
      .reset_index().
      rename(columns = {"index":"Event Name", 0:"lon", 1:"lat"}))

    px.set_mapbox_access_token(mapbox_token)
    fig = px.scatter_mapbox(df,
                            lat="lat",
                            lon="lon",
                            hover_name = "Event Name",
                    size_max=15,
                    zoom=3.5,
                    title = "New Parkrun Events",
                    mapbox_style = 'open-street-map')
    fig.write_html(save_fname)


def send_email(sender:str, password:str, recipient:str,mail_content:str) -> None:

    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = recipient
    message['Subject'] = 'This weeks new parkruns'   #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender, password) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender, recipient, text)
    session.quit()
    print('Mail Sent')


if __name__ == "__main__":
    config = read_toml("credentials.toml")
    uk_json_save_dir = config["json_directories"]["uk_save_dir"]
    mapbox_token = config['mapbox_token']['mapbox_token']
    sender_address = config['gmail']['sender_address']
    gmail_password = config['gmail']['password']

    latest_jsons_fnames = find_latest_n_jsons(uk_json_save_dir)
    latest_jsons = read_latest_n_jsons(uk_json_save_dir, latest_jsons_fnames)
    new_json = latest_jsons[0]
    prev_json = latest_jsons[1]
    new_parkruns = find_new_parkruns(new_json, prev_json)
    new_parkrun_loc_dict = {}
    for run in new_parkruns:
        new_parkrun_loc_dict[run] = find_new_parkun_locations(new_json, run)[1]

    create_map(new_parkrun_loc_dict, mapbox_token, MAP_SAVE_FNAME)
    test_content =  '''Hello,
    This is a simple mail. There is only text, no attachments are there The mail is sent using Python SMTP library.
    Thank You'''
    send_email(sender_address,
               gmail_password,
               "briananowe@gmail.com",
               test_content)
