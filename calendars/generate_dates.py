import random
from datetime import datetime


begin_date_timestamp = datetime.strptime(
    '30-05-22 10:03:45', '%d-%m-%y %H:%M:%S').timestamp()
end_date_timestamp = datetime.strptime(
    '01-08-22 10:03:45', '%d-%m-%y %H:%M:%S').timestamp()
dates = []


def generate_dates(single, FROM_TO):
    dates = ""
    for i in range(single):
        dates = dates + "{}\n".format(datetime.fromtimestamp(
            round(random.uniform(begin_date_timestamp, end_date_timestamp))
        ).strftime('%Y-%m-%d'))
    for i in range(FROM_TO):
        date_FROM_timestamp = round(random.uniform(
            begin_date_timestamp, end_date_timestamp))
        date_TO_timestamp = date_FROM_timestamp + \
            round(random.uniform(1800, 14400))
        dates = dates + "{} - {}\n".format(datetime.fromtimestamp(
            date_FROM_timestamp), datetime.fromtimestamp(date_TO_timestamp))
    return dates[:-1]


if __name__ == "__main__":
    try:
        for i in range(1, 10):
            with open('calendars/person{}.txt'.format(i), 'w', encoding="UTF-8") as file:
                file.write(generate_dates(
                    random.randint(0, 10), random.randint(0, 10)))
        print("Succesfully generated dates.")
    except Exception as e:
        with open('calendars/logs.txt', 'w', encoding="UTF-8") as file:
            file.write(str(e))
        print("Error! Check logs.txt for more info.")
