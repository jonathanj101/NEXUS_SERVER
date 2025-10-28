from django.utils import timezone


def date_formatted(date):
    print("helpers.date_formatted")
    print(type(date))
    # print(date)
    # print(timezone.localtime(date))
    new_date = timezone.localtime(date)
    is_pm = "pm" if new_date.hour > 12 else "am"
    year = new_date.year
    month = new_date.month
    day = new_date.day
    hour = standard_hour(new_date.hour)
    minutes = new_date.minute
    sec = new_date.second

    return f"{month}/{day}/{year} at {hour}:{minutes}:{sec} {is_pm}"


# 12 or 1 or 3
def standard_hour(hour):
    print("helpers.standard_hour")

    return int(hour) - 12 if int(hour) > 12 else int(hour)
