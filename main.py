from time import sleep
import logging.config

from logging_config import dict_config
from remote_storage import RemoteStorage
from local_storage import LocalStorage
from app_config import API_TOKEN

logger = logging.getLogger('app')
logging.config.dictConfig(dict_config)


def main() -> None:
    remote_storage = RemoteStorage(API_TOKEN)
    exists = remote_storage.init_remote_directory()
    while not exists:
        sleep(60)
        exists = remote_storage.init_remote_directory()

    local_storage = LocalStorage(remote_storage)
    local_storage.check_local_folder()
    while True:
        local_storage.sync_files()


if __name__ == '__main__':
    main()
