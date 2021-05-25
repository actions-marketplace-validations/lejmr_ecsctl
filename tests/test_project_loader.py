from ecs.project_loader import load_project_files, _find_td_ser, _find_values    
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