import pandas

data = pandas.read_csv("1976-2020-president.csv")
# print(data.head(15))

data["Rank"] = data.groupby(["year"])["candidatevotes"].rank(method="min", ascending=False)
print(data.head(15))

# viteze = data.sort_values(["Rank"] == 1)
# print(viteze)