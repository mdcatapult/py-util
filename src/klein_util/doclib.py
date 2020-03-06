import pathlib
# -*- coding: utf-8 -*-
from bson import ObjectId

from klein_config import config


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


def get_doclib_derivative_path(doc, derivative_file_name, derivatives_prefix):

    p = pathlib.Path(doc["source"])

    parts = list(p.parts)

    # todo get ingress from config config.get("doclib.local_temp") needs config aware unit test
    parts[0] = "ingress"

    if parts[1] != "derivatives":
        parts.insert(1, "derivatives")

    # todo get derivatives_prefix from config config.get("consumer.derivatives.prefix") needs config aware unit test
    parts[-1] = "{prefix}-{filename}".format(prefix=derivatives_prefix, filename=parts[-1])

    parts.append(derivative_file_name)

    parts = tuple(parts)

    derivative = str(pathlib.Path(*parts))

    return derivative

# TODO - cant seem to mock klein_mongo.docs, so for now, the collection is a method parameter
# TODO - to allow this to be tested
def set_document_metadata(collection, doc_id, key, value, replace=True):
    """
    Creates or updates a metadata object for a document.

    By default this will replace any existing metadata object(s) with the same
    key. Use `replace=False` to add without removing existing ones.

    @param pymongo.collection.Collection collection: the mongodb collection
    @param str doc_id: the document id
    @param str key: the metadata key
    @param str value: the metadata value
    @param bool replace: flag to replace existing metadata objects
    @return:
    """
    if replace:
        # remove any metadata object matching the key
        collection.update_one(
            {"_id": ObjectId(doc_id)},
            {"$pull": {"metadata": {"key": key}}}
        )

    # then create a new one with the provided details
    collection.update_one(
        {"_id": ObjectId(doc_id)},
        {"$push": {"metadata": {"key": key, "value": value}}},
    )


def _get_documents_with_ner(
        doc_query,
        doc_collection,
        ner_collection_name="documents_ner"
):
    """
    Returns a pymongo CommandCursor of matching documents with added NER info.

    :param dict doc_query: a dict defining the document query
    :param pymongo.collection.Collection doc_collection: the document mongo
    collection object
    :param str ner_collection_name: the ner mongo collection name (default:
    "documents_ner")
    :return: the pymongo.command_cursor.CommandCursor object
    """
    return doc_collection.aggregate([
        {"$match": doc_query},
        {"$lookup": {
            "from": ner_collection_name,
            "localField": "_id",
            "foreignField": "document",
            "as": "ner"}
        }
    ])


def get_document_with_ner(
        doc_query,
        doc_collection,
        ner_collection_name="documents_ner"
):
    """
    Returns a matching document with added NER information.

    Only returns a single document, so only suitable for use with queries that
    are expected to return a single hit - e.g. "_id" or other unique field.

    :param dict doc_query: a dict defining the document query
    :param pymongo.collection.Collection doc_collection: the document mongo
    collection object
    :param str ner_collection_name: the ner mongo collection name (default:
    "ner")
    :return: the document + ner info as dict
    """
    return _get_documents_with_ner(
        doc_query,
        doc_collection,
        ner_collection_name
    ).next()


# TODO - cant seem to mock klein_mongo.docs, so for now, the collection is a method parameter
# TODO - to allow this to be tested
def set_doclib_flag(collection, doc_id, started=None, ended=None, errored=None):
    """
    Creates or updates a doclib flag object for the consumer for a document.

    @param pymongo.collection.Collection collection: the mongodb collection
    @param str doc_id: the document id
    @param datetime started: started timestamp
    @param datetime ended: ended timestamp
    @param datetime errored: ended timestamp
    @return:
    """
    key = config.get("consumer.queue")

    flag = {
        "key": key,
        "version": config.get("consumer.version"),
        "started": started,
        "ended": ended,
        "errored": errored
    }

    # remove any existing flag(s) with the consumer's key
    collection.update_one(
        {"_id": ObjectId(doc_id)},
        {"$pull": {"doclib": {"key": key}}}
    )

    # then create a new one with the provided details
    collection.update_one(
        {"_id": ObjectId(doc_id)},
        {"$push": {"doclib": flag}},
    )