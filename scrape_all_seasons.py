import json, time, os
import scrape, info, tools, grade

player_stats_path = "data/seasons/{}/players/stats.json"
player_grades_path = "data/seasons/{}/players/grades.json"

teams_path = "data/seasons/{}/teams/{}.json"
team_grades_path = "data/seasons/{}/teams/grades.json"

info_path = "data/seasons/{}/info.json"
standings_path = "data/seasons/{}/league/standings.json"
league_path = "data/seasons/{}/league/league.json"

def get_team_list(data):
    teams = []
    for player in data:
        team = data[player]["Team"]
        if isinstance(team, list):
            for t in team:
                teams.append(t)
        else:
            teams.append(team)
    return set(teams)

def get_standings(year):
    pass

def get_teams(teams, year):
    pass

if __name__ == "__main__":
    for season in info.seasons:
        if season != 2024:
            continue
        print(f"Scraping {season} season")

        os.makedirs(f"data/seasons/{str(season)}", exist_ok=True)
        os.makedirs(f"data/seasons/{str(season)}/players", exist_ok=True)
        os.makedirs(f"data/seasons/{str(season)}/teams", exist_ok=True)
        os.makedirs(f"data/seasons/{str(season)}/league", exist_ok=True)

        print("Scraping player stats")
        player_data = scrape.scrape_stats(season)
        tools.dump(player_stats_path.format(season), player_data)

        print("Scraping team stats")
        teams = get_team_list(player_data)
        for team in teams:
            team_data = scrape.scrape_team(team, season)
            print(season, ":", team)
            tools.dump(teams_path.format(season, team), team_data, wait=True)

        print("Scraping standings")
        standings_data = scrape.scrape_standings(season)
        tools.dump(standings_path.format(season), standings_data)

        season_info = {
            "awards": scrape.scrape_champion_mvp(season),
            "all_nba": scrape.scrape_all_nba_teams(season),
        }
        tools.dump(info_path.format(season), season_info)
        
        # update internal info
        data = {}
        for team in standings_data:
            data[team] = {}
            data[team]["standings"] = standings_data[team]
            data[team]["img"] = standings_data[team]["img"]
            del data[team]["standings"]["img"]
            del data[team]["standings"]["link"]  
            data[team]["roster"] = []
        
        for team in teams:
            f = open(teams_path.format(season, team), 'r')
            t = json.load(f)
            f.close()

            data[team]["stats"] = t[team]["team_stats"]
            data[team]["info"] = t[team]["info"]
            data[team]["last_update"] = t[team]["last_update"]

        for player in player_data:
            if isinstance(player_data[player]["Team"], list):
                team = player_data[player]["Team"][-1]
            else:
                team = player_data[player]["Team"]
            data[team]["roster"].append(player)

        tools.dump(league_path.format(season), data)

        # grade players
        # grade teams