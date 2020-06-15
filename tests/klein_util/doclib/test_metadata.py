import sys

from tests.klein_util.test_mongo import docs, test_doc_id
# inject a test klein_mongo object
sys.modules['klein_mongo'] = __import__('tests.klein_util.test_mongo')

# pylint: disable=wrong-import-position
from src.klein_util.doclib import (
    parse_doclib_metadata, convert_document_metadata, create_doclib_metadata, 
    get_metadata_index_by_key, get_metadata_index_by_value, add_document_metadata
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

    
def _get_test_doc_metadata():
    test_document = docs.find_one({"_id": test_doc_id})
    return test_document['metadata']


def test_add_document_metadata():
    metadata = _get_test_doc_metadata()

    # initial data
    assert len(metadata) == 3
    assert get_metadata_index_by_key(metadata, "test1") == 0

    # add a new one:
    add_document_metadata(test_doc_id, "test3", "test three")

    metadata = _get_test_doc_metadata()
    assert len(metadata) == 4
    assert get_metadata_index_by_key(metadata, "test3") == 3

    # replace single
    add_document_metadata(test_doc_id, "test1", "test one modified", replace_all=True)

    metadata = _get_test_doc_metadata()
    assert len(metadata) == 4
    assert get_metadata_index_by_key(metadata, "test1") == 3

    # replace multiple
    add_document_metadata(test_doc_id, "test2", "test two modified", replace_all=True)

    metadata = _get_test_doc_metadata()
    assert len(metadata) == 3
    assert get_metadata_index_by_key(metadata, "test2") == 2

    meta_dict = parse_doclib_metadata(metadata)

    assert meta_dict["test1"] == "test one modified"
    assert meta_dict["test2"] == "test two modified"
    assert meta_dict["test3"] == "test three"

    # add duplicate key only
    add_document_metadata(test_doc_id, "test2", "test two modified dupe")

    metadata = _get_test_doc_metadata()
    assert len(metadata) == 4

    # add duplicate key and value
    add_document_metadata(test_doc_id, "test2", "test two modified dupe")

    metadata = _get_test_doc_metadata()
    assert len(metadata) == 4
