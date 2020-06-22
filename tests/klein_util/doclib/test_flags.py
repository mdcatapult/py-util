from datetime import datetime
import sys
from unittest.mock import patch

from tests.klein_util.test_common import test_config
from tests.klein_util.test_mongo import docs, test_doc_id
# inject a test klein_mongo object
sys.modules['klein_mongo'] = __import__('tests.klein_util.test_mongo')

# pylint: disable=wrong-import-position
from src.klein_util.doclib import get_doclib_flag, set_doclib_flag


other_flag_test_doc = {
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
}


@patch('src.klein_util.doclib.flags.config', new=test_config)
def test_get_doclib_flag_no_doclib_property():
    flag = get_doclib_flag({})

    assert flag is None


@patch('src.klein_util.doclib.flags.config', new=test_config)
def test_get_doclib_flag_other_flag():
    flag = get_doclib_flag(other_flag_test_doc)

    assert flag is None


@patch('src.klein_util.doclib.flags.config', new=test_config)
def test_set_doclib_flag():
    test_document = docs.find_one({"_id": test_doc_id})
    flags = test_document['doclib']

    # initial flag from another  queue
    assert len(flags) == 1

    # add a new flag, which errors
    initial_started = datetime.now()
    initial_errored = datetime.now()
    set_doclib_flag(test_doc_id, started=initial_started, errored=initial_errored)

    # refresh the document
    test_document = docs.find_one({"_id": test_doc_id})
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
    set_doclib_flag(test_doc_id, started=new_started, ended=new_ended)

    # refresh the document again
    test_document = docs.find_one({"_id": test_doc_id})
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


@patch('src.klein_util.doclib.flags.config', new=test_config)
def test_get_doclib_flag():
    flag = get_doclib_flag(get_flag_test_doc)

    assert flag["key"] == "doclib_test_queue"
    assert flag["ended"] is None
                                                                                                                                                                                                                         