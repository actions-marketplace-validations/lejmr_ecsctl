from ecs.helper import parse_value_override

def test_read_argument1():
    assert {"var":"val"} == parse_value_override("   var=val   ")