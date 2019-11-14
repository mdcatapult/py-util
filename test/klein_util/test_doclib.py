import pytest

from src.klein_util.doclib import (
    parse_doclib_metadata, convert_document_metadata, create_doclib_metadata, get_metadata_index_by_key,
    get_metadata_index_by_value, get_doclib_derivative_paths
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


# def test_get_paths_derivative_from_local_derivative():
#     path = "local/derivatives/ebi/supplementary/unarchived-PMC123456.zip/information.xml"
#
#     paths = get_doclib_derivative_paths(path=path, doclib_derivatives_prefix="raw_text", derivative_file_name="raw.txt")
#
#     assert paths[
#                "absolute_path"] == "/doclib_dev/local/derivatives/ebi/supplementary/unarchived-PMC123456.zip/information.xml"
#
#     assert paths["relative_path"] == path
#
#     assert paths["relative_temp_path"] == "ingress/derivatives/ebi/supplementary/unarchived-PMC123456.zip/raw_text-information.xml/raw.txt"
#
#     assert paths["relative_temp_directory"] == "ingress/derivatives/ebi/supplementary/unarchived-PMC123456.zip/raw_text-information.xml"
#
#     assert paths["absolute_temp_directory"] == "/doclib_dev/ingress/derivatives/ebi/supplementary/unarchived-PMC123456.zip/raw_text-information.xml"
#
#     assert paths["relative_target_path"] == "local/derivatives/ebi/supplementary/unarchived-PMC123456.zip/raw_text-information.xml/raw.txt"
#
#
# def test_get_paths_derivative_from_local_non_derivative():
#     path = "local/ebi/supplementary/compounds.xls"
#
#     paths = get_doclib_derivative_paths(path=path, doclib_derivatives_prefix="spreadsheet_conv", derivative_file_name="sheet1.tsv")
#
#     assert paths[
#                "absolute_path"] == "/doclib_dev/local/ebi/supplementary/compounds.xls"
#
#     assert paths["relative_path"] == path
#
#     assert paths["relative_temp_path"] == "ingress/derivatives/ebi/supplementary/spreadsheet_conv-compounds.xls/sheet1.tsv"
#
#     assert paths["relative_temp_directory"] == "ingress/derivatives/ebi/supplementary/spreadsheet_conv-compounds.xls"
#
#     assert paths["absolute_temp_directory"] == "/doclib_dev/ingress/derivatives/ebi/supplementary/spreadsheet_conv-compounds.xls"
#
#     assert paths["relative_target_path"] == "local/derivatives/ebi/supplementary/spreadsheet_conv-compounds.xls/sheet1.tsv"
#
#
# def test_get_paths_derivative_from_remote():
#     path = "remote/http/phpboyscout.uk/assets/text.zip"
#
#     paths = get_doclib_derivative_paths(path=path, doclib_derivatives_prefix="unarchived", derivative_file_name="evidence.png")
#
#     assert paths[
#                "absolute_path"] == "/doclib_dev/remote/http/phpboyscout.uk/assets/text.zip"
#
#     assert paths["relative_path"] == path
#
#     assert paths["relative_temp_path"] == "ingress/derivatives/remote/http/phpboyscout.uk/assets/unarchived-text.zip/evidence.png"
#
#     assert paths["relative_temp_directory"] == "ingress/derivatives/remote/http/phpboyscout.uk/assets/unarchived-text.zip"
#
#     assert paths["absolute_temp_directory"] == "/doclib_dev/ingress/derivatives/remote/http/phpboyscout.uk/assets/unarchived-text.zip"
#
#     assert paths["relative_target_path"] == "local/derivatives/remote/http/phpboyscout.uk/assets/unarchived-text.zip/evidence.png"
#
#
# def test_get_paths_derivative_from_remote_absolute_path():
#     path = "/doclib_dev/remote/http/phpboyscout.uk/assets/text.zip"
#
#     paths = get_doclib_derivative_paths(path=path, doclib_derivatives_prefix="unarchived", derivative_file_name="evidence.png", is_relative=False)
#
#     assert paths[
#                "absolute_path"] == "/doclib_dev/remote/http/phpboyscout.uk/assets/text.zip"
#
#     assert paths["relative_path"] == "remote/http/phpboyscout.uk/assets/text.zip"
#
#     assert paths["relative_temp_path"] == "ingress/derivatives/remote/http/phpboyscout.uk/assets/unarchived-text.zip/evidence.png"
#
#     assert paths["relative_temp_directory"] == "ingress/derivatives/remote/http/phpboyscout.uk/assets/unarchived-text.zip"
#
#     assert paths["absolute_temp_directory"] == "/doclib_dev/ingress/derivatives/remote/http/phpboyscout.uk/assets/unarchived-text.zip"
#
#     assert paths["relative_target_path"] == "local/derivatives/remote/http/phpboyscout.uk/assets/unarchived-text.zip/evidence.png"
