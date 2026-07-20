# Construction de data mapping

# Renommer les colonnes
tab_fr = tableau_fr.rename(columns={
    "Code": "Code",
    "Metier": "metier_fr"
})

tab_ar = tableau_ar.rename(columns={
    "Code": "Code",
    "Metier": "metier_ar"
})
# Fusion sur le code
tab_fr_ar = pd.merge(tab_fr, tab_ar, on="Code", how="inner")

# Réordonner les colonnes
tab_fr_ar = tab_fr_ar[["metier_fr", "metier_ar", "Code"]]

# Construction de data mapping
# construction de data mapping  merging tab_fr_ar avec tableau_fr par code 
merge = tableau_fr[["Code", "Intitule_Sous_Groupe", "Intitule_Sous_Grand_Groupe", "Intitule_Grand_Groupe"]]
# Fusion 
data_mapping = pd.merge(tab_fr_ar, merge, on="Code", how="left")
# Sauvgarder
data_mapping = data_mapping[["Code", "metier_fr", "metier_ar", "Intitule_Sous_Groupe", "Intitule_Sous_Grand_Groupe", "Intitule_Grand_Groupe"]]
data_mapping.to_excel("data/processed/data_mapping.xlsx", index=False)
data_mapping.head()