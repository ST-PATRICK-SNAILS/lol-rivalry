from utils import indexer
import pandas as pd

def playerPropagate():
    teamdata_dfs = []
    for index, row in indexer.records['Event'].iterrows():
        season, split, team1_id, team2_id = row["Season"], row["Split"], row["Team 1 ID"], row["Team 2 ID"]
        roster_data = indexer.getRosterDataByTeams(season, split, team1_id, team2_id)
        teamdata_dfs.append(roster_data)
        
    combined_players_df = pd.concat(teamdata_dfs, ignore_index=True)
    return combined_players_df