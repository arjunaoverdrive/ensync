# Ensync file tracking app

## Technologies used: Python 3.8

### Usage

1. Clone the project from the GitHub repository.
2. Open the config.ini file and add the following values:
    - API_TOKEN -- your Yandex Disk Api token
    - LOCATION -- the absolute path of the folder to track
3. Optionally, specify the values under the DEFAULT section.
    - REMOTE_LOCATION -- directory on Yandex Disk, in which the files will be uploaded. This must be an empty directory:
      if there are any files in it, they will be removed. If it doesn't exist, the app will create it.
    - PERIOD -- time interval to track changes in teh LOCATION folder.
    - LOG -- path to the log file.
4. Run the main.py script.

### How Does It Work?

The app tracks the files in the LOCATION folder. If there are new files, they are uploaded to your Yandex Disk storage;
if some files have been deleted from the LOCATION folder, they get deleted from the Yandex Disk storage;
if they have been modified, the files are updated in the Yandex Disk storage, too.
