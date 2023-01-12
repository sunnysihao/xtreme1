from .convert_to_coco import to_coco
from os.path import *
from xtreme1.exceptions import *


class Converter:

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

    def __init__(self, zip_file: str):
        if splitext(zip_file)[-1] == '.zip':
            self.zip_file = zip_file
        else:
            raise ConverterException(
                code='NOT_ZIPFILE',
                message="Enter the path of the (.zip) file exported by the annotation tool"
            )

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