def clean_arabic(text):
    """
    Nettoyage du texte arabe.
    """

    if pd.isna(text):
        return ""

    text = str(text)

    # Suppression du Tashkeel (voyelles courtes/diacritiques)
    tashkeel_pattern = re.compile(
        r"[\u064B\u064C\u064D\u064E\u064F\u0650\u0651\u0652]"
    )
    text = re.sub(tashkeel_pattern, "", text)

    # Suppression des espaces
    text = text.strip()

    # Suppression des espaces multiples
    text = re.sub(r"\s+", " ", text)

    # Suppression du Tatweel
    text = text.replace("ـ", "")

    # Normalisation de certaines lettres
    text = re.sub("[إأآا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("ؤ", "و", text)
    text = re.sub("ئ", "ي", text)

    return text