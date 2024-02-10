from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import requests
import random

def text(raw):
    if 'span class="desc"' in str(raw):
        t = raw.getText().strip().replace("\n", "")
        while "  " in t:
            t = t.replace("  ", " ")
        return t + "<i>"
    else:
        t = raw.getText().strip().replace("\n", "")
        while "  " in t:
            t = t.replace("  ", " ")
        return t

def get_id(url):
    return url.split("/")[-1].replace(".html", "")

def get_player_profile(url):

    soup = BeautifulSoup(urlopen(url), 'html.parser')

    stats = {}

    ps = soup.findAll('p')
    for p in range(len(ps)):

        t = text(ps[p])
        if p == 0 and "pronunciation" in t.lower():
            t = text(ps[p + 1])
        if p == 0 and "▪" not in t.lower():
            stats['name'] = t
        elif p == 0:
            ats = t.split(" ▪ ")
            stats['name'] = ats[0].split(": ")
            if 'twitter' in t.lower() and 'instagram' in t.lower():
                stats['twitter'] = ats[1].split(": ")[1]
                stats['instagram'] = ats[2].split(": ")[1]
            if 'twitter' in t.lower() and 'instagram' not in t.lower():
                stats['twitter'] = ats[1].split(": ")[1]
            if 'instagram' in t.lower() and 'twitter' not in t.lower():
                stats['instagram'] = ats[1].split(": ")[1]
        if (p == 1 or p == 2) and '<i>' in t.lower():
            stats['former_name'] = t.split("<i>")[0].replace(")", "").replace("(", "")
        if (p in list(range(0, 5))) and t.lower()[0] == '(' and '<i>' not in t.lower() and t[1] != '-':
            stats['nicknames'] = t.replace("(", "").replace(")", "").split(", ")
        if p in list(range(0, 6)) and 'position: ' in t.lower():
            stats['position'] = t.lower().split('position: ')[1].split(' ▪')[0]
            stats['shooting_hand'] = t.lower().split('shoots: ')[1]
        if p in list(range(1, 10)) and len(t) > 0 and t[1] == '-':
            stats['height'] = t.split(',')[0]
            stats['weight'] = t.split(',')[1].split('lb')[0].strip()
        if p in list(range(2, 11)) and len(t) > 0 and t.lower()[0:6] == 'born: ':
            stats['birthday'] = (t.lower().split('born')[1].split(' in')[0])[2:]
            if "in" in t.lower():
                stats['birthplace'] = t.lower().split('in ')[1].replace(', ', ', ')[0:-2] + " " + t.lower()[len(t)-2:len(t)].upper()
        if p in list(range(2, 12)) and len(t) > 0 and t.lower()[0:6] == 'died: ':
            stats['died'] = (t.lower().split('died')[1].split('(')[0])[2:].replace(' ', ' ')
        if p in list(range(2, 14)) and len(t) > 0 and (t.lower()[0:9] == 'college: ' or t.lower()[0:10] == 'colleges: '):
            if 'college: ' in t.lower():
                stats['college'] = t.lower().split('college:')[1][1:]
            if 'colleges: ' in t.lower():
                stats['colleges'] = t.lower().split('colleges:')[1][1:].split(', ')
        if p in list(range(2, 16)) and len(t) > 0 and t.lower().startswith("high school"):
            stats['high school'] = t.lower()[12:]
        if p in list(range(2, 18)) and len(t) > 0 and t.lower().startswith('draft: '):
            stats['draft'] = t.lower().split('draft: ')[1]
            # stats['drafted_to'] = t.lower().split('draft: ')[1].split(',')[0] + ", " + t.lower().split('), ')[1].replace(' nba draft', '')
            # stats['draft_pick'] = t.lower().split('draft: ')[1].split(',')[1][1:] + t.lower().split('draft: ')[1].split(',')[2]  
        if p in list(range(2, 20)) and len(t) > 0 and t.lower().startswith('nba debut: '):
            stats['debut'] = t.lower().split(': ')[1]
            break

    try:
        awards = []
        blings = soup.findAll('ul', {'id': 'bling'})[0].findAll('li')
        for b in blings:
            awards.append(b.getText().lower())

        stats['accomplishments'] = awards
    except IndexError:
        pass


    stats['career_summary'] = {}
    stats['link'] = url

    career_div = soup.findAll('div', {'class': 'stats_pullout'})[0]
    # print(r.text.split('<span><strong>SUMMARY</strong></span>')[1].split('<strong>WS</strong>')[0])
    stat_fields = career_div.findAll('span', {'class': 'poptip'})
    stat_names = []
    for stat_line in stat_fields:
        stat = str(stat_line)
        stat_name = stat.split('<strong>')[1].split('</strong>')[0]
        stat_names.append(stat_name)

    p_tags = career_div.findAll('p')[2:]
    
    counter = 0
    for p in range(1, len(p_tags), 2):
        stats['career_summary'][stat_names[counter]] = p_tags[p].getText()
        counter += 1

    player_string = get_id(url)

    stats['img_link'] = f'https://www.basketball-reference.com/req/202106291/images/headshots/{player_string}.jpg'

    return stats
