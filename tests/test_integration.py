import pytest
from python_utils import converters, formatters, decorators, logger, terminal, import_
from python_utils import import_
from python_utils import converters


# 1. 
def test_to_int_integration():
    values = ["42", 0, 3.14, "100"]
    expected = [42, 0, 3, 100]
    result = [converters.to_int(v) for v in values]
    assert result == expected

# 2. 
def test_listify_decorator_integration():
    @decorators.listify()
    def gen_numbers():
        for i in range(3):
            yield i
    result = gen_numbers()
    assert result == [0, 1, 2]


# 3. 
def test_logger_integration(caplog):
    log = logger.Logged()
    with caplog.at_level("INFO", logger=log.logger.name):
        log.logger.info("Test message")
    assert "Test message" in caplog.text


# 4. 
def test_terminal_size_integration():
    width, height = terminal.get_terminal_size()
    assert isinstance(width, int) and isinstance(height, int)
    assert width > 0 and height > 0


# 5.
def test_to_int_integration_error():
    invalid_values = ["abc", None, {}]

    for val in invalid_values:
        with pytest.raises((ValueError, TypeError)):
            converters.to_int(val)

# 6.
def test_to_int_boundary_integration():
    boundary_values = [
        0,
        -1,
        2**63 - 1,
        -(2**63),
        "  42  ",
        "000123",
    ]

    expected = [
        0,
        -1,
        2**63 - 1,
        -(2**63),
        42,
        123,
    ]

    result = [converters.to_int(v) for v in boundary_values]
    assert result == expected


