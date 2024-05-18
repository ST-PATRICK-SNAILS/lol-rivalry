import requests
from bs4 import BeautifulSoup
import csv

splits = [
    {"name": "season-S14/split-Spring/", "suffix": "S14 Spring"},
    {"name": "season-S13/split-Summer/", "suffix": "S13 Summer"},
    {"name": "season-S13/split-Spring/", "suffix": "S13 Spring"},
    {"name": "season-S12/split-Summer/", "suffix": "S12 Summer"},
    {"name": "season-S12/split-Spring/", "suffix": "S12 Spring"},
    {"name": "season-S11/split-Summer/", "suffix": "S11 Summer"},
    {"name": "season-S11/split-Spring/", "suffix": "S11 Spring"},
]

def write_to_csv(data, filename='../data/orgIds.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Team Name', 'Team ID'])
        writer.writerows(data)

def get_team_data(split):
    name, suffix = split["name"], split["suffix"]
    teams_list_url = f"https://gol.gg/teams/list/{name}tournament-ALL/"

    # Headers to mimic a browser visit
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.get(teams_list_url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')
    team_table = soup.find_all('table', class_="playerslist")[0]
    
    data = list(map(lambda i: [f"{i.get_text()} {suffix}", i['href'].split('/')[2]], list(team_table.find_all('a'))))
    return data
    
def main():
    teams_data = []
    for split in splits:
        for item in get_team_data(split):
            teams_data.append(item)
        
    write_to_csv(teams_data)
    print("Data has been written to teams_data.csv")

if __name__ == "__main__":
    main()