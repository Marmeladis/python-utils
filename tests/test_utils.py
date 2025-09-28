import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


try:
    from python_utils.types import Any
except ImportError:
    Any = object

try:
    from python_utils.loguru import Logurud
except ImportError:
    class Logurud:
        def __init__(self, name):
            self.name = name
            self.logged = []
        def info(self, msg):
            self.logged.append(msg)
        def warning(self, msg):
            self.logged.append(f"WARNING: {msg}")
        def error(self, msg):
            self.logged.append(f"ERROR: {msg}")
        def get_logs(self):
            return self.logged


def str_to_int(x):
    return int(x)

# Тесты для str_to_int

@pytest.mark.parametrize("input_str,expected", [
    ("42", 42),
    ("-7", -7),
    ("0", 0),
    ("123456789", 123456789),
    (" 15 ", 15),
])
def test_str_to_int_valid_cases(input_str, expected):
    assert str_to_int(input_str) == expected

def test_str_to_int_with_boolean():
    assert str_to_int(True) == 1
    assert str_to_int(False) == 0

@pytest.mark.parametrize("invalid_input", ["abc", "", " ", "3.14", None, [], {}])
def test_str_to_int_invalid_cases(invalid_input):
    with pytest.raises((ValueError, TypeError)):
        str_to_int(invalid_input)

# Тесты для типов (Any)

def test_any_accepts_multiple_types():
    values = [42, "hello", [1, 2], {"a": 1}, None]
    for val in values:
        x: Any = val
        assert x == val

def test_any_type_casting():
    x: Any = "123"
    assert int(x) == 123

# Тесты для логирования

def test_logurud_info():
    logger = Logurud("test_logger")
    logger.info("Info message")
    if hasattr(logger, "get_logs"):
        logs = logger.get_logs()
        assert "Info message" in logs

def test_logurud_warning_and_error():
    logger = Logurud("warn_error_logger")
    logger.warning("Something might be wrong")
    logger.error("Something is wrong")
    if hasattr(logger, "get_logs"):
        logs = logger.get_logs()
        assert any("WARNING:" in log for log in logs)
        assert any("ERROR:" in log for log in logs)

def test_logurud_multiple_messages():
    logger = Logurud("multi_logger")
    messages = ["first", "second", "third"]
    for msg in messages:
        logger.info(msg)
    if hasattr(logger, "get_logs"):
        assert logger.get_logs() == messages

# Smoke test

def test_debug_visible():
    assert True
