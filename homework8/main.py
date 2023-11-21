from datetime import datetime, timedelta, date


def calc_current_period(current_date):
    end_period = current_date + timedelta(days=7)
    return current_date, end_period


def update_birthday(birthday, current_date):
    year_now = current_date.year
    birthday_year_now = birthday.replace(year = year_now)
    if birthday_year_now < current_date:
        return birthday.replace(year = year_now+1)
    else:
        return birthday_year_now


def get_birthdays_per_week(users):
    birthdays = {}
    current_date = date.today()
    start_period, end_period = calc_current_period(current_date)
    users_to_congratulate = []
    for user in users:
        birthday = update_birthday(user['birthday'], current_date)
        if start_period <= birthday <= end_period:
            users_to_congratulate.append(user)
    if not users_to_congratulate:
        print('No users to congratulate')
        return {}
    for user in users_to_congratulate:
        current_birthday = update_birthday(user['birthday'], current_date)
        day_of_the_week = current_birthday.strftime('%A')
        if day_of_the_week in ('Saturday','Sunday'):
            day_of_the_week = 'Monday'
        birthdays[day_of_the_week] = birthdays.get(day_of_the_week, [])
        birthdays[day_of_the_week].append(user['name'])
    return birthdays


if __name__ == "__main__":
    users = [
        {"name": "Jan Koum", "birthday": datetime(1976, 1, 1).date()},
    ]

    result = get_birthdays_per_week(users)
    print(result)
    # Виводимо результат
    for day_name, names in result.items():
        print(f"{day_name}: {', '.join(names)}")
