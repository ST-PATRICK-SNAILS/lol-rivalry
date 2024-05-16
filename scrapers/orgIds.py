import requests
from bs4 import BeautifulSoup
import csv

base_url = "https://gol.gg"
teams_list_url = f"{base_url}/teams/list/season-S14/split-Spring/tournament-ALL/"

def write_to_csv(data, filename='../data/orgIds.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Team Name', 'Team ID'])
        writer.writerows(data)

def get_team_data(teams_list_url):

    # Headers to mimic a browser visit
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.get(teams_list_url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')
    team_table = soup.find_all('table', class_="playerslist")[0]
    
    data = list(map(lambda i: [i.get_text(), i['href'].split('/')[2]], list(team_table.find_all('a'))))
    write_to_csv(data)
    
def main():
    get_team_data(teams_list_url)

    print("Data has been written to teams_data.csv")

if __name__ == "__main__":
    main()