import scrape
import info
import json

import time

year = 2024

def update_teams():
    for team in info.teams[15:]:
        t = scrape.scrape_team(team, year)
        with open(f"data/team/teams/{team}.json", "w+", encoding="utf8") as file:
            time.sleep(5)
            file.write(json.dumps(t, ensure_ascii=False, indent=4))

def update_players():
    t = scrape.scrape_stats(year)
    with open(f"data/stat/players/stats/stats.json", "w+", encoding="utf8") as file:
        file.write(json.dumps(t, ensure_ascii=False, indent=4))

if __name__ == "__main__":
    update_teams()