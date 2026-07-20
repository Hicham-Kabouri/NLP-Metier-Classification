# Chargement de l'ensemble de test


test_dataset = pd.read_excel(
    "data/test/data_nap_test.xlsx",
    dtype={"Code": str}
)

# Evaluation

resultats_evaluation = []

for _, row in test_dataset.iterrows():

    profession = row["Metier"]
    code_attendu = row["Code"]

    # Recherche
    resultats = rechercher_metier(
        profession,
        model,
        embeddings,
        reference_corpus_final,
        data_mapping,
        top_k=20,
        top_n=5,
        seuil=0.80,
    )

    # Aucun résultat
    if resultats.empty:

        resultats_evaluation.append({
            "Profession": profession,
            "Code_attendu": code_attendu,
            "Code_top1": "",
            "Score_top1": "",
            "Top1": False,
            "Top5": False,
            "Rang": None
        })

        continue

    # Liste des codes proposés
    codes = resultats["Code"].astype(str).tolist()

    # Premier code proposé
    code_top1 = codes[0]

    score_top1 = resultats.iloc[0]["Score"]

    # Top1
    top1 = (code_top1 == code_attendu)

    # Top5
    top5 = code_attendu in codes

    # Rang
    if top5:
        rang = codes.index(code_attendu) + 1
    else:
        rang = None

    resultats_evaluation.append({

        "Profession": profession,

        "Code_attendu": code_attendu,

        "Code_top1": code_top1,

        "Score_top1": score_top1,

        "Top1": top1,

        "Top5": top5,

        "Rang": rang

    })


# Résultats détaillés

evaluation = pd.DataFrame(resultats_evaluation)

evaluation.to_excel(
    "data/test/evaluation_results.xlsx",
    index=False
)


# Calcul des métriques

nombre_tests = len(evaluation)

top1_accuracy = evaluation["Top1"].mean()

top5_accuracy = evaluation["Top5"].mean()

nombre_top1 = evaluation["Top1"].sum()

nombre_top5 = evaluation["Top5"].sum()

# Sauvegarde des métriques

metrics = pd.DataFrame({

    "Métrique": [

        "Nombre de tests",

        "Top-1 Accuracy",

        "Top-5 Accuracy",

        "Top-1 Correct",

        "Top-5 Correct"

    ],

    "Valeur": [

        nombre_tests,

        top1_accuracy,

        top5_accuracy,

        nombre_top1,

        nombre_top5

    ]

})

metrics.to_excel(
    "tests/evaluation_metrics.xlsx",
    index=False
)

# Affichage

print("\n================== ÉVALUATION ==================")

print(f"Nombre de tests      : {nombre_tests}")

print(f"Top-1 Accuracy       : {top1_accuracy:.2%}")

print(f"Top-5 Accuracy       : {top5_accuracy:.2%}")

print("================================================")