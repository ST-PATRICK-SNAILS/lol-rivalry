import requests
from bs4 import BeautifulSoup
import csv

import threading
import os

def get_team_page(id):
    # Headers to mimic a browser visit
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.get(f"https://gol.gg/teams/team-stats/{id}/split-ALL/tournament-ALL/", headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')
    options = list(map(lambda i:i['value'], soup.find_all('option')[1:]))
    
    return options

def get_team_tournament(id, tourney):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    response = requests.get(f"https://gol.gg/teams/team-stats/{id}/split-ALL/tournament-{tourney}/", headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all('table')
    
    def tableContainsTitle(table, text):
        th = table.find_all('th')
        if(th and th[0]):
            if(text.lower() in th[0].get_text().lower()):
                return True
        return False
    
    data = []
    
    generalTable = [t for t in tables if tableContainsTitle(t, "- S1")]
    if(len(generalTable) == 1):
        data.append(generalTable[0].find('th').get_text().replace(' - ', ' '))
        data.append(id)
        data.append(tourney)
        generalKeys = ["Region", "Win Rate", "Average game duration"]
        for key in generalKeys:
            val = '-'
            for row in generalTable[0].find_all('tr')[1:]:
                entries = row.find_all('td')
                if(len(entries) >= 2 and entries[0].get_text().lower().startswith(key.lower())):
                    val = entries[1].get_text().replace(u'\xa0', u' ')
                    break
            data.append(val)
    
    playersTable = [t for t in tables if tableContainsTitle(t, "ROLE")]
    if(len(playersTable) == 1):
        links = [l for l in playersTable[0].find_all('a') if not 'champion/champion-stats' in l['href']]
        rosterNames = list(map(lambda i:i['title'].split()[0], links))
        rosterIds = list(map(lambda i:i['href'].split('/')[3], links))
        data.append(' '.join(rosterNames[:5]))
        data.append(' '.join(rosterIds[:5]))
    
    allyBansTable = [t for t in tables if tableContainsTitle(t, "BANNED BY")]
    if(len(allyBansTable) == 1):
        for row in allyBansTable[0].find_all('tr')[2:]:
            banRow = []
            for link in row.find_all('a'):
                banRow.append(link['href'].split('/')[3])
            data.append(' '.join(banRow))
            
    enemyBansTable = [t for t in tables if tableContainsTitle(t, "BANNED AGAINST")]
    if(len(enemyBansTable) == 1):
        for row in enemyBansTable[0].find_all('tr')[2:]:
            banRow = []
            for link in row.find_all('a'):
                banRow.append(link['href'].split('/')[3])
            data.append(' '.join(banRow))
    
    aggressionTable = [t for t in tables if tableContainsTitle(t, "AGGRESSION")]
    if(len(aggressionTable) == 1):
        aggressionKeys = ['Damage Per Minute', 'First Blood', 'Kills Per Game', 'Deaths Per Game', 'Average Kill / Death Ratio', 'Average Assists / Kill']
        for key in aggressionKeys:
            val = '-'
            for row in aggressionTable[0].find_all('tr')[1:]:
                entries = row.find_all('td')
                if(len(entries) >= 2 and entries[0].get_text().lower().startswith(key.lower())):
                    val = entries[1].get_text().replace(u'\xa0', u'')
                    break
            data.append(val)
                    
    objectivesTable = [t for t in tables if tableContainsTitle(t, "OBJECTIVES")]
    if(len(objectivesTable) == 1):
        objectivesKeys = ['Plates / game (TOP|MID|BOT)', 'Dragons / game', 'Dragons at 15 min', 'Herald / game', 'Nashors / game']
        for key in objectivesKeys:
            val = '-'
            for row in objectivesTable[0].find_all('tr')[1:]:
                entries = row.find_all('td')
                if(len(entries) >= 2 and entries[0].get_text().lower().startswith(key.lower())):
                    val = entries[1].get_text().replace(u'\xa0', u'')
                    break
            data.append(val)
            
    return data

with open('../data/orgIds.csv', mode='r', newline='') as file:
    with open('../data/orgStats.csv', mode='w', newline='', encoding='utf-8') as writefile:
        writer = csv.writer(writefile)
        writer.writerow(['Team Name', 'Team ID', 'Event', 'Roster Names', 'Roster Ids', 'Region', 'Record', 'Average Game Duration', 'Ally Bans', 'Blue Ally Bans', 'Red Ally Bans', 
                    'Enemy Bans', 'Blue Enemy Bans', 'Red Enemy Bans', 'Damage Per Minute', 'First Blood', 'Kills Per Game', 
                    'Deaths Per Game', 'Average Kill / Death Ratio', 'Average Assists / Kill', 'Plates / game (TOP|MID|BOT)', 
                    'Dragons / game', 'Dragons at 15 min', 'Herald / game', 'Nashors / game'])
        writer_lock = threading.Lock()
        
        BATCH_SIZE = 200
        batches, acc = [], []
        count = 0
        for row in file:
            splits = row.split(',')
            if count < BATCH_SIZE:
                acc.append(splits[len(splits)-1].strip())
                count += 1
            else: 
                count = 0
                batches.append(acc)
                acc = []
                
        batches[0].pop()
                
        def process_batch(batch):
            for iden in batch:
                for option in get_team_page(iden):
                    data = get_team_tournament(iden, option)
                    with writer_lock:
                        writer.writerow(data)
                    
        threads = []
        for batch in batches:
            threads.append(threading.Thread(target=process_batch, args=(batch, )))
            
        for thread in threads:
            thread.start()
            
        for thread in threads:
            thread.join()
        
        print('Data has been written to org stats.csv')     
    
        