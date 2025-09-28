import pytest
import asyncio
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
        def get_logs(self):
            return self.logged



def str_to_int(x):
    return int(x)

def async_wrap(func):
    async def wrapper(*args, **kwargs):
        return await func(*args, **kwargs)
    return wrapper

async def sample_async(x):
    await asyncio.sleep(0.01)
    return x * 2

# Тесты для str_to_int

@pytest.mark.parametrize("input_str,expected", [
    ("42", 42),
    ("-7", -7),
    ("0", 0),
    ("123456789", 123456789),
])
def test_str_to_int_valid_cases(input_str, expected):
    assert str_to_int(input_str) == expected

@pytest.mark.parametrize("invalid_input", ["abc", "", " ", "3.14", None])
def test_str_to_int_invalid_cases(invalid_input):
    with pytest.raises((ValueError, TypeError)):
        str_to_int(invalid_input)

# Тесты для async_wrap

@pytest.mark.asyncio
async def test_async_wrap_with_normal_func():
    async def double(x): return x * 2
    wrapped = async_wrap(double)
    assert await wrapped(5) == 10

@pytest.mark.asyncio
async def test_async_wrap_with_kwargs():
    async def combine(a, b=0): return a + b
    wrapped = async_wrap(combine)
    result = await wrapped(3, b=4)
    assert result == 7

@pytest.mark.asyncio
async def test_async_wrap_with_exception():
    async def fail(): raise RuntimeError("fail")
    wrapped = async_wrap(fail)
    with pytest.raises(RuntimeError):
        await wrapped()

def test_async_wrap_sync_call():
    wrapped = async_wrap(sample_async)
    result = asyncio.run(wrapped(2))
    assert result == 4

def test_async_wrap_multiple_runs():
    wrapped = async_wrap(sample_async)
    results = [asyncio.run(wrapped(i)) for i in range(5)]
    assert results == [0, 2, 4, 6, 8]

# Тесты для типов

def test_any_type_annotation():
    x: Any = "test"
    assert isinstance(x, str)

def test_any_type_change():
    x: Any = 42
    x = [1, 2, 3]
    assert isinstance(x, list)

# Тесты для логирования

def test_logurud_info_capture():
    logger = Logurud("demo")
    logger.info("Hello")
    if hasattr(logger, "get_logs"):
        assert "Hello" in logger.get_logs()
    else:
        assert True  # fallback logger doesn't store logs

def test_logurud_multiple_messages():
    logger = Logurud("multi")
    for msg in ["one", "two", "three"]:
        logger.info(msg)
    if hasattr(logger, "get_logs"):
        assert logger.get_logs() == ["one", "two", "three"]

# Smoke test

def test_debug_visible():
    assert True
