import pandas

def evaluate_result(row):
    row = row.iloc[2:]
    if row.mean() <= 1.5 and row.max() <= 2:
        return "Prospěl(a) s vyznamenáním"
    elif row.max() == 5:
        return "Neprospěl(a)"
    else:
        return "Prospěl(a)"

def evaluate_application(row):
    if pandas.isnull(row["Poplatek"]):
        return "Vyřazen - nezaplatil"
    # elif row.iloc[2:6].mean() <= 2:
    elif row["Matematika"] == 1 and row["Český jazyk":"Matematika"].mean() <= 2:
        return "Přijat bez PZ"
    else:
        return "Musí absolvovat PZ"

data = pandas.read_csv("vysledky.csv")
data["vysledek"] = data.apply(evaluate_result, axis=1)
data["PZ"] = data.apply(evaluate_application, axis=1)
print(data)



