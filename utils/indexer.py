import pandas as pd

orgStatsInput = "../data/orgStats.csv"
playerChampsInput = "../data/playerChamps.csv"
playerHistoryInput = "../data/playerHistory.csv"

class Indexer():
    def __init__(self):
        orgStats = pd.read_csv(orgStatsInput)
        orgStats["Team ID"] = orgStats["Team ID"].astype("Int32")
        playerChamps = pd.read_csv(playerChampsInput)
        playerChamps["Player ID"] = playerChamps["Player ID"].astype("Int32")
        playerHistory = pd.read_csv(playerHistoryInput)
        playerHistory["Player ID"] = playerHistory["Player ID"].astype("Int32")
        
        self.orgStats = orgStats.sort_values("Team ID")
        self.orgCount = self.orgStats.shape[0]
        self.playerChamps = playerChamps.sort_values("Player ID")
        self.playerChampsCount = self.playerChamps.shape[0]
        self.playerHistory = playerHistory.sort_values("Player ID")
        self.playerHistoryCount = self.playerHistory.shape[0]
        
    def getTeamStatsById(self, id):
        start_pos = self.orgStats['Team ID'].searchsorted(id, side='left')
        end_pos = self.orgStats['Team ID'].searchsorted(id, side='right')
        return self.orgStats.iloc[start_pos:end_pos]
    
    def getPlayerChampsById(self, id):
        start_pos = self.playerChamps['Player ID'].searchsorted(id, side='left')
        end_pos = self.playerChamps['Player ID'].searchsorted(id, side='right')
        return self.playerChamps.iloc[start_pos:end_pos]
    
    def getPlayerHistoryById(self, id):
        start_pos = self.playerHistory['Player ID'].searchsorted(id, side='left')
        end_pos = self.playerHistory['Player ID'].searchsorted(id, side='right')
        return self.playerHistory.iloc[start_pos:end_pos]
        
i = Indexer()