import json
import getters

from datetime import datetime, timedelta

def grade_players(year, date_string,
            categories=[
                        "PTS", "AST", "TRB", "FG%", "FT%", "3P%", "STL", "BLK",
                        "MP", "PER", "TS%", "WS", "BPM", "2P%", "OWS", "DWS", 
                        "WS/48", "USG%", "OBPM", "DBPM", "VORP", "eFG%"
                        ],
            all_time_categories=["eFG%", "2P%","FG%", "AST", "PTS", "TS%", "FT%"],            
            extra_categories=[],
            ):

    categories = list(categories + extra_categories)

    stats = getters.get_player_stats(date_string, categories)

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
        
        # player_grade = 100 - ((player_grade / league_grade) * )


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

    sorted_players = {k: v for k, v in sorted(new_ranks.items(), key=lambda item: item[1]['grade'], reverse=True)}
    
    team_stats = getters.get_team_stats_quick(date_string)

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

    date_obj = datetime.strptime(date_string, "%m_%d_%Y")
    yesterday = date_obj - timedelta(days=1)
    yesterday_str = yesterday.strftime("%m_%d_%Y")
    yesterday_grades = getters.get_grades(yesterday_str)
    for player in sorted_players:
        try:
            sorted_players[player]["change"] = yesterday_grades[player]["rank"] - sorted_players[player]["rank"]  
        except:
            sorted_players[player]["change"] = 0

        if sorted_players[player]["change"] > 0:
            sorted_players[player]["change"] = f'+{sorted_players[player]["change"]}'
        elif sorted_players[player]["change"] < 0:
            sorted_players[player]["change"] = f'{sorted_players[player]["change"]}'
        else:
            sorted_players[player]["change"] = f'{sorted_players[player]["change"]}'

    return sorted_players

def grade_team(year, date_string,
            categories=[
                        "PTS", "AST", "TRB", "FG%", "FT%", "3P%", "STL", "BLK",
                        "MP", "PER", "TS%", "WS", "BPM", "2P%"
                        ],
            extra_categories=[],
            ):

    categories = list(categories + extra_categories)

    for i in range(len(categories)):
        categories.append(f'O_{categories[i]}')

    stats = getters.get_team_stats(date_string, categories)

    player_grades = getters.get_grades(date_string)

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
        for cat in stats[team]["stat_ranks"]:
            score += int(stats[team]["stat_ranks"][cat])
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

    date_obj = datetime.strptime(date_string, "%m_%d_%Y")
    yesterday = date_obj - timedelta(days=1)
    yesterday_str = yesterday.strftime("%m_%d_%Y")
    yesterday_grades = getters.get_grades_team(yesterday_str)
    sorted_players = sorted_teams
    for player in sorted_players:
        try:
            sorted_players[player]["change"] = yesterday_grades[player]["rank"] - sorted_players[player]["rank"]  
        except:
            sorted_players[player]["change"] = 0

        if sorted_players[player]["change"] > 0:
            sorted_players[player]["change"] = f'+{sorted_players[player]["change"]}'
        elif sorted_players[player]["change"] < 0:
            sorted_players[player]["change"] = f'{sorted_players[player]["change"]}'
        else:
            sorted_players[player]["change"] = f'{sorted_players[player]["change"]}'

    return sorted_players