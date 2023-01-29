"""
Query and save with Basic Ai standard format
"""
import os
import json
from os.path import *
from rich.progress import track
from tqdm import tqdm


def to_json(annotation: dict, dataset_name: str, export_folder: str):
    """

    Parameters
    ----------
    annotation
    dataset_name
    export_folder

    Returns
    -------

    """
    save_folder = join(export_folder, f'x1 dataset {dataset_name} annotations')
    if not exists(save_folder):
        os.makedirs(save_folder, exist_ok=True)
    for anno in tqdm(annotation, desc='progress'):
        file_name = f"{anno['data'].get('name')}-{anno['data'].get('id')}"
        json_file = join(save_folder, file_name + '.json')
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(anno.get('result'), f, indent=1)


def to_csv(annotation: dict, export_folder: str):
    pass


def to_txt(annotation: dict, export_folder: str):
    pass


def to_xml(annotation: dict, export_folder: str):
    pass
