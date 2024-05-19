import csv
from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd

could_not_find = 0
could_not_find_teams = []


def convert_time_to_seconds(time_string):
    try:
        # Split the time string by the colon
        parts = time_string.split(':')

        # Extract minutes and seconds as integers
        minutes = int(parts[0])
        seconds = int(parts[1])

        # Calculate total seconds
        total_seconds = minutes * 60 + seconds

        return total_seconds
    except (ValueError, IndexError):
        # Handle cases where the string is not properly formatted
        print("Error processing the time. Ensure it is in the format 'MM:SS'.")
        return None


def percentage_to_decimal(percentage_string):
    try:
        # Remove the '%' character and strip any spaces
        numeric_part = percentage_string.replace('%', '').strip()

        # Convert the numeric part to a float
        percentage_value = float(numeric_part)

        # Convert percentage to a decimal
        decimal_value = percentage_value / 100

        return decimal_value
    except ValueError:
        # Handle cases where the conversion might fail
        print("Error processing the percentage. Ensure it is a valid percentage string like 'XX%'.")
        exit()


def calculate_win_rate(record):
    # print("Record: ", record)
    try:
        # Split the record string on the hyphen to separate wins from losses
        parts = record.split('-')

        # Extract the number of wins, removing 'W' and stripping spaces
        wins = int(parts[0].strip().replace('W', '').strip())

        # Extract the number of losses, removing 'L' and stripping spaces
        losses = int(parts[1].strip().replace('L', '').strip())

        # Calculate the total number of games
        total_games = wins + losses

        # Calculate the win rate
        win_rate = wins / total_games

        # print("win_rate: ", win_rate)
        return win_rate
    except (ValueError, IndexError):
        # Handle cases where the string format is incorrect or conversion fails
        print("Error processing the record. Ensure it is in the format 'XXW - YYL'.")
        print("Record: ", record)
        return 0.5


def determine_winner(score):
    try:
        # Split the score string on the hyphen
        parts = score.split('-')

        # Convert the parts to integers
        team_a_score = int(parts[0].strip())  # .strip() removes any leading/trailing spaces
        team_b_score = int(parts[1].strip())

        # Determine the winner based on the scores
        if team_a_score > team_b_score:
            return "1"
        elif team_b_score > team_a_score:
            return "0"
        else:
            return "0.5"
    except ValueError:
        # Handle cases where conversion to integer fails (e.g., "FF")
        return "0.5"
    except IndexError:
        # Handle cases where split results in less than 2 parts
        return "0.5"


