# copyright 2022 Medicines Discovery Catapult
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest

from src.klein_util.lists import add_string


def test_add_string_with_string():
    result_list = add_string([], "foo")
    assert len(result_list) == 1


def test_add_string_with_list_of_strings():
    result_list = add_string([], ["bar", "moo"])
    assert len(result_list) == 2


def test_add_thing_to_existing_list_with_list_of_strings():
    result_list = add_string(["foo"], ["bar", "baz"])
    assert len(result_list) == 3


def test_add_thing_to_existing_list_with_list_of_strings_ensuring_uniqueness():
    result_list = add_string(["foo"], ["foo", "bar", "baz"])
    assert len(result_list) == 3


def test_add_thing_to_existing_list_dict():
    result_list = add_string([], {'monkey': 'tails'})
    assert isinstance(result_list, list)
    assert len(result_list) == 1
    assert "monkey" in result_list


def test_add_thing_to_existing_list_with_integer():
    result_list = add_string([], 1)
    assert len(result_list) == 1


def test_add_thing_to_existing_list_with_list_of_integers():
    result_list = add_string([], [1, 2])
    assert len(result_list) == 2


def test_add_thing_to_existing_list_with_list_of_dicts():
    with pytest.raises(TypeError):
        add_string([], [{'cow': 'moo'}, {'dog': 'bark'}])


def test_add_thing_to_existing_list_with_wrong_input_list_format():
    with pytest.raises(TypeError):
        add_string("foo", [{'cow': 'moo'}, {'dog': 'bark'}])


def test_add_thing_to_existing_list_with_complex_number():
    with pytest.raises(TypeError):
        add_string([], 2 + 3j)
