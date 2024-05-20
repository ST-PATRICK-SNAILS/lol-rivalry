import csv
from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd

could_not_find = 0
could_not_find_teams = []

def convert_time_to_seconds(time_string):

    try:
        parts = time_string.split(':')

        minutes = int(parts[0])
        seconds = int(parts[1])

        total_seconds = minutes * 60 + seconds

        return total_seconds
    
    except (ValueError, IndexError):

        # Handle cases where the string is not properly formatted
        print("Error processing the time. Ensure it is in the format 'MM:SS'.")
        exit()

def percentage_to_decimal(percentage_string):

    try:
        numeric_part = percentage_string.replace('%', '').strip()

        percentage_value = float(numeric_part)

        decimal_value = percentage_value / 100

        return decimal_value
    
    except ValueError:

        # Handle cases where the conversion might fail
        print("Error processing the percentage. Ensure it is a valid percentage string like 'XX%'.")
        exit()

# Record passed in following "W - L" format
def calculate_win_rate(record):

    try:
        parts = record.split('-')

        wins = int(parts[0].strip().replace('W', '').strip())

        losses = int(parts[1].strip().replace('L', '').strip())

        total_games = wins + losses

        win_rate = wins / total_games

        return win_rate
    
    except (ValueError, IndexError):

        # Handle cases where the string format is incorrect or conversion fails
        print("Error processing the record. Ensure it is in the format 'XXW - YYL'.")
        print("Record: ", record)

        # Note that values resulting in an error should NEVER return 0.5
        return None
