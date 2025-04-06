from unittest.mock import patch

import pytest

from decayculator.core.calculator import Calculator
from decayculator.core.models import DecayingNumber


@pytest.fixture
def calculator() -> Calculator:
    return Calculator()


def test_simple_addition(calculator):
    result = calculator.evaluate("2 + 3")
    assert isinstance(result, DecayingNumber)
    assert 4.0 < result.read() < 6.0  # Allow for a bit of noise


def test_operator_precedence(calculator):
    result = calculator.evaluate("2 + 3 * 4")  # 2 + 12 = 14
    val = result.read()
    assert 13.0 < val < 15.0


def test_negative_number(calculator):
    result = calculator.evaluate("-7")
    val = result.read()
    assert -8 < val < -6


def test_expression_with_parentheses(calculator):
    result = calculator.evaluate("(2 + 3) * 4")  # 5 * 4 = 20
    val = result.read()
    assert 18.0 < val < 22.0


def test_invalid_expression_raises(calculator):
    with pytest.raises(ValueError):
        calculator.evaluate("2 + unknown_var")


def test_entropy_accumulates_over_time(calculator):
    with patch("decayculator.core.models.time") as mock_time:
        mock_time.time.return_value = 100.0
        result = calculator.evaluate("5 + 5")

        mock_time.time.return_value = 100.0
        early = result.read()

        mock_time.time.return_value = 110.0
        late = result.read()

        assert early != late  # Noisy values drift with time
