# Extraction du fichier PDF officiel de la nomenclature analytique des professions (NAP 2014) en français

OUT_PATH = r"C:\Users\hp\Documents\NLP-Metier-Classification\data\interim\metiers_fr.xlsx"

doc_fr = pym.open("data/raw/Nomenclature analytique des professions, Décembre 2014 (Version Fr).pdf")

# 1) transformer le contenu du PDF en une liste de lignes
lines = []
for page in doc_fr:
    text = page.get_text()
    for l in text.split("\n"):
        l = l.strip()
        if l:
            lines.append(l)

# 2) limiter à la section "Structure de la nomenclature" (avant l'annexe
#    des définitions, qui répète du texte et perturberait le parsing)
start_idx = next(i for i, l in enumerate(lines) if l.strip() == "GRAND GROUPE 0 :")
end_idx = next(i for i, l in enumerate(lines) if i > start_idx and l.strip() == "ANNEXE :")
lines = lines[start_idx:end_idx]

# 3) pré-traitement : sur quelques pages, le code et son libellé sont collés
#    sur la même ligne (ex. "261    Cadres administratifs moyens" au lieu de
#    deux lignes séparées) -> on les sépare pour uniformiser le flux
clean_lines = []
for l in lines:
    m = re.match(r"^(\d{1,4})\s+(\S.*)$", l)
    if m:
        clean_lines.append(m.group(1))
        clean_lines.append(m.group(2))
    else:
        clean_lines.append(l)

# 4) parcourir les lignes et reconstituer la hiérarchie à 4 niveaux :
#    grand groupe (1 chiffre, précédé de "GRAND GROUPE n :"),
#    sous-grand groupe (2 chiffres), sous-groupe (3 chiffres),
#    groupe de base = le métier (4 chiffres)
results = []          # une entrée par code (tous niveaux confondus)
grand_titles = {}      # {code_grand_groupe: intitulé}

current_gg = None
gg_title_parts = None
current_code = None
current_level = None
buffer = []


def flush_item():
    if current_code is not None:
        metier = re.sub(r"\s+", " ", " ".join(buffer)).strip()
        if metier:
            results.append({
                "code": current_code,
                "text": metier,
                "level": current_level,
                "grand_groupe": current_gg,
            })


i = 0
n = len(clean_lines)
while i < n:
    line = clean_lines[i]

    m_gg = re.match(r"^GRAND GROUPE\s+(\d+)\s*:?$", line.upper())
    if m_gg:
        flush_item()
        current_code, buffer = None, []
        if current_gg is not None and gg_title_parts is not None:
            grand_titles[current_gg] = re.sub(r"\s+", " ", " ".join(gg_title_parts)).strip()
        current_gg = m_gg.group(1)
        gg_title_parts = []
        i += 1
        # le titre du grand groupe est écrit en MAJUSCULES sur les lignes
        # suivantes, jusqu'à ce qu'un code (2 chiffres) apparaisse
        while i < n:
            nxt = clean_lines[i]
            letters = re.sub(r"[^A-Za-zÀ-ÖØ-öø-ÿ]", "", nxt)
            if re.fullmatch(r"\d{1,4}", nxt) or (letters and not letters.isupper()):
                break
            gg_title_parts.append(nxt)
            i += 1
        continue

    if re.fullmatch(r"\d{1,4}", line):
        flush_item()
        current_code = line
        current_level = len(line)
        buffer = []
        i += 1
        continue

    buffer.append(line)
    i += 1

flush_item()
if current_gg is not None and gg_title_parts is not None:
    grand_titles[current_gg] = re.sub(r"\s+", " ", " ".join(gg_title_parts)).strip()

# supprimer les doublons de code (le PDF officiel contient une coquille :
# le code 1939 est imprimé deux fois avec deux intitulés différents)
seen = set()
dedup_results = []
for r in results:
    if r["code"] not in seen:
        seen.add(r["code"])
        dedup_results.append(r)
results = dedup_results

by_code = {r["code"]: r for r in results}


