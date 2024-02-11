# scrape
    # scrape_player
    # scrape_stats
    # scrape_team

# grade
    # grade_player
    # grade_team

# daily_update
    # update_teams
    # update_players
    # grade_teams
    # grade_players

import daily_update, grade

update_players()
update_standings()
update_teams()

update_internal_info()

ranks = grade.grade_players(2024, date_string)
with open(f"data/stat/players/grades/{date_string}.json", "w+", encoding="utf8") as file:
    file.write(json.dumps(ranks, ensure_ascii=False, indent=4))
    
ranks = grade.grade_team(2024, date_string)
with open(f"data/team/grades/{date_string}.json", "w+", encoding="utf8") as file:
    file.write(json.dumps(ranks, ensure_ascii=False, indent=4))