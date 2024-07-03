import csv

import requests
from bs4 import BeautifulSoup

data = []

def get_champion_data(season, split):
    # URL of the page to scrape
    url = f"https://gol.gg/champion/list/season-S{season}/split-{split}/tournament-ALL/"

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

    rows = champions_table.find_all('tr')
    data = []
    
    for row in rows[1:]:
        cols = row.find_all('td')
        link = cols[0].find('a')
        row_data = [f"S{season}", split, link.get_text().strip(), link['href'].split('/')[2]]
        for col in cols[1:]:
            text = col.get_text().strip()
            if text:
                row_data.append(col.get_text().strip())
            else: row_data.append('-')
        data.append(row_data)
        
    return data


# Defining the CSV file path
csv_file_path = '../data/champions.csv'

# Writing data to CSV
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Season', 'Split', 'Champion', 'Champion ID', 'Picks', 'Bans', 'Presence', 'Wins', 'Losses', 'Win Rate', 'KDA',
                                        'Avg BT', 'Avg GT', 'CSM', 'DPM', 'GPM', 'CSD@15', 'GD@15', 'XPD@15'])
    for season in range(11, 15):
        for split in ["Spring", "Summer"]:
            for champ in get_champion_data(season, split):
                writer.writerow(champ)
    
    print("Data written to champions.csv")
