from datetime import datetime
from os import listdir
import argparse


calendars = []


def parse_to_time_stamp(date):
    return round(datetime.strptime(date, '%Y-%m-%d %H:%M:%S').timestamp())


def dates_parse(directory):
    for calendar in listdir(directory.replace("/", "")):
        if calendar.endswith('.txt') and calendar != "logs.txt":
            with open(
                "{}/{}".format(directory.replace("/", ""),
                               calendar), "r") as file:
                dates_list = file.read().split('\n')
            dates_list_dictionaries = []
            for date in dates_list:
                date = date.split(" - ")
                if len(date) == 2:
                    dates_list_dictionaries.append(
                        {
                            "begin_date": parse_to_time_stamp(date[0]),
                            "end_date": parse_to_time_stamp(date[1])
                        })
                else:
                    dates_list_dictionaries.append({
                        "begin_date": parse_to_time_stamp("{} 00:00:00".format(
                            date[0])),
                        "end_date": parse_to_time_stamp("{} 23:59:59".format(
                            date[0]))
                    })
            calendars.append(dates_list_dictionaries)
    all_dates = []
    for calendar in calendars:
        for date in calendar:
            all_dates.append(date)
    return calendars, all_dates


def date_unavailable(begin_date, end_date, minutes, proposed_date):
    minutes = int(minutes*60)
    if proposed_date > begin_date - minutes and proposed_date < end_date:
        return True
    else:
        return False


def find_soonest_date(
    directory, minutes, how_many_people,
        now=round(datetime.now().timestamp())):
    calendars, all_dates = dates_parse(directory)
    all_dates.append({"begin_date": now,
                     "end_date": now})
    all_dates = sorted(all_dates, key=lambda date: date["end_date"])
    for i in range(len(all_dates)):
        proposed_date = all_dates[i]["end_date"]
        if proposed_date < now:
            continue
        available = 0
        for calendar in calendars:
            calendar_ok = True
            for dates in calendar:
                begin_date = dates["begin_date"]
                end_date = dates["end_date"]
                if date_unavailable(
                        begin_date, end_date, minutes, proposed_date):
                    calendar_ok = False
                    break
            if calendar_ok:
                available = available + 1
                if available == int(how_many_people):
                    return datetime.fromtimestamp(proposed_date+1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--calendars', required=True, help="""
    name of the directory for the calendars""")
    parser.add_argument("--duration-in-minutes", required=True, help="""
    for how many minutes do people need to be available""")
    parser.add_argument("--minimum-people", required=True, help="""
    minimum amount of people needed to be available""")
    args = parser.parse_args()
    print(find_soonest_date(
        args.calendars, args.duration_in_minutes, args.minimum_people))
