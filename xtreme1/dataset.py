from typing import Dict, Optional


class Dataset:

    def __init__(
            self,
            org_json,
            client
    ):
        self.id = org_json.get('id')
        self.name = org_json.get('name')
        self.type = org_json.get('type')
        self.description = org_json.get('description')
        self.annotated_count = org_json.get('annotatedCount')
        self.unannotated_count = org_json.get('notAnnotatedCount')
        self.invalid_count = org_json.get('invalidCount')
        self.item_count = org_json.get('itemCount')
        self.data = org_json.get('datas')
        self._client = client

    def __repr__(self):
        return f"BFDataset(id={self.id}, name={self.name})"

    def show_attrs(self, blocks=None):
        if blocks is None:
            blocks = ['_client']

        return {k: v for k, v in self.__dict__.items() if k not in blocks}

    def edit(self, new_name: str = None, new_description: str = None):
        self.name = new_name or self.name
        self.description = new_description or self.description
        return self._client.edit_dataset(self.id, self.name, self.description)

    def delete(self, is_sure: bool):
        return self._client.delete_dataset(self.id, is_sure)

    def query_data(
            self,
            page_no: int,
            page_size: int,
            name: Optional[str] = None,
            create_start_time: Optional[str] = None,
            create_end_time: Optional[str] = None,
            sort_by: Optional[str] = None,
            ascending: Optional[bool] = True,
            annotation_status: Optional[str] = None
    ) -> Dict:
        return self._client.query_data_under_dataset(
            self.id,
            page_no,
            page_size,
            name,
            create_start_time,
            create_end_time,
            sort_by,
            ascending,
            annotation_status
        )
