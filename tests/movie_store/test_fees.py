from movie_store.logic.fees import FeeCalculator
from datetime import datetime
import pytest


standard_fee_cases = [
    [datetime(2020, 1, 1, 0, 0, 0), datetime(2020, 1, 1, 0, 0, 0), 0],
    [datetime(2020, 1, 1, 0, 0, 0), datetime(2020, 1, 1, 0, 0, 1), 1],
    [datetime(2020, 1, 1, 0, 0, 0), datetime(2020, 1, 2, 0, 0, 0), 1],
    [datetime(2020, 1, 1, 0, 0, 0), datetime(2020, 1, 3, 0, 0, 0), 2],
    [datetime(2020, 1, 1, 0, 0, 0), datetime(2020, 1, 3, 0, 0, 1), 3],
    [datetime(2020, 1, 1, 0, 0, 0), datetime(2020, 1, 4, 0, 0, 0), 3],
    [datetime(2020, 1, 1, 0, 0, 0), datetime(2020, 1, 4, 0, 0, 1), 3.5],
    [datetime(2020, 1, 1, 0, 0, 0), datetime(2020, 1, 5, 0, 0, 1), 4],
    [datetime(2020, 1, 1, 0, 0, 0), datetime(2020, 1, 10, 0, 0, ), 6],
]


@pytest.mark.parametrize(
    "start_date, end_date, result", standard_fee_cases
)
def test_standard_fee_calculation(start_date, end_date, result):
    calculator = FeeCalculator(start_date, end_date, pricing="standard")
    fee = calculator.calculate_fee()
    assert fee == result


def test_calculator_exception_on_invalid_range():
    start_date = datetime(2020, 1, 2)
    end_date = datetime(2020, 1, 1)

    exc = None
    try:
        calculator = FeeCalculator(start_date, end_date, pricing="standard")
    except Exception as e:
        exc = e
    assert exc is not None