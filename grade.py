import json
import tools
import os
import getters

from datetime import datetime, timedelta
        
def get_all_min_categories(player, ranks):
    min_value = min(ranks[player].values())
    min_categories = [k for k, v in ranks[player].items() if v == min_value]
    return min_categories, min_value

def get_all_max_categories(player, ranks):
    max_value = max(ranks[player].values())
    max_categories = [k for k, v in ranks[player].items() if v == max_value]
    return max_categories, max_value

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
        min_categories, min_value = get_all_min_categories(player, ranks)
        new_ranks[player]["top_category"] = [f"{category}: {min_value}" for category in min_categories]
        max_categories, max_value = get_all_max_categories(player, ranks)
        new_ranks[player]["worst_category"] = [f"{category}: {max_value}" for category in max_categories]

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
    try:
        yesterday_grades = getters.get_grades(yesterday_str)
    except:
        yesterday_grades = {}
    for player in sorted_players:
        try:
            sorted_players[player]["change"] = yesterday_grades[player]["rank"] - sorted_players[player]["rank"]  
        except:
            sorted_players[player]["change"] = 0

    return sorted_players

def get_ordinal(i):
    SUFFIXES = {1: 'st', 2: 'nd', 3: 'rd'}

    if 10 <= i % 100 <= 20:
        return 'th'
    else:
        return SUFFIXES.get(i % 10, 'th')

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
    east_teams = 1
    west_teams = 1

    for team in stats:
        
        if "east" in stats[team]["standing"].lower():
            stats[team]["conference"] = "East"
            stats[team]["conference_rank"] = east_teams
            east_teams += 1
        else:
            stats[team]["conference"] = "West"
            stats[team]["conference_rank"] = west_teams
            west_teams += 1

        stats[team]["standing"] = f'{stats[team]["conference_rank"]}{get_ordinal(stats[team]["conference_rank"])} in {stats[team]["conference"]}'

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
    try:
        yesterday_grades = getters.get_grades_team(yesterday_str)
    except:
        yesterday_grades = {}
    sorted_players = sorted_teams
    for player in sorted_players:
        try:
            sorted_players[player]["change"] = yesterday_grades[player]["rank"] - sorted_players[player]["rank"]  
        except:
            sorted_players[player]["change"] = 0

    return sorted_players

def archive(year):
    r = {
        "players": {},
        "teams": {},
        "league_progression": [],
        "final_results": {}
    }

    player_path = f"data/archive/{year}/stat/players/grades"
    team_path = f"data/archive/{year}/team/grades"

    final_results_path = f"data/seasons/{year}/info.json"
    player_results_path = f"data/seasons/{year}/players/grades.json"
    team_results_path = f"data/seasons/{year}/teams/grades.json"

    for filename in os.listdir(player_path):
        player_grades = tools.load(os.path.join(player_path, filename))
        team_grades = tools.load(os.path.join(team_path, filename))

        r["league_progression"].append( 
            {
            "grade": player_grades[list(player_grades.keys())[0]]["league_grade"],
            "date": filename.split(".")[0]
            }
        )

        for player in player_grades:
            if player not in list(r["players"].keys()):
                r["players"][player] = []
            r["players"][player].append(
                {
                "grade": player_grades[player]["grade"],
                "rank": player_grades[player]["rank"],
                "games_played": player_grades[player]["games_played"],
                "team": player_grades[player]["team"],
                "date": filename.split(".")[0],
                }
            )
        
        for team in team_grades:
            if team not in list(r["teams"].keys()):
                r["teams"][team] = []
            r["teams"][team].append( {
                "score": team_grades[team]["score"],
                "rank": team_grades[team]["rank"],
                "avg_grade": team_grades[team]["avg_grade"],
                "standing": team_grades[team]["standing"],
                "date": filename.split(".")[0],
            })


    final_player_grades = tools.load(player_results_path)
    final_team_grades = tools.load(team_results_path)
    final_results = tools.load(final_results_path)

    r["final_results"] = final_results

    for data in r["league_progression"]:
        data["date"] = datetime.strptime(data["date"], "%m_%d_%Y")
    r["league_progression"].sort(key=lambda x: x['date'])
    for data in r["league_progression"]:
        data["date"] = data["date"].strftime("%m_%d_%Y")

    r["league_progression"].append( 
        {
        "grade": final_player_grades[list(final_player_grades.keys())[0]]["league_grade"],
        "date": "Final"
        }
    )

    for player in final_player_grades:

        # sort
        for data in r["players"][player]:
            data["date"] = datetime.strptime(data["date"], "%m_%d_%Y")
        
        r["players"][player].sort(key=lambda x: x['date'])

        for data in r["players"][player]:
            data["date"] = data["date"].strftime("%m_%d_%Y")

        if player in list(r["players"].keys()):    
            r["players"][player].append( 
                {
                "grade": final_player_grades[player]["grade"],
                "rank": final_player_grades[player]["rank"],
                "games_played": final_player_grades[player]["games_played"],
                "team": final_player_grades[player]["team"],
                "img": final_player_grades[player]["img"],
                "id": final_player_grades[player]["id"],
                "link": final_player_grades[player]["link"],
                "team_img": final_player_grades[player]["team_img"],
                "team": final_player_grades[player]["team"],
                "name": final_player_grades[player]["name"],
                }
            )
    
    for team in final_team_grades:

        # sort
        for data in r["teams"][team]:
            data["date"] = datetime.strptime(data["date"], "%m_%d_%Y")
        
        r["teams"][team].sort(key=lambda x: x['date'])

        for data in r["teams"][team]:
            data["date"] = data["date"].strftime("%m_%d_%Y")

        r["teams"][team].append (
            {
            "score": final_team_grades[team]["score"],
            "rank": final_team_grades[team]["rank"],
            "avg_grade": final_team_grades[team]["avg_grade"],
            "standing": final_team_grades[team]["standing"],
            "img": final_team_grades[team]["img"],
            "link": final_team_grades[team]["link"],
            "name": final_team_grades[team]["Name"],
            "conference": final_team_grades[team]["conference"],
            "conference_rank": final_team_grades[team]["conference_rank"],
            "record": final_team_grades[team]["record"]
        }
        )

    return r

if __name__ == "__main__":
    tools.dump("data/archive/2024/results.json", archive("2024"))