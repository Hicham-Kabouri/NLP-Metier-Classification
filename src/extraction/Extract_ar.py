# Extraction de donnée s à partir du PDF arabe
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

tableau_ar.to_excel("NAP_2014_vr_ar_1.xlsx", index=False)

print("Nombre de métiers :", len(tableau_ar))