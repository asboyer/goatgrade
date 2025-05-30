from datetime import datetime

teams = [
        'ATL',
        'BOS',
        'BRK',
        'CHI',
        'CHO',
        'CLE',
        'DAL',
        'DEN',
        'DET',
        'GSW',
        'HOU',
        'IND',
        'LAC',
        'LAL',
        'MEM',
        'MIA',
        'MIL',
        'MIN',
        'NOP',
        'NYK',
        'OKC',
        'ORL',
        'PHI',
        'PHO',
        'POR',
        'SAC',
        'SAS',
        'TOR',
        'UTA',
        'WAS'
        ]

seasons = [
    1956,
    1957,
    1958,
    1959,
    1960,
    1961,
    1962,
    1963,
    1964,
    1965,
    1966,
    1967,
    1968,
    1969,
    1970,
    1971,
    1972,
    1973,
    1974,
    1975,
    1976,
    1977,
    1978,
    1979,
    1980,
    1981,
    1982,
    1983,
    1984,
    1985,
    1986,
    1987,
    1988,
    1989,
    1990,
    1991,
    1992,
    1993,
    1994,
    1995,
    1996,
    1997,
    1998,
    1999,
    2000,
    2001,
    2002,
    2003,
    2004,
    2005,
    2006,
    2007,
    2008,
    2009,
    2010,
    2011,
    2012,
    2013,
    2014,
    2015,
    2016,
    2017,
    2018,
    2019,
    2020,
    2021,
    2022,
    2023,
    2024
]

archived_seasons = [
    "2024",
    "2025"
]

current_season = {
    "name": "2024-2025",
    "start_day": "10-24-2024",
    "end_day": "04-14-2025",
}

def get_season_months(start_day, end_day):
    start_date = datetime.strptime(start_day, "%m-%d-%Y")
    end_date = datetime.strptime(end_day, "%m-%d-%Y")

    months_earlier_year = []
    months_later_year = []
    current_date = start_date

    while current_date < end_date:
        if current_date.year == start_date.year and current_date.month not in months_earlier_year:
            months_earlier_year.append(current_date.month)
        elif current_date.year == end_date.year and current_date.month not in months_later_year:
            months_later_year.append(current_date.month)
        current_date = add_months(current_date, 1)

    if end_date.month not in months_later_year:
        months_later_year.append(end_date.month)

    return months_earlier_year, months_later_year

def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    return datetime(year, month, 1)

def in_season():
    today = datetime.today()
    start_date = datetime.strptime(current_season["start_day"], "%m-%d-%Y")
    end_date = datetime.strptime(current_season["end_day"], "%m-%d-%Y")

    return start_date <= today <= end_date

# write a function that returns the percentage of the season that has passed
def season_percentage():
    today = datetime.today()
    current_year = today.year
    current_month = today.month
    current_day = today.day

    early_season_months, late_season_moths = get_season_months(current_season["start_day"], current_season["end_day"])
    nba_season_months = early_season_months + late_season_moths
    season_year = int(current_season["name"].split("-")[1])

    in_season = current_month in nba_season_months
    in_early_season = current_month in early_season_months and current_year + 1 == season_year
    in_late_season = current_month in late_season_moths and current_year == season_year

    start_day = int(current_season["start_day"].split("-")[1])
    start_month = int(current_season["start_day"].split("-")[0])
    start_year = int(current_season["start_day"].split("-")[2])
    end_day = int(current_season["end_day"].split("-")[1])
    end_month = int(current_season["end_day"].split("-")[0])
    end_year = int(current_season["end_day"].split("-")[2])

    if in_early_season and (current_month == start_month and current_day < start_day):
        return 0
    if in_late_season and (current_month == end_month and current_day > end_day):
        return 1.0

    start_date = datetime(start_year, start_month, start_day)

    end_date = datetime(end_year, end_month, end_day)

    total_days = (end_date - start_date).days
    days_passed = (today - start_date).days
    return round((days_passed / total_days), 2)

if __name__ == "__main__":
    print(in_season())
    print(season_percentage())