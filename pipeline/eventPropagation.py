from utils import indexer
import pandas as pd

df = pd.read_csv('../data/records.csv')
classified_events = pd.concat(df['Event'].apply(lambda i: indexer.classifyTournamentRegionByName(i)).values, ignore_index=True)
processed_event_metas = pd.concat(df['Event'].apply(lambda i: indexer.processTournamentMetaByName(i)).values, ignore_index=True)
event_data = pd.concat([classified_events, processed_event_metas], axis=1)

teamdata_dfs = []
for index, row in df.iterrows():
    season, split, team1_id, team2_id = row["Season"], row["Split"], row["Team 1 ID"], row["Team 2 ID"]
    roster_data = indexer.getRosterDataByTeams(season, split, team1_id, team2_id)
    teamdata_dfs.append(roster_data)

df = df.drop(columns=['Event', 'Team 1 ID', 'Team 2 ID', 'Season', 'Split'])
combined_players_df = pd.concat(teamdata_dfs, ignore_index=True)
temp = pd.concat([event_data, combined_players_df, df], axis=1).dropna()
print(temp)
temp.to_csv('./tempEventProp.csv', index=False)