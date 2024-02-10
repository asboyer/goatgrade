from urllib.request import urlopen
from bs4 import BeautifulSoup, Comment
import json, requests, os, re

from datetime import datetime
today = datetime.today()
current_year = today.year
current_month = today.month
current_day = today.day

import player_profile
import info
import tools

import random

# gloabl variables
BASE_REG_STATS_URL = "https://www.basketball-reference.com/leagues/NBA_{}_per_game.html"
BASE_ADV_STATS_URL = "https://www.basketball-reference.com/leagues/NBA_{}_advanced.html"
BASE_TM_STAND_URL = "https://www.basketball-reference.com/leagues/NBA_{}_standings.html"
BASE_TM_URL = "https://www.basketball-reference.com/teams/{}/{}.html"

def scrape_player(url):
    return player_profile.get_player_profile(url)    

def scrape_stats(year):
    reg_stats = scrape(BASE_REG_STATS_URL.format(year))
    adv_stats = scrape(BASE_ADV_STATS_URL.format(year))

    for player in list(reg_stats):
        reg_stats[player].update(adv_stats[player])

    return clean(reg_stats)

def clean(stats):
    for player in list(stats):
        del stats[player]['\xa0']
        stats[player]["last_update"] = today.strftime("%b %d %Y %H:%M:%S")
    return stats

def extract_info(text):
    info = {}
    words = text.split(" ")

    p = 0
    for word in words:
        p+=1
        if word.lower() == "record:":
            info["record"] = words[p].replace(",", "")
            info["standing"] = words[p + 1]
        if word.lower() == "nba":
            info["standing"] += f" in {words[p].replace('ern', '')}"
        if word.lower() == "coach:":
            info["coach"] = " ".join(words[p:]).split("Executive")[0].strip()
        if word.lower() == "executive:":
            info["gm"] = " ".join(words[p:]).split("PTS/G")[0].strip()
        if word.lower() == "preseason":
            info["preseason_odds"] = " ".join(words[(p + 2)]).split(",")[0].strip().replace(" ", "")

    return info

def scrape_standings(year):    
    url = BASE_TM_STAND_URL.format(year)
    html = urlopen(url)
    soup = BeautifulSoup(html, "html.parser")

    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    for comment in comments:
        uncommented_content = BeautifulSoup(comment, 'html.parser')
        comment.replace_with(uncommented_content)

    table = soup.find('table', {'id': 'expanded_standings'})

    # Extract table headers
    headers = [th.text.strip() for th in table.find_all('tr')[1].find_all('th')]
    headers.append('link')

    # Initialize a list to store each row as a dictionary
    data_dicts = []

    # Process each row in the table body
    for tr in table.find('tbody').find_all('tr'):
        # Extract cell data
        cells = tr.find_all(['th', 'td'])
        row_data = [cell.text.strip() for cell in cells]
        team_link = tr.find('td', {'data-stat': 'team_name'}).find('a')['href']
        row_data.append(team_link)
        # Create a dictionary for the current row, mapping headers to cell data
        row_dict = dict(zip(headers, row_data))
        data_dicts.append(row_dict)

    img = "https://cdn.ssref.net/req/202312151/tlogo/bbr/{}-{}.png"

    standings = {}

    for item in data_dicts: 
        name = item["link"].split("teams/")[1].split("/")[0]
        item["img"] = img.format(name, year)
        standings[name] = item

    return standings


