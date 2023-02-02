import zipfile
import json
import os

from os.path import *
from xtreme1.exporter.annotation import __supported_format__, Annotation
from xtreme1.exceptions import *


class Result:
    _SUPPORTED_FORMAT_INFO = __supported_format__

    def __init__(self,
                 src_zipfile: str,
                 export_folder: str = None,
                 dropna: bool = False
                 ):
        if zipfile.is_zipfile(src_zipfile):
            self.src_zipfile = src_zipfile
        else:
            print('This is not zip')
            raise SDKException(code='SourceError', message=f'{src_zipfile} is not zip')
        zip_name = basename(src_zipfile)
        self.dataset_name = '-'.join(splitext(zip_name)[0].split('-')[:-1])
        if export_folder:
            self.export_folder = export_folder
        else:
            self.export_folder = join(dirname(self.src_zipfile), f'x1 dataset {self.dataset_name} annotations')
        if not exists(self.export_folder):
            os.mkdir(self.export_folder)
        self.dropna = dropna
        self.annotation = Annotation(annotation=self.__reconstitution(), dataset_name=self.dataset_name)

    def __setattr__(self, key, value):
        if key == '_SUPPORTED_FORMAT':
            raise NoPermissionException(message='You are performing an operation that is not allowed')
        else:
            self.__dict__[key] = value

    def __reconstitution(self):
        dropna = self.dropna
        zip_file = zipfile.ZipFile(self.src_zipfile, 'r')
        file_list = zip_file.namelist()
        results = []
        datas = []
        for fl in file_list:
            if fl.split('/')[1] == 'result':
                results.append(fl)
            else:
                datas.append(fl)
        id_result = {}
        annotation = []
        for result in results:
            result_content = json.loads(zip_file.read(result))
            id_result[result_content['dataId']] = result_content
        for data in datas:
            data_content = json.loads(zip_file.read(data))
            data_result = id_result.get(data_content['id'], {})
            anno = {
                'data': data_content,
                'result': data_result
            }
            if dropna:
                if data_result:
                    annotation.append(anno)
                else:
                    continue
            else:
                annotation.append(anno)
        return annotation

    def __str__(self):
        return f"Offline annotation(dataset_name={self.dataset_name})"

    def __repr__(self):
        return f"Offline annotation(dataset_name={self.dataset_name})"

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

    def __ensure_dir(self, input_dir):
        if input_dir:
            export_folder = input_dir
        else:
            export_folder = self.export_folder
        return export_folder

    def convert(self, format: str, export_folder: str = None):

        self.annotation.convert(format=format, export_folder=self.__ensure_dir(export_folder))

    def to_json(self, export_folder: str = None):

        self.annotation.to_json(export_folder=self.__ensure_dir(export_folder))

    def to_csv(self, export_folder: str = None):

        self.annotation.to_csv(export_folder=self.__ensure_dir(export_folder))

    def to_xml(self, export_folder: str = None):

        self.annotation.to_xml(export_folder=self.__ensure_dir(export_folder))

    def to_txt(self, export_folder: str = None):

        self.annotation.to_txt(export_folder=self.__ensure_dir(export_folder))

    def to_coco(self, export_folder: str = None):

        self.annotation.to_coco(export_folder=self.__ensure_dir(export_folder))

    def to_voc(self, export_folder: str = None):

        self.annotation.to_voc(export_folder=self.__ensure_dir(export_folder))

    def to_yolo(self, export_folder: str = None):

        self.annotation.to_yolo(export_folder=self.__ensure_dir(export_folder))
