from unittest.mock import patch
import sys

from tests.klein_util.test_common import test_config
# from tests.klein_util.test_mongo import docs, test_doc_id
# inject a test klein_mongo object
sys.modules['klein_mongo'] = __import__('tests.klein_util.test_mongo')

# pylint: disable=wrong-import-position

from src.klein_util.doclib import get_doclib_derivative_path


@patch('src.klein_util.doclib.derivatives.config', new=test_config)
def test_derivatives_path_remote():
    doc = {"source": "/remote/https/bbc.co.uk/test.pdf"}

    derivative_filename = "table1.csv"

    result = get_doclib_derivative_path(doc=doc, derivative_file_name=derivative_filename)

    assert result == "ingress/derivatives/remote/https/bbc.co.uk/pdf_to_table-test.pdf/table1.csv"


@patch('src.klein_util.doclib.derivatives.config', new=test_config)
def test_derivatives_path_local_derivatives():
    doc = {"source": "local/derivatives/remote/https/bbc.co.uk/test.pdf"}

    derivative_filename = "table1.csv"

    result = get_doclib_derivative_path(doc=doc, derivative_file_name=derivative_filename)

    assert result == "ingress/derivatives/remote/https/bbc.co.uk/pdf_to_table-test.pdf/table1.csv"


@patch('src.klein_util.doclib.derivatives.config', new=test_config)
def test_derivatives_path_local():
    doc = {"source": "local/xenobiotica/test.pdf"}

    derivative_filename = "table1.csv"

    result = get_doclib_derivative_path(doc=doc, derivative_file_name=derivative_filename)

    assert result == "ingress/derivatives/xenobiotica/pdf_to_table-test.pdf/table1.csv"

