from typing import List, Union, Optional

from .exceptions import ParamException


class Model:
    def __init__(
            self,
            client,
    ):
        self._client = client


class ImageModel(Model):
    supported_classes = frozenset(
        {"KNIFE", "SPOON", "BOWL", "BANANA", "APPLE", "SANDWICH", "ORANGE", "BROCCOLI", "CARROT",
         "HOT_DOG", "TRAFFIC_LIGHT", "PIZZA", "FIRE_HYDRANT", "DONUT", "STOP_SIGN", "CAKE",
         "PARKING_METER", "CHAIR", "BENCH", "COUCH", "BIRD", "POTTED_PLANT", "CAT", "DOG", "HORSE",
         "SHEEP", "PERSON", "BICYCLE", "CAR", "MOTORCYCLE", "AIRPLANE", "BUS", "TRAIN", "TRUCK", "BOAT",
         "BED", "DINING_TABLE", "TOILET", "TV", "COW", "LAPTOP", "ELEPHANT", "MOUSE", "BEAR", "REMOTE",
         "ZEBRA", "KEYBOARD", "GIRAFFE", "CELL_PHONE", "BACKPACK", "MICROWAVE", "UMBRELLA", "HANDBAG",
         "TIE", "SUITCASE", "OVEN", "TOASTER", "SINK", "REFRIGERATOR", "FRISBEE", "BOOK", "SKIS",
         "CLOCK", "SNOWBOARD", "VASE", "SPORTS_BALL", "SCISSORS", "KITE", "TEDDY_BEAR", "BASEBALL_BAT",
         "HAIR_DRIER", "BASEBALL_GLOVE", "SKATEBOARD", "SURFBOARD", "TENNIS_RACKET", "TOOTHBRUSH",
         "BOTTLE", "WINE_GLASS", "CUP", "FORK"}
    )

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


class PointCloudModel(Model):
    supported_classes = frozenset(
        {"CAR", "TRUCK", "CONSTRUCTION_VEHICLE", "BUS", "TRAILER", "BARRIER", "MOTORCYCLE", "BICYCLE", "PEDESTRIAN",
         "TRAFFIC_CONE"}
    )

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
