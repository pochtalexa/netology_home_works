import time
from datetime import datetime
import random

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']


def function_logger_out(path_to_log: str):
    def function_logger_in(func):
        def input_func(*args, **kwargs):
            result = func(*args, **kwargs)

            with open(path_to_log, 'a', encoding='utf-8') as f:
                f.write(f'{datetime.now()}; {func.__name__}; {args}; {kwargs}; {result}\n')

            print(f'log: {datetime.now()} {func.__name__} {args} {kwargs} {result}')
            return result

        return input_func

    return function_logger_in


@function_logger_out('decorator.log')
def check_diff(month_day: int, month: str, year: int):
    current_date = datetime.now()
    input_date = datetime.strptime(f'{month_day} {month} {year}', '%d %B %Y')
    diff_in_days = (current_date - input_date).days
    print(f'input_date: {input_date.strftime("%d-%m-%Y")}, diff with now(): {diff_in_days} days')
    return diff_in_days


def main():
    start = datetime.now()

    while True:
        month = MONTHS[random.randint(0, 11)]

        if month == 'February':
            month_day = random.randint(1, 28)
        else:
            month_day = random.randint(1, 30)

        year = random.randint(2000, 2030)

        check_diff(month_day, month, year=year)
        time.sleep(1)

        if (datetime.now() - start).seconds > 10:
            break


if __name__ == '__main__':
    main()
