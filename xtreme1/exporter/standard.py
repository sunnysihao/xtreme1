"""
Query and save with Basic Ai standard format
"""
import os
import json
from os.path import *
from rich.progress import track
from tqdm import tqdm


def to_json(annotation: dict, export_folder: str):
    """

    Parameters
    ----------
    annotation
    export_folder

    Returns
    -------

    """
    id_name_mapping = {}
    datas = annotation['data']
    results = annotation['results']
    dataset_name = annotation['datasetName']
    save_folder = join(export_folder, f'x1 dataset {dataset_name} annotations')
    if not exists(save_folder):
        os.makedirs(save_folder, exist_ok=True)
    for data in datas:
        id_name_mapping[data['id']] = f"{data['name']}-{data['id']}"
    for result in tqdm(results, desc='progress'):
        file_name = id_name_mapping.get(result['dataId'])
        json_file = join(save_folder, file_name + '.json')
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=1)


def to_csv(annotation: dict, export_folder: str):
    pass


def to_txt(annotation: dict, export_folder: str):
    pass


def to_xml(annotation: dict, export_folder: str):
    pass