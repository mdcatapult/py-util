import os
#from klein_config import config

# -*- coding: utf-8 -*-
def parse_doclib_metadata(metadata):
    """
    Return a new dict from a list of dicts defining `key`s and `value`s.

    e.g. [{'key': 'a', 'value': '1'}, {'key': 'b', 'value': '2'}] becomes
    {'a': 1, 'b': 2}

    Ignores any dicts in the list which do not provide both `key` and `value`.
    Any additional properties in a dict are also ignored.
    Any repeated keys will be updated with the last value provided.

    :param list metadata: list of dicts defining `key` and `value`
    :return: a dict created from all the keys and values in the metadata
    """
    return {d['key']: d['value'] for d in metadata if 'key' in d and 'value' in d}


def convert_document_metadata(doc):
    """
    Updates document metadata to usual dict format using the key/value pairs.

    :param dict doc: the document to update
    :return:
    """
    metadata = doc.pop('metadata', [])
    doc['metadata'] = parse_doclib_metadata(metadata)


def create_doclib_metadata(metadata):
    """
    Return a list of dicts defining each `key` and `value` from metadata dict.

    :param dict metadata: the dict to convert into the doclib metadata format
    :return:
    """
    return [{'key': k, 'value': v} for k, v in metadata.items()]


def _get_metadata_index_helper(metadata, key, value):
    """
    Return the index of the metadata dict matching the key and value provided.

    Returns the first match found.
    Returns None if a match is not found.

    :param list metadata: list of metadata dicts
    :param str key: the key to find
    :return:
    """
    for index, data in enumerate(metadata):
        data_key = data.get(key)
        if data_key == value:
            return index
    return None


def get_metadata_index_by_key(metadata, key):
    """
    Return the index of the metadata dict containing the given key.

    Returns the first matching key found.
    Returns None if the key is not found.

    :param list metadata: list of dicts
    :param str key: the key to find
    :return:
    """
    return _get_metadata_index_helper(metadata, 'key', key)


def get_metadata_index_by_value(metadata, value):
    """
    Return the index of the metadata dict containing the given value.

    Returns the first matching value found.
    Returns None if the value is not found.

    :param list metadata: list of dicts
    :param str value: the value to find
    :return:
    """
    return _get_metadata_index_helper(metadata, 'value', value)

def get_doclib_derivative_paths(path,doclib_derivatives_prefix,derivative_file_name, is_relative=True):

    # doclib_root = config.get("doclib.root")
    # doclib_derivatives_prefix = config.get("doclib.derivatives_prefix")
    # doclib_local_target = config.get("doclib.local_target")
    # doclib_local_temp = config.get("doclib.local_temp")

    doclib_root = "/doclib_dev/"
    doclib_local_target = "local"
    doclib_local_temp = "ingress"
    doclib_remote_target = "remote"

    paths = {}
    if is_relative:
        paths["absolute_path"] = os.path.join(doclib_root, path)
        paths["relative_path"] = path
    else:
        paths["absolute_path"] = path
        paths["relative_path"] = path.replace(doclib_root, "")

    path_array = paths["relative_path"].split("/")
    path_array[-1] = doclib_derivatives_prefix + "-" + path_array[-1]
    path_array.append(derivative_file_name)

    if path_array[1] != "derivatives":
        path_array.insert(1, "derivatives")

    if path_array[0] == doclib_remote_target:
        path_array.insert(2, doclib_remote_target)

    path_array[0] = doclib_local_temp

    paths["relative_temp_directory"] = "/".join(path_array[:-1])
    paths["absolute_temp_directory"] = os.path.join(doclib_root, paths["relative_temp_directory"])
    paths["relative_temp_path"] = "/".join(path_array)

    path_array[0] = doclib_local_target

    paths["relative_target_directory"] = "/".join(path_array[:-1])
    paths["relative_target_path"] = "/".join(path_array)

    return paths

