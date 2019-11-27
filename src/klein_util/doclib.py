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


def get_document_with_ner(
        doc_query,
        doc_collection,
        ner_collection_name="ner"
):
    """
    Return a matching document with added NER information.

    Only returns a single document, so only suitable for use with queries that
    are expected to return a single hit - e.g. "_id" or other unique field.

    :param dict doc_query: a dict defining the document
    :param pymongo.collection.Collection doc_collection: the document mongo
    collection object
    :param str ner_collection_name: the ner mongo collection name (default:
    "ner")
    :return: the new document as dict
    """
    # from pdb import set_trace
    # set_trace()
    return doc_collection.aggregate([
        {"$match": doc_query},
        {"$lookup": {
            "from": ner_collection_name,
            "localField": "_id",
            "foreignField": "document",
            "as": "ner"}
        }
    ]).next()
