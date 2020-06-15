import sys
from unittest.mock import patch

from tests.klein_util.test_common import test_config
from tests.klein_util.test_mongo import (
    test_doc_id, test_ner_data, test_occurrence_data, test_fragment_data
)
# inject a test klein_mongo object
sys.modules['klein_mongo'] = __import__('tests.klein_util.test_mongo')

# pylint: disable=wrong-import-position
from src.klein_util.doclib import get_document_ner


@patch('src.klein_util.doclib.ner.config', new=test_config)
def test_get_document_ner_without_occurrences():
    result = get_document_ner(test_doc_id, include_occurrences=False)
    assert len(result) == 1
    assert result[0] == test_ner_data


@patch('src.klein_util.doclib.ner.config', new=test_config)
def test_get_document_ner_include_schema_with_hits():
    result = get_document_ner(test_doc_id, include_schemas=["chemical_entities"])
    assert len(result) == 1


@patch('src.klein_util.doclib.ner.config', new=test_config)
def test_get_document_ner_include_schema_without_hits():
    result = get_document_ner(test_doc_id, include_schemas=["invalid_schema_name"])
    assert len(result) == 0


@patch('src.klein_util.doclib.ner.config', new=test_config)
def test_get_document_ner_exclude_schema_with_hits():
    result = get_document_ner(test_doc_id, exclude_schemas=["chemical_entities"])
    assert len(result) == 0


@patch('src.klein_util.doclib.ner.config', new=test_config)
def test_get_document_ner_exclude_schema_without_hits():
    result = get_document_ner(test_doc_id, exclude_schemas=["invalid_schema_name"])
    assert len(result) == 1


@patch('src.klein_util.doclib.ner.config', new=test_config)
def test_get_document_ner_with_occurrences():
    result = get_document_ner(test_doc_id)
    assert len(result) == 1
    occurrences = result[0].get("occurrences")
    assert len(occurrences) == 1
    assert occurrences[0] == test_occurrence_data 


@patch('src.klein_util.doclib.ner.config', new=test_config)
def test_get_document_ner_with_fragments():
    result = get_document_ner(test_doc_id, include_fragments=True)
    assert len(result) == 1
    print()
    print("RESULT:", result)
    print()
    fragments = result[0].get("fragments")
    assert len(fragments) == 1
    assert fragments[0] == test_fragment_data 