def scrape_team(team, year):
    url = BASE_TM_URL.format(team, year)
    
    # Fetching and parsing the HTML content
    html = urlopen(url)
    soup = BeautifulSoup(html, "html.parser")
    
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))

    for comment in comments:
        uncommented_content = BeautifulSoup(comment, 'html.parser')
        comment.replace_with(uncommented_content)

    template_content = soup.find_all(attrs={"data-template": "Partials/Teams/Summary"})
    extracted_data = [element.get_text() for element in template_content]
    text = tools.replace_multiple_whitespaces_with_single(extracted_data[0]).strip()
    info = extract_info(text)

    roster_table = soup.find('div', id='all_roster').find('table')
    player_td_tags = roster_table.find_all('td', {'data-stat': 'player'})
    player_names = [td.find('a').text for td in player_td_tags if td.find('a')]
    
    try:
        injury_table = soup.find('div', id='div_injuries').find('table')
        injury_reports = []
        for row in injury_table.find('tbody').find_all('tr'):
            player_name = row.find('th', {'data-stat': 'player'}).text
            team_name = row.find('td', {'data-stat': 'team_name'}).text
            update_date = row.find('td', {'data-stat': 'date_update'}).text
            description = row.find('td', {'data-stat': 'note'}).text
            injury_reports.append({
                'Player': player_name,
                'Team': team_name,
                'Update': update_date,
                'Description': description
            })
    except:
        injury_reports = []
    
    data_list = scrape_div(soup, 'div_team_and_opponent') 
    
    team_stats = {}                
    for item in data_list:
        if item['\xa0'] in team_stats:
            name = "Opp " + item['\xa0']
        else:
            name = item['\xa0']
        team_stats[name] = item
        del team_stats[name]['\xa0']

    data_list = scrape_div(soup, 'div_team_misc', overhead=True)

    for item in data_list:
        if item[""] in team_stats:
            name = "Misc " + item[""]
        else:
            name = item[""]
        team_stats[name] = item
        del team_stats[name][""]


    # Placeholder for team and player stats (use your existing scraping logic)
    final_stats = {}

    # Fetching the team image URL
    # Assuming the image can be identified by a specific tag and attribute
    team_logo_img = soup.find('img', class_='teamlogo')  # Adjust the class name as necessary
    team_image_url = team_logo_img['src'] if team_logo_img else "No image found"
    
    # Compiling the final JSON-like structure
    j = {
        team: {
            'info': info,
            'players': player_names,
            'injuries': injury_reports,
            'team_stats': team_stats,
            'image_url': team_image_url,
            'last_update': today.strftime("%b %d %Y %H:%M:%S")
        }
    }
    
    return j

def scrape_div(soup, id, overhead=False):
    # Initialize a list to store your data
    if not overhead:
        div = soup.find('div', id=id)

        data_list = []
        
        if div:
            table = div.find('table')
            if table:
                headers = [th.get_text() for th in table.find('thead').find_all('th')]
                
                # Extract table rows
                for tr in table.find('tbody').find_all('tr'):
                    row_data = [td.get_text() for td in tr.find_all('td', recursive=False)]  # Or tr.find_all(['th', 'td']) if the first column is important
                    
                    # Sometimes the first column is a header (<th>) within the row
                    row_header = tr.find('th', recursive=False)
                    if row_header:
                        row_data.insert(0, row_header.get_text())
                    
                    # Combine headers and row data into a dictionary
                    if row_data:  # Ensure there is data to process
                        row_dict = dict(zip(headers, row_data))
                        data_list.append(row_dict)

    if overhead:
    # Initialize a list to store each row's data
        div_container = soup.find('div', id=id)

        data_list = []

        # Proceed if the div container is found
        if div_container:
            # Find the table within the div
            table = div_container.find('table')
            
            # Proceed if the table is found
            if table:
                # Extract table headers, skipping 'over_header' by selecting the second row explicitly for headers
                headers = [th.get_text(strip=True) for th in table.find_all('tr')[1].find_all('th')]
                
                # Extract table rows, ignoring 'over_header' rows
                for tr in table.find('tbody').find_all('tr'):
                    # Ensure the row is not an 'over_header' before processing
                    if 'over_header' not in tr.get('class', []):  # The get method avoids AttributeError if 'class' is not present
                        row_data = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
                        data_list.append(row_data)

        
        structured_data = []
        for row in data_list:
            if len(row) == len(headers): 
                structured_data.append(dict(zip(headers, row)))
        data_list = structured_data

    return data_list

def scrape(url):
    html = urlopen(url)
    soup = BeautifulSoup(html, "html.parser")  

    headers = [th.getText() for th in soup.findAll("tr", limit=2)[0].findAll("th")]
    headers = headers[1:]

    rows = soup.findAll("tr")[1:]

    stats = {}
    for i in range(len(rows)):
        tds = rows[i].findAll("td")
        if len(tds) > 0:
            name_cell = tds[0]
            name = name_cell.getText()
            link = name_cell.find('a')['href'] if name_cell.find('a') else None
            try:
                if stats[name] != {}:
                    h = 0
                    for td in tds:
                        header = headers[h]
                        if header == "Tm":
                            team = td.getText()
                        h += 1
                    stats[name]["Tm"].append(team)
            except:
                stats[name] = {}
                stats[name]["link"] = f"https://www.basketball-reference.com{link}"
                h = 0
                for td in tds:
                    header = headers[h]
                    if header == "MP" and "advanced" in url:
                        header = "TMP"
                    stats[name][header] = td.getText()
                    h += 1
                if stats[name]["Tm"] == "TOT":
                    stats[name]["Tm"] = []
    return stats

if __name__ == "__main__":
    with open("test.json", "w+", encoding="utf8") as file:
        file.write(json.dumps(scrape_standings(2024), ensure_ascii=False, indent=4))