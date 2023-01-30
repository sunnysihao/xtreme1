
import os
import json
from os.path import *
from rich.progress import track
from tqdm import tqdm


def _to_json(annotation: list, dataset_name: str, export_folder: str):
    save_folder = join(export_folder, f'x1 dataset {dataset_name} annotations')
    if not exists(save_folder):
        os.makedirs(save_folder, exist_ok=True)
    for anno in tqdm(annotation, desc='progress'):
        file_name = f"{anno['data'].get('name')}-{anno['data'].get('id')}"
        json_file = join(save_folder, file_name + '.json')
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(anno.get('result'), f, indent=1)
    print(f"*** Standard json format results have been saved in '{save_folder}' ***")



def _to_csv(annotation: dict, dataset_name: str, export_folder: str):
    pass


def _to_txt(annotation: dict, dataset_name: str, export_folder: str):
    pass


def _to_xml(annotation: dict, dataset_name: str, export_folder: str):
    pass