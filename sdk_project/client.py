import os
from typing import List, Dict, Optional

import requests

from .api import Api
from .dataset import DatasetType, Dataset
from .exceptions import SDKException


class Client:

    def __init__(self, access_token: str, base_url: str):
        self.api = Api(access_token=access_token, base_url=base_url)

    def create_dataset(self, name: str, annotation_type: DatasetType, description: str = None) -> Dataset:
        endpoint = 'dataset/create'
        payload = {
            'name': name,
            'type': annotation_type.value,
            'description': description
        }

        resp = self.api.post_request(endpoint, payload=payload)

        return Dataset(resp, self)

    def edit_dataset(self, dataset_id: str, name: str, description: str) -> str:
        endpoint = f'dataset/update/{dataset_id}'
        payload = {
            'name': name,
            'description': description
        }

        self.api.post_request(endpoint, payload=payload)

        return 'Success!'

    def delete_dataset(self, dataset_id: str) -> str:
        endpoint = f'dataset/delete/{dataset_id}'
        self.api.post_request(endpoint=endpoint, payload=None)

        return 'Success!'

    def _query_a_single_dataset(self, dataset_id: str) -> Dict:
        endpoint = f'dataset/info/{dataset_id}'
        resp = self.api.get_request(endpoint=endpoint, params=None)

        return resp

    def _query_the_list_of_datasets(
            self,
            page_no: int,
            page_size: int,
            name: Optional[str] = None,
            create_start_time: Optional[str] = None,
            create_end_time: Optional[str] = None,
            sort_by: Optional[str] = None,
            ascending: Optional[bool] = True,
            dataset_type: Optional[DatasetType] = None
    ) -> Dict:
        endpoint = 'dataset/findByPage'

        params = {
            'pageNo': page_no,
            'pageSize': page_size,
            'name': name,
            'createStartTime': create_start_time,
            'createEndTime': create_end_time,
            'sortField': sort_by,
            'ascOrDesc': 'ASC' if ascending else 'DESC',
            'type': dataset_type
        }

        resp = self.api.get_request(endpoint=endpoint, params=params)

        return resp

    def query_dataset(
            self,
            dataset_id: Optional[str] = None,
            chunk_size: int = 1,
            dataset_name: Optional[str] = None,
            create_start_time: Optional[str] = None,
            create_end_time: Optional[str] = None,
            sort_by: Optional[str] = 'CREATED_AT',
            ascending: Optional[bool] = True,
            dataset_type: Optional[DatasetType] = None
    ) -> Dict:
        if dataset_id:
            dataset_name = self._query_a_single_dataset(dataset_id)['name']

        return self._query_the_list_of_datasets(
            page_no=1,
            page_size=chunk_size,
            name=dataset_name,
            create_start_time=create_start_time,
            create_end_time=create_end_time,
            sort_by=sort_by,
            ascending=ascending,
            dataset_type=dataset_type
        )

    def query_data_under_dataset(self, dataset_id: str, page_no: int, page_size: int, **kwargs) -> Dict:
        endpoint = 'data/findByPage'

        params = {
            'datasetId': dataset_id,
            'pageNo': page_no,
            'pageSize': page_size,
            'name': kwargs.get('name'),
            'createStartTime': kwargs.get('createStartTime'),
            'createEndTime': kwargs.get('createEndTime'),
        }

        resp = self.api.get_request(endpoint=endpoint, params=params)

        return resp

    def delete_multiple_data(self, ids: List[str]) -> str:
        endpoint = 'data/deleteBatch'

        payload = {
            'ids': ids
        }

        self.api.post_request(endpoint=endpoint, payload=payload)

        return 'success'

    def query_data(self, data_id: str) -> Dict:
        endpoint = f'data/info/{data_id}'
        resp = self.api.get_request(endpoint=endpoint, params=None)

        return resp

    def query_multiple_data(self, data_ids: str) -> Dict:
        endpoint = 'data/listByIds'

        params = {
            'dataIds': data_ids
        }

        resp = self.api.get_request(endpoint=endpoint, params=params)

        return resp

    def _generate_file_direct_upload_address(self, file_name: str, dataset_id: str) -> Dict:
        endpoint = 'data/generatePresignedUrl'

        params = {
            'fileName': file_name,
            'datasetId': dataset_id
        }

        resp = self.api.get_request(endpoint=endpoint, params=params)

        return resp

    def _upload(self, url, dataset_id, source):
        endpoint = 'data/upload'

        payload = {
            'fileUrl': url,
            'datasetId': dataset_id,
            'source': source
        }

        resp = self.api.post_request(endpoint=endpoint, payload=payload)

        return resp

    def upload_file(self, file_path: str, dataset_id: str, is_local: bool) -> str:
        file_name = os.path.split(file_path)[-1]
        url_dict = self._generate_file_direct_upload_address(file_name, dataset_id)
        put_resp = requests.put(url_dict['presignedUrl'], data=open(file_path, 'rb'))
        if put_resp.status_code != 200:
            raise SDKException(code=put_resp.status_code, message=put_resp.text)

        source = 'LOCAL' if is_local else 'URL'
        resp = self._upload(url_dict['accessUrl'], dataset_id, source)

        return resp

    # 存疑函数
    def get_data_and_result_info(self, dataset_id: Optional[str] = None, data_ids: Optional[List[str]] = None) -> Dict:
        endpoint = 'data/getDataAndResult'

        params = {
            'datasetId': dataset_id,
            'dataIds': data_ids
        }

        resp = self.api.get_request(endpoint=endpoint, params=params)

        return resp

    @staticmethod
    def as_table(data_list):
        pass
