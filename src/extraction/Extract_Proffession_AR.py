# Extraction de donnée s à partir du PDF arabe
doc_ar = pym.open("data/raw/Nomenclature analytique des professions, Décembre 2014 (Version ar).pdf") # open a document

# transformer le contenu du PDF en une de lignes 
lines = []

for page in doc_ar:
    text = page.get_text() # transforme le contenu de la page en texte brut
    for l in text.split("\n"): # parcourt chaque ligne du texte
        l = l.strip() # efface les espaces en début et fin de ligne
        if l: # si la ligne n'est pas vide, on l'ajoute à la liste
            lines.append(l)

records = [] # résultat final [(code, métier), ...]
buffer = [] # stocker le métier en cours de lecture

for line in lines:

    # Code à 4 chiffres -> métier final
    if re.fullmatch(r"\d{4}", line):

        metier = " ".join(buffer).strip()

        if metier:
            records.append({
                "Code": line,
                "Metier": metier
            })

        buffer = [] # vider le buffer pour le prochain métier

    # Code à 1, 2 ou 3 chiffres -> titre de groupe
    elif re.fullmatch(r"\d{1,3}", line):
        buffer = []

    else:
        buffer.append(line)

tableau_ar = pd.DataFrame(records)

tableau_ar.drop_duplicates(subset="Code", inplace=True)
tableau_ar.reset_index(drop=True, inplace=True)
tableau_ar = tableau_ar.astype({"Code": int})

tableau_ar.to_excel("data/interim/metiers_ar.xlsx", index=False)
# eviter la suppression des zéros à gauche du code
tableau_ar["Code"] = tableau_ar["Code"].astype(str)
for i in tableau_ar.index:
    if len(tableau_ar.loc[i, "Code"]) == 3:
        tableau_ar.loc[i, "Code"] = "0" + tableau_ar.loc[i, "Code"]
print("Nombre de métiers :", len(tableau_ar))
tableau_ar.head()