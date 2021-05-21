import os
from ecs_render.render import load_path
import pytest


# test on simple files
def test_non_existing():
    with pytest.raises(FileNotFoundError):
        load_path('tests/variables/env1')

def test_read_flat_file():
    v = load_path('tests/variables/env1.yml')
    assert v.__class__.__name__ == 'list'
    assert len(v) == 1
    assert v == [{"name": "vars"}]

def test_read_nonyaml_flat_file():
    with pytest.raises(Exception, match=r"^Not a loadable yaml format.*"):
        load_path('tests/variables/env1.noyml')

def test_read_json_file():
    v = load_path('tests/variables/test.json')
    assert v.__class__.__name__ == 'list'
    assert len(v) == 1
    assert v == [{"test": "value", "test1": "value2"}]
    
# Test on multiple files in 
def test_load_simple_dir():
    v = load_path('tests/variables/env2')
    assert v.__class__.__name__ == 'list'
    assert len(v) == 1
    assert v == [{'name': 'vars', 'version': 'milos'}]
        
def test_load_combined_dir():
    v = load_path('tests/variables/env3')
    assert v.__class__.__name__ == 'list'
    assert len(v) == 2

    # compare two list-dicts
    exp = [{'name': 'milos'}, {'image': 'v1'}]
    assert all([x in exp for x in v])
