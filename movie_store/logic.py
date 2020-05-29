import datetime


class FeeCalculator:

    def __init__(self, start_date: datetime.datetime,
                 end_date: datetime.datetime,
                 pricing: str="standard"):
        self._start_date = start_date
        self._end_date = end_date
        self._pricing = pricing

    def _standard_fee_calculator(self) -> float:
        diff = self._end_date - self._start_date
        days = diff.days

        fee = 0
        if days <= 2:
            # 2 days passed, count the current one (third) as well
            fee = (days + 1) * 1
        else:
            # 3 days passed, we are at the very least on the fourth
            fee = 3 * 1
            fee += 0.5 * (days - 3)

        return fee

    def calculate_fee(self) -> float:
        if self._pricing == "standard":
            return self._standard_fee_calculator()

        return self._standard_fee_calculator()
