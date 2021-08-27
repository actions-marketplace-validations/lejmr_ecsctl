from ecs.helper import parse_value_override, format_flyway

def test_read_argument1():
    assert {"var":"val"} == parse_value_override("   var=val   ")

def test_flyway_formater1():
    a = {
        "flyway": {
            "a": 1,
            "b": 2
        }
    }
    assert format_flyway(a).split('\n') == ["flyway.a = 1", "flyway.b = 2"]


def test_flyway_formater2():
    a = {
        "flyway": {
            "a": 1,
            "b": {
                "c": 5,
                "d": 56
            }
        }
    }
    assert format_flyway(a).split('\n') == ["flyway.a = 1", "flyway.b.c = 5", "flyway.b.d = 56"]