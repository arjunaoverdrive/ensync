from typing import Dict, Optional, Any
from requests import get, put, delete
import json
import logging

from app_config import REMOTE_LOCATION
logger = logging.getLogger('storage')
API = 'https://cloud-api.yandex.net/v1/disk/resources'


class RemoteStorage:

    def __init__(self, api_token: str):
        self.__api_token = api_token
        self.__headers = {'Authorization': f'OAuth {self.__api_token}', 'Content-Type': 'application/json',
                          'Accept': '*/*'}

        self.__params = {'fields': '_embedded.items.name'}

    def get_files_data(self) -> Optional[Dict[str, Any]]:
        data = {}
        self.__params['path'] = REMOTE_LOCATION

        response = get(API, headers=self.__headers, params=self.__params)
        if response.status_code == 401:
            logger.warning('Token is absent or invalid!')
            logger.error(f'{data["message"]} {data["error"]}')
            return
        data = json.loads(response.text)

        return data['_embedded']['items']

    def init_remote_directory(self) -> Optional[bool]:
        self.__params['path'] = REMOTE_LOCATION
        try:
            response = get(API, headers=self.__headers, params=self.__params)

            data = json.loads(response.text)
            if response.status_code == 401:
                logger.warning('Token is absent or invalid!')
                logger.error(f'{data["message"]} {data["error"]}')
                raise ValueError(f'{data["message"]} {data["error"]}')
            elif response.status_code == 404:
                self.create_remote_directory()
                return True
            elif response.status_code == 200:
                logger.info(f'Found existing directory {REMOTE_LOCATION}.')
                return True
            else:
                logger.error(f'{response.status_code} {response.text} {response.content}')
                return False
        except Exception as e:
            logger.error(e)
            return False

    def create_remote_directory(self) -> None:
        logger.info('Remote folder does not exist. Creating...')
        response = put(API, headers=self.__headers, params=self.__params)

        if response.status_code == 200:
            logger.info('Successfully created remote directory')
        else:
            logger.error(f'{response.status_code} {response.text} {response.content}')

    def load(self, path: str, overwrite: bool = False) -> None:
        self.__params['path'] = REMOTE_LOCATION + '/' + path
        self.__params['overwrite'] = overwrite
        try:
            response = get(API + '/upload', headers=self.__headers, params=self.__params)
            link = json.loads(response.text)['href']
            res = put(link, headers=self.__headers)
            if res.status_code != 201:
                logger.error(f'{res.status_code} {res.text} {res.content}')
        except Exception as e:
            logger.error(e)

    def reload(self, path: str) -> None:
        logger.info(f'Updating file {path}...')
        self.load(path, True)
        logger.info(f'Successfully updated file {path}')

    def delete_file(self, path: str) -> None:
        self.__params['path'] = REMOTE_LOCATION + f'/{path}'
        self.__params['permanently'] = True

        try:
            logger.info(f'Deleting file {path} from storage...')
            response = delete(API, headers=self.__headers, params=self.__params)
            if response.status_code == 204:
                logger.info(f'Successfully deleted file {path} from storage.')
            else:
                logger.error(f'{response.status_code} {response.text} {response.content}')
        except Exception as e:
            logger.error(e)
