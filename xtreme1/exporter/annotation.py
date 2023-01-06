from xtreme1.client import Client


class Annotation:

    _SUPPORTED_FORMAT_INFO = {
        "STANDARD_JSON": {
            "description"
        },
        "CSV": {
            "description"
        },
        "XML": {
            "description"
        },
        "COCO": {
            "description"
        },
    }

    def __init__(self, access_token, base_url, dataset_id):
        self.dataset_id = dataset_id
        self.client = Client(access_token=access_token, base_url=base_url)
        self.annotation = self.client.query_result(dataset_id=self.dataset_id)

    def supported_format(self):
        """"""
        return self._SUPPORTED_FORMAT_INFO

    def conventer(self, input_annotations, export_folder, format: str):
        format = format.upper()
        if format == 'STANDARD_JSON':
            self.to_standard_json(input_annotations, export_folder)
        elif format == 'CSV':
            self.to_csv(input_annotations, export_folder)
        elif format == 'COCO':
            self.to_coco(input_annotations, export_folder)

    def to_standard_json(self, input_annotations, export_folder):
        pass

    def to_csv(self, input_annotations, export_folder):
        pass

    def to_xml(self, input_annotations, export_folder):
        pass

    def to_txt(self, input_annotations, export_folder):
        pass

    def to_coco(self, input_annotations, export_folder):
        pass
