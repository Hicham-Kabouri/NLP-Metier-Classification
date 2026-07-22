import streamlit as st
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from src.search_engine.search_engine import rechercher_metier

st.set_page_config(page_title="Recherche de codes Proffession (NAP)", layout="wide")

# --- Chargement (une seule fois, mis en cache) ---

@st.cache_resource
def load_model():
    return SentenceTransformer("sentence-transformers/paraphrase-multilingual-mpnet-base-v2")

@st.cache_resource
def load_data():
    embeddings = np.load("data/processed/embeddings.npy")
    reference_corpus_final = pd.read_excel("data/processed/reference_corpus_final.xlsx")
    data_mapping = pd.read_excel("data/processed/data_mapping.xlsx")
    return embeddings, reference_corpus_final, data_mapping

model = load_model()
embeddings, reference_corpus_final, data_mapping = load_data()

# --- Interface ---

st.title("🔎 Recherche de codes professions (NAP)")
st.write("Entrez une profession en français ou en arabe pour trouver les codes les plus proches.")

requete = st.text_input("Profession recherchée :")

if requete:
    with st.spinner("Recherche en cours..."):
        resultats = rechercher_metier(
            requete,
            model,
            embeddings,
            reference_corpus_final,
            data_mapping,
        )

    if resultats.empty:
        st.warning(
            "Aucune profession suffisamment proche n'a été trouvée. "
            "Cette requête ne semble correspondre à aucune profession "
            "du référentiel NAP. Essayez de reformuler votre recherche."
        )
    else:
        st.subheader(f"Top {len(resultats)} résultats")

        for i, row in resultats.iterrows():
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**Code :** {row['Code']}")
                    st.markdown(f"**Profession (FR) :** {row['metier_fr']}")
                    st.markdown(f"**Profession (AR) :** {row['metier_ar']}")
                    st.caption(
                        f"{row['Intitule_Sous_Groupe']} → "
                        f"{row['Intitule_Sous_Grand_Groupe']} → "
                        f"{row['Intitule_Grand_Groupe']}"
                    )
                with col2:
                    st.metric("Score", f"{row['Score']:.3f}")