# Construction de data mapping
data_set = pd.read_excel("NAP_2014_vr_fr.xlsx")
# construction de data mapping  merging tableau_fr avec data_set par code 
merge = data_set[["Code", "Intitule_Sous_Groupe", "Intitule_Sous_Grand_Groupe", "Intitule_Grand_Groupe"]]
# Fusion 
data_mapping = pd.merge(tableau_fr, merge, on="Code", how="left")
# Sauvgarder
data_mapping = data_mapping[["Code", "metier_fr", "metier_ar", "Intitule_Sous_Groupe", "Intitule_Sous_Grand_Groupe", "Intitule_Grand_Groupe"]]
data_mapping.to_excel("data_mapping.xlsx", index=False)
data_mapping.head()