# -*- coding: utf-8 -*-
from klein_mongo import docs


# TODO - allow for duplicate keys??
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

    Note - to create metadata items with duplicate keys, provide a list.

    :param dict metadata: the dict to convert into the doclib metadata format
    :return:
    """
    doclib_metadata = []
    for key, value in metadata.items():
        if isinstance(value, list):
            for item in value:
                doclib_metadata.append({'key': key, 'value': item})
        else:
            doclib_metadata.append({'key': key, 'value': value})
    return doclib_metadata


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


def add_document_metadata(doc_id, key, value, collection=docs, replace_all=False):
    """
    Creates or updates a metadata object for a document.

    By default this will not replace any existing metadata object(s) with the
    same key. Use `replace_all=True` to removing all existing ones.
    NOTE - exact duplicates (matching key and value) will not be created in
    either case.
    
    @param uuid.UUID doc_id: the document uuid
    @param str key: the metadata key
    @param str value: the metadata value
    @param pymongo.collection.Collection collection: the mongodb collection
    (defaults to the configured 'docs' collection)
    @param bool replace_all: flag to replace all existing metadata objects
    matching the key
    @return:
    """
    if replace_all:
        # remove any metadata object matching the key
        collection.update_one(
            {"_id": doc_id},
            {"$pull": {"metadata": {"key": key}}}
        )

    # then create a new one with the provided details
    # (exact duplicates will not be created, only duplicate keys if replace_all=False)
    collection.update_one(
        {"_id": doc_id},
        {"$addToSet": {"metadata": {"key": key, "value": value}}},
    )
