def parse_int(value):

    if value is None:
        return None

    value = str(value)

    value = (
        value
        .replace(",", "")
        .replace("$", "")
        .strip()
    )

    if value == "":
        return None

    try:
        return int(float(value))
    except:
        return None


def parse_float(value):

    if value is None:
        return None

    value = str(value)

    value = (
        value
        .replace(",", "")
        .replace("$", "")
        .strip()
    )

    if value == "":
        return None

    try:
        return float(value)
    except:
        return None