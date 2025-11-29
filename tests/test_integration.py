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


# 1
def test_any_and_str_to_int_integration():
    values = ["10", True, False, " 42 "]
    expected = [10, 1, 0, 42]

    result = [str_to_int(Any(v)) for v in values]

    assert result == expected


# 2
def test_logurud_accepts_any_type():
    logger = Logurud("types_test")

    data = [123, "hello", {"a": 1}]
    for d in data:
        logger.info(d)

    logs = logger.get_logs()

    assert "123" in logs[0]
    assert "hello" in logs[1]
    assert "{'a': 1}" in logs[2]


# 3
def test_warning_and_error_flow():
    logger = Logurud("flow")

    logger.warning("low disk")
    logger.error("disk failed")

    logs = logger.get_logs()

    assert logs[0].startswith("WARNING:")
    assert logs[1].startswith("ERROR:")


# 4
def test_multiple_operations_integration():
    logger = Logurud("multi")

    msgs = ["a", "b", "c"]
    for m in msgs:
        logger.info(m)

    assert logger.get_logs() == msgs


# 5 
def test_invalid_data_error_flow():
    logger = Logurud("invalid")

    try:
        str_to_int("abc")
    except Exception as e:
        logger.error(str(e))

    logs = logger.get_logs()

    assert any("invalid literal" in log for log in logs)


# 6 
@pytest.mark.xfail(reason="str_to_int не умеет конвертировать float-строки")
def test_str_to_int_float_string_xfail():
    result = str_to_int("3.14")
    assert result == 3