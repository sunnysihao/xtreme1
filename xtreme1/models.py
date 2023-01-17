from enum import Enum
from typing import List, Union, Optional, Dict, FrozenSet

from .exceptions import ParamException


class ImageModelClass(Enum):
    tool = frozenset({'KNIFE', 'BACKPACK', 'UMBRELLA', 'HANDBAG', 'TIE', 'SUITCASE',
                      'CLOCK', 'SCISSORS', 'TOOTHBRUSH'})
    dishware = frozenset({'SPOON', 'BOWL', 'BOTTLE', 'CUP', 'WINE_GLASS', 'FORK'})
    sports = frozenset({'FRISBEE', 'SKIS', 'SNOWBOARD', 'SPORTS_BALL', 'BASEBALL_BAT', 'BASEBALL_GLOVE', 'SKATEBOARD',
                        'SURFBOARD', 'TENNIS_RACKET'})
    toy = frozenset({'KITE', 'TEDDY_BEAR'})
    vegetable = frozenset({'BANANA', 'APPLE', 'ORANGE', 'BROCCOLI', 'CARROT'})
    food = frozenset({'SANDWICH', 'HOT_DOG', 'PIZZA', 'DONUT', 'CAKE'})
    traffic = frozenset({'TRAFFIC_LIGHT', 'STOP_SIGN', 'PARKING_METER', 'PERSON', 'BICYCLE', 'CAR', 'MOTORCYCLE',
                         'AIRPLANE', "BUS", "TRAIN", "TRUCK", "BOAT"})
    electronic = frozenset({'LAPTOP', 'KEYBOARD', 'CELL_PHONE', 'TV', 'MICROWAVE', 'OVEN', 'TOASTER',
                            'REFRIGERATOR', 'HAIR_DRIER'})
    furniture = frozenset({'CHAIR', 'BENCH', 'COUCH', 'POTTED_PLANT', 'BED', 'DINING_TABLE', 'TOILET', 'SINK'})
    animal = frozenset({'BIRD', 'CAT', 'DOG', 'HORSE', 'SHEEP', 'COW', 'ELEPHANT', 'MOUSE', 'BEAR', 'ZEBRA',
                        'GIRAFFE'})
    others = frozenset({'FIRE_HYDRANT', 'BOOK', 'VASE', 'REMOTE'})


class PointCloudModelClass(Enum):
    traffic = frozenset(
        {"CAR", "TRUCK", "CONSTRUCTION_VEHICLE", "BUS", "TRAILER", "BARRIER", "MOTORCYCLE", "BICYCLE", "PEDESTRIAN",
         "TRAFFIC_CONE"}
    )


class Model:
    classes = None

    def __init__(
            self,
            client,
    ):
        self._client = client

    def show_classes(
            self
    ) -> Dict[str, FrozenSet]:
        """
        Return all classes which are supported by a trained model as a dict.

        Returns
        -------
        Dict[str, FrozenSet]
            Various classes.
        """

        return {x.name: x.value for x in self.classes}


