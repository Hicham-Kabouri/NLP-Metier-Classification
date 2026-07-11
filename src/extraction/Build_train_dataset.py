# Construction de data train 
# Lire les deux fichiers
tableau_fr = pd.read_excel("NAP_2014_vr_fr.xlsx")
tableau_ar = pd.read_excel("NAP_2014_vr_ar_1.xlsx")

# Renommer les colonnes
tableau_fr = tableau_fr.rename(columns={
    "Code": "Code",
    "Metier": "metier_fr"
})

tableau_ar = tableau_ar.rename(columns={
    "Code": "Code",
    "Metier": "metier_ar"
})

# Fusion sur le code
tableau_fr = pd.merge(tableau_fr, tableau_ar, on="Code", how="inner")

# Réordonner les colonnes
tableau_fr = tableau_fr[["metier_fr", "metier_ar", "Code"]]

# Sauvegarder
tableau_fr.to_excel("NLP 2014 fr-ar.xlsx", index=False)

print(tableau_fr.head())
print("Nombre de métiers :", len(tableau_fr))