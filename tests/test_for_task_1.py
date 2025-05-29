import pytest

from tasks.task1.task1 import strict


@strict
def add(a: int, b: int) -> int:
    return a + b

@strict
def greet(name: str, age: int) -> str:
    return f"Hi {name}! Are you really {age} years old?"

def test_correct_types():
    assert add(1, 2) == 3
    assert greet("Alex", 36) == "Hi Alex! Are you really 36 years old?"

def test_wrong_argument_types():
    with pytest.raises(ValueError):
        add(1, 2.0)
    with pytest.raises(ValueError):
        greet("Bob", "25")

def test_wrong_return_type():
    @strict
    def bad_func(x: int) -> str:
        return x
    with pytest.raises(ValueError):
        bad_func(10)
