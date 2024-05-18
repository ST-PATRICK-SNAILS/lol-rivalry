import requests
from bs4 import BeautifulSoup
import csv
import threading
import os

def get_player_stats(player_id, champion_id):
    url = f"https://gol.gg/players/player-stats/{player_id}/season-ALL/split-ALL/tournament-ALL/?post_player_id={player_id}&post_season=ALL&post_split=ALL&post_tournament=ALL&cbtournament=ALL&champion={champion_id}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the required table
    tables = soup.find_all('table')
    
    def tableContainsTitle(table, text):
        th = table.find_all('th')
        if(th and th[0]):
            if(text.lower() in th[0].get_text().lower()):
                return True
        return False
    
    data = []

    generalTable = [t for t in tables if tableContainsTitle(t, "GENERAL")]
    if(len(generalTable) == 1):
        generalKeys = ["Win Rate", "Record", "KDA", "CS per Minute", "Gold Per Minute", "Gold%", "Kill Participation"]
        for key in generalKeys:
            val = '-'
            for row in generalTable[0].find_all('tr')[1:]:
                entries = row.find_all('td')
                if(len(entries) >= 2 and entries[0].get_text().lower().startswith(key.lower())):
                    val = entries[1].get_text().replace(u'\xa0', u' ').strip()
                    break
            data.append(val)
    else: data.extend(['-' for _ in range(7)])
            
    aggressionTable = [t for t in tables if tableContainsTitle(t, "AGGRESSION")]
    if(len(aggressionTable) == 1):
        aggressionKeys = ['Damage Per Minute', 'Damage%', 'K+A Per Minute', 'Solo Kills', 'Pentakills']
        for key in aggressionKeys:
            val = '-'
            for row in aggressionTable[0].find_all('tr')[1:]:
                entries = row.find_all('td')
                if(len(entries) >= 2 and entries[0].get_text().lower().startswith(key.lower())):
                    val = entries[1].get_text().replace(u'\xa0', u'')
                    break
            data.append(val)
    else: data.extend(['-' for _ in range(5)])
            
    earlyTable = [t for t in tables if tableContainsTitle(t, "EARLY GAME")]
    if(len(earlyTable) == 1):
        earlyKeys = ['Ahead in CS at 15 min', 'CS Differential at 15 min', 'Gold Differential at 15 min', 
                          'XP Differential at 15 min', 'First Blood Participation',
                          'First Blood Victim']
        for key in earlyKeys:
            val = '-'
            for row in earlyTable[0].find_all('tr')[1:]:
                entries = row.find_all('td')
                if(len(entries) >= 2 and entries[0].get_text().lower().startswith(key.lower())):
                    val = entries[1].get_text().replace(u'\xa0', u'')
                    break
            data.append(val)
    else: data.extend(['-' for _ in range(6)])

    return data

def get_player_champ_IDs(player_id):
    url = f"https://gol.gg/players/player-stats/{player_id}/season-ALL/split-ALL/tournament-ALL/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.content, 'html.parser')

    for table_possible in soup.find_all('table', class_='table_list'):
        
        if table_possible.find('tr').find('th').text.strip() == 'Champion':

            table = table_possible

    ids = []

    for row in table.find_all('tr')[1::2]:
        url = row.find_all('a')[0]
        champ_name = url.get_text().strip()
        
        td_log = row.find_all('td')
        champ_link = td_log[0].find('a')['href']
        champ_id = champ_link.split('/')[3]

        ids.append([champ_name, champ_id])

    # print(ids)
    return ids



input_filename = '../data/playerIds.csv'
output_filename = '../data/playerChamps.csv'

with open(input_filename, newline='', encoding='utf-8') as infile:
    BATCH_SIZE = 500
    batches, acc = [], []
    count = 0
    for row in infile:
        splits = row.strip().split(',')
        if count < BATCH_SIZE:
            acc.append(splits)
            count += 1
        else: 
            count = 0
            batches.append(acc)
            acc = []
            
    batches[0] = batches[0][1:]
    

    with open(output_filename, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['Player Name', 'Player ID', 'Champion Name', 'Champion ID', 
                         "Win Rate", "Record", "KDA", "CS per Minute", "Gold Per Minute", "Gold%", "Kill Participation",
                         'Damage Per Minute', 'Damage%', 'K+A Per Minute', 'Solo Kills', 'Pentakills',
                         'Ahead in CS at 15 min', 'CS Differential at 15 min', 'Gold Differential at 15 min', 
                          'XP Differential at 15 min', 'First Blood Participation',
                          'First Blood Victim'])

        def process_batch(batch):
            for pair in batch:
                player_name, player_id = pair[0], pair[1]
                for champion_pair in get_player_champ_IDs(player_id):
                    champion_name, champion_id = champion_pair[0], champion_pair[1]
                    stats = get_player_stats(player_id, champion_id)
                    writer.writerow([player_name, player_id, champion_name, champion_id] + stats)
                    
        threads = []
        for batch in batches:
            threads.append(threading.Thread(target=process_batch, args=(batch, )))
            
        for thread in threads:
            thread.start()
            
        for thread in threads:
            thread.join()

        print("Data has been written to player champs.csv")
                    
        