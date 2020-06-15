# -*- coding: utf-8 -*-
from klein_config import config
from klein_mongo import db


# TODO - fragments isn't strictly NER data - should it be a separate method (and module)?
def get_document_ner(
        doc_id, 
        include_schemas=None,
        exclude_schemas=None,
        include_occurrences=True, 
        include_fragments=False,
    ):
    """
    Returns ner data for a given document id as a dict.

    An optional list of NER schema keys can be provided to either filter
    (`incude_schemas`) or exclude (`exclude_schemas`). 
    The data can optionally include occurrences and/or fragments for each
    entity found.

    :param uuid.UUID doc_id: the document uuid
    :param list include_schemas: list of NER schema keys to include
    :param list exclude_schemas: list of NER schema keys to exclude
    :param bool include_occurrences: flag to include occurrences in the output
    (default: True)
    :param bool include_fragments: flag to include fragments in the output
    (default: False)
    """
    ner_collection = ner_collection = db[config.get("mongo.ner_collection")]

    doc_criteria = [{"document": doc_id}]
    
    if include_schemas:
        doc_criteria.append({"schema.key": {"$in": include_schemas}})
    
    if exclude_schemas:
        doc_criteria.append({"schema.key": {"$nin": exclude_schemas}})

    pipeline = [
        {"$match": {"$and": doc_criteria}},
    ]

    if include_occurrences:
        pipeline.append(
            {"$lookup": {
                "from": config.get("mongo.ner_occurrences_collection"),
                "localField": "_id",
                "foreignField": "nerDocument",
                "as": "occurrences"
            }},
        )

    if include_fragments:
        pipeline.append(
            {"$lookup": {
                "from": config.get("mongo.fragments_collection"),
                "localField": "document",
                "foreignField": "document",
                "as": "fragments"
            }},
        )

    return list(ner_collection.aggregate(pipeline=pipeline))
