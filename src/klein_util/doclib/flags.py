# -*- coding: utf-8 -*-
from klein_config import config
from klein_mongo import docs


def get_doclib_flag(doc):
    """
    Returns a doclib flag object for a given document or None.

    Uses the consumer name of the configured consumer as the flag key.
    
    @param dict doc: the document
    :return: the doclib flag as a dict (or None)
    """
    key = config.get("consumer.name")

    for flag in doc.get("doclib", []):
        if flag["key"] == key:
            return flag

    return None


def set_doclib_flag(doc_id, started=None, ended=None, errored=None, collection=docs):
    """
    Creates or updates a doclib flag object for the consumer for a document.

    
    @param uuid.UUID doc_id: the document uuid
    @param datetime started: started timestamp
    @param datetime ended: ended timestamp
    @param datetime errored: ended timestamp
    @param pymongo.collection.Collection collection: the mongodb collection
    (defaults to the configured 'docs' collection)
    @return:
    """
    key = config.get("consumer.name")

    flag = {
        "key": key,
        "version": config.get("consumer.version"),
        "started": started,
        "ended": ended,
        "errored": errored
    }

    # TODO - perform in a single update using $ notation? (as per the scala code)
    # remove any existing flag(s) with the consumer's key
    collection.update_one(
        {"_id": doc_id},
        {"$pull": {"doclib": {"key": key}}}
    )

    # then create a new one with the provided details
    collection.update_one(
        {"_id": doc_id},
        {"$push": {"doclib": flag}},
    )
