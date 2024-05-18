import requests
from bs4 import BeautifulSoup
import csv
import threading
from itertools import islice

event_list_total = []

def write_match_stats(event_list, writer_lock, writer):

    for event in event_list:

        sub_url = ''

        for word in event.split(' '):
            sub_url += word + "%20"

        url = f"https://gol.gg/tournament/tournament-matchlist/{sub_url[:-3] + '/'}"

        print(url)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        table = soup.find('table', class_='table_list')
        
        for row in table.find_all('tr')[1:]:

            team1Name = ''
            team2Name = ''
            record = ''
            stage = ''
            patch = ''
            date = ''
            team1ID = ''
            team2ID = ''
                
            try:

                td_list = row.find_all('td')

                team1Name = td_list[1].text.strip()
                team2Name = td_list[3].text.strip()
                record = td_list[2].text.strip()
                stage = td_list[4].text.strip()
                patch = td_list[5].text.strip()
                date = td_list[6].text.strip()

                game_link = td_list[0].find('a')['href']

                # print(f"GAME LINK TO ACCESS {game_link}")

                game_link_final = ''

                for sub in game_link.split('/')[:-2]:
                    game_link_final += sub + '/'

                response_game_link = requests.get('https://gol.gg/' + game_link_final + 'page-summary/', headers=headers)
                response_game_link.raise_for_status()

                soup_game_link = BeautifulSoup(response_game_link.content, 'html.parser')

                div_list = soup_game_link.find_all('div', class_="col-4")

                team1ID = div_list[0].find('a')['href'][20:24]
                team2ID = div_list[2].find('a')['href'][20:24]

            except:
                print('ERROR: Cannot find data.')

            print([event, team1Name, team1ID, team2Name, team2ID, record, stage, patch, date])

            with writer_lock:
                writer.writerow([event, team1Name, team1ID, team2Name, team2ID, record, stage, patch, date])

def run_write_match_stats_in_thread(event_chunk, writer_lock, writer):
    thread = threading.Thread(target=write_match_stats, args=(event_chunk, writer_lock, writer))
    thread.start()
    return thread

def chunked_event_list(event_list, chunk_size):
    it = iter(event_list)
    while True:
        chunk = list(islice(it, chunk_size))
        if not chunk:
            break
        yield chunk

output_filename = '../data/gameData.csv'
input_filename = '../data/tournamentList.csv'

def get_event_list(csv_file_path):
    second_column_values = []
    with open(csv_file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) > 1:
                second_column_values.append(row[1])
    return second_column_values[1:]


with open(output_filename, mode='w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['Event', 'Team 1', "Team 1 ID", 'Team 2', 'Team 2 ID', 'Record', 'Stage', 'Patch', 'Date'])

    writer_lock = threading.Lock()
    threads = []
    chunk_size = 20

    event_list_total = get_event_list(input_filename)

    print(event_list_total)

    for event_chunk in chunked_event_list(event_list_total, chunk_size):
        thread = run_write_match_stats_in_thread(event_chunk, writer_lock, writer)
        threads.append(thread)

    for thread in threads:
        thread.join()