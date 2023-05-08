import pandas

ioef = pandas.read_csv("ioef.csv")
ioef = ioef[["Name", "Index Year", "Overall Score"]]
ioef["Rank"] = ioef.groupby(["Index Year"])["Overall Score"].rank(ascending=False)
ioef = ioef.sort_values(["Name", "Index Year"], ascending=[True, False])
# ioef = ioef[ioef["Name"] == "Czech Republic"]
# ioef = ioef.sort_values(["Index Year", "Rank"])
ioef["Rank Previous Year"] = ioef.groupby(["Name"])["Rank"].shift(-1)
ioef["Rank Change"] = ioef["Rank Previous Year"] - ioef["Rank"]
print(ioef.head(5))

