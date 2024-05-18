import csv
import requests

def get_tournament_data(season):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    form_data = {
        'season': f'S{season}'
    }
    response = requests.post("https://gol.gg/tournament/ajax.trlist.php", headers=headers, data=form_data)
    response.raise_for_status()

    return response.json()

def write_to_csv(data, filename='../data/tournamentList.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Season', 'Tournament Name', 'Region', 'Games', 'Average Time', 'First Game', 'Last Game'])
        writer.writerows(data)
      
def main():
    rows = []
    keys = ['trname', 'region', 'nbgames', 'avgtime', 'firstgame', 'lastgame']
    for i in range(11, 15):
        for tournament in get_tournament_data(i):
            data = [f"S{i}"]
            for key in keys:
                for entry in tournament.items():
                    if len(entry) == 2 and entry[0] == key:
                        data.append(entry[1])
                        break
                else:
                    data.append('-')
            rows.append(data)
    write_to_csv(rows)
    print("Data has been written to tournament_list.csv")
        
if __name__ == "__main__":
    main()