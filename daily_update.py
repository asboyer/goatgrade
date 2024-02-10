import scrape
import json
import time
import os

from datetime import datetime

import info
import tools

year = 2024

def update_teams():
    for team in info.teams:
        t = scrape.scrape_team(team, year)
        with open(f"data/team/teams/{team}.json", "w+", encoding="utf8") as file:
            time.sleep(5)
            file.write(json.dumps(t, ensure_ascii=False, indent=4))

def update_players():
    t = scrape.scrape_stats(year)
    with open(f"data/stat/players/stats/{tools.date_to_str(datetime.today())}.json", "w+", encoding="utf8") as file:
        file.write(json.dumps(t, ensure_ascii=False, indent=4))

def update_standings():
    t = scrape.scrape_standings(year)
    with open(f"data/team/standings/{tools.date_to_str(datetime.today())}.json", "w+", encoding="utf8") as file:
        file.write(json.dumps(t, ensure_ascii=False, indent=4))

def update_internal_info():
    

if __name__ == "__main__":
    update_standings()