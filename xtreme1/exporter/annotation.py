from xtreme1.client import Client
from .standard import *


class Annotation:
    _SUPPORTED_FORMAT_INFO = {
        "STANDARD_JSON": {
            "description": 'Basic AI standard format'
        },
        "CSV": {
            "description"
        },
        "XML": {
            "description"
        },
        "TXT": {
            "description"
        },
        "COCO": {
            "description"
        },
        "VOC": {
            "description"
        },
        "YOLO": {
            "description"
        },
    }

    def __init__(self, annotation_data):
        self.annotation = annotation_data

    def supported_format(self):
        """
        Query the supported conversion format
        """

        return self._SUPPORTED_FORMAT_INFO

    def converter(self, format: str, export_folder):
        format = format.upper()
        if format == 'STANDARD_JSON':
            self.to_standard_json(export_folder)
        elif format == 'CSV':
            self.to_csv(self.annotation, export_folder)
        elif format == 'COCO':
            self.to_coco(self.annotation, export_folder)

    def to_standard_json(self, export_folder):
        to_json(annotation=self.annotation, export_folder=export_folder)

    def to_csv(self, input_annotations, export_folder):
        pass

    def to_xml(self, input_annotations, export_folder):
        pass

    def to_txt(self, input_annotations, export_folder):
        pass

    def to_coco(self, input_annotations, export_folder):
        pass

    def to_voc(self, input_annotations, export_folder):
        pass

    def to_yolo(self, input_annotations, export_folder):
        pass
