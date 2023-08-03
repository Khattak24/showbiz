def split_full_name(full_name):
    """Splits full name into first and last name"""
    if not full_name:
        return None, None
    names = full_name.split(" ")
    if len(names) == 1:
        return names[0], None
    return names[0], " ".join(names[1:])
