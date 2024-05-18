import requests
from bs4 import BeautifulSoup
import csv
import threading
from itertools import islice

event_list_total = [
    "MSI 2024",
    "LCO Split 1 Playoffs 2024",
    "CBLOL Academy Split 1 Playoffs 2024",
    "EMEA Masters Spring 2024",
    "CBLOL Split 1 Playoffs 2024",
    "LPL Spring Playoffs 2024",
    "EMEA Masters Spring Play-In 2024",
    "LEC Spring Playoffs 2024",
    "LCK Spring Playoffs 2024",
    "LVP SL 2nd Div Spring Playoffs 2024",
    "LCK CL Spring Playoffs 2024",
    "Prime League Spring Playoffs 2024",
    "GLL Spring Playoffs 2024",
    "Prime League 2nd Div Spring Playoffs 2024",
    "LFL Div2 Spring Playoffs 2024",
    "PCS Spring Playoffs 2024",
    "VCS Spring Playoffs 2024",
    "LLA Opening Playoffs 2024",
    "LPLOL Spring Playoffs 2024",
    "Arabian League Spring Playoffs 2024",
    "LFL Spring Playoffs 2024",
    "LVP SL Spring Playoffs 2024",
    "TCL Playoffs Spring 2024",
    "EBL Spring Playoffs 2024",
    "TCL Div2 Winter Playoffs 2024",
    "NACL Spring Playoffs 2024",
    "LCS Spring Playoffs 2024",
    "Elite Series Spring Playoffs 2024",
    "Hitpoint Masters Spring Playoffs 2024",
    "LIT Spring Playoffs 2024",
    "NLC Spring Playoffs 2024",
    "LPL Spring 2024",
    "LEC Spring Season 2024",
    "LCK Spring 2024",
    "Ultraliga Spring Playoffs 2024",
    "LCK CL Spring 2024",
    "Arabian League Spring 2024",
    "CBLOL Split 1 2024",
    "LFL Div2 Spring 2024",
    "LVP SL 2nd Div Spring 2024",
    "LVP SL Spring 2024",
    "LFL Spring 2024",
    "GLL Spring 2024",
    "TCL Div2 Winter 2024",
    "Prime League Spring 2024",
    "Prime League 2nd Div Spring 2024",
    "LCS Spring 2024",
    "VCS Spring 2024",
    "NACL Spring 2024",
    "Hitpoint Masters Spring 2024",
    "TCL Spring 2024",
    "EBL Spring 2024",
    "LIT Spring 2024",
    "LPLOL Spring 2024",
    "Elite Series Spring 2024",
    "NLC Spring 2024",
    "CBLOL Academy Split 1 2024",
    "PCS Spring 2024",
    "LJL Spring Playoffs 2024",
    "LLA Opening 2024",
    "Ultraliga Spring 2024",
    "LCO Split 1 2024",
    "LJL Spring 2024",
    "LEC Winter Playoffs 2024",
    "LEC Winter Season 2024",
    "Demacia Cup 2023"
    "Worlds Main Event 2023",
    "Worlds Play-In 2023",
    "Worlds Qualifying Series 2023",
    "LFL Promotion 2024",
    "SuperLiga Promotion 2024",
    "Prime League Promotion 2024",
    "LFL Promotion 2024",
    "LEC Season Finals 2023",
    "CBLOL Split 2 Playoffs 2023",
    "PCS Summer Playoffs 2023",
    "VCS Summer Playoffs 2023",
    "EMEA Masters Summer 2023",
    "CBLOL Academy Split 2 Playoffs 2023",
    "LCK Regional Finals 2023",
    "LLA Closing Playoffs 2023",
    "LCK CL Summer Playoffs 2023",
    "LCK Summer Playoffs 2023",
    "LCS Championship 2023",
    "LJL Summer Playoffs 2023",
    "EMEA Masters Play-In Summer 2023",
    "LFL Div2 Summer Playoffs 2023",
    "EBL Summer Playoffs 2023",
    "Elite Series Summer Playoffs 2023",
    "Prime League Summer Playoffs 2023",
    "SuperLiga Summer Playoffs 2023",
    "TCL Summer Playoffs 2023",
    "Ultraliga Season 10 Playoffs 2023",
    "Arabian League Summer Playoffs 2023",
    "LFL Summer Playoffs 2023",
    "SuperLiga 2nd Div Summer Playoffs 2023",
    "NACL Summer Playoffs 2023",
    "Prime League 2nd Div Summer Playoffs 2023",
    "CBLOL Academy Split 2 2023",
    "LPL Regional Finals 2023",
    "PCS Summer 2023",
    "CBLOL Split 2 2023",
    "LCK Summer 2023",
    "VCS Summer 2023",
    "GLL Summer Playoffs 2023",
    "Hitpoint Masters Summer Playoffs 2023",
    "LPL Summer Playoffs 2023",
    "LPLOL Summer Playoffs 2023",
    "NLC Summer Playoffs 2023",
    "PG Nationals Summer Playoffs 2023",
    "LCK CL Summer 2023",
    "LCO Split 2 Playoffs 2023",
    "LEC Summer Playoffs 2023",
    "LFL Summer 2023",
    "Arabian League Summer 2023",
    "LEC Summer Groups 2023",
    "EBL Summer 2023",
    "Hitpoint Masters Summer 2023",
    "LCS Summer 2023",
    "LFL Div2 Summer 2023",
    "PG Nationals Summer 2023",
    "Prime League Summer 2023",
    "SuperLiga 2nd Div Summer 2023",
    "TCL Summer 2023",
    "Elite Series Summer 2023",
    "SuperLiga Summer 2023",
    "Ultraliga Season 10 2023",
    "LLA Closing 2023",
    "NLC Summer 2023",
    "Prime League 2nd Div Summer 2023",
    "LPL Summer 2023",
    "NACL Summer 2023",
    "LJL Summer 2023",
    "LPLOL Summer 2023",
    "GLL Summer 2023",
    "LCO Split 2 2023",
    "LEC Summer 2023",
    "MSI 2023",
    "EMEA Masters Spring 2023",
    "LCO Split 1 Stage 2 2023",
    "LEC Spring Playoffs 2023",
    "VCS Spring Playoffs 2023",
    "CBLOL Academy Split 1 Playoffs 2023",
    "LEC Spring Groups 2023",
    "CBLOL Split 1 Playoffs 2023",
    "LJL Spring Playoffs 2023",
    "LPL Spring Playoffs 2023",
    "LLA Opening Playoffs 2023",
    "VCS Spring 2023",
    "LCK Spring Playoffs 2023",
    "LCS Spring Playoffs 2023",
    "PCS Spring Playoffs 2023",
    "EMEA Masters Spring Play-In 2023",
    "LCK CL Spring Playoffs 2023",
    "SuperLiga 2nd Div Spring Playoffs 2023",
    "LFL Div2 Spring Playoffs 2023",
    "NACL Spring Playoffs 2023",
    "EBL Spring Playoffs 2023",
    "GLL Spring Playoffs 2023",
    "LPLOL Spring Playoffs 2023",
    "Prime League Spring Playoffs 2023",
    "SuperLiga Spring Playoffs 2023",
    "TCL Spring Playoffs 2023",
    "Hitpoint Masters Spring Playoffs 2023",
    "LFL Spring Playoffs 2023",
    "PG Nationals Spring Playoffs 2023",
    "Ultraliga Season 9 Playoffs 2023",
    "Arabian League Spring Playoffs 2023",
    "Elite Series Spring Playoffs 2023",
    "Prime League 2nd Div Spring Playoffs 2023",
    "NLC Spring Playoffs 2023",
    "LEC Spring Season 2023",
    "LJL Spring 2023",
    "LPL Spring 2023",
    "CBLOL Academy Split 1 2023",
    "CBLOL Split 1 2023",
    "LCK Spring 2023",
    "Hitpoint Masters Spring 2023",
    "LCK CL 2023 Spring",
    "LCS Spring 2023",
    "SuperLiga 2nd Div Spring 2023",
    "TCL Spring 2023",
    "LFL Spring 2023",
    "Prime League Spring 2023",
    "PCS Spring 2023",
    "Arabian League Spring 2023",
    "EBL Spring 2023",
    "LFL Div2 Spring 2023",
    "LPLOL Spring 2023",
    "NLC Spring 2023",
    "PG Nationals Spring 2023",
    "Elite Series Spring 2023",
    "SuperLiga Spring 2023",
    "GLL Spring 2023",
    "LLA Opening 2023",
    "Ultraliga Season 9 2023",
    "NACL Spring 2023",
    "Prime League 2nd Div Spring 2023",
    "LEC Winter Playoffs 2023",
    "LEC Winter Groups 2023",
    "LCO Split 1 2023",
    "LEC Winter 2023"
    "World Championship 2022",
    "World Championship Play-In 2022",
    "EU Masters Summer 2022",
    "LFL Promotion 2023",
    "LCS Championship 2022",
    "LEC Summer Playoffs 2022",
    "CBLOL Academy Split 2 Playoffs 2022",
    "TCL Summer Playoffs 2022",
    "LCO Split 2 Playoffs 2022",
    "LJL Summer Playoffs 2022",
    "LPL Regional Finals 2022",
    "PCS Summer Playoffs 2022",
    "VCS Summer Playoffs 2022",
    "CBLOL Split 2 Playoffs 2022",
    "LCK Regionals Finals 2022",
    "LPL Summer Playoffs 2022",
    "LCS Proving Grounds Summer 2022",
    "LCK Summer Playoffs 2022",
    "EU Masters Summer Play-In 2022",
    "LLA Closing Playoffs 2022",
    "LCK CL Summer Playoffs 2022",
    "Hitpoint Masters Summer Playoffs 2022",
    "VCS Summer 2022",
    "NLC Summer Playoffs 2022",
    "Prime League Summer Playoffs 2022",
    "LVP SL Summer Playoffs 2022",
    "LFL Summer Playoffs 2022",
    "LJL Summer 2022",
    "Turkey Academy Summer Playoffs 2022",
    "Ultraliga Season 8 Playoffs",
    "LFL Div2 Summer Playoffs 2022",
    "LVP2 Summer Playoffs 2022",
    "LCK Summer 2022",
    "LCS Summer 2022",
    "LEC Summer 2022",
    "LPL Summer 2022",
    "TCL Summer 2022",
    "EBL Summer Playoffs 2022",
    "LCK CL Summer 2022",
    "Turkey Academy Summer 2022",
    "CBLOL Academy Split 2 2022",
    "LCO Split 2 2022",
    "CBLOL Split 2 2022",
    "Elite Series Summer Playoffs 2022",
    "LPLOL Summer Playoffs 2022",
    "PCS Summer 2022",
    "PG Nationals Summer Playoffs 2022",
    "GLL Summer Playoffs 2022",
    "LLA Closing 2022",
    "Prime League Summer 2022",
    "NA Academy Summer 2022",
    "Hitpoint Masters Summer 2022",
    "LFL Summer 2022",
    "LVP SL Summer 2022",
    "NLC Summer 2022",
    "LVP2 Summer 2022",
    "Ultraliga Season 8",
    "LFL Div2 Summer 2022",
    "LPLOL Summer 2022",
    "EBL Summer 2022",
    "Elite Series Summer 2022",
    "PG Nationals Summer 2022",
    "GLL Summer 2022",
    "MSI 2022",
    "EU Masters Spring 2022",
    "LCS Spring Playoffs 2022",
    "VCS Spring Playoffs 2022",
    "CBLOL Split 1 Playoffs 2022",
    "LPL Spring Playoffs 2022",
    "PCS Spring Playoffs 2022",
    "CBLOL Academy Split 1 Playoffs 2022",
    "LLA Opening Playoffs 2022",
    "LCS Proving Grounds Spring 2022",
    "VCS Spring 2022",
    "LCO Sprit 1 Playoffs 2022",
    "LEC Spring Playoffs 2022",
    "LJL Spring Playoffs 2022",
    "TCL Winter Playoffs 2022",
    "EU Masters Spring Play-In 2022",
    "LFL Div2 Spring Playoffs 2022",
    "LCK Spring Playoffs 2022",
    "LCK CL Spring Playoffs 2022",
    "LFL Spring Playoffs 2022",
    "NLC Spring Playoffs 2022",
    "LVP SL Spring Playoffs 2022",
    "Ultraliga Season 7 Playoffs",
    "LCS Spring 2022",
    "LJL Spring 2022",
    "LPL Spring 2022",
    "CBLOL Academy Split 1 2022",
    "Turkey Academy Winter Playoffs 2022",
    "LCO Split 1 2022",
    "CBLOL Split 1 2022",
    "GLL Spring Playoffs 2022",
    "Hitpoint Masters Spring Playoffs 2022",
    "LCK Spring 2022",
    "PCS Spring 2022",
    "PG Nationals Spring Playoffs 2022",
    "Prime League Spring Playoffs 2022",
    "TCL Winter 2022",
    "EBL Spring Playoffs 2022",
    "Elite Series Spring Playoffs 2022",
    "LCK CL Spring 2022",
    "LPLOL Spring Playoffs 2022",
    "Turkey Academy Winter 2022",
    "LFL Div2 Spring 2022",
    "LLA Opening 2022",
    "NA Academy Spring 2022",
    "LFL Spring 2022",
    "LVP SL Spring 2022",
    "NLC Spring 2022",
    "Ultraliga Season 7",
    "LEC Spring 2022",
    "EBL Spring 2022",
    "Hitpoint Masters Spring 2022",
    "Elite Series Spring 2022",
    "LPLOL Spring 2022",
    "PG Nationals Spring 2022",
    "GLL Spring 2022",
    "Prime League Spring 2022",
    "LCL Spring 2022",
    "LCS Lock In 2022"
    "Demacia Cup 2021",
    "Kespa Cup 2021",
    "VCS Winter Playoffs 2021",
    "VCS Winter 2021",
    "GLL Winter Playoffs 2021",
    "GLL Winter 2021",
    "Prime League Winter Cup 2021",
    "LPLOL Grand Final 2021",
    "World Championship 2021",
    "World Championship Play-In 2021",
    "LFL Finals 2021",
    "LCS Proving Grounds Summer 2021",
    "LFL Promotion 2021",
    "EU Masters Summer 2021",
    "LJL Academy Playoffs 2021",
    "LJL Academy 2021",
    "LJL Summer Playoffs 2021",
    "LPL Regional Finals 2021",
    "CBLOL Split 2 Playoffs 2021",
    "LCL Summer Playoffs 2021",
    "TCL Summer Playoffs 2021",
    "LCK Regional Finals 2021",
    "LPL Summer Playoffs 2021",
    "LCO Split 2 Playoffs 2021",
    "LCS Championship 2021",
    "LEC Summer Playoffs 2021",
    "PCS Summer Playoffs 2021",
    "CBLOL Academy Split 2 Playoffs 2021",
    "LCK Summer Playoffs 2021",
    "LLA Closing Playoffs 2021",
    "LCK CL Summer Playoffs 2021",
    "LFL Div2 Summer Playoffs 2021",
    "EU Masters Summer Play-In 2021",
    "NA Academy Summer Playoffs 2021",
    "LFL Div2 Summer 2021",
    "LCK Summer 2021",
    "LFL Summer Playoffs 2021",
    "LVP Summer Playoffs 2021",
    "Baltic Masters Summer Playoffs 2021",
    "LCO Split 2 2021",
    "Ultraliga Season 6 Playoffs",
    "Dutch League Summer Playoffs 2021",
    "LCK CL Summer 2021",
    "Belgian League Summer Playoffs 2021",
    "Hitpoint Masters Summer Playoffs 2021",
    "LCL Summer 2021",
    "LLA Closing 2021",
    "LPL Summer 2021",
    "NLC Summer Playoffs 2021",
    "PCS Summer 2021",
    "Prime League Summer Playoffs 2021",
    "TCL Summer 2021",
    "PG Nationals Summer Playoffs 2021",
    "CBLOL Academy Split 2 2021",
    "LJL Summer 2021",
    "LPLOL Summer Playoffs 2021",
    "CBLOL Split 2 2021",
    "LCS Summer 2021",
    "LEC Summer 2021",
    "EBL Season 9",
    "NA Academy Summer 2021",
    "LVP SL Summer 2021",
    "LFL Summer 2021",
    "GLL Summer Playoffs 2021",
    "Prime League Summer 2021",
    "LPLOL Summer 2021",
    "Ultraliga Season 6",
    "Baltic Masters Summer 2021",
    "Dutch League Summer 2021",
    "NLC Summer 2021",
    "Belgian League Summer 2021",
    "Hitpoint Masters 2021 Summer",
    "PG Nationals Summer 2021",
    "GLL Summer 2021",
    "Hitpoint Challengers 2021 Summer",
    "MSI 2021",
    "EU Masters Spring 2021",
    "LCS Proving Grounds Spring 2021",
    "CBLOL Split 1 Playoffs 2021",
    "LPL Spring Playoffs 2021",
    "PCS Spring Playoffs 2021",
    "VCS Spring Playoffs 2021",
    "CBLOL Academy Split 1 Playoffs 2021",
    "LCL Spring Playoffs 2021",
    "TCL Spring Playoffs 2021",
    "LCS Mid-Season Showdown 2021",
    "LEC Spring Playoffs 2021",
    "LJL Spring Playoffs 2021",
    "LCK Spring Playoffs 2021",
    "LCO Split 1 Playoffs 2021",
    "LLA Opening Playoffs 2021",
    "LCK CL Spring Playoffs 2021",
    "VCS Spring 2021",
    "EU Masters Spring Play-In 2021",
    "LCK Spring 2021",
    "LCL Spring 2021",
    "LPL Spring 2021",
    "EBL Season 8 Playoffs",
    "LCO Split 1 2021",
    "LFL Spring Playoffs 2021",
    "LVP SL Spring Playoffs 2021",
    "Hitpoint Challengers 2021 Spring Playoffs",
    "Ultraliga Season 5",
    "Dutch League Spring Playoffs 2021",
    "GLL 2021 Spring Playoffs",
    "LCK CL Spring 2021",
    "Belgian League Spring Playoffs 2021",
    "LLA Opening 2021",
    "Hitpoint Masters 2021 Spring Playoffs",
    "LPLOL Spring Playoffs 2021",
    "NLC Spring Playoffs 2021",
    "PCS Spring 2021",
    "PG Nationals Spring Playoffs 2021",
    "Prime League Spring Playoffs 2021",
    "TCL Spring 2021",
    "CBLOL Academy Split 1 2021",
    "CBLOL Split 1 2021",
    "EBL Season 8",
    "LCS Spring 2021",
    "LEC Spring 2021",
    "LFL Spring 2021",
    "LJL Spring 2021",
    "LVP Superliga Spring 2021",
    "LPLOL Spring 2021",
    "Baltic Masters Spring Playoffs 2021",
    "Hitpoint Challengers 2021 Spring",
    "Prime League Spring 2021",
    "Dutch League Spring 2021",
    "Belgian League Spring 2021",
    "Hitpoint Masters 2021 Spring",
    "Baltic Masters Spring 2021",
    "NLC Spring 2021",
    "PG Nationals Spring 2021",
    "GLL 2021 Spring",
    "NA Academy Spring 2021",
    "LCS Lock In 2021",
    "KeSPA Cup 2020",
    "Demacia Cup 2020",
    "Trinity Force Puchar Polski"
]

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
input_filename = '../data/orgIds.csv'

with open(output_filename, mode='w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['Event', 'Team 1', "Team 1 ID", 'Team 2', 'Team 2 ID', 'Record', 'Stage', 'Patch', 'Date'])

    writer_lock = threading.Lock()
    threads = []
    chunk_size = 20  # Adjust the chunk size as needed

    for event_chunk in chunked_event_list(event_list_total, chunk_size):
        thread = run_write_match_stats_in_thread(event_chunk, writer_lock, writer)
        threads.append(thread)

    for thread in threads:
        thread.join()