import pandas as pd


dfs = list()
for i in range(1, 50):
	pth = "./info/" + str(i) + ".csv"
	df = pd.read_csv(pth)
	df.drop(df.columns[[0]], axis=1, inplace=True)
	dfs.append(df)

DF = pd.concat(dfs)
DF = DF.reset_index(drop = True)
# print(DF)
DF.to_csv("user_info.csv")
# print(DF)