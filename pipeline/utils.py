import pandas as pd
import warnings

orgStatsInput = "../data/orgStats.csv"
playerChampsInput = "../data/playerChamps.csv"
playerHistoryInput = "../data/playerHistory.csv"
tournamentListInput = "../data/tournamentList.csv"
tournamentChampsInput = "../data/tournamentChamps.csv"

class Indexer():
    def __init__(self):
        orgStats = pd.read_csv(orgStatsInput, keep_default_na=False, na_values='-')
        orgStats["Team ID"] = orgStats["Team ID"].astype("Int32")
        playerChamps = pd.read_csv(playerChampsInput)
        playerChamps["Player ID"] = playerChamps["Player ID"].astype("Int32")
        playerHistory = pd.read_csv(playerHistoryInput, keep_default_na=False, na_values='-')
        playerHistory["Player ID"] = playerHistory["Player ID"].astype("Int32")
        tournamentList = pd.read_csv(tournamentListInput, keep_default_na=False, na_values='-')
        tournamentList["Tournament Name"] = tournamentList["Tournament Name"].astype("string_")
        tournamentChamps = pd.read_csv(tournamentChampsInput, keep_default_na=False, na_values='-')
        tournamentChamps["Tournament Name"] = tournamentChamps["Tournament Name"].astype("string_")
        
        self.orgStats = orgStats.sort_values("Team ID")
        self.orgCount = self.orgStats.shape[0]
        self.playerChamps = playerChamps.sort_values("Player ID")
        self.playerChampsCount = self.playerChamps.shape[0]
        self.playerHistory = playerHistory.sort_values("Player ID")
        self.playerHistoryCount = self.playerHistory.shape[0]
        self.tournamentList = tournamentList.sort_values("Tournament Name")
        self.tournamentCount = self.tournamentList.shape[0]
        self.tournamentChamps = tournamentChamps.sort_values("Tournament Name")
        self.tournamentChampsCount = self.tournamentChamps.shape[0]
        
        #Event propagation
        self.regions = ["WR", "KR", "CN", "EUW", "NA", "PCS", "VN", "JP", "BR", "LAT"]
        self.significantRegions = ["PCS", "VN", "JP", "BR", "LAT"]
        self.westernMajorRegions = ["NA", "EUW"]
        self.easternMajorRegions = ["KR", "CN"]
        self.nullRegionRow = {f"Is{region}" : 0 for region in self.regions}
        
        #Player propagation
        self.playerFields = ["KDA", "CSPM", "GPM", "Gold %", "Kill Participation %", "Damage Per Minute", "Damage %", "K+A/M","Solo Kills","Penta Kills"]
        self.mappedPlayerFields = ["KDA", "CSPM", "GPM", "GoldPercent", "KP", "DPM", "DamagePercent", "KAM", "SoloKills", "Pentakills"]
        self.percentFields = ["GoldPercent", "KP", "DamagePercent"]
        
        self.nullPlayerFieldsRowArray = [
            {f"T{i+1}_P{j+1}_{field}": None for field in self.mappedPlayerFields}
            for i in range(2)
            for j in range(5)
        ]
        self.memo_rosterdata = {}
    
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
    
    def getTournamentDataByName(self, name):
        start_pos = self.tournamentList['Tournament Name'].searchsorted(name, side='left')
        end_pos = self.tournamentList['Tournament Name'].searchsorted(name, side='right')
        return self.tournamentList.iloc[start_pos:end_pos]
    
    def getTournamentChampsByName(self, name):
        start_pos = self.tournamentChamps['Tournament Champs'].searchsorted(name, side='left')
        end_pos = self.tournamentChamps['Tournament Name'].searchsorted(name, side='right')
        return self.tournamentChamps.iloc[start_pos:end_pos]
    
    def getRosterDataByTeams(self, season, split, team1, team2):
        def getRosterFromId(team_id, prefix):
            if f"T{prefix}_{team_id}" in self.memo_rosterdata:
                return self.memo_rosterdata[f"T{prefix}_{team_id}"]
            
            def getPlayerRelevantSplitById(id, playerPrefix):
                playerData = self.getPlayerHistoryById(int(id.strip())).sort_values("Player Name")
                if(playerData.shape[0] > 0):
                    playerName = ' '.join(playerData.iloc[0]["Player Name"].split()[:-2])
                    searchSeason, searchSplit = season, split
                    if searchSplit == "Summer":
                        searchSeason += 1
                        searchSplit = "Spring"
                    else: searchSplit = "Summer"
                    while searchSeason >= 11:
                        condition = (
                            (playerData['Player Name'] == f"{playerName} S{searchSeason} {searchSplit}") &
                            (~playerData['Record'].isna())
                        )
                        if condition.any():
                            relevant_data = playerData[condition].iloc[0]
                            player_win_loss = list(map(lambda s: float(s.strip()[:-1]), relevant_data["Record"].split("-")))
                            relevant_data = relevant_data.fillna(0)
                            player_result_data = {f"T{prefix}_P{playerPrefix}_WinRate":[player_win_loss[0]/(player_win_loss[0]+player_win_loss[1])]}
                            for i, field in enumerate(self.playerFields):
                                if self.mappedPlayerFields[i] in self.percentFields:
                                    player_result_data[f"T{prefix}_P{playerPrefix}_{self.mappedPlayerFields[i]}"] = [float(relevant_data[field].strip()[:-1])/100]
                                else:
                                    player_result_data[f"T{prefix}_P{playerPrefix}_{self.mappedPlayerFields[i]}"] = [relevant_data[field]]
                            return pd.DataFrame(player_result_data)
                        if searchSplit == "Spring":
                            searchSeason -= 1
                            searchSplit = "Summer"
                        else: searchSplit = "Spring"
                    warnings.warn(f"!! No relevant splits for playerId {id} of name {playerName} before {season}/{split} found")
                    return pd.DataFrame([self.nullPlayerFieldsRowArray[5 * (prefix - 1) + (playerPrefix - 1)]])
                else:
                    warnings.warn(f"!! Player data for id {id} not found")
                    return pd.DataFrame([self.nullPlayerFieldsRowArray[5 * (prefix - 1) + (playerPrefix - 1)]])
            
            data = self.getTeamStatsById(team_id)
            filter = data[data["Team Name"].str.strip().str.endswith(f"S{season}")]
            if filter.shape[0] > 0 and "Roster Ids" in filter.columns:
                roster = filter.iloc[0]["Roster Ids"].split()
                team_res = pd.concat([getPlayerRelevantSplitById(roster[i], i+1) for i in range(5)], axis=1)
                self.memo_rosterdata[f"{prefix}{team_id}"] = team_res
                return team_res
            else: 
                warnings.warn(f"!! Roster data for team {team_id} not found")
                return pd.DataFrame(pd.concat([pd.DataFrame([self.nullPlayerFieldsRowArray[5 * (prefix - 1) + i]]) for i in range(5)], axis=1))
        
        df_t1, df_t2 = getRosterFromId(team1, 1), getRosterFromId(team2, 2)
        return pd.concat([df_t1, df_t2], axis=1)
    
    def classifyEventTier(self, region):
        if region in self.significantRegions: return 2
        elif region in self.westernMajorRegions: return 3
        elif region in self.easternMajorRegions: return 4
        elif region == "WR": return 5
        return 1
    
    def classifyTournamentRegionByName(self, name):
        data = self.getTournamentDataByName(name)
        if data.shape[0] >= 1:
            tr_region = data.iloc[0]["Region"]
            if tr_region:
                result_data = {}
                if tr_region in self.regions:
                    for region in self.regions: 
                        result_data[f"Is{region}"] = [1 if tr_region == region else 0]
                    result_data["IsMinorRegion"] = [0]
                else: 
                    result_data = self.nullRegionRow
                    result_data["IsMinorRegion"] = [1]
                result_data["EventTier"] = [self.classifyEventTier(tr_region)]
                return pd.DataFrame(result_data)
            else:
                warnings.warn(f"!! Region data for {name} not found")
                return pd.DataFrame()
        else:
            warnings.warn(f"!! Tournament data for {name} not found")
            return pd.DataFrame()
        
    def processTournamentMetaByName(self, name):
        data = self.getTournamentDataByName(name)
        if data.shape[0] >= 1:
            tr_avg = data.iloc[0]["Average Time"]
            result_data = {}
            result_data["Average Time"] = [tr_avg]
            return pd.DataFrame(result_data)
        else:
            warnings.warn(f"!! Tournament data for {name} not found")
            return pd.DataFrame()
        
indexer = Indexer()