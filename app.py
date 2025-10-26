from flask import Flask, Response
from flask_cors import CORS
import os, json

import tools
import jsonpickle

import info, scrape_all_seasons

from datetime import datetime, timedelta

write_file_path = "data/stat/league/{}.json"
player_stats_path = "data/stat/players/stats/{}.json"
standings_path = "data/team/standings/{}.json"
team_path = "data/team/teams/{}.json"
player_grades_path = "data/stat/players/grades/{}.json"
team_grades_path = "data/team/grades/{}.json"
seasons_path = "data/league/seasons.json"
archive_path = "data/archive/{}/results.json"

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonpickle.encode({'message': 'asboyer is watching u...'}, indent=4)

@app.route("/teams")
def get_team_grades_current():
    date_obj = datetime.today()
    date_string = tools.date_to_str(datetime.today())

    while not os.path.isfile(team_grades_path.format(date_string)):
        date_obj = date_obj - timedelta(days=1)
        date_string = tools.date_to_str(date_obj)

    f = open(team_grades_path.format(date_string), 'r')
    data = json.load(f)
    f.close()

    r = []

    for team in data:
        j = {
            "name": data[team]["Name"],
            "abbr": team,
            "standing": data[team]["standing"],
            "grade": data[team]["score"],
            "rank": data[team]["rank"],
            "change": data[team]["change"],
            "img": data[team]["img"],
            "link": data[team]["link"],
            "last_update": data[team]["last_update"]
        }
        r.append(j)

    return jsonpickle.encode(r)

@app.route("/teams/<year>")
def get_team_grades(year):

    if year not in [str(i) for i in info.seasons]:
        return jsonpickle.encode({"error": "Season not found"})
    
    data = tools.load(scrape_all_seasons.team_grades_path.format(year))

    r = []

    for team in data:
        j = {
            "name": data[team]["Name"],
            "abbr": team,
            "standing": data[team]["standing"],
            "grade": data[team]["score"],
            "rank": data[team]["rank"],
            "img": data[team]["img"],
            "link": data[team]["link"],
            "last_update": data[team]["last_update"],
            "record": data[team]["record"]
        }
        r.append(j)

    return jsonpickle.encode(r)
    
@app.route("/players")
def get_player_grades_current():
    date_obj = datetime.today()
    date_string = tools.date_to_str(datetime.today())

    while not os.path.isfile(team_grades_path.format(date_string)):
        date_obj = date_obj - timedelta(days=1)
        date_string = tools.date_to_str(date_obj)

    f = open(player_grades_path.format(date_string), 'r')
    data = json.load(f)
    f.close()

    f = open(team_grades_path.format(date_string), 'r')
    teams = json.load(f)
    f.close()

    r = []

    for player in data:
        data[player]["team_standing_string"] = teams[data[player]["team"]]["standing"]
        j = data[player]
        r.append(j)

    return jsonpickle.encode(r)

@app.route("/players/<year>")
def get_player_grades(year):

    if year == "all":
        return get_all_players()

    elif year not in [str(i) for i in info.seasons]:
        return jsonpickle.encode({"error": "Season not found"})
    
    data = tools.load(scrape_all_seasons.player_grades_path.format(year))

    r = []

    for player in data:
        j = data[player]
        r.append(j)

    return jsonpickle.encode(r, indent=4)

def get_all_players():
    r = []
    
    # Iterate through all seasons
    for year in info.seasons:
        year_str = str(year)
        
        # Check if player grades file exists for this season
        player_grades_file = scrape_all_seasons.player_grades_path.format(year_str)
        if os.path.isfile(player_grades_file):
            try:
                data = tools.load(player_grades_file)
                
                # Add each player with year information
                for player in data:
                    player_data = data[player].copy()
                    player_data["year"] = year_str
                    r.append(player_data)
                    
            except Exception as e:
                # Skip seasons that can't be loaded
                continue
    
    # Sort players by grade in descending order (highest grade first)
    r.sort(key=lambda x: x.get("grade", 0), reverse=True)
    
    # Add total_rank field to each player record
    for i, player in enumerate(r[:250]):
        player["total_rank"] = i + 1
    
    # Return only the top 250 players
    return Response(jsonpickle.encode(r[:250], indent=4), mimetype='application/json')

@app.route("/seasons/<year>")
def get_season(year):
    if year not in [str(i) for i in info.seasons]:
        return jsonpickle.encode({"error": "Season not found"})
    data = tools.load(scrape_all_seasons.info_path.format(year))

    return jsonpickle.encode(data)

@app.route("/seasons")
def get_seaons():
    return jsonpickle.encode(info.seasons)

@app.route("/in_season")
def in_season():
    return jsonpickle.encode({"in_season": info.in_season()})

@app.route("/archive/<year>")
def archive(year):
    if year not in [str(i) for i in info.archived_seasons]:
        return jsonpickle.encode({"error": "Season not found"})

    data = tools.load(archive_path.format(year))

    return jsonpickle.encode(data)