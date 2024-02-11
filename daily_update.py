import scrape
import json
import time
import os

from datetime import datetime

import info
import tools
import grade

year = 2024

write_file_path = "data/stat/league/{}.json"
player_stats_path = "data/stat/players/stats/{}.json"
standings_path = "data/team/standings/{}.json"
team_path = "data/team/teams/{}.json"
player_grades_path = "data/stat/players/grades/{}.json"
team_grades_path = "data/team/grades/{}.json"

date_string = tools.date_to_str(datetime.today())

def update_teams():
    for team in info.teams:
        t = scrape.scrape_team(team, year)
        with open(f"data/team/teams/{team}.json", "w+", encoding="utf8") as file:
            time.sleep(5)
            print(team)
            file.write(json.dumps(t, ensure_ascii=False, indent=4))

def update_players():
    t = scrape.scrape_stats(year)
    with open(f"data/stat/players/stats/{date_string}.json", "w+", encoding="utf8") as file:
        file.write(json.dumps(t, ensure_ascii=False, indent=4))

def update_standings():
    t = scrape.scrape_standings(year)
    with open(f"data/team/standings/{date_string}.json", "w+", encoding="utf8") as file:
        file.write(json.dumps(t, ensure_ascii=False, indent=4))

def update_internal_info():
    data = {}

    f = open(standings_path.format(date_string), 'r')
    standings = json.load(f)
    f.close()
    for team in standings:
        data[team] = {}
        data[team]["standings"] = standings[team]
        data[team]["img"] = standings[team]["img"]
        del data[team]["standings"]["img"]
        del data[team]["standings"]["link"]  
        data[team]["roster"] = []

    for team in info.teams:
        f = open(team_path.format(team), 'r')
        t = json.load(f)
        f.close()

        data[team]["stats"] = t[team]["team_stats"]
        data[team]["info"] = t[team]["info"]
        data[team]["last_update"] = t[team]["last_update"]

    f = open(player_stats_path.format(date_string), 'r')
    players = json.load(f)
    f.close()

    for player in players:
        if isinstance(players[player]["Tm"], list):
            team = players[player]["Tm"][-1]
        else:
            team = players[player]["Tm"]
        data[team]["roster"].append(player)

    with open(f"data/stat/league/{date_string}.json", "w+", encoding="utf8") as file:
        file.write(json.dumps(data, ensure_ascii=False, indent=4))

def update_grades_players():
    ranks = grade.grade_players(year, date_string)
    with open(player_grades_path.format(date_string), "w+", encoding="utf8") as file:
        file.write(json.dumps(ranks, ensure_ascii=False, indent=4))

def update_grades_teams():
    ranks = grade.grade_team(year, date_string)
    with open(team_grades_path.format(date_string), "w+", encoding="utf8") as file:
        file.write(json.dumps(ranks, ensure_ascii=False, indent=4))


if __name__ == "__main__":

    # ranks = grade.grade_players(2024, date_string)
    # with open(f"data/stat/players/grades/{date_string}.json", "w+", encoding="utf8") as file:
    #     file.write(json.dumps(ranks, ensure_ascii=False, indent=4))
    # update_internal_info()
    ranks = grade.grade_team(2024, date_string)
    with open(f"data/team/grades/{date_string}.json", "w+", encoding="utf8") as file:
        file.write(json.dumps(ranks, ensure_ascii=False, indent=4))