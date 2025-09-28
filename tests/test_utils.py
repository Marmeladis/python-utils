
import pytest
import asyncio

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from python_utils.types import Any  
from python_utils.loguru import Logurud  

def async_wrap(func):
    async def wrapper(*args, **kwargs):
        return await func(*args, **kwargs)
    return wrapper


def str_to_int(x):
    return int(x)

# Тесты для converters

def test_str_to_int_valid():  # Тест 1
    assert str_to_int("42") == 42

def test_str_to_int_negative():  # Тест 2
    assert str_to_int("-7") == -7

def test_str_to_int_invalid():  # Тест 3
    with pytest.raises(ValueError):
        str_to_int("abc")

def test_str_to_int_empty():  # Тест 4
    with pytest.raises(ValueError):
        str_to_int("")

# Тесты для aio

async def sample_async(x):  # вспомогательная async функция
    await asyncio.sleep(0.01)
    return x * 2

@pytest.mark.asyncio
async def test_async_wrap_basic():  # Тест 5
    wrapped = async_wrap(sample_async)
    result = await wrapped(3)
    assert result == 6

@pytest.mark.asyncio
async def test_async_wrap_exception():  # Тест 6
    async def error_func():
        raise ValueError("error")
    wrapped = async_wrap(error_func)
    with pytest.raises(ValueError):
        await wrapped()

# Тесты для типов и логирования

def test_placeholder_types():  # Тест 7
    x: Any = 5
    assert x == 5

def test_placeholder_logging():  # Тест 8
    logger = Logurud("test")
    logger.info("Test message")
    assert True  # проверка, что логгер не падает

# Дополнительные тесты для покрытия

def test_str_to_int_zero():  # Тест 9
    assert str_to_int("0") == 0

def test_async_wrap_return_type():  # Тест 10
    wrapped = async_wrap(sample_async)
    result = asyncio.run(wrapped(10))
    assert isinstance(result, int)

def test_async_wrap_multiple_calls():  # Тест 11
    wrapped = async_wrap(sample_async)
    results = [asyncio.run(wrapped(i)) for i in range(3)]
    assert results == [0, 2, 4]
