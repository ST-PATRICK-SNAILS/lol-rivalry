import pandas as pd

input_filename = '../data/gameData.csv'
output_filename = '../data/records.csv'
    
df = pd.read_csv(input_filename)
df = df.dropna()

df["Team 1 ID"] = df["Team 1 ID"].astype("Int32")
df["Team 2 ID"] = df["Team 2 ID"].astype("Int32")
df["Season"] = df["Date"].apply(lambda i: int(i.split('-')[0][2:]) - 10).astype("Int8")
df["Split"] = df["Date"].apply(lambda i: 'Summer' if int(i.split('-')[1]) >= 6 else 'Spring').astype("|S6")
df["Games"] = df["Record"].apply(lambda i: 2 * max(list(map(lambda j: int(j.strip()), i.split('-')))) - 1).astype("Int8")
df["Result"] = df["Record"].apply(lambda i: max(enumerate(list(map(lambda j: int(j.strip()), i.split('-')))), key=lambda k: k[1])[0]).astype("Int8")

df = df.drop(axis=1, labels=["Team 1", "Team 2", "Stage", "Patch", "Record", "Date"])
print(df.dtypes)

df.to_csv(output_filename, index=False)