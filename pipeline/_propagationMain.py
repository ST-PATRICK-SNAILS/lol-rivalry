from indexer import indexer
from eventPropagation import eventPropagate
from orgPropagation import orgPropagate
from playerPropagation import playerPropagate
from alive_progress import alive_bar
import pandas as pd

rows = indexer.records.shape[0]

with alive_bar(rows, title='Step 1: Event Propagation', bar='smooth') as event_bar: event = eventPropagate(event_bar)
with alive_bar(rows, title='Step 2: Organization Propagation', bar='smooth') as org_bar: orgs = orgPropagate(org_bar)
with alive_bar(rows, title='Step 3: Player/Roster Propagation', bar='smooth') as player_bar: players = playerPropagate(player_bar)

df = pd.concat([event, orgs, players, indexer.records['Games'], indexer.records['Result']], axis=1).dropna()
print("Pipeline finished, printing dataframe:")
print(df.columns)
print(df)

df.to_csv('./writes/shortpropdata.csv', index=False)


