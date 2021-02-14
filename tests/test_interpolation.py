from ecs_render.render import interpolate_values


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
