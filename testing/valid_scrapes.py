import pandas as pd
from os import listdir
from os.path import isfile, join

route = "../data/"

files = [f for f in listdir(route) if isfile(join(route, f))]

success = 0

for i, file in enumerate(files, start=1):
    try:
        df = pd.read_csv(f"{route}/{file}")
    except Exception as e:
        print(f"\nTEST {i}: Exception occured in reading file {file}")
        print(e)
    else:
        print(f"TEST {i}: Reading test case {file} successful.")
        success += 1

print(f"\nAll test cases ran: {success} of {len(files)} cases passed!")
        