import os
import json
import cv2
import numpy as np
from tqdm import tqdm
from datetime import datetime
from os.path import join, exists
from .._version import __version__


def to_coco(annotation: list, dataset_name: str, export_folder: str):
    save_folder = join(export_folder, f'x1 dataset {dataset_name} annotations')
    if not exists(save_folder):
        os.makedirs(save_folder, exist_ok=True)
    images = []
    annotations = []
    categorys = []
    category_mapping = {}
    img_id = 0
    object_id = 0
    category_id = 1
    for anno in tqdm(annotation, desc='progress'):
        try:
            img_width = anno['data']['width']
            img_height = anno['data']['height']
            img_url = anno['data']['imageUrl']
            result = anno['result']
            if not result:
                continue
            else:
                objects = result['objects']
            for obj in objects:
                class_name = obj['className']
                if class_name not in category_mapping.keys():
                    category_mapping[class_name] = category_id
                    category = {
                        "id": category_id,
                        "name": class_name,
                        "supercategory": "",
                        "attributes": {}
                    }
                    categorys.append(category)
                    category_id += 1
                score = obj['modelConfidence']
                tool_type = obj['type']
                if tool_type == 'RECTANGLE':
                    points = obj['contour']['points']
                    xl = []
                    yl = []
                    for point in points:
                        xl.append(point['x'])
                        yl.append(point['y'])
                    x0 = min(xl)
                    y0 = min(yl)
                    width = max(xl)-x0
                    height = max(yl)-y0
                    attributes = {}
                    class_values = obj['classValues']
                    for cv in class_values:
                        attributes[cv['name']] = cv['value']
                    anno = {
                        "id": object_id,
                        "image_id": img_id,
                        "category_id": category_mapping[class_name],
                        "segmentation": [],
                        "score": score,
                        "area": width*height,
                        "bbox": [x0, y0, width, height],
                        "iscrowd": 0,
                        "attributes": attributes
                    }
                    annotations.append(anno)
                    object_id += 1
                elif tool_type == 'POLYGON':
                    segmentation = []
                    coordinate = []
                    points = obj['contour']['points']
                    for point in points:
                        coordinate.append([int(point['x']), int(point['y'])])
                        segmentation.append(point['x'])
                        segmentation.append(point['y'])
                    mask = np.zeros((img_height, img_width), dtype=np.int32)
                    cv2.fillPoly(mask, [np.array(coordinate)], 1)
                    aera = int(np.sum(mask))
                    attributes = {}
                    class_values = obj['classValues']
                    for cv in class_values:
                        attributes[cv['name']] = cv['value']
                    anno = {
                        "id": object_id,
                        "image_id": img_id,
                        "category_id": category_mapping[class_name],
                        "segmentation": segmentation,
                        "score": score,
                        "area": aera,
                        "bbox": [],
                        "iscrowd": 0,
                        "attributes": attributes
                    }
                    annotations.append(anno)
                    object_id += 1
                elif tool_type == 'POLYLINE':
                    keypoints = []
                    points = obj['contour']['points']
                    for point in points:
                        keypoints.append(point['x'])
                        keypoints.append(point['y'])
                        keypoints.append(2)

                    attributes = {}
                    class_values = obj['classValues']
                    for cv in class_values:
                        attributes[cv['name']] = cv['value']
                    anno = {
                        "id": object_id,
                        "image_id": img_id,
                        "category_id": category_mapping[class_name],
                        "segmentation": [],
                        "bbox": [],
                        "keypoints": keypoints,
                        "num_keypoints": len(points),
                        "score": score,
                        "iscrowd": 0
                    }
                    annotations.append(anno)
                    object_id += 1

            one_image = {
                    "id": img_id,
                    "license": 0,
                    "file_name": img_url.split('?')[0].split('/')[-1],
                    "xtreme1_url": img_url,
                    "width": img_width,
                    "height": img_height,
                    "date_captured": None
            }
            images.append(one_image)
            img_id += 1
        except Exception:
            continue

    info = {
        "contributor": "",
        "date_created": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "description":
            f'Basic AI Xtreme1 dataset {dataset_name} exported to COCO format (https://github.com/basicai/xtreme1)',
        "url": "https://github.com/basicai/xtreme1",
        "year": f"{datetime.utcnow().year}",
        "version": __version__,
    }

    final_json = {
        "info": info,
        "licenses": [],
        "images": images,
        "annotations": annotations,
        "categories": categorys
    }
    save_json = join(save_folder, 'coco_results.json')
    with open(save_json, 'w', encoding='utf-8') as jf:
        json.dump(final_json, jf, indent=1, ensure_ascii=False)
    print(f"*** coco format results have been saved in {save_json} ***")
