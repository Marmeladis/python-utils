import pytest
import asyncio
from python_utils.aio import async_wrap
from python_utils.converters import str_to_int
from python_utils.decorators import ensure_positive
from python_utils.time import measure_time
from python_utils.generators import number_generator

# 1. Тест асинхронной функции
@pytest.mark.asyncio
async def test_async_wrap():
    async def sample(x):
        return x + 1
    wrapped = async_wrap(sample)
    result = await wrapped(2)
    assert result == 3

# 2. Тест конвертера
def test_str_to_int():
    assert str_to_int("123") == 123
    with pytest.raises(ValueError):
        str_to_int("abc")

# 3. Тест декоратора ensure_positive
@ensure_positive
def square(x):
    return x*x

def test_ensure_positive():
    assert square(3) == 9
    with pytest.raises(ValueError):
        square(-1)

# 4. Тест генератора чисел
def test_number_generator():
    gen = number_generator(1, 3)
    assert list(gen) == [1,2,3]

# 5. Тест measure_time
def test_measure_time():
    @measure_time
    def fast():
        return 5
    result, elapsed = fast()
    assert result == 5
    assert elapsed >= 0
