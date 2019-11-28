from bson import ObjectId
from mongomock import MongoClient

from src.klein_util.doclib import (
    parse_doclib_metadata, convert_document_metadata, create_doclib_metadata, get_metadata_index_by_key,
    get_metadata_index_by_value, get_document_with_ner
)


def test_parse_doclib_metadata_1():
    metadata = [
        {'key': 'a', 'value': 1},
        {'key': 'b', 'value': 2},
        {'key': 'c', 'value': 3},
    ]
    result = parse_doclib_metadata(metadata)
    expected_result = {'a': 1, 'b': 2, 'c': 3}
    assert result == expected_result


def test_parse_document_metadata_2():
    metadata = [
        {'key': 'a', 'value': 1, 'arbitrary_property': 'blah'},
        {'key': 'a'},
        {'value': 1},
    ]
    result = parse_doclib_metadata(metadata)
    expected_result = {'a': 1}
    assert result == expected_result


def test_parse_document_metadata_3():
    metadata = [
        {'key': 'a', 'value': 1, 'arbitrary_property': 'blah'},
        {'key': 'a', 'value': 2},
        {'value': 1},
    ]
    result = parse_doclib_metadata(metadata)
    expected_result = {'a': 2}
    assert result == expected_result


def test_parse_document_metadata_4():
    result = parse_doclib_metadata([])
    expected_result = {}
    assert result == expected_result


def test_combine_document_with_metadata_1():
    doc = {
        'id': 12345,
        'metadata': [
            {'key': 'a', 'value': 1},
            {'key': 'b', 'value': 2},
            {'key': 'c', 'value': 3},
        ]
    }

    convert_document_metadata(doc)

    expected_result = {
        'id': 12345,
        'metadata': {
            'a': 1,
            'b': 2,
            'c': 3
        }
    }

    assert doc == expected_result


def test_create_doclib_metadata_1():
    metadata = {
        'a': 1,
        'b': 2,
        'c': 3
    }

    result = create_doclib_metadata(metadata)

    expected_result = [
        {'key': 'a', 'value': 1},
        {'key': 'b', 'value': 2},
        {'key': 'c', 'value': 3},
    ]

    assert result == expected_result


def test_get_metadata_index_by_key_1():
    metadata = [
        {'key': 'a', 'value': 1},
        {'key': 'b', 'value': 2},
        {'key': 'c', 'value': 3},
    ]
    result = get_metadata_index_by_key(metadata, 'b')

    assert result == 1


def test_get_metadata_index_by_key_2():
    metadata = [
        {'key': 'a', 'value': 1},
        {'key': 'b', 'value': 2},
        {'key': 'c', 'value': 3},
    ]
    result = get_metadata_index_by_key(metadata, 'd')

    assert result is None


def test_get_metadata_index_by_value_1():
    metadata = [
        {'key': 'a', 'value': 1},
        {'key': 'b', 'value': 2},
        {'key': 'c', 'value': 3},
    ]
    result = get_metadata_index_by_value(metadata, 3)

    assert result == 2


# create a new mocked collection
test_db = MongoClient()['doclib']
test_doc_collection = test_db['documents']
test_doc_id = ObjectId("123456781234567812345678")
test_doc_collection.insert_one({
    "_id": test_doc_id,

})

test_ner_data = {
    "value": "aspirin",
    "hash": "90ea1eeaf311dc6d503bf7cb8056f8bb",
    "total": 1,
    "document": test_doc_id,
    "fragment": None,
    "occurrences": [
        {
            "entityType" : "DictMol",
            "entityGroup" : None,
            "schema" : "leadmine",
            "characterStart" : 0,
            "characterEnd" : 6,
            "fragment" : None,
            "correctedValue" : None,
            "type" : "Document"
        }
    ]
}

test_ner_collection = test_db['ner']
test_ner_collection.insert_one(test_ner_data)


def test_get_document_with_ner():
    result = get_document_with_ner({"_id": test_doc_id}, test_doc_collection)
    assert len(result['ner']) == 1
    assert result['ner'][0] == test_ner_data
