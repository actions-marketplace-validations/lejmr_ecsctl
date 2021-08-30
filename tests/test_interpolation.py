from ecs.render import interpolate_values
import pytest

def test_no_interpolation():
    inp = {
        "b": "c"
    }
    v = interpolate_values(inp)
    assert v == {"b": "c"}


def test_simple_interpolation():
    inp = {
        "a": "{{ b }}",
        "b": "c"
    }
    v = interpolate_values(inp)
    assert v == {"a": "c", "b": "c"}


def test_nested_interpolation():
    inp = {
        "a": "{{ b }}",
        "b": "inp_{{ c }}",
        "c": "test"
    }
    v = interpolate_values(inp)
    assert v == {"a": "inp_test", "b": "inp_test", "c": "test"}

def test_too_deep():
    # Input list of dicts - happy path
    inp = {
        "a": "{{ b }}",
        "b": "{{ c }}",
        "c": "{{ d }}",
        "d": "{{ e }}",
        "e": "{{ f }}",
        "f": "{{ g }}"
    }

    # just the merge
    with pytest.raises(Exception):
        interpolate_values(inp)