def parents(code):
    return code[0], (code[:2] if len(code) >= 2 else None), (code[:3] if len(code) >= 3 else None)


# 5) construire le fichier Excel (4 feuilles)
wb = Workbook()
ws = wb.active
ws.title = "NAP_2014_vr_fr"
ws.append(["Code", "Metier", "Code_Sous_Groupe", "Intitule_Sous_Groupe",
           "Code_Sous_Grand_Groupe", "Intitule_Sous_Grand_Groupe",
           "Code_Grand_Groupe", "Intitule_Grand_Groupe"])
for cell in ws[1]:
    cell.font = Font(bold=True, color="FFFFFF", name="Arial")
    cell.fill = PatternFill("solid", start_color="4472C4")
    cell.alignment = Alignment(horizontal="center", vertical="center")

for item in sorted((x for x in results if x["level"] == 4), key=lambda x: x["code"]):
    code = item["code"]
    p1, p2, p3 = parents(code)
    ws.append([
        code, item["text"],
        p3, by_code.get(p3, {}).get("text", ""),
        p2, by_code.get(p2, {}).get("text", ""),
        p1, grand_titles.get(p1, ""),
    ])
for i, w in enumerate([10, 60, 14, 40, 14, 45, 12, 55], 1):
    ws.column_dimensions[get_column_letter(i)].width = w
for row in ws.iter_rows(min_row=2):
    for cell in row:
        cell.font = Font(name="Arial", size=10)
ws.freeze_panes = "A2"

ws2 = wb.create_sheet("Sous_Groupes")
ws2.append(["Code", "Intitule", "Code_Sous_Grand_Groupe", "Code_Grand_Groupe", "Intitule_Grand_Groupe"])
for cell in ws2[1]:
    cell.font = Font(bold=True, color="FFFFFF", name="Arial")
    cell.fill = PatternFill("solid", start_color="4472C4")
for item in sorted((x for x in results if x["level"] == 3), key=lambda x: x["code"]):
    code = item["code"]
    p1, p2, _ = parents(code)
    ws2.append([code, item["text"], p2, p1, grand_titles.get(p1, "")])
for i, w in enumerate([10, 60, 16, 12, 55], 1):
    ws2.column_dimensions[get_column_letter(i)].width = w

ws3 = wb.create_sheet("Sous_Grands_Groupes")
ws3.append(["Code", "Intitule", "Code_Grand_Groupe", "Intitule_Grand_Groupe"])
for cell in ws3[1]:
    cell.font = Font(bold=True, color="FFFFFF", name="Arial")
    cell.fill = PatternFill("solid", start_color="4472C4")
for item in sorted((x for x in results if x["level"] == 2), key=lambda x: x["code"]):
    code = item["code"]
    ws3.append([code, item["text"], code[0], grand_titles.get(code[0], "")])
for i, w in enumerate([10, 60, 12, 55], 1):
    ws3.column_dimensions[get_column_letter(i)].width = w

ws4 = wb.create_sheet("Grands_Groupes")
ws4.append(["Code", "Intitule"])
for cell in ws4[1]:
    cell.font = Font(bold=True, color="FFFFFF", name="Arial")
    cell.fill = PatternFill("solid", start_color="4472C4")
for code in sorted(grand_titles):
    ws4.append([code, grand_titles[code]])
ws4.column_dimensions["A"].width = 10
ws4.column_dimensions["B"].width = 90


wb.save(OUT_PATH)

print("Groupes de base (métiers) :", sum(1 for x in results if x["level"] == 4))
print("Sous-groupes               :", sum(1 for x in results if x["level"] == 3))
print("Sous-grands groupes        :", sum(1 for x in results if x["level"] == 2))
print("Grands groupes             :", len(grand_titles))

tableau_fr = pd.read_excel("data/interim/metiers_fr.xlsx ")
tableau_fr["Code"] = tableau_fr["Code"].astype(str)
for i in tableau_fr.index:
    if len(tableau_fr.loc[i, "Code"]) == 3:
        tableau_fr.loc[i, "Code"] = "0" + tableau_fr.loc[i, "Code"]
tableau_fr.head()