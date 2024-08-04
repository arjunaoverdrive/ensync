import logging
from os import path, listdir
from time import sleep
from typing import List, Dict, Any

from app_config import LOCATION, PERIOD
from remote_storage import RemoteStorage
from registry import Registry

logger = logging.getLogger('local')
REGISTRY = '.registry.json'


class LocalStorage:

    def __init__(self, remote_storage: RemoteStorage):
        self.__local_folder = path.abspath(LOCATION)
        self.__remote_storage = remote_storage
        self.__period = int(PERIOD) * 60
        self.__registry = Registry(path.join(self.__local_folder, REGISTRY))

    def check_local_folder(self) -> None:
        if not path.exists(path.abspath(self.__local_folder)):
            logger.error(f'Folder {self.__local_folder} doesn\'t exist.')
            raise IOError('Please specify the absolute path to the existing folder to track as the LOCATION parameter '
                          'in the config.ini file.')
        else:
            logger.info(f'Started tracking files in {self.__local_folder}')

    def sync_files(self) -> None:
        logger.info("Synching files...")

        registry_data = self.__registry.read_registry()
        self.__registry.update_registry(registry_data=registry_data,
                                        local_folder=self.__local_folder)

        s_files = {}
        try:
            s_files = self.__remote_storage.get_files_data()
        except Exception as e:
            logger.error(e)
        s_files_names = [item['name'] for item in s_files]

        files = listdir(self.__local_folder)

        files_to_reload = self.__registry.get_updated_files_list(registry_data=registry_data,
                                                                 local_folder=self.__local_folder)
        self.upload_new_files(files, s_files_names)
        self.delete_local_files(files, s_files)
        for file in files_to_reload:
            self.__remote_storage.reload(file)
        sleep(self.__period)

    def upload_new_files(self, files: List[str], s_files_names: List[str]) -> None:
        for file in files:
            if file not in s_files_names and file != REGISTRY:
                logger.info(f'Uploading new file {file} to storage...')
                self.__remote_storage.load(file)
                logger.info(f'Uploaded new file {file} to storage.')

    def delete_local_files(self, files: List[str], s_files: Dict[str, Any]) -> None:
        for s_file in s_files:
            if s_file['name'] not in files:
                self.__remote_storage.delete_file(s_file['name'])
