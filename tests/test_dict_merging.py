from ecs_render.render import merge_dicts


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

