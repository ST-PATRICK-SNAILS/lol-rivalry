from utils import indexer
import pandas as pd

def playerPropagate(bar):
    teamdata_dfs = []
    for _, row in indexer.records.iterrows():
        season, split, team1_id, team2_id = row["Season"], row["Split"], row["Team 1 ID"], row["Team 2 ID"]
        roster_data = indexer.processRosterDataByTeams(season, split, team1_id, team2_id)
        teamdata_dfs.append(roster_data)
        bar()       
    combined_players_df = pd.concat(teamdata_dfs, ignore_index=True)
    return combined_players_df