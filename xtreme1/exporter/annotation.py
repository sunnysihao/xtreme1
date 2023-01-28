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

    def __init__(
            self,
            version,
            dataset_id,
            dataset_name,
            export_time,
            annotation_data
    ):
        self.version = version
        self.dataset_id = dataset_id
        self.dataset_name = dataset_name
        self.export_time = export_time
        self.annotation = annotation_data

    def __str__(self):
        return f"Annotation(dataset_id={self.dataset_id}, dataset_name={self.dataset_name})"

    def __repr__(self):
        return f"Annotation(dataset_id={self.dataset_id}, dataset_name={self.dataset_name})"

    def supported_format(self):
        """Query the supported conversion format.

        Returns
        -------
        dict
            Formats that support transformations
        """

        return self._SUPPORTED_FORMAT_INFO

    def head(self, count=5):
        return self.annotation[:count]

    def tail(self, count=5):
        return self.annotation[-count:]

    def converter(self, format: str, export_folder: str):
        """

        Parameters
        ----------
        format: str
            Target format

        export_folder: str


        Returns
        -------

        """
        format = format.upper()
        if format == 'STANDARD_JSON':
            self.to_standard_json(export_folder)
        elif format == 'CSV':
            self.to_csv(self.annotation, export_folder)
        elif format == 'COCO':
            self.to_coco(self.annotation, export_folder)

    def to_standard_json(self, export_folder):
        """Convert the saved result to a json file in the xtreme1 standard format.
        Find more info, see 'https://docs.xtreme1.io/xtreme1-docs'

        Parameters
        ----------
        export_folder: The path to save the conversion result

        Returns
        -------

        """
        to_json(annotation=self.annotation, dataset_name=self.dataset_name, export_folder=export_folder)

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
