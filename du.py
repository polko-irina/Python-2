import pandas

data = pandas.read_csv("1976-2020-president.csv")
# print(data.head())

data = data[["year", "state", "party_simplified", "candidatevotes", "totalvotes"]]
# print(data.head())

data["Rank"] = data.groupby(["year"])["candidatevotes"].rank(ascending=False)
data = data.sort_values(["candidatevotes", "state", "year"], ascending=[False, False, True])
# print(data.head(30))
 
viteze = data.sort_values(["candidatevotes"])
print(viteze)

