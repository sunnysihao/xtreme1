import os
import json
from rich import print_json
from os.path import join, exists
from xtreme1.exporter.standard import _to_json, _to_csv, _to_txt, _to_xml
from xtreme1.exporter.popular import _to_coco, _to_voc, _to_yolo, _to_labelme, _to_kitti
from xtreme1.exceptions import *

__supported_format__ = {
    "JSON": {
        "description": 'Basic AI standard json format'
    },
    "CSV": {
        "description": ''
    },
    "XML": {
        "description": ''
    },
    "TXT": {
        "description": ''
    },
    "COCO": {
        "description": ''
    },
    "VOC": {
        "description": ''
    },
    "YOLO": {
        "description": ''
    },
    "LABELME": {
        "description": ''
    },
    "KITTI": {
        "description": ''
    }
}


class Annotation:
    _SUPPORTED_FORMAT = __supported_format__

    def __init__(
            self,
            client,
            annotation,
            dataset_name,
            version=None,
            dataset_id=None,
            export_time=None
    ):
        self.version = version
        self.dataset_id = dataset_id
        self.dataset_name = dataset_name
        self.export_time = export_time
        self.annotation = annotation
        self._client = client

    def __str__(self):
        return f"Annotation(dataset_id={self.dataset_id}, dataset_name={self.dataset_name})"

    def __repr__(self):
        return f"Annotation(dataset_id={self.dataset_id}, dataset_name={self.dataset_name})"

    def __setattr__(self, key, value):
        if key == '_SUPPORTED_FORMAT':
            raise NoPermissionException(message='You are performing an operation that is not allowed')
        else:
            self.__dict__[key] = value

    def __gen_dir(self, input_dir):
        save_folder = join(input_dir, f'x1 dataset {self.dataset_name} annotations')
        if not exists(save_folder):
            os.makedirs(save_folder, exist_ok=True)
        return save_folder

    def view(self, count: int = 5):
        print_json(json.dumps(self.annotation[:count]))

    def supported_format(self):
        """Query the supported conversion format.

        Returns
        -------
        dict
            Formats that support transformations
        """

        return self._SUPPORTED_FORMAT

    def head(self, count: int = 5):
        """

        Parameters
        ----------
        count: int
            Displays the first n results in the list. The default number is 5

        Returns
        -------
        list
            Result list
        """
        return self.annotation[:count]

    def tail(self, count=5):
        """

        Parameters
        ----------
        count: int
            Displays the last n results in the list. The default number is 5

        Returns
        -------
        list
            Result list
        """
        return self.annotation[-count:]

    def to_dict(self):
        return self.annotation

    def convert(self, format: str, export_folder: str):
        """Convert the saved result to a target format.
        Find more info, see `description <https://docs.xtreme1.io/xtreme1-docs>`_.

        Parameters
        ----------
        format: str
            Target format,Optional (JSON, CSV, XML, TXT, COCO, VOC, YOLO, LABEL_ME). Case-insensitive

        export_folder: str
            The path to save the conversion result

        Returns
        -------

        """
        format = format.upper()
        if format == 'JSON':
            self.to_json(self.__gen_dir(export_folder))
        elif format == 'CSV':
            self.to_csv(self.__gen_dir(export_folder))
        elif format == 'XML':
            self.to_xml(self.__gen_dir(export_folder))
        elif format == 'TXT':
            self.to_txt(self.__gen_dir(export_folder))
        elif format == 'COCO':
            self.to_coco(self.__gen_dir(export_folder))
        elif format == 'VOC':
            self.to_voc(self.__gen_dir(export_folder))
        elif format == 'YOLO':
            self.to_yolo(self.__gen_dir(export_folder))
        elif format == 'LABELME':
            self.to_yolo(self.__gen_dir(export_folder))
        elif format == 'KITTI':
            self.to_kitti(self.__gen_dir(export_folder))

    def to_json(self, export_folder):
        """Convert the saved result to a json file in the xtreme1 standard format.

        Parameters
        ----------
        export_folder: The path to save the conversion result

        Returns
        -------

        """
        _to_json(annotation=self.annotation,
                 export_folder=self.__gen_dir(export_folder))

    def to_csv(self, export_folder):
        """Convert the saved result to a csv file in the xtreme1 standard format.

        Parameters
        ----------
        export_folder

        Returns
        -------

        """
        _to_csv(annotation=self.annotation,
                dataset_name=self.dataset_name,
                export_folder=self.__gen_dir(export_folder))

    def to_xml(self, export_folder):
        """Convert the saved result to a xml file in the xtreme1 standard format.

        Parameters
        ----------
        export_folder

        Returns
        -------

        """
        _to_xml(annotation=self.annotation,
                dataset_name=self.dataset_name,
                export_folder=self.__gen_dir(export_folder))

    def to_txt(self, export_folder):
        """Convert the saved result to a txt file in the xtreme1 standard format.

        Parameters
        ----------
        export_folder

        Returns
        -------

        """
        _to_txt(annotation=self.annotation,
                dataset_name=self.dataset_name,
                export_folder=self.__gen_dir(export_folder))

    def to_coco(self, export_folder):
        """
        Export data in coco format, and the resulting format varies somewhat depending on the tool type
        (RECTANGLE,POLYGON,POLYLINE,KEYPOINTS).
        Note that exports in this format only support image-type annotations.

        Parameters
        ----------
        export_folder: The path to save the conversion result

        Returns
        -------

        """
        _to_coco(annotation=self.annotation,
                 dataset_name=self.dataset_name,
                 export_folder=self.__gen_dir(export_folder))

    def to_voc(self, export_folder):
        """

        Parameters
        ----------
        export_folder

        Returns
        -------

        """
        _to_voc(annotation=self.annotation,
                dataset_name=self.dataset_name,
                export_folder=self.__gen_dir(export_folder))

    def to_yolo(self, export_folder):
        """

        Parameters
        ----------
        export_folder

        Returns
        -------

        """
        _to_yolo(annotation=self.annotation,
                 dataset_name=self.dataset_name,
                 export_folder=self.__gen_dir(export_folder))

    def to_labelme(self, export_folder):
        """Export data in label_me format.
        Note that exports in this format only support image-type annotations.

        Parameters
        ----------
        export_folder

        Returns
        -------

        """
        _to_labelme(annotation=self.annotation,
                    export_folder=self.__gen_dir(export_folder))

    def to_kitti(self, export_folder):
        """

        Parameters
        ----------
        export_folder

        Returns
        -------

        """
        _to_kitti(annotation=self.annotation,
                  dataset_name=self.dataset_name,
                  export_folder=self.__gen_dir(export_folder))
