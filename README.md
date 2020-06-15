[![pipeline status](https://gitlab.mdcatapult.io/informatics/klein/py-util/badges/update-to-uuid/pipeline.svg)](https://gitlab.mdcatapult.io/informatics/klein/py-util/-/commits/update-to-uuid)

[![coverage report](https://gitlab.mdcatapult.io/informatics/klein/py-util/badges/update-to-uuid/coverage.svg)](https://gitlab.mdcatapult.io/informatics/klein/py-util/-/commits/update-to-uuid)

# Klein Util

Module to contain some basic utility components


### klein_util.dict
`traverse_dict()` - function for traversing nested dicts using a list of keys

*Example:* get a field from a mongo `doc` using dot notation:
```
from klein_util.dict import traverse_dict

property = 'ner.chemicalentities.found'
entities_found = traverse_dict(doc, property.split('.'))
```

### klein_util.doclib
Functions for interacting with doclib metadata in the following format:
```
    ...
    'metadata': [
        {"key": "key1", "value": "value1"}, 
        {"key": "key2", "value": "value2"}, 
        {"key": "key3", "value": "value3"}, 
    ],  
    ...
```

`parse_doclib_metadata()` - converts metadata list in the above format to 
standard dict notation.

`convert_document_metadata` - updates a mongo doc's metadata to standard dict 
notation.

`create_doclib_metadata()` - converts a standard dict to a list of dicts 
defining a `key` and `value` for each pair.

`get_metadata_index_by_key() / get_metadata_index_by_value()` - returns the 
index from a metadata list for the first matching key or value.

Convenience functions for other doclib activities

`get_document_with_ner` - takes a simple document query (e.g. `_id` or
`source`) and returns it with an `ner` field containing matches from the `ner`
collection.

## Tests
To run tests, run the following command in the project root directory:

```
python -m pytest
```