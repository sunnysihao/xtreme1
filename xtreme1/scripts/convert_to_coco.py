import os
import json
import zipfile
import cv2
import numpy as np
from tqdm import tqdm
from datetime import datetime
from os.path import join, basename, dirname, splitext, exists
from .._version import __version__


def coco_converter(zip_src, dst_dir: str = None):
    # result_path = join(dst_dir, os.listdir(dst_dir)[0], 'result')
    # data_path = join(dst_dir, os.listdir(dst_dir)[0], 'data')
    # export_path = join(dst_dir, f'x1 dataset {dataset_name} annotations')
    # if not exists(export_path):
    #     os.mkdir(export_path)
    zip_name = basename(zip_src)
    dataset_name = splitext(zip_name)[0].split('-')[0]
    if dst_dir:
        dst_dir = dst_dir
    else:
        dst_dir = join(dirname(zip_src), f'x1 dataset {dataset_name} annotations')
    if not exists(dst_dir):
        os.mkdir(dst_dir)
    zip_file = zipfile.ZipFile(zip_src, 'r')
    file_list = zip_file.namelist()
    results = []
    datas = []
    for fl in file_list:
        if fl.split('/')[1] == 'result':
            results.append(fl)
        else:
            datas.append(fl)
    images = []
    annotations = []
    categorys = []
    category_mapping = {}
    img_id = 0
    object_id = 0
    category_id = 1
    for result in tqdm(results, desc='progress'):
        try:
            result_content = json.loads(zip_file.read(result))
            file_name = result.split('/')[-1]
            data_content = json.loads(zip_file.read(f"{zip_name}/data/{file_name}"))
            # file_name = basename(file)
            # data_file = join(data_path, file_name)
            # result_content = load_json(file)
            # data_content = load_json(data_file)
            img_width = data_content['width']
            img_height = data_content['height']
            img_url = data_content['imageUrl']
            objects = result_content['objects']
            for obj in objects:
                if 'className' not in obj.keys():
                    continue
                else:
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

                    tool_type = obj['type']
                    points = obj['contour']['points']
                    if tool_type == 'RECTANGLE':
                        xl = []
                        yl = []
                        for point in points:
                            xl.append(point['x'])
                            yl.append(point['y'])
                        x0 = min(xl)
                        y0 = min(yl)
                        width = max(xl) - x0
                        height = max(yl) - y0
                        anno = {
                            "id": object_id,
                            "image_id": img_id,
                            "category_id": category_mapping[class_name],
                            "segmentation": [],
                            "area": width * height,
                            "bbox": [x0, y0, width, height],
                            "iscrowd": 0
                        }
                    elif tool_type == 'POLYGON':
                        segmentation = []
                        coordinate = []
                        for point in points:
                            coordinate.append([int(point['x']), int(point['y'])])
                            segmentation.append(point['x'])
                            segmentation.append(point['y'])
                        mask = np.zeros((img_height, img_width), dtype=np.int32)
                        cv2.fillPoly(mask, [np.array(coordinate)], 1)
                        aera = int(np.sum(mask))
                        anno = {
                            "id": object_id,
                            "image_id": img_id,
                            "category_id": category_mapping[class_name],
                            "segmentation": segmentation,
                            "area": aera,
                            "bbox": [],
                            "iscrowd": 0
                        }
                    elif tool_type == 'POLYLINE':
                        keypoints = []
                        for point in points:
                            keypoints.append(point['x'])
                            keypoints.append(point['y'])
                            keypoints.append(2)
                        anno = {
                            "id": object_id,
                            "image_id": img_id,
                            "category_id": category_mapping[class_name],
                            "segmentation": [],
                            "bbox": [],
                            "keypoints": keypoints,
                            "num_keypoints": len(points),
                            "iscrowd": 0
                        }
                    attributes = {}
                    class_values = obj['classValues']
                    for cv in class_values:
                        attributes[cv['name']] = cv['value']
                    if attributes:
                        anno['attributes'] = attributes
                    if 'modelConfidence' in obj.keys():
                        anno['score'] = obj['modelConfidence']
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
    save_json = join(dst_dir, f'{dataset_name}_coco.json')
    with open(save_json, 'w', encoding='utf-8') as jf:
        json.dump(final_json, jf, indent=1, ensure_ascii=False)
    print(f"*** Coco format results have been saved in '{save_json}' ***")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('zip_src', type=str, help='The path of the zip file')
    parser.add_argument('dst_dir', type=str, help='The save folder')
    args = parser.parse_args()

    zip_src = args.zip_src
    dst_dir = args.dst_dir
    if len(os.listdir(dst_dir)):
        input("The save folder needs to be empty, press any key to exit")
    else:
        coco_converter(zip_src, dst_dir)
        input("Complete, press any key to exit")
