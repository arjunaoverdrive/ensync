import util
import json
from typing import Dict, List, Any
from os import path, listdir

REGISTRY = '.registry.json'


class Registry:

    def __init__(self, registry: str):
        self.__registry = registry

    def read_registry(self) -> Dict[str, Any]:
        registry_data = {}
        if path.exists(self.__registry) and path.getsize(self.__registry) > 0:
            with open(self.__registry, 'r', encoding='utf-8') as fin:
                registry_data = json.load(fin)

        return registry_data

    def update_registry(self, registry_data: Dict[str, str], local_folder: str) -> None:
        files = listdir(local_folder)

        for file in files:
            if file not in registry_data and file != REGISTRY:
                f_modified = path.getmtime(path.join(local_folder, file))
                registry_data[file] = util.convert_timestamp_to_datetime_str(f_modified)

        file_names_to_delete = []

        for file_name in registry_data.keys():
            if file_name not in files:
                file_names_to_delete.append(file_name)

        for file_name in file_names_to_delete:
            del registry_data[file_name]

        if len(registry_data) > 0:
            with open(self.__registry, 'w', encoding='utf-8') as fout:
                json.dump(registry_data, fout, indent=2)

    def get_updated_files_list(self, registry_data: Dict[str, str], local_folder: str) -> List[str]:
        files = listdir(local_folder)
        files_data = {file: util.get_file_modified_time_str(file, local_folder) for file in files}

        files_to_reload = []
        for file, modified in files_data.items():
            if file not in registry_data:
                continue

            r_modified = registry_data[file].strip()
            if r_modified < modified:
                files_to_reload.append(file)
                registry_data[file] = modified
        with open(self.__registry, 'w', encoding='utf-8') as fout:
            json.dump(registry_data, fout, indent=2)

        return files_to_reload
