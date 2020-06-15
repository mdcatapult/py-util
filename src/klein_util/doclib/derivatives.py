# -*- coding: utf-8 -*-
import pathlib

from klein_config import config
from klein_mongo import docs


def get_doclib_derivative_path(doc, derivative_file_name):

    p = pathlib.Path(doc["source"])
    parts = list(p.parts)
    parts[0] = config.get("doclib.local_temp")

    if parts[1] != "derivatives":
        parts.insert(1, "derivatives")

    prefix = config.get("doclib.derivatives_prefix")
    parent_filename=parts[-1]
    parts[-1] = f"{prefix}-{parent_filename}"

    parts.append(derivative_file_name)
    parts = tuple(parts)

    return str(pathlib.Path(*parts))


def get_document_parent(doc):
    """
    Return the immediate parent of a document (or None).

    :param doc: the document
    :return: the document's parent or None
    """
    deriv_collection_name = config.get("mongo.derivatives_collection", "documents_derivatives")
    deriv_collection = docs.database[deriv_collection_name]

    # TODO - what about multiple parents?
    derivative = deriv_collection.find_one({"child": doc["_id"]})
    
    if derivative:
        return docs.find_one({"_id": derivative["parent"]})

    return None