from ecs.render import merge_dicts
import pytest


def test_simple_merge():
    # Input list of dicts - happy path
    inp = [
        {"a": "b"},
        {"b": "c", "c": "d"},
        {"c": "override"}
    ]

    # just the merge
    m = merge_dicts(inp)
    print(m)
    assert m == {"a": "b", "b": "c", "c": "override"}


def test_null_input():
    # Input list of dicts - happy path
    inp = []

    # just the merge
    m = merge_dicts(inp)
    assert m == {}


def test_one_dict():
    # Input list of dicts - happy path
    inp = [{"a": "b"}]

    # just the merge
    m = merge_dicts(inp)
    assert m == {"a": "b"}

def test_nested1():
    # Input list of dicts - happy path
    inp = [
        {
            "a": "b",
            "b": [{"name": "test1", "family": "family1"}]
        },
        {
            "b": [{"name": "test2", "family": "family2"}],
            "a": "b"
        }
    ]

    # just the merge
    m = merge_dicts(inp)
    assert m == {
        "a": "b",
        "b": [
            {"name": "test1", "family": "family1"},
            {"name": "test2", "family": "family2"}
        ]
    }


def test_nested2():
    # Input list of dicts - happy path
    inp = [
        {
            "a": "b",
            "b": [{"name": "test1", "family": "family1"}],
            "c": 1,
            "d": 0.5
        },
        {
            "b": [{"name": "test2", "family": "family2"}],
            "a": "b",
            "c": 5
        }
    ]

    # just the merge
    m = merge_dicts(inp)
    assert m == {
        "a": "b",
        "b": [
            {"name": "test1", "family": "family1"},
            {"name": "test2", "family": "family2"}
        ],
        "c": 5,
        "d": 0.5
    }

def test_same_values():
    # Input list of dicts - happy path
    inp = [{"a": "b"}, {"a": "b"}]

    # just the merge
    m = merge_dicts(inp)
    assert m == {"a": "b"}

def test_type_conflict():
    # Input list of dicts - happy path
    inp = [{"a": "b"}, {"a": ["b"]}]

    # just the merge
    with pytest.raises(Exception, match=r'^Conflict at'):
        m = merge_dicts(inp)
    
def test_nested_dicts():
    # Input list of dicts - happy path
    inp = [ 
        {"a": {
            "c": "d",
            "e": "f"
            }
        }, 
        {"a": 
            {
                "f": "g",
                "c": "e"
            }
        }
    ]

    # just the merge
    m = merge_dicts(inp)
    assert m == {"a": {
        "c": "e",
        "e": "f",
        "f": "g"
    }}