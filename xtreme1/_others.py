from functools import reduce


def _to_single(query_result):
    if query_result[1] == 1:
        return query_result[0][0]
    return query_result


def _to_camel(
        var
):
    parts = var.split('_')
    return reduce(lambda x, y: x + y.capitalize(), parts)
