def print_attr(obj, attr: str) -> None:
    """
    Dynamically prints attribute, prints None if it does not exist
    """
    try:
        attr_val = getattr(obj, attr)
    except AttributeError as a:
        attr_val = None
    print(f"{attr}:\t{str(attr_val)}")


def print_attrs(obj, attrs: list[str]) -> None:
    """
    Prints a list of attributes from a given Object
    """
    for attr in attrs:
        print_attr(obj, attr)
