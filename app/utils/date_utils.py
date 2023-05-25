import calendar
from datetime import datetime, date


def season_to_start_date(season_year):
    seasons = {
        'Spring': 3,
        'Summer': 6,
        'Autumn': 9,
        'Winter': 12
    }

    season, year = season_year.split()
    month = seasons.get(season.title())
    date_string = f'01.{month:02d}.{year}'
    return datetime.strptime(date_string, '%d.%m.%Y').date()


def season_to_end_date(season_year):
    seasons = {
        'Spring': 5,
        'Summer': 8,
        'Autumn': 11,
        'Winter': 2,
    }

    season, year = season_year.split()
    month = seasons.get(season.title())
    date_string = f'1.{month:02d}.{year}'
    date_obj = datetime.strptime(date_string, '%d.%m.%Y').date()

    year = date_obj.year
    month = date_obj.month
    _, last_day = calendar.monthrange(date_obj.year, date_obj.month)

    return date(year, month, last_day)


def decade_to_start_date(decade):
    decade_start = int(decade[:4])
    date_string = f'01.01.{decade_start}'
    return datetime.strptime(date_string, '%d.%m.%Y').date()


def decade_to_end_date(decade):
    decade_end = int(decade[:3])
    date_string = f'31.12.{decade_end}9'
    return datetime.strptime(date_string, '%d.%m.%Y').date()
