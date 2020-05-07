import pytest
from datetime import datetime
from unittest.mock import patch

from test.klein_util.test_common import test_config

from bson import ObjectId
from mongomock import MongoClient

from src.klein_util.doclib import (
    parse_doclib_metadata, convert_document_metadata, create_doclib_metadata, get_metadata_index_by_key,
    get_metadata_index_by_value, get_document_with_ner, set_doclib_flag, add_document_metadata,
    get_doclib_derivative_path, get_doclib_flag
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


@patch('src.klein_util.doclib.config', new=test_config)
def test_derivatives_path_remote():
    doc = {"source": "/remote/https/bbc.co.uk/test.pdf"}

    derivative_filename = "table1.csv"

    result = get_doclib_derivative_path(doc=doc, derivative_file_name=derivative_filename)

    assert result == "ingress/derivatives/remote/https/bbc.co.uk/pdf_to_table-test.pdf/table1.csv"


@patch('src.klein_util.doclib.config', new=test_config)
def test_derivatives_path_local_derivatives():
    doc = {"source": "local/derivatives/remote/https/bbc.co.uk/test.pdf"}

    derivative_filename = "table1.csv"

    result = get_doclib_derivative_path(doc=doc, derivative_file_name=derivative_filename)

    assert result == "ingress/derivatives/remote/https/bbc.co.uk/pdf_to_table-test.pdf/table1.csv"


@patch('src.klein_util.doclib.config', new=test_config)
def test_derivatives_path_local():
    doc = {"source": "local/xenobiotica/test.pdf"}

    derivative_filename = "table1.csv"

    result = get_doclib_derivative_path(doc=doc, derivative_file_name=derivative_filename)

    assert result == "ingress/derivatives/xenobiotica/pdf_to_table-test.pdf/table1.csv"


# create a new mocked collection
test_db = MongoClient()['doclib']
test_doc_collection = test_db['documents']
test_doc_id = ObjectId("123456781234567812345678")
test_doc = {
    "_id": test_doc_id,
    "doclib": [
        {
            "key": "doclib_other_key",
            "version" : {
                    "number" : "2.0.1-SNAPSHOT",
                    "major" : 2,
                    "minor" : 0,
                    "patch" : 1,
                    "hash" : "192544e4"
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
test_doc_collection.insert_one(test_doc)

test_ner_data = {
    "value": "aspirin",
    "hash": "90ea1eeaf311dc6d503bf7cb8056f8bb",
    "total": 1,
    "document": test_doc_id,
    "fragment": None,
    "occurrences": [
        {
            "entityType": "DictMol",
            "entityGroup": None,
            "schema": "leadmine",
            "characterStart": 0,
            "characterEnd": 6,
            "fragment": None,
            "correctedValue": None,
            "type": "Document"
        }
    ]
}

test_ner_collection = test_db['documents_ner']
test_ner_collection.insert_one(test_ner_data)


def test_get_document_with_ner():
    result = get_document_with_ner({"_id": test_doc_id}, test_doc_collection)
    assert len(result['ner']) == 1
    assert result['ner'][0] == test_ner_data


@patch('src.klein_util.doclib.config', new=test_config)
def test_set_doclib_flag():
    test_document = test_doc_collection.find_one({"_id": test_doc_id})
    flags = test_document['doclib']

    # initial flag from another  queue
    assert len(flags) == 1

    # add a new flag, which errors
    initial_started = datetime.now()
    initial_errored = datetime.now()
    set_doclib_flag(test_doc_collection, test_doc_id, started=initial_started, errored=initial_errored)

    # refresh the document
    test_document = test_doc_collection.find_one({"_id": test_doc_id})
    flags = test_document['doclib']
    new_flag = list(filter(lambda x: x['key'] == 'doclib_test_queue', flags))[0]

    assert len(flags) == 2
    # TODO - timestamps are recorded in mongo at different level of precision so need to account for that here
    # TODO (e.g. "2020-02-14 14:48:45.079866" becomes "2020-02-14 14:48:45.079000")
    # assert new_flag['errored'] == initial_errored
    assert new_flag['ended'] is None

    # add a new flag which completes:
    new_started = datetime.now()
    new_ended = datetime.now()
    set_doclib_flag(test_doc_collection, test_doc_id, started=new_started, ended=new_ended)

    # refresh the document again
    test_document = test_doc_collection.find_one({"_id": test_doc_id})
    updated_flags = test_document['doclib']
    new_updated_flags = list(filter(lambda x: x['key'] == 'doclib_test_queue', updated_flags))
    new_updated_flag = new_updated_flags[0]

    assert len(list(filter(lambda x: x['key'] == 'doclib_test_queue', new_updated_flags))) == 1
    assert new_updated_flag['errored'] is None
    # TODO - see above
    # assert new_updated_flag['ended'] == new_ended


get_flag_test_doc = {
    "doclib": [
        {
            "key": "doclib_other_key",
            "version" : {
                    "number" : "1.0.1-SNAPSHOT",
                    "major" : 1,
                    "minor" : 0,
                    "patch" : 1,
                    "hash" : "578543ed2"
            },
            "started": datetime.now(),
            "ended": datetime.now(),
            "errored": None
        },
        {
            "key": "doclib_test_queue",
            "version" : {
                    "number" : "2.0.1-SNAPSHOT",
                    "major" : 2,
                    "minor" : 0,
                    "patch" : 1,
                    "hash" : "192544e4"
            },
            "started": datetime.now(),
            "ended": None,
            "errored": datetime.now()
        }
    ],
}


@patch('src.klein_util.doclib.config', new=test_config)
def test_get_doclib_flag():
    flag = get_doclib_flag(get_flag_test_doc)

    assert flag["key"] == "doclib_test_queue"
    assert flag["ended"] is None


@patch('src.klein_util.doclib.config', new=test_config)
def test_get_doclib_flag_no_flag():
    flag = get_doclib_flag(test_doc)

    assert flag is None


@patch('src.klein_util.doclib.config', new=test_config)
def test_get_doclib_flag_no_doclib_property():
    flag = get_doclib_flag({})

    assert flag is None


def _get_test_doc_metadata():
    test_document = test_doc_collection.find_one({"_id": test_doc_id})
    return test_document['metadata']


@patch('src.klein_util.doclib.config', new=test_config)
def test_add_document_metadata():
    metadata = _get_test_doc_metadata()

    # initial data
    assert len(metadata) == 3
    assert get_metadata_index_by_key(metadata, "test1") == 0

    # add a new one:
    add_document_metadata(test_doc_collection, test_doc_id, "test3", "test three")

    metadata = _get_test_doc_metadata()
    assert len(metadata) == 4
    assert get_metadata_index_by_key(metadata, "test3") == 3

    # replace single
    add_document_metadata(test_doc_collection, test_doc_id, "test1", "test one modified", replace_all=True)

    metadata = _get_test_doc_metadata()
    assert len(metadata) == 4
    assert get_metadata_index_by_key(metadata, "test1") == 3

    # replace multiple
    add_document_metadata(test_doc_collection, test_doc_id, "test2", "test two modified", replace_all=True)

    metadata = _get_test_doc_metadata()
    assert len(metadata) == 3
    assert get_metadata_index_by_key(metadata, "test2") == 2

    meta_dict = parse_doclib_metadata(metadata)

    assert meta_dict["test1"] == "test one modified"
    assert meta_dict["test2"] == "test two modified"
    assert meta_dict["test3"] == "test three"

    # add duplicate key only
    add_document_metadata(test_doc_collection, test_doc_id, "test2", "test two modified dupe")

    metadata = _get_test_doc_metadata()
    assert len(metadata) == 4

    # add duplicate key and value
    add_document_metadata(test_doc_collection, test_doc_id, "test2", "test two modified dupe")

    metadata = _get_test_doc_metadata()
    assert len(metadata) == 4
