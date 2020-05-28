import datetime


def calculate_fee(start_date: datetime.datetime, end_date: datetime.datetime) -> float:
    # TODO: make better :P
    print(start_date, end_date)

    diff = end_date - start_date

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