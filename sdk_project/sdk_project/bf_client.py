from .bf_api import BFApi
from .bf_dataset import BFDataset


class BFClient:

    def __init__(self, access_token):
        self.api = BFApi(access_token=access_token)

    def create_dataset(self, name, annotation_type, description=None):
        endpoint = 'dataset/create'
        payload = {
            'name': name,
            'type': annotation_type,
            'description': description
        }

        resp = self.api.post_request(endpoint, data=payload)

        return BFDataset(resp, self)

    def edit_dataset(self, dataset_id, name, description):
        endpoint = f'dataset/update/{dataset_id}'
        payload = {
            'name': name,
            'description': description
        }

        resp = self.api.post_request(endpoint, data=payload)

        return resp

    def delete_dataset(self, dataset_id):
        endpoint = f'dataset/delete/{dataset_id}'
        resp = self.api.post_request(endpoint=endpoint, data=None)

        return resp

    def query_dataset(self, dataset_id):
        endpoint = f'dataset/info/{dataset_id}'
        resp = self.api.get_request(endpoint=endpoint, params=None)

        return BFDataset(resp, self)

    def query_datasets(self, page_no, page_size, **kwargs):
        endpoint = 'dataset/findByPage'

        params = {
            'pageNo': page_no,
            'pageSize': page_size,
            'name': kwargs.get('name'),
            'createStartTime': kwargs.get('createStartTime'),
            'createEndTime': kwargs.get('createEndTime'),
        }

        resp = self.api.get_request(endpoint=endpoint, params=params)

        return resp

    def upload_data(self, file_path, dataset_id, source):
        endpoint = 'data/upload'

        payload = {
            'fileUrl': file_path,
            'datasetId': dataset_id,
            'source': source
        }

        resp = self.api.post_request(endpoint=endpoint, data=payload)

        return resp

    def query_data_under_dataset(self, dataset_id, page_no, page_size, **kwargs):
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

    def delete_multiple_data(self, ids):
        endpoint = 'data/deleteBatch'

        payload = {
            'ids': ids
        }

        resp = self.api.post_request(endpoint=endpoint, data=payload)

        return resp

    def query_data(self, data_id):
        endpoint = f'data/info/{data_id}'
        resp = self.api.get_request(endpoint=endpoint, params=None)

        return resp

    def query_multiple_data(self, data_ids):
        endpoint = 'data/listByIds'

        params = {
            'dataIds': data_ids
        }

        resp = self.api.get_request(endpoint=endpoint, params=params)

        return resp

    def _generate_file_direct_upload_address(self, file_name, dataset_id):
        endpoint = 'data/generatePresignedUrl'

        params = {
            'fileName': file_name,
            'datasetId': dataset_id
        }

        resp = self.api.get_request(endpoint=endpoint, params=params)

        return resp

    def get_data_and_result_info(self, dataset_id, data_ids):
        endpoint = 'data/getDataAndResult'

        params = {
            'datasetId': dataset_id,
            'dataIds': data_ids
        }

        resp = self.api.get_request(endpoint=endpoint, params=params)

        return resp

