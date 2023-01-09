from typing import Union, List, Dict, Optional

from rich.table import Table
from rich import box

from .dataset import Dataset


def _get_value_by_key(json_info, key):
    if type(json_info) == list:
        if ':' in key:
            key, n = key.split(':')
            return _get_value_by_key(json_info[int(n)], key)

        else:
            result = []
            for j in json_info:
                single_result = _get_value_by_key(j, key)
                if single_result:
                    result.append(single_result)
            return result

    elif type(json_info) == dict:
        value = json_info.get(key)
        if value:
            return value

        for k, v in json_info.items():
            if type(v) in [dict, list]:
                result = _get_value_by_key(v, key)
                if result:
                    return result


def _get_value_by_keys(json_info, keys):
    result = json_info

    for k in keys:
        result = _get_value_by_key(result, k)

    return result


def get_values(json_info, needed_keys):
    result = []

    if type(json_info) == list:
        for j in json_info:
            result.append(get_values(j, needed_keys))

    elif type(json_info) == dict:
        for k in needed_keys:
            if type(k) in [tuple, list]:
                result.append(_get_value_by_keys(json_info, k))
            else:
                result.append(_get_value_by_key(json_info, k))

    return result


def as_table(
        target_list: Union[List[Dataset], List[Dict], List[List]],
        blocks: Optional[List[str]] = None,
        headers: Optional[List[str]] = None
):
    if blocks is None:
        blocks = ['data', '_client']

    sample = target_list[0]
    if not headers:
        if type(sample) == dict:
            headers = sample.keys()
        elif type(sample) == Dataset:
            headers = sample.__dict__
        headers = [key for key in headers if key not in blocks]

    total = []
    if type(sample) == Dataset:
        total = [x.show_attrs(blocks).values() for x in target_list]
    elif type(sample) == dict:
        total = [[v for k, v in y.items() if k not in blocks] for y in target_list]
    elif type(target_list[0]) == list:
        total = target_list

    tb = Table(*headers, box=box.SIMPLE_HEAD)

    for data in total:
        tb.add_row(*map(str, data))

    return tb