def generate_row_data(orgA, orgB, season, split, event, score, field_names):
    global could_not_find
    # contents of the csv row
    contents = []

    roster_A_names = []
    roster_B_names = []

    # generate the data for the csv row
    data = [""] * len(field_names)

    input_filename = '../data/orgStats.csv'

    roster_not_found_A = True
    roster_not_found_B = True

    with open(input_filename, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:

            # print("unmodified: ", row[1])
            # print("modified: ", row[1][:-4])
            if row[3] == event and row[1][:-4] == orgA and roster_not_found_A:
                roster_not_found_A = False
                roster_A_names = row[4].split()
                print("Roster A for event " + event + ": " + row[4])

            elif row[3] == event and row[1][:-4] == orgB and roster_not_found_B:
                roster_not_found_B = False
                roster_B_names = row[4].split()
                print("Roster B for event " + event + ": " + row[4])

    if roster_not_found_A:
        print("ERROR: Could not find Team A in the orgStats.csv file for event: " + event)
        could_not_find += 1
        could_not_find_teams.append((orgA, event))

        # for i in range(0, 123):
        #     data[i] = ("Err")

        return []

    elif roster_not_found_B:
        print("ERROR: Could not find Team B in the orgStats.csv file for event: " + event)
        could_not_find += 1
        could_not_find_teams.append((orgB, event))

        # for i in range(0, 123):
        #     data[i] = ("Err")

        return []

    else:
        input_filename = '../data/playerHistory.csv'

        found_A_players = 0
        found_B_players = 0

        print(roster_A_names)
        print(roster_B_names)

        if len(roster_A_names) != 5 or len(roster_B_names) != 5:
            print("ERROR: Roster does not have 5 players.")
            exit()

        with open(input_filename, newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:

                for player in roster_A_names:
                    if row[0] == (player + " " + season + " " + split):

                        for stat_index in range(0, 12):
                            if stat_index == 0:
                                # print("winrate: " + str(calculate_win_rate(row[stat_index + 1])))
                                data[stat_index + (found_A_players * 12)] = str(calculate_win_rate(row[stat_index + 1]))
                            elif stat_index != 11:
                                if '%' in row[stat_index + 1]:
                                    data[stat_index + (found_A_players * 12)] = str(percentage_to_decimal(row[stat_index + 1]))
                                else:
                                    data[stat_index + (found_A_players * 12)] = row[stat_index + 1]
                            else:
                                data[stat_index + (found_A_players * 12)] = "1"

                        found_A_players += 1

                for player in roster_B_names:
                    if row[0] == (player + " " + season + " " + split):

                        for stat_index in range(0, 12):
                            if stat_index == 0:
                                data[stat_index + (found_B_players * 12) + 60] = str(calculate_win_rate(row[stat_index + 1]))
                            elif stat_index != 11:
                                if '%' in row[stat_index + 1]:
                                    data[stat_index + (found_B_players * 12) + 60] = str(percentage_to_decimal(row[stat_index + 1]))
                                else:
                                    data[stat_index + (found_B_players * 12) + 60] = row[stat_index + 1]
                            else:
                                data[stat_index + (found_B_players * 12) + 60] = "1"

                        found_B_players += 1

    input_filename = '../data/orgStats.csv'

    with open(input_filename, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if row[3] == event and row[1][:-4] == orgA:
                data[120] = str(convert_time_to_seconds(row[8]))
            elif row[3] == event and row[1][:-4] == orgB:
                data[121] = str(convert_time_to_seconds(row[8]))

    # print(data)
    data[122] = determine_winner(score)

    # convert the data and headers into a dictionary (the csv row)
    entry = dict(zip(field_names, data))

    contents.append(entry)

    print(contents)

    # return the generated row
    return contents


def main():
    field_names = []

    for team in range(1, 3):
        for player in range(1, 6):
            team_name = "A" if team == 1 else "B"

            field_names.append("Player " + str(player) + str(team_name) + " Winrate")
            field_names.append("Player " + str(player) + str(team_name) + " KDA")
            field_names.append("Player " + str(player) + str(team_name) + " CSPM")
            field_names.append("Player " + str(player) + str(team_name) + " GPM")
            field_names.append("Player " + str(player) + str(team_name) + " Gold %")
            field_names.append("Player " + str(player) + str(team_name) + " Kill Participation %")
            field_names.append("Player " + str(player) + str(team_name) + " Damage Per Minute")
            field_names.append("Player " + str(player) + str(team_name) + " Damage %")
            field_names.append("Player " + str(player) + str(team_name) + " K+A/M")
            field_names.append("Player " + str(player) + str(team_name) + " Solo Kills")
            field_names.append("Player " + str(player) + str(team_name) + " Penta Kills")
            field_names.append("Player " + str(player) + str(team_name) + " Meta Score")

    # field_names.append("Team A Winrate")
    # field_names.append("Team B Winrate")

    field_names.append("Team A Average Game Time (In Tournament)")
    field_names.append("Team B Average Game Time (In Tournament)")
    # field_names.append("Series Average Game Time")

    field_names.append("Winner")

    orgA_names = []
    orgB_names = []
    seasons = []
    splits = []
    events = []
    scores = []

    input_filename = '../data/gameData.csv'

    with open(input_filename, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:

            if row[0] == 'Event':
                continue

            orgA_names.append(row[1])
            orgB_names.append(row[3])
            events.append(row[0])
            seasons.append('S' + str((int(row[8].split('-')[0][2:])) - 10))

            splits.append('Spring' if int(row[8].split('-')[1]) < 6 else 'Summer')
            scores.append(row[5])

    # print(events)
    #
    # example_row = []
    # example_row.append(orgA_names[0])
    # example_row.append(orgB_names[0])
    # example_row.append(seasons[0])
    # example_row.append(splits[0])
    # example_row.append(events[0])
    # print(seasons)

    if len(orgA_names) == len(orgB_names) and len(orgA_names) == len(seasons) and len(orgA_names) == len(splits):
        pass
    else:
        print('ERROR: The lengths of the lists are not equal.')
        exit()

    # orgA_names = orgA_names[:5000]

    all_contents = []
    with ThreadPoolExecutor(max_workers=1000) as executor:
        # Initialize an empty list to hold the future objects
        futures = []

        # len(orgA_names)
        # Iterate over player_links with an index
        for index in range(0, len(orgA_names)):
            # Submit the scrape_player_data function to the executor
            future = executor.submit(generate_row_data, orgA_names[index], orgB_names[index], seasons[index],
                                     splits[index], events[index], scores[index], field_names)
            # Append the future object to the list
            futures.append(future)

        # Iterate over the futures as they complete
        for future in as_completed(futures):
            all_contents.extend(future.result())

    # Defining the CSV file path to save in the current directory
    csv_file_path = './masterSpreadsheet.csv'

    # Writing data to CSV
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(all_contents)

    df = pd.read_csv('./masterSpreadsheet.csv')
    df.replace("-", "0", inplace=True)
    df.fillna(0, inplace=True)
    df.to_csv('./masterSpreadsheet.csv', index=False)

    print("Could not find: " + str(could_not_find) + " teams.")
    print("Could not find the following teams: " + str(could_not_find_teams))


if __name__ == '__main__':
    main()
