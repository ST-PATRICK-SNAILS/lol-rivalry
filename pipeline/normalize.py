import pandas as pd

normalize_columns = ["T1_AvgGameTime","T1_DPM","T1_FirstBlood","T1_KillsPG","T1_DeathsPG","T1_AverageKDR","T1_AverageAPK","T1_Plates_Absolute","T1_Plates_Split1","T1_Plates_Split2","T1_Plates_Split3","T1_Dragons_Absolute","T1_Dragons_Relative","T1_D15","T1_Heralds_Absolute",
                     "T1_Heralds_Relative","T1_Nashors_Absolute","T1_Nashors_Relative","T1_Wins","T1_Losses","T1_WinRate","T2_AvgGameTime","T2_DPM","T2_FirstBlood","T2_KillsPG","T2_DeathsPG","T2_AverageKDR","T2_AverageAPK","T2_Plates_Absolute","T2_Plates_Split1",
                     "T2_Plates_Split2","T2_Plates_Split3","T2_Dragons_Absolute","T2_Dragons_Relative","T2_D15","T2_Heralds_Absolute","T2_Heralds_Relative","T2_Nashors_Absolute","T2_Nashors_Relative","T2_Wins","T2_Losses","T2_WinRate","T1_P1_Wins","T1_P1_Losses","T1_P1_WinRate","T1_P1_KDA","T1_P1_CSPM","T1_P1_GPM","T1_P1_GoldPercent","T1_P1_KP","T1_P1_DPM","T1_P1_DamagePercent","T1_P1_KAM","T1_P1_SoloKills",
                     "T1_P1_Pentakills","T1_P2_Wins","T1_P2_Losses","T1_P2_WinRate","T1_P2_KDA","T1_P2_CSPM","T1_P2_GPM","T1_P2_GoldPercent","T1_P2_KP","T1_P2_DPM","T1_P2_DamagePercent","T1_P2_KAM","T1_P2_SoloKills","T1_P2_Pentakills","T1_P3_Wins","T1_P3_Losses","T1_P3_WinRate","T1_P3_KDA","T1_P3_CSPM","T1_P3_GPM","T1_P3_GoldPercent","T1_P3_KP","T1_P3_DPM","T1_P3_DamagePercent","T1_P3_KAM","T1_P3_SoloKills","T1_P3_Pentakills","T1_P4_Wins","T1_P4_Losses","T1_P4_WinRate","T1_P4_KDA","T1_P4_CSPM","T1_P4_GPM","T1_P4_GoldPercent","T1_P4_KP","T1_P4_DPM","T1_P4_DamagePercent","T1_P4_KAM","T1_P4_SoloKills","T1_P4_Pentakills","T1_P5_Wins","T1_P5_Losses","T1_P5_WinRate","T1_P5_KDA","T1_P5_CSPM","T1_P5_GPM","T1_P5_GoldPercent","T1_P5_KP","T1_P5_DPM","T1_P5_DamagePercent","T1_P5_KAM","T1_P5_SoloKills","T1_P5_Pentakills","T2_P1_Wins","T2_P1_Losses","T2_P1_WinRate","T2_P1_KDA","T2_P1_CSPM","T2_P1_GPM","T2_P1_GoldPercent","T2_P1_KP","T2_P1_DPM","T2_P1_DamagePercent","T2_P1_KAM","T2_P1_SoloKills","T2_P1_Pentakills","T2_P2_Wins","T2_P2_Losses","T2_P2_WinRate","T2_P2_KDA","T2_P2_CSPM","T2_P2_GPM","T2_P2_GoldPercent","T2_P2_KP","T2_P2_DPM","T2_P2_DamagePercent","T2_P2_KAM","T2_P2_SoloKills","T2_P2_Pentakills","T2_P3_Wins","T2_P3_Losses","T2_P3_WinRate","T2_P3_KDA","T2_P3_CSPM","T2_P3_GPM","T2_P3_GoldPercent","T2_P3_KP","T2_P3_DPM","T2_P3_DamagePercent","T2_P3_KAM","T2_P3_SoloKills","T2_P3_Pentakills","T2_P4_Wins","T2_P4_Losses","T2_P4_WinRate","T2_P4_KDA","T2_P4_CSPM","T2_P4_GPM","T2_P4_GoldPercent","T2_P4_KP","T2_P4_DPM","T2_P4_DamagePercent","T2_P4_KAM","T2_P4_SoloKills","T2_P4_Pentakills","T2_P5_Wins","T2_P5_Losses","T2_P5_WinRate","T2_P5_KDA","T2_P5_CSPM","T2_P5_GPM","T2_P5_GoldPercent","T2_P5_KP","T2_P5_DPM","T2_P5_DamagePercent","T2_P5_KAM","T2_P5_SoloKills","T2_P5_Pentakills"]
df = pd.read_csv('./writes/shortpropdata.csv')

for column in normalize_columns:
    mean, std = df[column].mean(), df[column].std()
    if std != 0:
        df[column] = df[column].apply(lambda x: (x - mean) / std)
    else: 
        df[column] = df[column].apply(lambda _: 0)
    
drop_suffixes = ["_Wins", "_Losses", "_Spilt1", "_Split2", "_Split3", "_GoldPercent", "_DamagePercent", "_Relative", "_Pentakills", "_GPM", "_KAM", "_RegionStrength", "Average Time"]
drops = []

for column in df.columns:
    for suffix in drop_suffixes:
        if column.endswith(suffix):
            drops.append(column)
            break

df.drop(columns=drops, inplace=True)

df.to_csv('./writes/normalizedpropdata.csv')