class ImageModel(Model):
    classes = ImageModelClass

    def __init__(
            self,
            client
    ):
        super().__init__(client)

    def predict(
            self,
            classes: Union[List[List[str]], List[str], str],
            min_confidence: Union[Union[int, float], List[Union[int, float]]],
            max_confidence: Union[Union[int, float], List[Union[int, float]]] = 1,
            data_id: Optional[Union[str, List[str]]] = None,
            dataset_id: Optional[str] = None
    ) -> List[Dict]:
        """
        Use a trained model to recognize given objects in an image.

        Parameters
        ----------
        classes: Union[List[List[str]], List[str], str]
            Object classes.
            If you pass a 'str', the model will predict the given object in each data.
            If you pass a list of 'str', the model will predict all the given objects in each data.
            If you pass a nested list, the function will match 'classes' and 'data_id' first,
            which means the model will predict different objects in different data.
        min_confidence: Union[Union[int, float], List[Union[int, float]]]
            Filter all the results that has a lower confidence than 'min_confidence'.
        max_confidence: Union[Union[int, float], List[Union[int, float]]], default 1
            Filter all the results that has a higher confidence than 'max_confidence'.
        data_id: Optional[Union[str, List[str]]], default None
            If you pass this parameter, the model will only predict the given data.
        dataset_id: Optional[str], default None
            If you pass this parameter, the model will predict all the data under this dataset.

        Returns
        -------
        List[Dict]:
            A list of data dict. Each dict represents a copy of data, containing all the boxes predicted by the model.
        """

        if data_id:
            if type(data_id) == str:
                data_id = [data_id]
        else:
            if dataset_id:
                data = self._client.query_data_under_dataset(dataset_id)
                data_id = [x['id'] for x in data['list']]
            else:
                raise ParamException(message='You need to pass either data_id or dataset_id !!!')

        n = len(data_id)

        if type(min_confidence) in [int, float]:
            min_confidence = [min_confidence] * n

        if type(max_confidence) in [int, float]:
            max_confidence = [max_confidence] * n

        if type(classes) == str:
            classes = [classes]

        if type(classes[0]) == str:
            classes = [classes] * n

        if len(classes) != n:
            raise ParamException(message="Wrong shape of 'classes'. Can not match 'data_id' !!!")

        total = []
        for i in range(n):
            endpoint = f'model/image/recognition'
            payload = {
                'dataId': data_id[i],
                'minConfidence': min_confidence[i],
                'maxConfidence': max_confidence[i],
                'classes': classes[i]
            }

            total.append(self._client.api.post_request(endpoint, payload=payload))

        # total = [x['modelResult'] for x in total]
        return total


class PointCloudModel(Model):
    classes = PointCloudModelClass

    def __init__(
            self,
            client
    ):
        super().__init__(client)

    def predict(
            self,
            classes: Union[List[List[str]], List[str]],
            min_confidence: Union[Union[int, float], List[Union[int, float]]],
            max_confidence: Union[Union[int, float], List[Union[int, float]]] = 1,
            data_id: Optional[Union[str, List[str]]] = None,
            dataset_id: Optional[str] = None
    ):
        """
        Use a trained model to recognize given objects in a point cloud.

        Parameters
        ----------
        classes: Union[List[List[str]], List[str], str]
            Object classes.
            If you pass a 'str', the model will predict the given object in each data.
            If you pass a list of 'str', the model will predict all the given objects in each data.
            If you pass a nested list, the function will match 'classes' and 'data_id' first,
            which means the model will predict different objects in different data.
        min_confidence: Union[Union[int, float], List[Union[int, float]]]

        max_confidence: Union[Union[int, float], List[Union[int, float]]], default 1
        data_id: Optional[Union[str, List[str]]], default None
            If you pass this parameter, the model will only predict the given data.
        dataset_id: Optional[str], default None
            If you pass this parameter, the model will predict all the data under this dataset.

        Returns
        -------
        List[Dict]:
            A list of data dict. Each dict represents a copy of data, containing all the boxes predicted by the model.
            Here's an example of objects:
                [
                    {
                        'points': [{'x': 1166, 'y': 498}, {'x': 1246, 'y': 548}],
                        'objType': 'rectangle',
                        'confidence': 0.64111328125,
                        'modelClass': 'Truck',
                        'modelClassId': 8
                    },
                    {
                        'points': [{'x': 1382, 'y': 528}, {'x': 1472, 'y': 567}],
                        'objType': 'rectangle',
                        'confidence': 0.64794921875,
                        'modelClass': 'Car',
                        'modelClassId': 3
                    }
                ]
        """

        if data_id:
            if type(data_id) == str:
                data_id = [data_id]
        else:
            if dataset_id:
                data = self._client.query_data_under_dataset(dataset_id)
                data_id = [x['id'] for x in data['list']]
            else:
                raise ParamException(message='You need to pass either data_id or dataset_id !!!')

        n = len(data_id)

        if type(min_confidence) in [int, float]:
            min_confidence = [min_confidence] * n

        if type(max_confidence) in [int, float]:
            max_confidence = [max_confidence] * n

        if type(classes) == str:
            classes = [classes]

        if type(classes[0]) == str:
            classes = [classes] * n

        total = []
        for i in range(n):
            endpoint = f'model/image/recognition'
            payload = {
                'dataId': data_id[i],
                'minConfidence': min_confidence[i],
                'maxConfidence': max_confidence[i],
                'classes': classes[i]
            }

            total.append(self._client.api.post_request(endpoint, payload=payload))

        # total = [x['modelResult'] for x in total]
        return total
