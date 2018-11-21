# -*- coding: utf-8 -*-

def traverse_dict(data, parts):
    remaining = len(parts)
    key = parts.pop(0)
    if key not in data:
        raise LookupError("Key '%s' does not exist in %s" % (key, json.dumps(data)))
    return traverse_dict(data[key], parts) if remaining > 1 else data[key]