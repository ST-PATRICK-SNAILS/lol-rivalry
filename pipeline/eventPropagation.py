from indexer import indexer
import pandas as pd

def eventPropagate(bar):
    def classifyTournamentRegionWrapper(i):
        bar()
        return indexer.classifyTournamentRegionByName(i)
    
    classified_events = pd.concat(indexer.records['Event'].apply(lambda i: classifyTournamentRegionWrapper(i)).values, ignore_index=True)
    event_data = pd.concat([classified_events], axis=1)
    return event_data