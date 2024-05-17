import requests
from bs4 import BeautifulSoup
import csv

# URL of the page with the list of players
base_url = "https://gol.gg"

# Function to get player data
def get_player_data(players_list_url):

    # Headers to mimic a browser visit
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.get(players_list_url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    players_data = []

    # Find the table with players
    table = soup.find('table', class_='table_list')

    # Iterate through all rows in the table
    for row in table.find_all('tr')[1:]:
        # Find the player's name and the link to their stats page

        td_tag = row.find_all('td')[0]

        player_name = td_tag.text.strip()
        player_link = td_tag.find('a')['href']

        # Extract the playerID from the URL
        player_id = player_link.split('/')[2]

        # Append the player name and playerID to the list
        players_data.append([player_name, player_id])

    return players_data

# Function to write data to CSV
def write_to_csv(data, filename='../data/playerIds.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Player Name', 'Player ID'])
        writer.writerows(data)

# Main function
def main():
    players = {}
    for i in range(11, 15):
        for pair in get_player_data(f"{base_url}/players/list/season-S{i}/split-ALL/tournament-ALL/"):
            players[pair[0]] = pair[1]
            
    data = list(players.items())
    data.sort(key=lambda x:x[0])
            
    write_to_csv(data)

    print("Data has been written to players_data.csv")

if __name__ == "__main__":
    main()
