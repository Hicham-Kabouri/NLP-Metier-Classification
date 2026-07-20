# fonctions de nettoyage

def clean_french(text):
    """
    Nettoyage du texte français.
    """

    if pd.isna(text):
        return ""

    text = str(text)

    # Suppression des espaces en début et fin
    text = text.strip()

    # Remplacement des espaces multiples par un seul
    text = re.sub(r"\s+", " ", text)

    # Passage en minuscules
    text = text.lower()

    return text