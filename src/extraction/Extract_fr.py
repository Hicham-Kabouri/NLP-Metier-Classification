# Extraction de données à partir du PDF français
"""
Extraction du dataset (Code, Metier) de la NAP 2014 (version française)
avec PyMuPDF (fitz), en utilisant la même logique que le script fourni
pour la version arabe.

Différence clé avec le script original (arabe) :
Dans le PDF français, l'ordre des lignes extraites par PyMuPDF est
CODE puis TEXTE (le code apparaît avant son libellé), et non
TEXTE puis CODE comme supposé dans le script arabe. L'algorithme a donc
été adapté en conséquence (on ouvre le "buffer" du texte APRES avoir vu
le code, et on le clôture quand le code suivant apparaît).

Deux ajustements supplémentaires, nécessaires uniquement pour le
français :
1. Restriction à la section "Structure de la nomenclature" (entre
   "GRAND GROUPE 0 :" et "ANNEXE :"), pour ignorer le sommaire et les
   numéros de page qui ressemblent parfois à des codes.
2. Sur quelques pages, le code et le libellé sont collés sur la même
   ligne (ex. "261    Cadres administratifs moyens" au lieu de deux
   lignes séparées) : un pré-traitement les sépare avant le parsing.
"""


doc_fr = pym.open("Nomenclature analytique des professions, Décembre 2014 (Version fr).pdf")

# transformer le contenu du PDF en une liste de lignes
lines = []
for page in doc_fr:
    text = page.get_text()
    for l in text.split("\n"):
        l = l.strip()
        if l:
            lines.append(l)

# limiter à la section "Structure de la nomenclature"
start_idx = next(i for i, l in enumerate(lines) if l.strip() == 'GRAND GROUPE 0 :')
end_idx = next(i for i, l in enumerate(lines) if i > start_idx and l.strip() == 'ANNEXE :')
lines = lines[start_idx:end_idx]

# séparer les lignes où code et texte sont collés ("261   Cadres ...")
clean_lines = []
for l in lines:
    m = re.match(r'^(\d{1,4})\s+(\S.*)$', l)
    if m:
        clean_lines.append(m.group(1))
        clean_lines.append(m.group(2))
    else:
        clean_lines.append(l)

records = []          # résultat final [(code, métier), ...]
current_code = None
current_level = None
buffer = []            # stocke le libellé en cours de lecture


def flush():
    """Enregistre le métier en cours (uniquement les codes à 4 chiffres)."""
    if current_code and current_level == 4:
        metier = re.sub(r'\s+', ' ', " ".join(buffer)).strip()
        if metier:
            records.append({"Code": current_code, "Metier": metier})


for line in clean_lines:
    if re.fullmatch(r"\d{1,4}", line):
        # nouveau code (1 à 4 chiffres) -> on clôture le métier précédent
        flush()
        current_code = line
        current_level = len(line)
        buffer = []
    else:
        buffer.append(line)
flush()  # dernier enregistrement de la boucle

tableau_fr = pd.DataFrame(records)

tableau_fr.drop_duplicates(subset="Code", inplace=True)
tableau_fr.reset_index(drop=True, inplace=True)

tableau_fr.to_excel("NAP_2014_vr_fr_01.xlsx", index=False)

print("Nombre de métiers :", len(tableau_fr))