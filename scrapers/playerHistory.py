import csv
import time
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed


def get_soup(url_url):
    response_url = requests.get(url_url, headers=headers)
    response_url.raise_for_status()
    return BeautifulSoup(response_url.text, 'html.parser')


player_links = []
player_names = []

# Loop through all seasons and extract player links and names
for season in range(11, 15):
    # URL of the page to scrape
    list_url = f'https://gol.gg/players/list/season-S' + str(season) + '/split-ALL/tournament-ALL/'

    # Headers to mimic a browser visit
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # Parse the initial list of players
    soup = get_soup(list_url)
    players_table = soup.find('table', class_='table_list')

    for row in players_table.find_all('tr')[1:]:  # Skip the header
        cols = row.find_all('td')
        raw_name = str(cols[0].find('a'))
        name = raw_name[raw_name.find('>') + 1: raw_name.find('</')]
        if name not in player_names:
            player_names.append(name)
            if cols:
                player_link = "https://gol.gg/players" + str(cols[0].find('a')['href'])[1:]
                player_links.append(player_link)

# print(player_links)
# print(len(player_links))
# print(len(player_names))

# Limiting the player names and links for testing purposes
# player_names = player_names[:15]
# player_links = player_links[:15]

def scrape_player_data(link, name_counter):
    contents = []
    for season in range(11, 15):
        for split in range(1, 3):
            if season == 14 and split == 2:
                continue

            split_name = "Spring" if split == 1 else "Summer"
            player_url_number = link[link.find('player-stats/') + 13: link.find('/season')]
            url = f"https://gol.gg/players/player-stats/{player_url_number}/season-S{season}/split-{split_name}/tournament-ALL/"
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                continue
            soup = BeautifulSoup(response.content, 'html.parser')
            tables = soup.find_all('table')

            data = [str(player_names[name_counter]) + " S" + str(season) + " " + str(split_name)]

            def table_contains_title(table, text):
                th = table.find_all('th')
                return th and th[0] and text.lower() in th[0].get_text().lower()

            general_table = [t for t in tables if table_contains_title(t, "GENERAL STATS")]
            if general_table:
                general_keys = ['Record', 'KDA', 'CS Per Minute', 'Gold per minute', 'Gold%', 'Kill Participation']
                for key in general_keys:
                    val = '-'
                    for row in general_table[0].find_all('tr')[1:]:
                        entries = row.find_all('td')
                        if len(entries) >= 2 and entries[0].get_text().lower().startswith(key.lower()):
                            val = entries[1].get_text().replace(u'\xa0', u'')
                            break
                    data.append(val)

            temp_data = data[0]
            if data[1] == "0W - 0L":
                data = [temp_data] + ['-'] * 20

            aggression_table = [t for t in tables if table_contains_title(t, "AGGRESSION")]
            if aggression_table:
                aggression_keys = ['Damage Per Minute', 'Damage%', 'K+A Per Minute', 'Solo Kills', 'Penta Kills']
                for key in aggression_keys:
                    val = '-'
                    for row in aggression_table[0].find_all('tr')[1:]:
                        entries = row.find_all('td')
                        if len(entries) >= 2 and entries[0].get_text().lower().startswith(key.lower()):
                            val = entries[1].get_text().replace(u'\xa0', u'')
                            break
                    data.append(val)

            champion_table = soup.find_all('table', class_="table_list")
            for table in champion_table:
                if table_contains_title(table, "Champion"):
                    rows = table.find_all('tr')
                    for i in range(1, min(len(rows), 7)):
                        if i % 2 == 1:
                            td_list = rows[i].find_all('td')
                            name = td_list[0].find('img')['alt']
                            data.append(name)
                            data.append(td_list[1].text.strip())
                            data.append(td_list[2].text.strip())

            data += ['-'] * (21 - len(data))

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

    print(contents)
    return contents


def main():
    all_contents = []
    with ThreadPoolExecutor(max_workers=300) as executor:
        futures = [executor.submit(scrape_player_data, link, name_counter) for name_counter, link in
                   enumerate(player_links)]
        for future in as_completed(futures):
            all_contents.extend(future.result())

    # Defining the CSV file path
    csv_file_path = '../data/playerHistory.csv'

    # Writing data to CSV
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=[
            'Name', 'Record', 'KDA', 'CSPM', 'GPM', 'Gold %', 'Kill Participation %',
            'Damage Per Minute', 'Damage %', 'K+A/M', 'Solo Kills', 'Penta Kills',
            'Champion A', 'Games A', 'Winrate A', 'Champion B', 'Games B',
            'Winrate B', 'Champion C', 'Games C', 'Winrate C'
        ])
        writer.writeheader()
        writer.writerows(all_contents)


if __name__ == '__main__':
    main()
