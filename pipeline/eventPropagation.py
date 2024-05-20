from utils import indexer
import pandas as pd

def eventPropagate(bar):
    def classifyTournamentRegionWrapper(i):
        bar()
        return indexer.classifyTournamentRegionByName(i)
    
    def processTournamentMetaWrapper(i):
        bar()
        return indexer.processTournamentMetaByName(i)
    
    classified_events = pd.concat(indexer.records['Event'].apply(lambda i: classifyTournamentRegionWrapper(i)).values, ignore_index=True)
    processed_event_metas = pd.concat(indexer.records['Event'].apply(lambda i: processTournamentMetaWrapper(i)).values, ignore_index=True)
    event_data = pd.concat([classified_events, processed_event_metas], axis=1)
    return event_data