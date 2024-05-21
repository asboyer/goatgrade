from flask import Flask
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
    return {'message': 'asboyer is watching u...'}

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

    r = []

    for player in data:
        j = data[player]
        r.append(j)

    return jsonpickle.encode(r)

@app.route("/players/<year>")
def get_player_grades(year):

    if year not in [str(i) for i in info.seasons]:
        return jsonpickle.encode({"error": "Season not found"})
    
    data = tools.load(scrape_all_seasons.player_grades_path.format(year))

    r = []

    for player in data:
        j = data[player]
        r.append(j)

    return jsonpickle.encode(r)

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