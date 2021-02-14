from ecs_render.render import load_path


def test_simple_td():
    ivars = {
        "var": "PROD",
        "var2": "test2"
    }
    o = load_path('tests/task_definitions/simple.json.j2', ivars)
    assert o == [{'family': 'test', 'other': 'test2'}]


def test_simple2_td():
    ivars = {
        "var": "DEMO",
        "var2": "test2"
    }
    o = load_path('tests/task_definitions/simple.json.j2', ivars)
    assert o == [{'family': 'test'}]


def test_simple3_td():
    o = load_path('tests/task_definitions/simple.json.j2', {})
    assert o == [{'family': 'test'}]


def test_complex_deployment1():
    o = load_path('tests/task_definitions/complex1', {})    
    expected = [
        {'container_definition': [{'name': 'db', 'image': 'postgres:latest'}]},
        {'container_definition': [
            {'name': 'app', 'image': 'lejmr/image:latest', 'container_ports': ['4500:4500'], 'links': ['db']}]},
        {'task_role': 'arn:gfgf:gfdg:gg', 'volumes': [
            {'name': 'test1'}, {'name': 'test2'}]}
    ]

    assert len(o) == len(expected)
    assert all([x in expected for x in o])


def test_complex_deployment2():
    ivars = {
        "env": "PROD"
    }
    o = load_path('tests/task_definitions/complex1', ivars)
    expected = [
        {'container_definition': [
            {'name': 'app', 'image': 'lejmr/image:latest', 'container_ports': ['4500:4500']}]},
        {'task_role': 'arn:gfgf:gfdg:gg', 'volumes': [
            {'name': 'test1'}, {'name': 'test2'}]}
    ]

    assert len(o) == len(expected)
    assert all([x in expected for x in o])
