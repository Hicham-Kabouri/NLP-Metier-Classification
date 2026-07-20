# Affichage des résultats
def afficher_resultats(resultats):

    print("\n" + "=" * 100)
    print("               TOP 5 DES CODES LES PLUS PROCHES")
    print("=" * 100)

    if resultats.empty:

        print("\nAucun métier suffisamment proche n'a été trouvé.")

        return

    for i, row in resultats.iterrows():

        print(f"\nRésultat {i+1}")

        print(f"Code                 : {row['Code']}")
        print(f"Score                : {row['Score']:.4f}")

        print(f"Métier (FR)          : {row['metier_fr']}")
        print(f"Métier (AR)          : {row['metier_ar']}")

        print(f"Sous-groupe          : {row['Intitule_Sous_Groupe']}")
        print(f"Sous-grand groupe    : {row['Intitule_Sous_Grand_Groupe']}")
        print(f"Grand groupe         : {row['Intitule_Grand_Groupe']}")

        print("-" * 100)


# Utilisation interactive
if __name__ == "__main__":

    # Le modèle, les embeddings et les DataFrames doivent être
    # chargés avant cette section.

    requete = input("\nEntrez une profession : ")

    resultats = rechercher_metier(
        requete,
        model,
        embeddings,
        reference_corpus_final,
        data_mapping,
    )

    afficher_resultats(resultats)