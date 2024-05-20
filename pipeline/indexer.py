import pandas as pd
import warnings
import re
import math

orgStatsInput = "../data/orgStats.csv"
playerChampsInput = "../data/playerChamps.csv"
playerHistoryInput = "../data/playerHistory.csv"
tournamentListInput = "../data/tournamentList.csv"
tournamentChampsInput = "../data/tournamentChamps.csv"

class Indexer():
    def __init__(self):
        self.records = pd.read_csv('../data/records.csv')
        
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
        self.regionWeights = [1.25, 1.5, 2.5, 3.25, 4] #whatever
        self.nullRegionRow = {f"Is{region}" : 0 for region in self.regions}
        
        #Team propagation
        self.orgComputedFields = ["Wins", "Losses", "WinRate", "Appearance", "RegionStrength"]
        self.orgFields = ["Damage Per Minute","First Blood","Kills Per Game","Deaths Per Game","Average Kill / Death Ratio","Average Assists / Kill","Plates / game (TOP|MID|BOT)","Dragons / game","Dragons at 15 min","Herald / game","Nashors / game"]
        self.mappedOrgFields = ["DPM", "FirstBlood", "KillsPG", "DeathsPG", "AverageKDR", "AverageAPK", "Plates", "Dragons", "D15", "Heralds", "Nashors"]
        self.orgPercentFields = ["FirstBlood"]
        self.orgSplitterFields = ["Dragons","Heralds","Nashors"]
        self.orgTrisplitFields = ["Plates"]
        def generate_nullOrgFieldsRowArray(prefix):
            data, newMappedFields = {}, [*self.orgComputedFields, *self.mappedOrgFields]
            for i, _ in enumerate([*self.orgComputedFields, *self.orgFields]):
                if newMappedFields[i] in self.orgSplitterFields:
                    data[f"T{prefix}_{newMappedFields[i]}_Absolute"] = None
                    data[f"T{prefix}_{newMappedFields[i]}_Relative"] = None
                elif newMappedFields[i] in self.orgTrisplitFields:
                    data[f"T{prefix}_{newMappedFields[i]}_Absolute"] = None
                    data[f"T{prefix}_{newMappedFields[i]}_Split1"] = None
                    data[f"T{prefix}_{newMappedFields[i]}_Split2"] = None
                    data[f"T{prefix}_{newMappedFields[i]}_Split3"] = None
                else:
                    data[f"T{prefix}_{newMappedFields[i]}"] = None
            return data
        self.nullOrgFieldsRowArray = [generate_nullOrgFieldsRowArray(i+1) for i in range(2)]
        self.memo_orgdata = {}
        
        #Player propagation
        self.playerFields = ["KDA", "CSPM", "GPM", "Gold %", "Kill Participation %", "Damage Per Minute", "Damage %", "K+A/M","Solo Kills","Penta Kills"]
        self.mappedPlayerFields = ["KDA", "CSPM", "GPM", "GoldPercent", "KP", "DPM", "DamagePercent", "KAM", "SoloKills", "Pentakills"]
        self.playerPercentFields = ["GoldPercent", "KP", "DamagePercent"]
        self.nullPlayerFieldsRowArray = [
            {f"T{i+1}_P{j+1}_{field}": None for field in self.mappedPlayerFields}
            for i in range(2)
            for j in range(5)
        ]
        self.memo_rosterdata = {}
        
    def form_batches(self, df, batch_count):
        rows = df.shape[0]
        inc = int(rows/batch_count + 1)
        batches = []
        for i in range(0, rows+inc, inc):
            batches.append(df.iloc[i:i+inc])
        return batches
    
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
    
    def processRosterDataByTeams(self, season, split, team1, team2):
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
                            player_result_data = {
                                f"T{prefix}_P{playerPrefix}_Wins":[player_win_loss[0]],
                                f"T{prefix}_P{playerPrefix}_Losses":[player_win_loss[1]],
                                f"T{prefix}_P{playerPrefix}_WinRate":[player_win_loss[0]/(player_win_loss[0]+player_win_loss[1])],
                            }
                            for i, field in enumerate(self.playerFields):
                                if self.mappedPlayerFields[i] in self.playerPercentFields:
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
    
    def classifyRegionTier(self, region):
        if region in self.significantRegions: return self.regionWeights[1]
        elif region in self.westernMajorRegions: return self.regionWeights[2]
        elif region in self.easternMajorRegions: return self.regionWeights[3]
        elif region == "WR": return self.regionWeights[4]
        return self.regionWeights[0]
    
    def classifyEventTierByName(self, name):
        data = self.getTournamentDataByName(name)
        if data.shape[0] >= 1:
            tr_region = data.iloc[0]["Region"]
            return self.classifyRegionTier(tr_region)
        else:
            warnings.warn(f"!! Tournament data for {name} not found")
            return pd.DataFrame(0)
    
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
                result_data["EventTier"] = [self.classifyRegionTier(tr_region)]
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
        
    def processOrgDataByIds(self, team1, team2):
        def processOrgFromId(team_id, prefix):
            if f"T{prefix}_{team_id}" in self.memo_rosterdata:
                return self.memo_orgdata[f"T{prefix}_{team_id}"]
            
            team_stats = self.getTeamStatsById(team_id)
            if team_stats.shape[0] > 0:
                team_stats = team_stats.fillna(0)
                data = {}
                
                def custom_float(s):
                    if s == '': return 0.0
                    else: return float(s)

                for i, field in enumerate(self.orgFields):
                    if self.mappedOrgFields[i] in self.orgPercentFields:
                        data[f"T{prefix}_{self.mappedOrgFields[i]}"] = team_stats.apply(lambda row: custom_float(row[field].strip()[:-1])/100, axis=1).tolist()
                    elif self.mappedOrgFields[i] in self.orgSplitterFields:
                        def get_splits_splitter(entry):
                            splits = str(entry).split()
                            return (splits[0], custom_float(splits[1].strip()[1:-2])/100) if len(splits) == 2 else (0, 0)
                        data[f"T{prefix}_{self.mappedOrgFields[i]}_Absolute"] = team_stats.apply(lambda row: get_splits_splitter(row[field])[0], axis=1).tolist()
                        data[f"T{prefix}_{self.mappedOrgFields[i]}_Relative"] = team_stats.apply(lambda row: get_splits_splitter(row[field])[1], axis=1).tolist()
                    elif self.mappedOrgFields[i] in self.orgTrisplitFields:
                        def get_splits_trisplit(entry):
                            splits = re.split(r'[ ()|]', entry)
                            return [float(splits[0]), float(splits[2]), float(splits[3]), float(splits[4])] if len(splits) == 6 else [0, 0, 0, 0]
                        data[f"T{prefix}_{self.mappedOrgFields[i]}_Absolute"] = team_stats.apply(lambda row: get_splits_trisplit(row[field])[0], axis=1).tolist()
                        data[f"T{prefix}_{self.mappedOrgFields[i]}_Split1"] = team_stats.apply(lambda row: get_splits_trisplit(row[field])[1], axis=1).tolist()
                        data[f"T{prefix}_{self.mappedOrgFields[i]}_Split2"] = team_stats.apply(lambda row: get_splits_trisplit(row[field])[2], axis=1).tolist()
                        data[f"T{prefix}_{self.mappedOrgFields[i]}_Split3"] = team_stats.apply(lambda row: get_splits_trisplit(row[field])[3], axis=1).tolist()
                    else:
                        data[f"T{prefix}_{self.mappedOrgFields[i]}"] = team_stats.apply(lambda row: row[field], axis=1).tolist()
                
                #arithmetic mean on this for now too
                def average_array(arr):
                    sum = 0
                    for item in arr: 
                        sum += custom_float(item)
                    return sum/len(arr)
                
                for key in data:
                    data[key] = [average_array(data[key])]
                
                #aggregate appearance: quadratic mean
                #aggregate regiontier: arithmetic mean
                
                tr_aggregate_appearance, tr_aggregate_regiontier, tr_aggregate_wins, tr_aggregate_losses = 0, 0, 0, 0
                
                def add_to_record(record):
                    nonlocal tr_aggregate_wins, tr_aggregate_losses
                    splits = record.split("-")
                    if len(splits) == 2:
                        tr_aggregate_wins += int(splits[0].strip()[:-1])
                        tr_aggregate_losses += int(splits[1].strip()[:-1])
                    return record
                
                team_stats["Record"].apply(lambda i: add_to_record(i))
                data[f"T{prefix}_Wins"] = [tr_aggregate_wins]
                data[f"T{prefix}_Losses"] = [tr_aggregate_losses]
                data[f"T{prefix}_WinRate"] = [float(tr_aggregate_wins)/(float(tr_aggregate_losses) + float(tr_aggregate_wins))]
                
                def add_to_appearance(event):
                    nonlocal tr_aggregate_appearance
                    eventTier = self.classifyEventTierByName(event)
                    tr_aggregate_appearance += eventTier * eventTier
                    return event
                
                team_stats["Event"].apply(lambda i: add_to_appearance(i))
                data[f"T{prefix}_Appearance"] = [math.sqrt(custom_float(tr_aggregate_appearance)/custom_float(team_stats.shape[0]))]
                
                def add_to_regiontier(region):
                    nonlocal tr_aggregate_regiontier
                    regionTier = self.classifyRegionTier(region)
                    tr_aggregate_regiontier += regionTier
                    return region
                
                team_stats["Region"].apply(lambda i: add_to_regiontier(i))
                data[f"T{prefix}_RegionStrength"] = [custom_float(tr_aggregate_regiontier)/custom_float(team_stats.shape[0])]
                return pd.DataFrame(data)
            else: 
                warnings.warn(f"!!Org data for team {team_id} not found")
                return pd.DataFrame([self.nullOrgFieldsRowArray[prefix-1]])
        
        df_t1, df_t2 = processOrgFromId(team1, 1), processOrgFromId(team2, 2)
        return pd.concat([df_t1, df_t2], axis=1)
        
indexer = Indexer()