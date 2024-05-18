import requests
from bs4 import BeautifulSoup
import csv

def get_event_champs(season, event, region):
    # Headers to mimic a browser visit
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.get(f"https://gol.gg/champion/list/season-{season}/split-ALL/tournament-{event}/", headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all('table', class_="table_list")
    
    rows = tables[0].find_all('tr')
    data = []
    
    for row in rows[1:]:
        cols = row.find_all('td')
        link = cols[0].find('a')
        row_data = [season, event, region, link.get_text().strip(), link['href'].split('/')[2]]
        for col in cols[1:]:
            text = col.get_text().strip()
            if text:
                row_data.append(col.get_text().strip())
            else: row_data.append('-')
        data.append(row_data)
             
    return data

input_filename = '../data/tournamentList.csv'
output_filename = '../data/tournamentChamps.csv'        

with open(input_filename, newline='', encoding='utf-8') as infile:
    with open(output_filename, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['Season', 'Tournament Name', 'Region', 'Champion Name', "Champion ID", "Picks", "Bans", "Presence", 
                    "Wins", "Losses", "Winrate", "KDA", "Avg BT", "GT", "CSM", "DPM", "GPM", "CSD@15", 
                    "GD@15", "XPD@15"])
        for row in list(infile)[1:]:
            splits = row.split(',')
            tr_season, tr_name, tr_region = splits[0], splits[1], splits[2]
            for champ in get_event_champs(tr_season, tr_name, tr_region):
                writer.writerow(champ)

    print("Data has been written to tournament champs.csv")
