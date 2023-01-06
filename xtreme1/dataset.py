from typing import Dict
from enum import Enum


class DatasetType(Enum):
    LidarFusion = 'LIDAR_FUSION'
    LidarBasic = 'LIDAR_BASIC'
    Image = 'IMAGE'


class Dataset:
    def __init__(self, data, client):
        for k, v in data.items():
            self.__setattr__(k, v)
        self._client = client
        self._data = {k: v for k, v in self.__dict__.items() if '_' not in k}

    def __str__(self):
        result = []
        for k, v in self._data.items():
            result.append(f'{k}={v}')
        return ', '.join(result)

    def __repr__(self):
        return f"BFDataset({self._data})"

    def edit(self, new_name: str = None, new_description: str = None):
        self.name = new_name or self.name
        self.description = new_description or self.description
        return self._client.edit_dataset(self.id, self.name, self.description)

    def delete(self, is_sure: bool):
        if is_sure:
            return self._client.delete_dataset(self.id)

    def query_data(self, page_no: int, page_size: int, **kwargs) -> Dict:
        return self._client.query_data_under_dataset(self.id, page_no, page_size, **kwargs)
