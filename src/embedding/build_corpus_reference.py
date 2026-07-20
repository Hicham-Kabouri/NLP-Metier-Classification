# Construction de embedding_corpus

embedding_corpus = data_mapping[["Code", "metier_fr", "metier_ar"]]

# application du nettoyage

embedding_corpus["metier_fr"] = embedding_corpus["metier_fr"].apply(clean_french)
embedding_corpus["metier_ar"] = embedding_corpus["metier_ar"].apply(clean_arabic)


# Suppression des doublons


embedding_corpus = embedding_corpus.drop_duplicates()

# Réinitialisation des index

embedding_corpus = embedding_corpus.reset_index(drop=True)


print("Prétraitement terminé avec succès.")
print(f"Nombre de lignes : {len(embedding_corpus)}")

#  Construire le corpus de référence

reference_corpus = pd.concat([
    pd.DataFrame({
        "Code": embedding_corpus["Code"],
        "type": "FR",
        "Profession": embedding_corpus["metier_fr"]
    }),

    pd.DataFrame({
        "Code": embedding_corpus["Code"],
        "type": "AR",
        "Profession": embedding_corpus["metier_ar"]
    })

], ignore_index=True)

# Supprimer les lignes vides

reference_corpus = reference_corpus.dropna(subset=["Profession"])

reference_corpus = reference_corpus[
    reference_corpus["Profession"].str.strip() != ""
]

# Définir l'ordre souhaité : fr puis ar

reference_corpus["type"] = pd.Categorical(
    reference_corpus["type"],
    categories=["FR", "AR"],
    ordered=True
)

# Trier selon le code et le type (fr/ar)

reference_corpus = reference_corpus.sort_values(
    by=["Code", "type"]
).reset_index(drop=True)

data_train = pd.read_excel("data/processed/Nomenclatures_NAP2014.xlsx", dtype={"Code": str})
data_train = data_train.rename(columns={
    "Texte (FR)": "Profession(FR)",
    "Texte (AR)": "Profession(AR)"
})

# application du nettoyage

data_train["Profession(FR)"] = data_train["Profession(FR)"].apply(clean_french)
data_train["Profession(AR)"] = data_train["Profession(AR)"].apply(clean_arabic)


# Suppression des doublons


data_train = data_train.drop_duplicates()

# Réinitialisation des index

data_train = data_train.reset_index(drop=True)


print("Prétraitement terminé avec succès.")
print(f"Nombre de lignes : {len(data_train)}")

#  Construire le corpus de référence

reference_corpus_clean = pd.concat([
    pd.DataFrame({
        "Code": data_train["Code"],
        "type": "FR",
        "Profession": data_train["Profession(FR)"]
    }),

    pd.DataFrame({
        "Code": data_train["Code"],
        "type": "AR",
        "Profession": data_train["Profession(AR)"]
    })

], ignore_index=True)

# Supprimer les lignes vides

reference_corpus_clean = reference_corpus_clean.dropna(subset=["Profession"])

reference_corpus_clean = reference_corpus_clean[
    reference_corpus_clean["Profession"].str.strip() != ""
]

# Définir l'ordre souhaité : fr puis ar

reference_corpus_clean["type"] = pd.Categorical(
    reference_corpus_clean["type"],
    categories=["FR", "AR"],
    ordered=True
)

# Trier selon le code et le type (fr/ar)

reference_corpus_clean = reference_corpus_clean.sort_values(
    by=["Code", "type"]
).reset_index(drop=True)

# Fusion verticale
reference_corpus_final = pd.concat([reference_corpus_clean, reference_corpus], ignore_index=True)

# Trier par code
reference_corpus_final = reference_corpus_final.sort_values(by="Code").reset_index(drop=True)
# suprimer les doublons
reference_corpus_final = reference_corpus_final.drop_duplicates()
# Sauvegarder
reference_corpus_final.to_excel("data/processed/reference_corpus_final.xlsx", index=False)
reference_corpus_final.head()
