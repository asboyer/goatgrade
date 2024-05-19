import tools, info, grade

player_stats_path = "data/seasons/{}/players/stats.json"
player_grades_path = "data/seasons/{}/players/grades.json"

teams_path = "data/seasons/{}/teams/{}.json"
team_grades_path = "data/seasons/{}/teams/grades.json"

info_path = "data/seasons/{}/info.json"
standings_path = "data/seasons/{}/league/standings.json"
league_path = "data/seasons/{}/league/league.json"

categories=[
            "PTS", "AST", "TRB", "FG%", "FT%", "3P%", "STL", "BLK",
            "MP", "PER", "TS%", "WS", "BPM", "2P%", "OWS", "DWS", 
            "WS/48", "USG%", "OBPM", "DBPM", "VORP", "eFG%"
            ]
all_time_categories=["eFG%", "2P%","FG%", "AST", "PTS", "TS%", "FT%"]        

def get_team_categories(data):
    categories=[
                "PTS", "AST", "TRB", "FG%", "FT%", "3P%", "STL", "BLK",
                "MP", "PER", "TS%", "WS", "BPM", "2P%"
                ]
    old_categories = []
    for i in range(len(categories)):
        category = categories[i]
        cats = list(data[list(data.items())[0][0]]['stats']['Team'].keys())
        if category in cats:
            old_categories.append(category)
        for category in old_categories:
            categories.remove(category)
        
        return categories

def get_categories(data):
    old_categories = []
    for i in range(len(categories)):
        category = categories[i]
        if category not in list(data[list(data)[0]]):
            old_categories.append(category)
    for category in old_categories:
        categories.remove(category)
    
    return categories

def clean_team_stats_quick(data):
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

def clean_player_stats(data):
    categories = get_categories(data)

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
    return stats, categories

def clean_team_stats(data):
    categories = get_team_categories(data)

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

    return stats, categories

def grade_players(data, categoires, year):
    ranks = {}
    for player in stats:
        ranks[player] = {}

    topster_averages = []

    def rank(category):
        category_rankings = []
        for player in stats:
            if stats[player][category] != "":
                category_rankings.append([player, float(stats[player][category])])
            else:
                category_rankings.append([player, 0])
        category_rankings = sorted(category_rankings, key=lambda x: x[1])
        category_rankings.reverse()

        if category in all_time_categories:
            avg = 0
            topsters = category_rankings[0:10]
            
            for player in topsters:
                avg += player[1]

            topster_averages.append([category, round(avg / 10, 2)])

        for i in range(len(category_rankings)):
            name = category_rankings[i][0]
            value = category_rankings[i][1]
            ranks[name][category] = i + 1

    for category in categories:
        rank(category)

    league_grade = 0
    for t in topster_averages:
        if t[0] in ["PTS", "AST"]:
            league_grade += t[1] / 2
        else:
            league_grade += t[1] * 10

    league_grade = round((league_grade / len(all_time_categories)) * 11, 2)
    
    new_ranks = {}

    for player in ranks:
        score = 0
        for category in ranks[player]:
            score += ranks[player][category]

        # divide total score by all categories used    
        player_grade = score / len(categories)

        # divide by all players then multiply by 100
        player_grade = (player_grade / len(list(stats))) * 100

        # divide score by league grade times 2
        player_grade = player_grade / (league_grade * 2)

        # subtract from 100
        player_grade = 100 - (player_grade * 100)
        player_grade += (5 * (league_grade/100))
        player_grade -= (2.5 - (league_grade/100))

        new_ranks[player] = {}

        new_ranks[player]["grade"] = round(player_grade, 2)
        new_ranks[player]["name"] = stats[player]["name"]
        new_ranks[player]["league_grade"] = league_grade
        new_ranks[player]["year"] = year
        new_ranks[player]["games_played"] = int(stats[player]["G"])
        new_ranks[player]["team"] = stats[player]["team"] 
        new_ranks[player]["img"] = stats[player]["img"] 
        new_ranks[player]["id"] = stats[player]["id"]
        new_ranks[player]["age"] = stats[player]["age"]
        new_ranks[player]["pos"] = stats[player]["pos"]
        new_ranks[player]["link"] = stats[player]["link"]
        new_ranks[player]["last_update"] = stats[player]["last_update"]
        min_categories, min_value = grade.get_all_min_categories(player, ranks)
        new_ranks[player]["top_category"] = [f"{category}: {min_value}" for category in min_categories]
        max_categories, max_value = grade.get_all_max_categories(player, ranks)
        new_ranks[player]["worst_category"] = [f"{category}: {max_value}" for category in max_categories]

    sorted_players = {k: v for k, v in sorted(new_ranks.items(), key=lambda item: item[1]['grade'], reverse=True)}
    
    team_stats = clean_team_stats_quick(tools.load(league_path.format(year)))

    for player in sorted_players:
        team = sorted_players[player]["team"]
        sorted_players[player]["team_standing_string"] = team_stats[team]["standing"]
        sorted_players[player]["team_league_ranking"] = team_stats[team]["RRK"]
        sorted_players[player]["team_name"] = team_stats[team]["Name"]
        sorted_players[player]["team_img"] = team_stats[team]["img"]

    placement = 1
    for player in sorted_players:
        sorted_players[player]["rank"] = placement
        placement += 1

    return sorted_players

def grade_team(stats, player_grades, categories, year):

    f = {}

    for team in stats:
        
        grades = []
        for player in stats[team]["Players"]:
            try:
                grades.append(player_grades[player]["grade"])
            except KeyError:
                pass
        grades = sorted(grades, reverse=True)
        grades = grades[0:8]
        grade_avg = round((sum(grades) / len(grades)), 2)

        score = 0
        # for cat in categories:
        #     score += int(stats[team]["stat_ranks"][cat])
        score += int(stats[team]["RRK"])*2.5

        grade = 100 - round(score/len(categories), 2)
        grade = round((grade*2 + grade_avg)/3, 2)

        f[team] = {}

        f[team] = stats[team]
        del f[team]["stat_ranks"]
        del f[team]["Players"]

        f[team]["avg_grade"] = grade_avg
        f[team]['score'] = grade
        f[team]['last_update'] = stats[team]["last_update"]
        f[team]['link'] = "https://www.basketball-reference.com/teams/{}/{}.html".format(year, team)

    sorted_teams = {k: v for k, v in sorted(f.items(), key=lambda item: item[1]['score'], reverse=True)}
   
    placement = 1
    for player in sorted_teams:
        sorted_teams[player]["rank"] = placement
        placement += 1

if __name__ == "__main__":
    for season in info.seasons:
        stats, categories = clean_player_stats(tools.load(player_stats_path.format(season)))
        ranks = grade_players(stats, categories, season)
        tools.dump(player_grades_path.format(season), ranks)


        team_stats, team_categories = clean_team_stats(tools.load(league_path.format(season, season)))
        ranks = grade_team(team_stats, ranks, team_categories, season)
        tools.dump(team_grades_path.format(season), ranks)
