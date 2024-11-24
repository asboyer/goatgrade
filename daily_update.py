import scrape
import json
import time
import os

from datetime import datetime

import info
import tools
import scrape_all_seasons
import grade

year = int(info.current_season["name"].split("-")[1])

write_file_path = "data/stat/league/{}.json"
player_stats_path = "data/stat/players/stats/{}.json"
standings_path = "data/team/standings/{}.json"
team_path = "data/team/teams/{}.json"
player_grades_path = "data/stat/players/grades/{}.json"
team_grades_path = "data/team/grades/{}.json"

date_string = tools.date_to_str(datetime.today())

def init_archive():
    if not os.path.exists(f"data/archive/{year}"):
        os.makedirs(f"data/archive/{year}")
        os.makedirs(f"data/archive/{year}/stat")
        os.makedirs(f"data/archive/{year}/stat/players")
        os.makedirs(f"data/archive/{year}/stat/players/grades")
        os.makedirs(f"data/archive/{year}/stat/players/stats")
        os.makedirs(f"data/archive/{year}/stat/league")
        os.makedirs(f"data/archive/{year}/team")
        os.makedirs(f"data/archive/{year}/team/grades")
        os.makedirs(f"data/archive/{year}/team/standings")
        os.makedirs(f"data/archive/{year}/team/teams")
    if not os.path.exists(f"data/archive/{year}/stat/players/results.json"):
        with open(f"data/archive/{year}/results.json", "w+", encoding="utf8") as file:
            file.write(json.dumps({}, ensure_ascii=False, indent=4))

def update_teams():
    for team in info.teams:
        t = scrape.scrape_team(team, year)
        with open(f"data/team/teams/{team}.json", "w+", encoding="utf8") as file:
            time.sleep(2.5)
            print(team)
            file.write(json.dumps(t, ensure_ascii=False, indent=4))
        with open(f"data/archive/{year}/team/teams/{team}.json", "w+", encoding="utf8") as file:
            time.sleep(2.5)
            file.write(json.dumps(t, ensure_ascii=False, indent=4))

def update_players():
    t = scrape.scrape_stats(year)
    with open(f"data/stat/players/stats/{date_string}.json", "w+", encoding="utf8") as file:
        file.write(json.dumps(t, ensure_ascii=False, indent=4))

    init_archive()

    with open(f"data/archive/{year}/stat/players/stats/{date_string}.json", "w+", encoding="utf8") as file:
        file.write(json.dumps(t, ensure_ascii=False, indent=4))

def update_standings():
    t = scrape.scrape_standings(year)
    with open(f"data/team/standings/{date_string}.json", "w+", encoding="utf8") as file:
        file.write(json.dumps(t, ensure_ascii=False, indent=4))

    with open(f"data/archive/{year}/team/standings/{date_string}.json", "w+", encoding="utf8") as file:
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
        if isinstance(players[player]["Team"], list):
            team = players[player]["Team"][-1]
        else:
            team = players[player]["Team"]
        data[team]["roster"].append(player)

    with open(f"data/stat/league/{date_string}.json", "w+", encoding="utf8") as file:
        file.write(json.dumps(data, ensure_ascii=False, indent=4))
    
    with open(f"data/archive/{year}/stat/league/{date_string}.json", "w+", encoding="utf8") as file:
        file.write(json.dumps(data, ensure_ascii=False, indent=4))

def update_grades_players():
    ranks = grade.grade_players(year, date_string)
    with open(player_grades_path.format(date_string), "w+", encoding="utf8") as file:
        file.write(json.dumps(ranks, ensure_ascii=False, indent=4))
    
    with open(f"data/archive/{year}/stat/players/grades/{date_string}.json", "w+", encoding="utf8") as file:
        file.write(json.dumps(ranks, ensure_ascii=False, indent=4))

def update_grades_teams():
    ranks = grade.grade_team(year, date_string)
    with open(team_grades_path.format(date_string), "w+", encoding="utf8") as file:
        file.write(json.dumps(ranks, ensure_ascii=False, indent=4))
    
    with open(f"data/archive/{year}/team/grades/{date_string}.json", "w+", encoding="utf8") as file:
        file.write(json.dumps(ranks, ensure_ascii=False, indent=4))

def update_upstream():
    tools.dump(f"data/archive/{year}/results.json", grade.soft_archive(str(year)))
    os.system("git add .")
    os.system("git commit -m 'daily update'")
    os.system("git push")

def clean_up():

    scrape_all_seasons.grade_season(year)

    grade.archive(str(year))
    

    for file in os.listdir("data/stat/league"):
        os.remove(f"data/stat/league/{file}")

    for file in os.listdir("data/stat/players/grades"):
        os.remove(f"data/stat/players/grades/{file}")

    for file in os.listdir("data/stat/players/stats"):
        os.remove(f"data/stat/players/stats/{file}")

    for file in os.listdir("data/team/standings"):
        os.remove(f"data/team/standings/{file}")

    for file in os.listdir("data/team/grades"):
        os.remove(f"data/team/grades/{file}")

if __name__ == "__main__":

    # ranks = grade.grade_players(2024, date_string)
    # with open(f"data/stat/players/grades/{date_string}.json", "w+", encoding="utf8") as file:
    #     file.write(json.dumps(ranks, ensure_ascii=False, indent=4))
    # update_internal_info()
    ranks = grade.grade_team(2024, "05_18_2024")
    with open(f"data/team/grades/05_18_2024.json", "w+", encoding="utf8") as file:
        file.write(json.dumps(ranks, ensure_ascii=False, indent=4))