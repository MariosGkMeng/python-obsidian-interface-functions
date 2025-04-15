def flatten_dict(d, parent_key='', sep='__'):
    """
    Recursively flattens a nested dictionary by concatenating keys.
    
    :param d: Dictionary to flatten
    :param parent_key: Used for recursive key concatenation
    :param sep: Separator for flattened keys
    :return: Flattened dictionary
    """
    flattened = {}
    
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            flattened.update(flatten_dict(v, new_key, sep))
        else:
            flattened[new_key] = v
    
    return flattened
