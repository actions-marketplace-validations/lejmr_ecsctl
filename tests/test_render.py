from ecs_render.render import render


def test_simple_render():
    # task definition
    td = {
        "version": "latest",
        "task_name": "name_{{ var1 }}"
    }
    # Variable definition
    vars = {
        "var1": "value1"
    }

    # The render
    r = render(td,vars)

    # Asserts
    assert r == {"version": "latest", "task_name": "name_value1"}

def test_nested_case1():
    # task definition
    td = {
        "version": "latest",
        "task_name": "name_{{ var1 }}"
    }
    # Variable definition
    vars = {
        "var1": "{{ var2 }}",
        "var2": "value1"
    }

    # The render
    r = render(td,vars)

    # Asserts
    assert r == {"version": "latest", "task_name": "name_value1"}
