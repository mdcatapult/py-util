def uniqify(seq, idfun=None):
    # pylint: disable=function-redefined
    # order preserving
    if idfun is None:
        def idfun(x): return x
    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        if marker in seen:
            continue
        seen[marker] = 1
        result.append(item)
    return result


def add_thing_to_list(input_list, thing):
    """
    Adds a value to a list; checks thing type, and handles cases of the thing being a list or string.
    Currently doesn't handle dict data types.
    :param input_list: the input list to which we're adding the thing
    :param thing: the thing to be added
    :return list
    """
    if not isinstance(input_list, list):
        raise TypeError("Target list is is not a list: type detected = %s" % type(input_list))

    if isinstance(thing, int):
        thing = str(thing)

    if isinstance(thing, str):
        thing = [thing]

    if isinstance(thing, dict):
        thing = list(thing.keys())

    if not isinstance(thing, list):
            raise TypeError("Item to be added to the target list is of unhandled type %s" % type(thing))

    return uniqify(input_list + thing)
