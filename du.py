import pandas

data = pandas.read_csv("1976-2020-president.csv")
# print(data.head(15))

data = data[["year", "state", "party_simplified", "candidatevotes", "totalvotes"]]
data["rank"] = data.groupby(["year", "state"])["candidatevotes"].rank(method="min", ascending=False)
# print(data.head(15))

viteze = data[data["rank"] == 1]
# print(viteze)


