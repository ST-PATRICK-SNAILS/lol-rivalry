import requests
from bs4 import BeautifulSoup
import csv
import time

def get_player_stats(player_id, champion_id):
    url = f"https://gol.gg/players/player-stats/{player_id}/season-ALL/split-ALL/tournament-ALL/?post_player_id={player_id}&post_season=ALL&post_split=ALL&post_tournament=ALL&cbtournament=ALL&champion={champion_id}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the required table
    tables = soup.find_all('table', class_='table_list')

    # Iterate through all rows in the table
    td_list = tables[0].find_all('td')

    record = td_list[1].text.strip()

    if record is None:
        return [None]

    wr = td_list[3].text.strip()

    adj = 0

    if wr == '100%':
        adj = -1

    kd = td_list[7 + adj].text.strip()
    cspm = td_list[9 + adj].text.strip()
    gpm = td_list[11 + adj].text.strip()
    gp = td_list[13 + adj].text.strip()
    kp = td_list[15 + adj].text.strip()

    for agression_possible in tables:

        if agression_possible.find('tr').find('th').text.strip() == 'Aggression':

            agression = agression_possible

    td_list_agression = agression.find_all('td')
    
    dpm = td_list_agression[1].text.strip()
    dp = td_list_agression[3].text.strip()
    kapm = td_list_agression[5].text.strip()
    sk = td_list_agression[7].text.strip()
    pk = td_list_agression[9].text.strip()

    return [record, wr, kd, cspm, gpm, gp, kp, dpm, dp, kapm, sk, pk]

def get_player_champ_IDs(player_id):
    url = f"https://gol.gg/players/player-stats/{player_id}/season-S14/split-ALL/tournament-ALL/"
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
        td_log = row.find_all('td')
        champ_link = td_log[0].find('a')['href']
        champ_id = champ_link.split('/')[3]

        ids.append(champ_id)

    # print(ids)
    return ids



def main():
    input_filename = 'Player_to_ID.csv'
    output_filename = 'Player_Champ_Stats_All.csv'

    with open(input_filename, newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        header = next(reader)  # Skip header
        players = list(reader)

    entries = 0

    with open(output_filename, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['Player Name', 'Player ID', 'Champion ID', 'Record', 'Winrate', 'KDA', 'CS /min', 'Gold /min', 'Gold %', 'KP', 'Damage /min', 'Damage %', 'K + A /min', 'Solo kills', 'Pentakills'])

        for player_name, player_id in players:
            # print(f"summoner {player_name}")

            for champion_id in get_player_champ_IDs(player_id):
                # print(f"new champ pass {champion_id}")
                stats = get_player_stats(player_id, champion_id)
                # print(stats)
                writer.writerow([player_name, player_id, champion_id] + stats)

                entries += 1

                if entries % 100 == 0:
                    print(f"{entries} entries written to .csv")

if __name__ == "__main__":
    main()
