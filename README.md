# Automatic Parkrun event notification with Python and Apache Airflow


## Background

[Parkrun](https://www.parkrun.org.uk/) is a free, community event where you can walk, jog, run, volunteer or spectate. parkrun is 5k and takes place every Saturday morning. junior parkrun is 2k, dedicated to 4-14 year olds and their families, every Sunday morning.

There are currently more than 2,000 parkrun locations taking part in over 22 countries.

To try and "complete" different parkrun challenegs is fairly common, including running all the events within a city, or trying to complete a different event for each letter of the alphabet.

New parkrun events are always springing up, however a list of new events is not published by parkrun itself, mainly to avoid very large turnouts to new events.

## Project


![architecture diagram](readme_visuals\architecture.png)

The workflow automatically runs weekly, every Sunday morning. It uses the Python [requests](https://requests.readthedocs.io/en/latest/) library to scrape parkrun event json data and store it locally.

All UK events are then filtered out and the latest event data compared to that of the previous week. All new events are collected and their locations plotted on an interactive map of the UK, an example static version is shown below. For the full interative version, check out [my blog post mirror of this readme](https://jmoro0408.github.io/).


![static_map](readme_visuals\map_static.png)

Finally the new events are emailed along with the interactive map to a distirbution list.

These tasks are orchestrated via [Apache Airflow](https://airflow.apache.org/docs/apache-airflow/stable/index.html), contained within Docker, hosted on a raspberry pi. This is almost certainly overkill for what could feasibly automated with a simple cron job, however it was a good opportunity to expand both my Docker and Airflow knowledge.