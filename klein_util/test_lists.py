import pytest


def test_add_thing_to_list_with_string():
    from .lists import add_thing_to_list
    result_list = add_thing_to_list([], "foo")
    assert len(result_list) == 1


def test_add_thing_to_list_with_list_of_strings():
    from .lists import add_thing_to_list
    result_list = add_thing_to_list([], ["bar", "moo"])
    assert len(result_list) == 2


def test_add_thing_to_existing_list_with_list_of_strings():
    from .lists import add_thing_to_list
    result_list = add_thing_to_list(["foo"], ["bar", "baz"])
    assert len(result_list) == 3


def test_add_thing_to_existing_list_with_list_of_strings_ensuring_uniqueness():
    from .lists import add_thing_to_list
    result_list = add_thing_to_list(["foo"], ["foo", "bar", "baz"])
    assert len(result_list) == 3


def test_add_thing_to_existing_list_dict():
    from .lists import add_thing_to_list
    result_list = add_thing_to_list([], {'monkey': 'tails'})
    assert isinstance(result_list, list)
    assert len(result_list) == 1
    assert "monkey" in result_list


def test_add_thing_to_existing_list_with_integer():
    from .lists import add_thing_to_list
    result_list = add_thing_to_list([], 1)
    assert len(result_list) == 1


def test_add_thing_to_existing_list_with_list_of_integers():
    from .lists import add_thing_to_list
    result_list = add_thing_to_list([], [1, 2])
    assert len(result_list) == 2


def test_add_thing_to_existing_list_with_list_of_dicts():
    from .lists import add_thing_to_list
    with pytest.raises(TypeError):
        add_thing_to_list([], [{'cow': 'moo'}, {'dog': 'bark'}])


def test_add_thing_to_existing_list_with_wrong_input_list_format():
    from .lists import add_thing_to_list
    with pytest.raises(TypeError):
        add_thing_to_list("foo", [{'cow': 'moo'}, {'dog': 'bark'}])


def test_add_thing_to_existing_list_with_complex_number():
    from .lists import add_thing_to_list
    with pytest.raises(TypeError):
        add_thing_to_list([], 2 + 3j)
