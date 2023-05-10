"""V případě amerických prezidentských voleb obecně platí, že ve většině států dlouhodobě vyhrávají kandidáti jedné strany. Například v Kalifornii vyhrává kandidát Demokratické strany or roku 1992, v Texasu kandidát Republikánské strany od roku 1980, v Kansasu do konce od roku 1968 atd. Státy, kde se vítězné strany střídají, jsou označovány jako "swing states" ("kolísavé státy"). Tvým úkolem je vybrat státy, které lze označit jako swing states.
V souboru 1976-2020-president.csv najdeš historické výsledky amerických prezidentských voleb. Každý řádek souboru obsahuje počet hlasů pro kandidáta dané strany v daném roce.
V souboru jsou důležité následující sloupce:

year - rok voleb,
state - stát,
party_simplified - zjednodušené označení politické strany,
candidatevotes - počet hlasů pro vybraného kandidáta,
totalvotes - celkový počet odevzdaných hlasů.
Proveď níže uvedené úkoly."""

import pandas
import matplotlib.pyplot as plt

data = pandas.read_csv("1976-2020-president.csv")
data = data[["year", "state", "party_simplified", "candidatevotes", "totalvotes"]]
# print(data.head(15))

# Urči pořadí jednotlivých kandidátů v jednotlivých státech a v jednotlivých letech (pomocí metody rank()). Nezapomeň, že data je před použitím metody nutné seřadit a spolu s metodou rank() je nutné použít metodu groupby().
data["rank"] = data.groupby(["year", "state"])["candidatevotes"].rank(method="min", ascending=False)
# print(data.head(20))

# Pro další analýzu jsou důležití pouze vítězové. Vytvoř novou tabulku, která bude obsahovat pouze vítěze voleb.
vitezove = data[data["rank"] == 1]
# print(viteze)

# Pomocí metody shift() přidej nový sloupec, abys v jednotlivých řádcích měl(a) po sobě vítězné strany ve dvou po sobě jdoucích letech.
vitezove = vitezove.sort_values(["state", "year"])
# print(vitezove.head(20))
vitezove["minule vyhrala strana"] = vitezove.groupby("state")["party_simplified"].shift()
# print(vitezove.head(20))

# Porovnej, jestli se ve dvou po sobě jdoucích letech změnila vítězná strana. Můžeš k tomu použít např. funkci numpy.where() nebo metodu apply().
def zmena_strany(vitezove):
    if vitezove["party_simplified"] == vitezove["minule vyhrala strana"]:
        return 0
    else:
        return 1
    
vitezove = vitezove.dropna()
vitezove["zmena strany"] = vitezove.apply(zmena_strany, axis=1)
# print(vitezove)

# Proveď agregaci podle názvu státu a seřaď státy podle počtu změn vítězných stran.
data_pivot = vitezove.groupby(["state"])["zmena strany"].sum()
data_pivot = pandas.DataFrame(data_pivot)
data_pivot = data_pivot.sort_values("zmena strany", ascending=False)
# print(data_pivot)

# Vytvoř sloupcový graf s 10 státy, kde došlo k nejčastější změně vítězné strany. Jako výšku sloupce nastav počet změn.
top_swinging_states = data_pivot[data_pivot["zmena strany"] >= 1]
top_swinging_states.plot(kind="bar", color="green")
plt.xlabel("state")
plt.ylabel("počet zmen")
plt.show()

# Pro další část pracuj s tabulkou se dvěma nejúspěšnějšími kandidáty pro každý rok a stát (tj. s tabulkou, která oproti té minulé neobsahuje jen vítěze, ale i druhého v pořadí).
# Přidej do tabulky sloupec, který obsahuje absolutní rozdíl mezi vítězem a druhým v pořadí.
vitez2 = data[data["rank"] <= 2].sort_values(["year", "state", "rank"])
vitez2["candidatevotes2"] = vitez2.groupby("state")["candidatevotes"].shift()
vitez2["absolutni rozdil"] =abs(vitez2["candidatevotes"] - vitez2["candidatevotes2"])
vitez2 = vitez2.dropna()
# print (vitez2.head(20))

# řidej sloupec s relativním marginem, tj. rozdílem vyděleným počtem hlasů.
vitez2["relativni margin"] = vitez2["absolutni rozdil"]/vitez2["totalvotes"]
# print (vitez2.head(20))

# Seřaď tabulku podle velikosti relativního marginu a zjisti, kdy a ve kterém státě byl výsledek voleb nejtěsnější
vitez2 = vitez2.sort_values(["relativni margin"])
# print(vitez2)

"""Vytvoř pivot tabulku, která zobrazí pro jednotlivé volební roky, kolik států přešlo od Republikánské strany k Demokratické straně, kolik států přešlo od Demokratické strany k Republikánské straně a kolik států volilo kandidáta stejné strany.
Zde je lepší využít tabulku z předchozí části, kde už máme vítězné strany z minulého období. Poté je potřeba přidat nový sloupec, který porovná sloupec s vítěznou stranou daného roku a sloupec s vítěznou stranou z minulého roku. Opět pozor na rok 1976, aby vám neudělal neplechu. Rozlišujeme tři různé stavy: přechod od Republikánů k Demokratům, přechod od Demokratů k Republikánům a volba stejné strany."""

print(vitezove)
def swing(vitezove):
    if vitezove["zmena strany"] == 1:
        if vitezove["party_simplified"] == "REPUBLICAN":
            return "to REP."
        else:
            return "to DEM."
    else:
        return "no swing"
    
vitezove["swing"] = vitezove.apply(swing, axis = 1)
# print(vitezove.head(20))

swings_pivot = pandas.pivot_table(data=vitezove, values="zmena strany", index="year", columns="swing", aggfunc=len)
# print(swings_pivot)
