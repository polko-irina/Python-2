import pandas

data = pandas.read_csv("prijimaci_zkousky.csv")

def get_points(row):
    if row[["body_aj", "body_mat", "body_cj"]].min() < 60:
        return 0
    skore = row[["body_aj", "body_mat", "body_cj"]].sum()
    if not pandas.isnull(row["souteze"]):
        skore += 10
    if row["letni_skola"] == "ano":
        skore += 5
    return skore
    
data["body"] = data.apply(get_points, axis=1)

data = data[data["body"] > 0]
data = data.reset_index()
print(data.head())

# Vytvoříme pořadí pro každý obor:
# ...method="min": v případě shody bodů u více řádků přiřadí všem shodně nejmenší hodnotu pořadí
# ...ascending=False: sestupně, tzn. nejvíc bodů = 1. místo
data["poradi"] = data.groupby("obor")["body"].rank(method="min", ascending=False)
data = data.sort_values(["obor", "poradi"])

print(data.tail(40))

# Nakonec vytvoř tabulku s přijatými uchazeči, kde budou uchazeči hodnocení od 1. do 30. místa pro daný obor.
def prijat(row):
    if row["poradi"] <= 30:
        return "Ano"
    else:
        return "Ne"
# ...Zde je to pro názornost "Ano"/"Ne", ale jinak by se pro případné další zpracování spíš hodilo použít hodnoty True/False

data["prijat"] = data.apply(prijat, axis=1)

# Alternativa z předchozích lekcí:
data["prijat_cut"] = pandas.cut(data["poradi"], bins=[0,30,float("inf")], labels=["Ano", "Ne"])

print(data.tail())