from utils import indexer
import pandas as pd

def eventPropagate():
    classified_events = pd.concat(indexer.records['Event'].apply(lambda i: indexer.classifyTournamentRegionByName(i)).values, ignore_index=True)
    processed_event_metas = pd.concat(indexer.records['Event'].apply(lambda i: indexer.processTournamentMetaByName(i)).values, ignore_index=True)
    event_data = pd.concat([classified_events, processed_event_metas], axis=1)
    return event_data