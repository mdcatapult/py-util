from unittest.mock import patch
import sys

from tests.klein_util.test_common import test_config
# from tests.klein_util.test_mongo import docs, test_doc_id
# inject a test klein_mongo object
sys.modules['klein_mongo'] = __import__('tests.klein_util.test_mongo')

# pylint: disable=wrong-import-position
from src.klein_util.doclib import get_doclib_derivative_path, get_doclib_derivative_paths


@patch('src.klein_util.doclib.derivatives.config', new=test_config)
def test_derivatives_path_remote():
    doc = {"source": "/remote/https/bbc.co.uk/test.pdf"}

    derivative_filename = "table1.csv"

    result = get_doclib_derivative_path(doc=doc, derivative_file_name=derivative_filename)

    assert result == "ingress/derivatives/remote/https/bbc.co.uk/raw_text-test.pdf/table1.csv"


@patch('src.klein_util.doclib.derivatives.config', new=test_config)
def test_derivatives_path_local_derivatives():
    doc = {"source": "local/derivatives/remote/https/bbc.co.uk/test.pdf"}

    derivative_filename = "table1.csv"

    result = get_doclib_derivative_path(doc=doc, derivative_file_name=derivative_filename)

    assert result == "ingress/derivatives/remote/https/bbc.co.uk/raw_text-test.pdf/table1.csv"


@patch('src.klein_util.doclib.derivatives.config', new=test_config)
def test_derivatives_path_local():
    doc = {"source": "local/xenobiotica/test.pdf"}

    derivative_filename = "table1.csv"

    result = get_doclib_derivative_path(doc=doc, derivative_file_name=derivative_filename)

    assert result == "ingress/derivatives/xenobiotica/raw_text-test.pdf/table1.csv"


@patch('src.klein_util.doclib.derivatives.config', new=test_config)
def test_get_paths_derivative_from_local_derivative():
    path = "local/derivatives/ebi/supplementary/unarchived-PMC123456.zip/information.xml"

    paths = get_doclib_derivative_paths(path, derivative_file_name="raw.txt")

    assert paths["absolute_path"] == "/doclib_dev/local/derivatives/ebi/supplementary/unarchived-PMC123456.zip/information.xml"
    assert paths["relative_path"] == path
    assert paths["relative_temp_path"] == "ingress/derivatives/ebi/supplementary/unarchived-PMC123456.zip/raw_text-information.xml/raw.txt"
    assert paths["relative_temp_directory"] == "ingress/derivatives/ebi/supplementary/unarchived-PMC123456.zip/raw_text-information.xml"
    assert paths["absolute_temp_directory"] == "/doclib_dev/ingress/derivatives/ebi/supplementary/unarchived-PMC123456.zip/raw_text-information.xml"
    assert paths["relative_target_path"] == "local/derivatives/ebi/supplementary/unarchived-PMC123456.zip/raw_text-information.xml/raw.txt"


@patch('src.klein_util.doclib.derivatives.config', new=test_config)
def test_get_paths_derivative_from_local_non_derivative():
    path = "local/ebi/supplementary/compounds.xls"
    
    paths = get_doclib_derivative_paths(
        path, 
        derivative_file_name="sheet1.tsv",  
        doclib_derivatives_prefix="spreadsheet_conv"
    )

    assert paths["absolute_path"] == "/doclib_dev/local/ebi/supplementary/compounds.xls"
    assert paths["relative_path"] == path
    assert paths["relative_temp_path"] == "ingress/derivatives/ebi/supplementary/spreadsheet_conv-compounds.xls/sheet1.tsv"
    assert paths["relative_temp_directory"] == "ingress/derivatives/ebi/supplementary/spreadsheet_conv-compounds.xls"
    assert paths["absolute_temp_directory"] == "/doclib_dev/ingress/derivatives/ebi/supplementary/spreadsheet_conv-compounds.xls"
    assert paths["relative_target_path"] == "local/derivatives/ebi/supplementary/spreadsheet_conv-compounds.xls/sheet1.tsv"


@patch('src.klein_util.doclib.derivatives.config', new=test_config)
def test_get_paths_derivative_from_remote():
    path = "remote/http/phpboyscout.uk/assets/text.zip"

    paths = get_doclib_derivative_paths(
        path, 
        derivative_file_name="evidence.png",
        doclib_derivatives_prefix="unarchived"
    )

    assert paths["absolute_path"] == "/doclib_dev/remote/http/phpboyscout.uk/assets/text.zip"
    assert paths["relative_path"] == path
    assert paths["relative_temp_path"] == "ingress/derivatives/remote/http/phpboyscout.uk/assets/unarchived-text.zip/evidence.png"
    assert paths["relative_temp_directory"] == "ingress/derivatives/remote/http/phpboyscout.uk/assets/unarchived-text.zip"
    assert paths["absolute_temp_directory"] == "/doclib_dev/ingress/derivatives/remote/http/phpboyscout.uk/assets/unarchived-text.zip"
    assert paths["relative_target_path"] == "local/derivatives/remote/http/phpboyscout.uk/assets/unarchived-text.zip/evidence.png"


@patch('src.klein_util.doclib.derivatives.config', new=test_config)
def test_get_paths_derivative_from_remote_absolute_path():
    path = "/doclib_dev/remote/http/phpboyscout.uk/assets/text.zip"

    paths = get_doclib_derivative_paths(
        path, 
        derivative_file_name="evidence.png",
        doclib_derivatives_prefix="unarchived", 
        is_relative=False
    )

    assert paths["absolute_path"] == "/doclib_dev/remote/http/phpboyscout.uk/assets/text.zip"
    assert paths["relative_path"] == "remote/http/phpboyscout.uk/assets/text.zip"
    assert paths["relative_temp_path"] == "ingress/derivatives/remote/http/phpboyscout.uk/assets/unarchived-text.zip/evidence.png"
    assert paths["relative_temp_directory"] == "ingress/derivatives/remote/http/phpboyscout.uk/assets/unarchived-text.zip"
    assert paths["absolute_temp_directory"] == "/doclib_dev/ingress/derivatives/remote/http/phpboyscout.uk/assets/unarchived-text.zip"
    assert paths["relative_target_path"] == "local/derivatives/remote/http/phpboyscout.uk/assets/unarchived-text.zip/evidence.png"
