from datetime import datetime
from uuid import uuid4

from mongomock import MongoClient


# create a new mock db and documents collection
client = MongoClient()
db = client['doclib']
docs = db['documents']

# create a test document
test_doc_id = uuid4()
test_doc = {
    "_id": test_doc_id,
    "doclib": [
        {
            "key": "doclib_other_key",
            "version": {
                    "number": "2.0.1-SNAPSHOT",
                    "major": 2,
                    "minor": 0,
                    "patch": 1,
                    "hash": "192544e4"
            },
            "started": datetime.now(),
            "ended": datetime.now(),
            "errored": None
        }
    ],
    "metadata": [
        {"key": "test1", "value": "test one"},
        {"key": "test2", "value": "test two"},
        {"key": "test2", "value": "test two"},
    ]
}

docs.insert_one(test_doc)

# create a test ner record linked to the test document
test_ner_id = uuid4()
test_ner_data = {
    "_id": test_ner_id,
    "document": test_doc_id,
    "hash": "90ea1eeaf311dc6d503bf7cb8056f8bb",
    "schema": {
            "key": "chemical_entities",
            "config": "/srv/config/common/mdc/config/chemical_entities.yml",
            "lastRun": datetime(2020, 3, 16, 11, 14, 50),
            "tool": "leadminer",
            "version": "4"
    },
    "entityGroup": "Chemical",
    "entityType": "DictMol",
    "resolvedEntity": "O=C(C)Oc1ccccc1C(=O)O",
    "resolvedEntityHash": "c3bc9911c2e78082e91a6744b6bab22d",
    "value": "aspirin",
}

test_ner_collection = db['documents_ner']
test_ner_collection.insert_one(test_ner_data)

# create a test fragment linked to the test document
test_fragment_id = uuid4()
test_fragment_data = {
        "_id": test_fragment_id,
        "document": test_doc_id,
        "index": 0,
        "startAt": 3750,
        "endAt": 3776,
        "length": 26,
        "xpath": "/fake/xpath/text()"
}

test_fragments_collection = db['documents_fragments']
test_fragments_collection.insert_one(test_fragment_data)

# create a test ner occurrence record linked to the test document and test fragment
test_occurence_id = uuid4()
test_occurrence_data = {
        "_id": test_occurence_id,
        "nerDocument": test_ner_id,
        "characterStart": 3760,
        "characterEnd": 3766,
        "fragment": test_fragment_id,
        "correctedValue": None,
        "correctedValueHash": None,
        "wordIndex": None,
        "type": "document"
}

test_occurrences_collection = db['documents_ner_occurrences']
test_occurrences_collection.insert_one(test_occurrence_data)
