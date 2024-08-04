from os import path
from datetime import datetime
DATEFORMAT = '%Y-%m-%d %H:%M:%S'


def get_file_modified_time_str(file, local_folder):
    return convert_timestamp_to_datetime_str(path.getmtime(path.join(local_folder, file)))


def convert_timestamp_to_datetime_str(timestamp):
    return datetime.strftime(datetime.fromtimestamp(timestamp), DATEFORMAT)