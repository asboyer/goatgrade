from flask import Flask
from flask_cors import CORS
import os, json

import tools
import jsonpickle

import info

from datetime import datetime, timedelta

write_file_path = "data/stat/league/{}.json"
player_stats_path = "data/stat/players/stats/{}.json"
standings_path = "data/team/standings/{}.json"
team_path = "data/team/teams/{}.json"
player_grades_path = "data/stat/players/grades/{}.json"
team_grades_path = "data/team/grades/{}.json"
seasons_path = "data/league/seasons.json"

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return {'message': 'asboyer is watching u...'}

@app.route("/teams")
def get_team_grades_current():
    date_string = tools.date_to_str(datetime.today())
    if not os.path.isfile(team_grades_path.format(date_string)):
        date_obj = datetime.strptime(date_string, "%m_%d_%Y")
        yesterday = date_obj - timedelta(days=1)
        yesterday_str = yesterday.strftime("%m_%d_%Y")
        date_string = yesterday_str

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
    date_string = tools.date_to_str(datetime.today())
    if not os.path.isfile(team_grades_path.format(date_string)):
        date_obj = datetime.strptime(date_string, "%m_%d_%Y")
        yesterday = date_obj - timedelta(days=1)
        yesterday_str = yesterday.strftime("%m_%d_%Y")
        date_string = yesterday_str

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
    
@app.route("/players")
def get_player_grades_current():
    date_string = tools.date_to_str(datetime.today())
    if not os.path.isfile(team_grades_path.format(date_string)):
        date_obj = datetime.strptime(date_string, "%m_%d_%Y")
        yesterday = date_obj - timedelta(days=1)
        yesterday_str = yesterday.strftime("%m_%d_%Y")
        date_string = yesterday_str    

    f = open(player_grades_path.format(date_string), 'r')
    data = json.load(f)
    f.close()

    r = []

    for player in data:
        j = data[player]
        r.append(j)

    return jsonpickle.encode(r)

@app.route("/players/<year>")
def get_player_grades():
    date_string = tools.date_to_str(datetime.today())
    if not os.path.isfile(team_grades_path.format(date_string)):
        date_obj = datetime.strptime(date_string, "%m_%d_%Y")
        yesterday = date_obj - timedelta(days=1)
        yesterday_str = yesterday.strftime("%m_%d_%Y")
        date_string = yesterday_str    

    f = open(player_grades_path.format(date_string), 'r')
    data = json.load(f)
    f.close()

    r = []

    for player in data:
        j = data[player]
        r.append(j)

    return jsonpickle.encode(r)

@app.route("/seasons")
def get_seasons():
    f = open(seasons_path, 'r')
    data = json.load(f)
    f.close()

    return jsonpickle.encode(data)
