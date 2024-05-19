import pandas as pd

input_filename = '../data/gameData.csv'
output_filename = '../data/lists.csv'

df = pd.read_csv(input_filename)

teamA = []
teamB = []
season = []
event = []
split = []

for index, row in df.iterrows():
    if row['Event'] == 'Event':
        continue

    teamA.append(row['Team 1'])
    teamB.append(row['Team 2'])
    event.append(row['Event'])
    season.append('S' + row['Date'].split('-')[0][2:])
    split.append('Spring' if int(row['Date'].split('-')[1]) < 6 else 'Summer')

lists_df = pd.DataFrame({
    'TeamA': teamA,
    'TeamB': teamB,
    'Event': event,
    'Season': season,
    'Split': split
})

lists_df.to_csv(output_filename, index=False)

print(f"Data has been written to {output_filename}")
