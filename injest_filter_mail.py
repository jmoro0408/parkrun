from email_new_events import email_new_events_main
from filter_uk_events import filter_uk_events_main
from injest_json import injest_main


def injest_filter_mail():
    injest_main()
    filter_uk_events_main()
    email_new_events_main()


if __name__ == "__main__":
    injest_filter_mail()
