import os
from typing import List, Dict, Optional, Union, Iterable
from datetime import datetime

import requests

from .api import Api
from .dataset import Dataset
from .exceptions import SDKException


class Client:

    def __init__(
            self,
            access_token: str,
            base_url: str
    ):
        self.api = Api(access_token=access_token, base_url=base_url)

    def create_dataset(
            self, name: str,
            annotation_type: str,
            description: str = None
    ) -> Dataset:
        """
        Create a dataset with specific name and description.

        Parameters
        ----------
        name: str
            Dataset name.
        annotation_type: str
            An annotation type which can only choose from this list:
            ['LIDAR_FUSION', 'LIDAR_BASIC', 'IMAGE']
        description: str
            Further description about this dataset.

        Returns
        -------
        Dataset
            An instance of dataset class.
        """
        endpoint = 'dataset/create'
        payload = {
            'name': name,
            'type': annotation_type,
            'description': description
        }

        resp = self.api.post_request(endpoint, payload=payload)

        return Dataset(resp, self)

    def edit_dataset(
            self,
            dataset_id: str,
            name: str,
            description: Optional[str] = None
    ) -> str:
        """
        Change the name or description of a dataset.

        Parameters
        ----------
        dataset_id: str
            Dataset id. You can find this in the last part of dataset url, for example:
            'https://x1-community.alidev.beisai.com/#/datasets/overview?id=766416'
        name: str
            New name of the dataset.
        description: Optional[str], default None
            New description of the dataset

        Returns
        -------
        str
            'Success'.
        """
        endpoint = f'dataset/update/{dataset_id}'
        payload = {
            'name': name,
            'description': description
        }

        self.api.post_request(endpoint, payload=payload)

        return 'Success'

    def delete_dataset(
            self,
            dataset_id: str,
            is_sure: bool = False
    ) -> str:
        """
        Delete a dataset.

        Parameters
        ----------
        dataset_id: str
            Dataset id. You can find this in the last part of the dataset URL, for example:
            'https://x1-community.alidev.beisai.com/#/datasets/overview?id=766416'
        is_sure: bool, default False
            Set it to 'True' to delete the dataset.

        Returns
        -------
        str
            'Unsure' if 'is_sure' is not set to 'True'.
            'Success' if the dataset is deleted.
        """
        if not is_sure:
            return 'Unsure'

        endpoint = f'dataset/delete/{dataset_id}'
        self.api.post_request(endpoint=endpoint, payload=None)

        return 'Success'

    def _query_a_single_dataset(
            self,
            dataset_id: str
    ) -> Dict:
        endpoint = f'dataset/info/{dataset_id}'
        resp = self.api.get_request(endpoint=endpoint, params=None)

        return resp

    def _query_the_list_of_datasets(
            self,
            page_no: int,
            page_size: int,
            name: Optional[str] = None,
            create_start_time: Optional[Iterable] = None,
            create_end_time: Optional[Iterable] = None,
            sort_by: Optional[str] = None,
            ascending: Optional[bool] = True,
            dataset_type: Optional[str] = None
    ) -> Dict:
        endpoint = 'dataset/findByPage'

        create_start_time = datetime(*create_start_time) if create_start_time else datetime(1000, 1, 1)
        create_end_time = datetime(*create_end_time) if create_end_time else datetime.today()

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
            page_no: int = 1,
            page_size: int = 1,
            dataset_name: Optional[str] = None,
            create_start_time: Optional[Iterable] = None,
            create_end_time: Optional[Iterable] = None,
            sort_by: str = 'CREATED_AT',
            ascending: Optional[bool] = True,
            dataset_type: Optional[str] = None
    ) -> List[Dataset]:
        """
        Query a specific dataset or query several datasets with some restrictions.

        Parameters
        ----------
        dataset_id: Optional[str], default None
            Use this parameter to query a specific dataset.
        page_no: int, default 1
            Number of the page you would like to see.
            This is used when you have lots of datasets and only want to check them part by part.
        page_size: int, default 1
            Number of datasets on one page.
        dataset_name: str
            Name of the dataset you want to query.
            Notice that it's a fuzzy query.
        create_start_time: Iterable, default None
            An iterable object. For example:
             (2023, 1, 1, 12, 30, 30) means querying datasets created after 2023-01-01T12:30:30.
            Hour, minute and second are optional.
        create_end_time: Iterable, default None
            An iterable object. For example:
             (2023, 1, 1, 12, 30, 30) means querying datasets created before 2023-01-01T12:30:30.
            Hour, minute and second are optional.
        sort_by: str, default CREATED_AT
            A sort field that can only choose from this list:
            ['NAME', 'CREATED_AT', 'UPDATED_AT']
        ascending: bool, default True
            Whether the order of datasets is ascending or descending.
        dataset_type: str
            An annotation type that can only choose from this list:
            ['LIDAR_FUSION', 'LIDAR_BASIC', 'IMAGE']

        Returns
        -------
        List[Dataset]
            A list of Dataset classes.
            Notice that this function only returns one dataset at a time unless you change the 'page_size' parameter.
        """
        if dataset_id:
            dataset_name = self._query_a_single_dataset(dataset_id)['name']

        resp = self._query_the_list_of_datasets(
            page_no=page_no,
            page_size=page_size,
            name=dataset_name,
            create_start_time=create_start_time,
            create_end_time=create_end_time,
            sort_by=sort_by,
            ascending=ascending,
            dataset_type=dataset_type
        )

        datasets = [Dataset(d, self) for d in resp['list']]

        return datasets

    def query_data_under_dataset(
            self,
            dataset_id: str,
            page_no: int = 1,
            page_size: int = 10,
            name: Optional[str] = None,
            create_start_time: Optional[Iterable] = None,
            create_end_time: Optional[Iterable] = None,
            sort_by: str = 'CREATED_AT',
            ascending: Optional[bool] = True,
            annotation_status: Optional[str] = None
    ) -> Dict:
        """
        Query data under a specific dataset with some restrictions.

        Parameters
        ----------
        dataset_id: Optional[str], default None
            Id of the dataset that you want to search data from.
        page_no: int, default 1
            Number of the page you would like to see.
            This is used when you have lots of data and only want to check them part by part.
        page_size: int, default 10
            Number of data on one page.
            Notice that data ≠ file. For example:
            for a 'LIDAR_FUSION' dataset, one single data means:
            {'a pcd file' + 'a camera config json' + 'several 2D images'}.
        name: str
            Name of the data you want to query.
            Notice that it's a fuzzy query.
        create_start_time: Iterable, default None
            An iterable object. For example:
             (2023, 1, 1, 12, 30, 30) means querying datasets created after 2023-01-01T12:30:30.
            Hour, minute and second are optional.
        create_end_time: Iterable, default None
            An iterable object. For example:
             (2023, 1, 1, 12, 30, 30) means querying datasets created before 2023-01-01T12:30:30.
            Hour, minute and second are optional.
        sort_by: str, default CREATED_AT
            A sort field that can only choose from this list:
            ['NAME', 'CREATED_AT', 'UPDATED_AT']
        ascending: bool, default True
            Whether the order of datasets is ascending or descending.
        annotation_status: Optional[str], default None
            Annotation status of the data that can only choose from this list:
            ['ANNOTATED', 'NOT_ANNOTATED', 'INVALID'].

        Returns
        -------
        Dict
            JSON data containing all the data you're querying and information of all the files within these data.
        """
        endpoint = 'data/findByPage'

        create_start_time = datetime(*create_start_time) if create_start_time else datetime(1000, 1, 1)
        create_end_time = datetime(*create_end_time) if create_end_time else datetime.today()

        params = {
            'datasetId': dataset_id,
            'pageNo': page_no,
            'pageSize': page_size,
            'name': name,
            'createStartTime': create_start_time,
            'createEndTime': create_end_time,
            'sortField': sort_by,
            'ascOrDesc': 'ASC' if ascending else 'DESC',
            'annotationStatus': annotation_status
        }

        resp = self.api.get_request(endpoint=endpoint, params=params)

        return resp

    def delete_data(
            self,
            dataset_id: str,
            data_id: Union[str, List[str]],
            is_sure: bool = False
    ) -> str:
        """
        Delete one specific data or list of data from a specific dataset.

        Parameters
        ----------
        dataset_id: str
            Id of the dataset you want to delete from.
        data_id: Union[str, List[str]]
            An id or list of ids of the data you want to delete.
        is_sure: bool, default False
            Set it to 'True' to delete the data.

        Returns
        -------
        str
            'Unsure' if 'is_sure' is not set to 'True'.
            'Success' if the data is deleted.
        """
        if not is_sure:
            return 'Unsure'

        if type(data_id) == str:
            data_id = [data_id]

        endpoint = 'data/deleteBatch'

        payload = {
            'datasetId': dataset_id,
            'ids': data_id
        }

        self.api.post_request(endpoint=endpoint, payload=payload)

        return 'Success'

    def query_data(
            self,
            data_id: Union[str, List[str]]
    ) -> List[Dict]:
        """
        Use a specific id or list of ids to query data.

        Parameters
        ----------
        data_id: Union[str, List[str]]
            A specific id or a list of ids.

        Returns
        -------
        List[Dict]
            List of JSON data.
        """
        endpoint = 'data/listByIds'

        if type(data_id) == str:
            data_id = [data_id]
        params = {
            'dataIds': data_id
        }

        resp = self.api.get_request(endpoint=endpoint, params=params)

        return resp

    def _generate_file_direct_upload_address(
            self,
            file_name: str,
            dataset_id: str
    ) -> Dict:
        endpoint = 'data/generatePresignedUrl'

        params = {
            'fileName': file_name,
            'datasetId': dataset_id
        }

        resp = self.api.get_request(endpoint=endpoint, params=params)

        return resp

    def _upload(
            self,
            url: str,
            dataset_id: str,
            source: str
    ):
        endpoint = 'data/upload'

        payload = {
            'fileUrl': url,
            'datasetId': dataset_id,
            'source': source
        }

        resp = self.api.post_request(endpoint=endpoint, payload=payload)

        return resp

    def upload_file(
            self,
            file_path: str,
            dataset_id: str,
            is_local: bool = True
    ) -> str:
        """
        Upload data to a specific dataset by using a local path or URL.
        Notice that this function always returns a serial number if the parameters are right.
        However, it doesn't mean the upload process is successful.
        Therefore, it's necessary to check the upload status by using the 'query_upload_status' function.

        Parameters
        ----------
        file_path: str
            A local path or URL.
            Notice that if you're using a local path, wrong path or unsupported file format raises a 'param error'.
        dataset_id: str
            Id of the dataset where files are pushed into.
        is_local: bool, default True
            Whether the upload file is local or not.

        Returns
        -------
        str
            A serial number for querying the upload status.
        """
        if is_local:
            file_name = os.path.split(file_path)[-1]
            url_dict = self._generate_file_direct_upload_address(file_name, dataset_id)
            put_resp = requests.put(url_dict['presignedUrl'], data=open(file_path, 'rb'))

            if put_resp.status_code != 200:
                raise SDKException(code=put_resp.status_code, message=put_resp.text)

            upload_url = url_dict['accessUrl']
            source = 'LOCAL'

        else:
            upload_url = file_path
            source = 'URL'

        resp = self._upload(upload_url, dataset_id, source)

        return resp

    def query_upload_status(
            self,
            serial_numbers: Union[str, List[str]]
    ) -> List[Dict]:
        """
        Query if the upload process is completed.
        Also shows the number of parsed data.

        Parameters
        ----------
        serial_numbers: Union[str, List[str]]
            A specific serial_number or list of serial_numbers.
            Notice that 'serial_number' is the response of 'upload_file' function,
            and it can't be acquired from other functions.

        Returns
        -------
        List[Dict]
            List of upload status.
        """
        endpoint = 'data/findUploadRecordBySerialNumbers'

        params = {
            'serialNumbers': serial_numbers
        }

        resp = self.api.get_request(endpoint=endpoint, params=params)

        return resp

    def _get_data_and_result_info(
            self,
            dataset_id: Union[str, List[str]],
            data_ids: Optional[List[str]] = None
    ) -> Dict:
        endpoint = 'data/getDataAndResult'

        params = {
            'datasetId': dataset_id,
            'dataIds': data_ids
        }

        resp = self.api.get_request(endpoint=endpoint, params=params)

        return resp

    def query_result(
            self,
            dataset_id: Union[str, List[str]],
            data_ids: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        Query the annotation result of a specific dataset or list of datasets.
        Accept a 'data_ids' parameter to query specific data.

        Parameters
        ----------
        dataset_id: Union[str, List[str]]
            Id of the dataset you want to query.
        data_ids: Optional[List[str]], default None
            Id or ids of the data you want to query.

        Returns
        -------
        List[Dict]
            List of JSON annotation results.
        """
        return self._get_data_and_result_info(dataset_id, data_ids)['results']
