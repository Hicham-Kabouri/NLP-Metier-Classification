
import re
import pandas as pd
import numpy as np
# Prétraitement du texte
def nettoyer_texte(texte):
    """
    Nettoie une requête utilisateur en français ou en arabe.

    Le nettoyage doit être identique à celui utilisé pour construire
    le corpus de référence.
    """

    if not isinstance(texte, str) or texte.strip() == "":
        return ""

    texte = texte.strip()
    texte = re.sub(r"\s+", " ", texte)

    # Détection de l'arabe
    contient_arabe = bool(re.search(r"[\u0600-\u06FF]", texte))

    if contient_arabe:

        diacritiques = re.compile(
            r"[\u0610-\u061A\u064B-\u065F\u06D6-\u06DC\u06DF-\u06E8\u06EA-\u06ED]"
        )

        texte = diacritiques.sub("", texte)

        texte = (
            texte.replace("أ", "ا")
                 .replace("إ", "ا")
                 .replace("آ", "ا")
                 .replace("ى", "ي")
                 .replace("ة", "ه")
        )

    else:

        texte = texte.lower()

        texte = re.sub(
            r"[^\w\séàâäéèêëïîôöùûüç'-]",
            " ",
            texte,
            flags=re.UNICODE
        )

        texte = re.sub(r"\s+", " ", texte).strip()

    return texte


# Moteur de recherche sémantique
def rechercher_metier(
    requete,
    model,
    embeddings,
    reference_corpus_final,
    data_mapping,
    top_k=20,
    top_n=5,
    seuil=0.50,
):
    """
    Recherche les codes NAP les plus proches d'une profession.

    Retour
    ------
    DataFrame contenant :
        Code
        Score
        metier_fr
        metier_ar
        Intitule_Sous_Groupe
        Intitule_Sous_Grand_Groupe
        Intitule_Grand_Groupe
    """

    colonnes_resultat = [
        "Code",
        "Score",
        "metier_fr",
        "metier_ar",
        "Intitule_Sous_Groupe",
        "Intitule_Sous_Grand_Groupe",
        "Intitule_Grand_Groupe",
    ]

    # Prétraitement

    requete = nettoyer_texte(requete)

    if requete == "":
        return pd.DataFrame(columns=colonnes_resultat)

    # Embedding de la requête

    requete_embedding = model.encode(
        requete,
        normalize_embeddings=True,
        convert_to_numpy=True,
    )

    # Similarité cosinus

    similarites = embeddings @ requete_embedding

    # Top K

    indices_topk = np.argsort(similarites)[::-1][:top_k]

    topk = reference_corpus_final.iloc[indices_topk].copy()

    topk["Score"] = similarites[indices_topk]

    # Filtre par seuil

    topk = topk[topk["Score"] >= seuil]

    if topk.empty:
        return pd.DataFrame(columns=colonnes_resultat)

    # Suppression des doublons de Code

    top_codes = topk.drop_duplicates(
        subset="Code",
        keep="first"
    )

    # Top N

    topn = top_codes.head(top_n)

    # Fusion avec data_mapping

    resultats = topn.merge(
        data_mapping,
        on="Code",
        how="left"
    )

    resultats = resultats[colonnes_resultat]

    resultats["Score"] = resultats["Score"].round(4)

    resultats = (
        resultats
        .sort_values("Score", ascending=False)
        .reset_index(drop=True)
    )

    return resultats