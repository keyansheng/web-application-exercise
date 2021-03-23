from datetime import datetime
from pytz import timezone

DT_FORMAT = "%Y-%m-%d %H:%M:%S"
UTC = timezone("UTC")
END = timezone("Asia/Singapore")


def convert_timezone(dt_str, start=UTC, end=END):
    # converts datetime string to datetime object (no time zone)
    dt_none = datetime.strptime(dt_str, DT_FORMAT)

    # converts datetime object (no time zone) to datetime object (start time zone)
    dt_start = start.localize(dt_none)

    # converts datetime object (start time zone) to datetime object (end time zone)
    dt_end = dt_start.astimezone(end)

    # converts datetime object (end time zone) to datetime string and returns it
    return dt_end.strftime(DT_FORMAT)
