
import os
import json
from os.path import *
from rich.progress import track


def _to_json(annotation: list, export_folder: str):
    if not exists(export_folder):
        os.makedirs(export_folder, exist_ok=True)
    for anno in track(annotation, description='progress'):
        file_name = f"{anno['data'].get('name')}-{anno['data'].get('id')}"
        json_file = join(export_folder, file_name + '.json')
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(anno.get('result'), f, indent=1)
    print(f"*** Standard json format results have been saved in '{export_folder}' ***")



def _to_csv(annotation: dict, dataset_name: str, export_folder: str):
    pass


def _to_txt(annotation: dict, dataset_name: str, export_folder: str):
    pass


def _to_xml(annotation: dict, dataset_name: str, export_folder: str):
    pass