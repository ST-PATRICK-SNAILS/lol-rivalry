import requests
from bs4 import BeautifulSoup
import csv
import threading
import os

events_list_2023 = [
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
]

def write_match_stats(year, writer):

    event_list = []

    if year == 2023:
        event_list = events_list_2023

    for event in event_list[0:5]:

        sub_url = ''

        for word in event.split(' '):
            sub_url += word + "%20"

        url = f"https://gol.gg/tournament/tournament-matchlist/{sub_url[-3:] + '/'}"

        print(sub_url[:-3] + '/')

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # table = soup.find('table', class_='table_list')
        
        print(soup)
        print('out loop')

        # for row in table.find('tbody').find_all('tr')[1:]:

        #     print('in loop')

        #     td_list = row.find_all('td')

        #     team1Name = td_list[1]
        #     team2Name = td_list[3]
        #     record = td_list[2]
        #     stage = td_list[4]
        #     patch = td_list[5]
        #     date = td_list[6]

        #     print([event, team1Name, team2Name, record, stage, patch, date])

        #     writer.writerow([event, team1Name, team2Name, record, stage, patch, date])

output_filename = '../data/gameData.csv'

with open(output_filename, mode='w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['Event', 'Team 1', "Team 1 ID", 'Team 2', 'Team 2 ID', 'Record', 'Stage', 'Patch', 'Date'])

    write_match_stats(2023, writer)