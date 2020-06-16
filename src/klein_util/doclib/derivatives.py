# -*- coding: utf-8 -*-
import os
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


# TODO - use 'os.path.isabs()' instead of 'is_relative' param??
def get_doclib_derivative_paths(
        path,
        derivative_file_name,
        doclib_derivatives_prefix=None,
        is_relative=True
    ):
    """
    Returns a dict containing file paths for doclib derivative files.

    `Wiki - File Paths
    <https://wiki.mdcatapult.io/Projects/Document_Library/v2#File_Paths>`_

    :param str path: the path of the parent file
    :param str derivative_file_name: the name of the derivative file
    :param bool is_relative: flag indicating if the path provided is relative
    """
    doclib_root = config.get("doclib.root")
    doclib_local_target = config.get("doclib.local_target")
    doclib_local_temp = config.get("doclib.local_temp")
    doclib_remote_target = config.get("doclib.remote_target")

    # use the provided prefix or default to the configured prefix for the consumer
    doclib_derivatives_prefix = doclib_derivatives_prefix or config.get("doclib.derivatives_prefix")

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
    paths["absolute_temp_path"] = os.path.join(doclib_root, paths["relative_temp_path"])

    path_array[0] = doclib_local_target

    paths["relative_target_directory"] = "/".join(path_array[:-1])
    paths["relative_target_path"] = "/".join(path_array)

    return paths


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