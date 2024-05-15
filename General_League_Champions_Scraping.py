import csv

import requests
from bs4 import BeautifulSoup

data = []

for season in range(11, 15):
    for split in range(1, 3):

        if season == 14 and split == 2:
            continue

        split_name = "None"

        if split == 1:
            split_name = "Spring"
        elif split == 2:
            split_name = "Summer"

        # URL of the page to scrape
        url = "https://gol.gg/champion/list/season-S" + str(season) + "/split-" + str(split_name) + "/tournament-ALL/"

        # Headers to mimic a browser visit
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        # Sending a GET request to the URL with headers
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Ensures we notice bad responses

        # Parsing the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Finding the table containing the data
        champions_table = soup.find('table', class_='table_list')

        # Parsing each row in the table
        for row in champions_table.find_all('tr')[1:]:  # skipping the header row
            cols = row.find_all('td')
            if cols:
                champion_name = cols[0].text.strip()
                picks = cols[1].text.strip()
                bans = cols[2].text.strip()
                presence = cols[3].text.strip()
                wins = cols[4].text.strip()
                losses = cols[5].text.strip()
                win_rate = cols[6].text.strip()
                kda = cols[7].text.strip()
                avg_bt = cols[8].text.strip()
                avg_gt = cols[9].text.strip()
                csm = cols[10].text.strip()
                dpm = cols[11].text.strip()
                gpm = cols[12].text.strip()
                data.append({
                    'Champion': champion_name + " S" + str(season) + " " + str(split_name),
                    'Picks': picks,
                    'Bans': bans,
                    'Presence': presence,
                    'Wins': wins,
                    'Losses': losses,
                    'Win Rate': win_rate,
                    'KDA': kda,
                    'Avg BT': avg_bt,
                    'Avg GT': avg_gt,
                    'CSM': csm,
                    'DPM': dpm,
                    'GPM': gpm
                })


# Defining the CSV file path
csv_file_path = 'General_League_Champions_Scraping.csv'

# Writing data to CSV
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.DictWriter(file,
                            fieldnames=['Champion', 'Picks', 'Bans', 'Presence', 'Wins', 'Losses', 'Win Rate', 'KDA',
                                        'Avg BT', 'Avg GT', 'CSM', 'DPM', 'GPM'])
    writer.writeheader()
    writer.writerows(data)
