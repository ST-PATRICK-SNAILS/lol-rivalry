from indexer import indexer
import pandas as pd

def orgPropagate(bar):
    orgdata_dfs = []
    for _, row in indexer.records.iterrows():
        team1_id, team2_id = row["Team 1 ID"], row["Team 2 ID"]
        roster_data = indexer.processOrgDataByIds(team1_id, team2_id)
        orgdata_dfs.append(roster_data)
        bar() 
    combined_orgs_df = pd.concat(orgdata_dfs, ignore_index=True)
    return combined_orgs_df