import json

year = 2024

write_file_path = "data/stat/league/{}.json"
player_stats_path = "data/stat/players/stats/{}.json"
standings_path = "data/team/standings/{}.json"
team_path = "data/team/teams/{}.json"
player_grades_path = "data/stat/players/grades/{}.json"
team_grades_path = "data/team/grades/{}.json"

def get_player_stats(date_string, categories):
    f = open(player_stats_path.format(date_string), 'r')
    data = json.load(f)
    f.close()
    
    stats = {}
    for player in data:
        stats[player]= {}
        for category in categories:
            stats[player][category] = data[player][category] 
        stats[player]["G"] = data[player]["G"]
        stats[player]["id"] = data[player]["id"]
        stats[player]["img"] = data[player]["img"]
        stats[player]["name"] = data[player]["Player"]
        stats[player]["last_update"] = data[player]["last_update"]
        stats[player]["age"] = data[player]["Age"]
        stats[player]["pos"] = data[player]["Pos"]
        stats[player]["link"] = data[player]["link"]
        if isinstance(data[player]["Tm"], list):
            team = data[player]["Tm"][-1]
        else:
            team = data[player]["Tm"]
        stats[player]["team"] = team
    return stats

def get_team_stats(date_string, categories):
    f = open(write_file_path.format(date_string), 'r')
    data = json.load(f)
    f.close()

    stats = {}  
    for team in data:

        stat_ranks = {}
        for cat in data[team]["stats"]["Lg Rank"]:
            if cat in categories:
                stat_ranks[cat] = data[team]["stats"]["Lg Rank"][cat]

        for cat in data[team]["stats"]["Opp Lg Rank"]:
            if cat in categories:
                stat_ranks[f'O_{cat}'] = data[team]["stats"]["Opp Lg Rank"][cat]

        j = {
            "Tm": team,
            "RRK": data[team]["standings"]["Rk"],
            "Name": data[team]["standings"]["Team"],
            "img": data[team]["img"],
            "Players": data[team]["roster"],
            "stat_ranks": stat_ranks,
            'standing': data[team]["info"]["standing"],
            "last_update": data[team]["last_update"]
        }

        stats[team] = j

    return stats

def get_grades(date_string):
    f = open(player_grades_path.format(date_string), 'r')
    data = json.load(f)
    f.close()

    return data

def get_team_stats_quick(date_string):
    f = open(write_file_path.format(date_string), 'r')
    data = json.load(f)
    f.close()
    
    stats = {}  

    for team in data:
        j = {
            "Tm": team,
            "RRK": data[team]["standings"]["Rk"],
            "Name": data[team]["standings"]["Team"],
            "img": data[team]["img"],
            'standing': data[team]["info"]["standing"],
            "last_update": data[team]["last_update"]
        }

        stats[team] = j

    return stats


def get_grades_team(date_string):
    f = open(team_grades_path.format(date_string), 'r')
    data = json.load(f)
    f.close()

    return data