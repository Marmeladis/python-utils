import pytest
from python_utils import converters, formatters, decorators, logger, terminal, import_


# 1. 
def test_to_int_integration():
    values = ["42", 0, 3.14, "100"]
    expected = [42, 0, 3, 100]
    result = [converters.to_int(v) for v in values]
    assert result == expected


# 2. 
def test_camel_to_underscore_integration():
    data = {"value": "camelCaseString", "nested": {"inner": "innerCamel"}}
    
    formatters.apply_recursive(data, lambda v: formatters.camel_to_underscore(v) if isinstance(v, str) else v)
    
    assert data["value"] == "camel_case_string"
    assert data["nested"]["inner"] == "inner_camel"



# 3. 
def test_listify_decorator_integration():
    @decorators.listify()
    def gen_numbers():
        for i in range(3):
            yield i
    result = gen_numbers()
    assert result == [0, 1, 2]


# 4. 
def test_logger_integration(caplog):
    log = logger.Logged()
    log.logger.info("Test message")
    assert "Test message" in caplog.text


# 5. 
def test_terminal_size_integration(monkeypatch):
    monkeypatch.setattr(terminal, "os", type("OsMock", (), {"get_terminal_size": lambda: (80, 24)})())
    width, height = terminal.get_terminal_size()
    assert width == 80 and height == 24


# 6. 
def test_import_global_integration():
    mod = import_.import_global("math")
    assert hasattr(mod, "sqrt")
    with pytest.raises(import_.DummyError):
        import_.import_global("non_existing_module")

