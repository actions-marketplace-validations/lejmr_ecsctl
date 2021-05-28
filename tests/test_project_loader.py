from ecs.project_loader import load_project_files, _find_td_ser, _find_values, _load_and_interpolate_values, load_output
from ecs.exceptions import InvalidProjectStructure, InvalidInputFiles
import pytest
import os


### Loaders
def test_find_td1():
    with pytest.raises(FileNotFoundError):
        _find_td_ser('tests/projects/')

def test_find_td2():
    p = 'tests/projects/proj1'
    assert _find_td_ser(p) == os.path.join(p, 'task-definition.yml')

def test_find_td3():
    p = 'tests/projects/proj2'
    assert _find_td_ser(p) == os.path.join(p, 'task-definition.yml')

def test_find_td4():
    p = 'tests/projects/proj3'
    assert _find_td_ser(p) == os.path.join(p, 'task-definition/')

def test_find_values1():
    with pytest.raises(FileNotFoundError):
        _find_values('tests/projects/')

def test_find_values2():
    p = 'tests/projects/proj1'
    assert _find_values(p) == [os.path.join(p, "values.yml")]

def test_find_values3():
    p = 'tests/projects/proj2'
    assert _find_values(p) == [os.path.join(p, "values.yaml")]

def test_find_values4():
    p = 'tests/projects/proj3'
    assert _find_values(p) == [os.path.join(p, "values/default.json")]

def test_load_project1():
    with pytest.raises(InvalidProjectStructure):
        load_project_files('tests/projects/')

def test_load_project2():
    load_project_files('tests/projects/proj1')

def test_load_project3():
    p = 'tests/projects/proj1'
    with pytest.raises(InvalidInputFiles):
        load_project_files(p,
            [os.path.join(p, 'values.json')])

def test_load_project4():
    p = 'tests/projects/proj1'
    load_project_files(p, [os.path.join(p, 'values.yml')])

def test_load_project5():
    p = 'tests/projects/proj4'
    with pytest.raises(InvalidProjectStructure):
        load_project_files(p)

# values management
def test_load_variables_default():
    vals = _load_and_interpolate_values(['tests/projects/proj1/values.yml'], {})
    assert vals == {'environment': 'dev', 'sn': 'test-service'}

def test_load_variables_default2():
    vals = _load_and_interpolate_values([
        'tests/projects/proj1/values.yml',
        'tests/projects/proj2/values.yaml'], {})
    assert vals == {'environment': 'dev', 'sn': 'test-service', 'proj2_environment': 'dev'}


def test_load_variables_override():
    vals = _load_and_interpolate_values(['tests/projects/proj1/values.yml'], {"environment": "test"})
    assert vals == {'environment': 'test', 'sn': 'test-service'}

def test_load_variables_override2():
    vals = _load_and_interpolate_values([
        'tests/projects/proj1/values.yml',
        'tests/projects/proj2/values.yaml'], {"environment": "test"})
    assert vals == {'environment': 'test', 'sn': 'test-service', 'proj2_environment': 'test'}

# Test outputing mechanism
def test_output_is_loaded():
    p = 'tests/projects/proj1'
    a = load_output(p, [os.path.join(p, 'values.yml')], {})
    assert a == "<b>Service</b> test-service <br />\n<b>Environmnet</b> dev"

def test_output_is_loaded2():
    p = 'tests/projects/proj1'
    a = load_output(p, [os.path.join(p, 'values.yml')], {"environment": "test"})
    assert a == "<b>Service</b> test-service <br />\n<b>Environmnet</b> test"

