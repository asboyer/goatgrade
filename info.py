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

current_season = {
    "name": "2023-2024",
    "start_day": "10-24-2023",
    "end_day": "4-14-2024",
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
    end_day = int(current_season["end_day"].split("-")[1])
    end_month = int(current_season["end_day"].split("-")[0])

    if in_early_season and (current_month == start_month and current_day < start_day):
        return False
    if in_late_season and (current_month == end_month and current_day > end_day):
        return False

    return in_season and (in_early_season or in_late_season)

if __name__ == "__main__":
    print(in_season())