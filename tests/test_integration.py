import pytest
from python_utils import converters, formatters, decorators, logger, terminal, import_


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
def test_import_global_integration():
    mod = import_.import_global("math")
    assert hasattr(mod, "sqrt")
    with pytest.raises(import_.DummyError):
        import_.import_global("non_existing_module")

