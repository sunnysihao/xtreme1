class BFDataset:
    def __init__(self, data, client):
        for k, v in data.items():
            self.__setattr__(k, v)
        self._client = client
        self._data = {k: v for k, v in self.__dict__.items() if '_' not in k}

    def __str__(self):
        result = []
        for k, v in self._data.items():
            result.append(f'{k}={v}')
        return ', '.join(result)

    def __repr__(self):
        return f"BFDataset({self._data})"
