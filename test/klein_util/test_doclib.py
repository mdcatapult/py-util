from src.klein_util.doclib import (
    parse_doclib_metadata, convert_document_metadata, create_doclib_metadata, get_metadata_index_by_key,
    get_metadata_index_by_value
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
