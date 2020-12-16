def validate_int(value: int, lower_limit: int=None, upper_limit: int=None,
                 no_exceptions=True, force_limts=False):
    if value is None:
        return None

    if not isinstance(value, int):
        return None

    if lower_limit is not None:
        if value < lower_limit:
            return None

    if upper_limit is not None:
        if value > upper_limit:
            return None

    return value
