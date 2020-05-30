import datetime


class FeeCalculator:

    def __init__(self, start_date: datetime.datetime,
                 end_date: datetime.datetime,
                 pricing: str="standard"):
        """
        FeeCalculator - calculates fee of a rental
        :param start_date: rental date - UTC time
        :param end_date: rental return date - UTC time
        :param pricing: pricing strategy
        """
        self._start_date = start_date
        self._end_date = end_date
        self._pricing = pricing

        if self._start_date > self._end_date:
            raise Exception("Start date cannot be later than end date")

    def _standard_fee_calculator(self) -> float:
        day_pricing = 1
        after_threshold_day_pricing = 0.5
        days_threshold = 3


        diff = self._end_date - self._start_date
        seconds = diff.total_seconds()
        seconds_in_day = 60*60*24

        days = int(seconds / seconds_in_day)
        remainder = seconds % seconds_in_day

        if remainder != 0:
            days += 1

        fee = 0
        if days <= days_threshold:
            fee = days * day_pricing
        else:
            fee = days_threshold * day_pricing
            fee += after_threshold_day_pricing * (days - days_threshold)

        return fee

    def calculate_fee(self) -> float:
        if self._pricing == "standard":
            return self._standard_fee_calculator()

        return self._standard_fee_calculator()
