import csv
import time

import requests
from bs4 import BeautifulSoup

# URL of the page to scrape
base_url = 'https://gol.gg'
list_url = f'{base_url}/players/list/season-S14/split-Spring/tournament-ALL/'

# Headers to mimic a browser visit
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}


def get_soup(url_url):
    response_url = requests.get(url_url, headers=headers)
    response_url.raise_for_status()
    return BeautifulSoup(response_url.text, 'html.parser')


# Parse the initial list of players
soup = get_soup(list_url)
players_table = soup.find('table', class_='table_list')
player_links = []

player_names = []

for row in players_table.find_all('tr')[1:]:  # Skip the header
    cols = row.find_all('td')
    raw_name = str(cols[0].find('a'))
    name = raw_name[raw_name.find('>') + 1: raw_name.find('</')]

    player_names.append(name)

    if cols:
        # Concatenate the base URL with the href attribute of the anchor tag within the first column
        player_link = base_url + "/players" + str(cols[0].find('a')['href'])[1:]
        player_links.append(player_link)

# Print all player profile links
# for link in player_links:
#     print(link)

contents = []

name_counter = 0

player_names = player_names[:3]
player_links = player_links[:3]

for link in player_links:
    for season in range(11, 15):
        for split in range(1, 3):

            if season == 14 and split == 2:
                continue

            split_name = "None"

            if split == 1:
                split_name = "Spring"
            elif split == 2:
                split_name = "Summer"

            player_url_number = link[link.find('player-stats/') + 13: link.find('/season')]
            # print(player_url_number)

            # Step 1: Fetch the webpage content with headers
            url = "https://gol.gg/players/player-stats/" + player_url_number + "/season-S" + str(
                season) + "/split-" + str(split_name) + "/tournament-ALL/"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
            }
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                raise Exception(f"Failed to load page {url}")
            html_content = response.content

            # Step 2: Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            tables = soup.find_all('table')

            data = [str(player_names[name_counter]) + " S" + str(season) + " " + str(split_name)]


            def tableContainsTitle(table, text):
                th = table.find_all('th')
                if (th and th[0]):
                    if (text.lower() in th[0].get_text().lower()):
                        return True
                return False


            # Step 3: Extract the general stats
            generalTable = [t for t in tables if tableContainsTitle(t, "GENERAL STATS")]
            if (len(generalTable) == 1):
                generalKeys = ['Record', 'KDA', 'CS Per Minute', 'Gold per minute', 'Gold%', 'Kill Participation']
                for key in generalKeys:
                    val = '-'
                    for row in generalTable[0].find_all('tr')[1:]:
                        entries = row.find_all('td')
                        if (len(entries) >= 2 and entries[0].get_text().lower().startswith(key.lower())):
                            val = entries[1].get_text().replace(u'\xa0', u'')
                            break
                    data.append(val)

            # print(data[1])
            temp_data = data[0]
            if data[1] == "0W - 0L":
                data.clear()
                for i in range(0, 21):
                    if i == 0:
                        data.append(temp_data)
                    else:
                        data.append('-')

            # Step 4: Extract the aggression stats
            aggressionTable = [t for t in tables if tableContainsTitle(t, "AGGRESSION")]
            if (len(aggressionTable) == 1):
                aggressionKeys = ['Damage Per Minute', 'Damage%', 'K+A Per Minute', 'Solo Kills', 'Penta Kills']
                for key in aggressionKeys:
                    val = '-'
                    for row in aggressionTable[0].find_all('tr')[1:]:
                        entries = row.find_all('td')
                        if (len(entries) >= 2 and entries[0].get_text().lower().startswith(key.lower())):
                            val = entries[1].get_text().replace(u'\xa0', u'')
                            break
                    data.append(val)

            # Step 5: Extract the champion stats
            tables = soup.find_all('table', class_="table_list")

            for table in tables:
                if tableContainsTitle(table, "Champion"):
                    rows = table.find_all('tr')

                    # print(rows)
                    for i in range(1, len(rows)):

                        if i > 6:
                            break
                        if i % 2 == 1:
                            td_list = rows[i].find_all('td')

                            time.sleep(1)
                            name = td_list[0].find('img')['alt']
                            data.append(name)

                            games = td_list[1].text.strip()
                            data.append(games)

                            winrate = td_list[2].text.strip()
                            data.append(winrate)

            if len(data) < 21:
                for i in range(21 - len(data)):
                    data.append('-')

            # print(champion_stats)
            contents.append({
                'Name': data[0],
                'Record': data[1],
                'KDA': data[2],
                'CSPM': data[3],
                'GPM': data[4],
                'Gold %': data[5],
                'Kill Participation %': data[6],
                'Damage Per Minute': data[7],
                'Damage %': data[8],
                'K+A/M': data[9],
                'Solo Kills': data[10],
                'Penta Kills': data[11],
                'Champion A': data[12],
                'Games A': data[13],
                'Winrate A': data[14],
                'Champion B': data[15],
                'Games B': data[16],
                'Winrate B': data[17],
                'Champion C': data[18],
                'Games C': data[19],
                'Winrate C': data[20],
            })
            print(data)

    name_counter += 1

# Defining the CSV file path
csv_file_path = '../data/playerHistory.csv'

# Writing data to CSV
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.DictWriter(file,
                            fieldnames=['Name', 'Record', 'KDA', 'CSPM', 'GPM', 'Gold %',
                                        'Kill Participation %', 'Damage Per Minute', 'Damage %',
                                        'K+A/M', 'Solo Kills', 'Penta Kills', 'Champion A', 'Games A',
                                        'Winrate A', 'Champion B', 'Games B', 'Winrate B',
                                        'Champion C', 'Games C', 'Winrate C'])
    writer.writeheader()
    writer.writerows(contents)
