import requests
from bs4 import BeautifulSoup
import csv

def get_team_page(id):

    # Headers to mimic a browser visit
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.get("", headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')
    team_table = soup.find_all('table', class_="playerslist")[0]