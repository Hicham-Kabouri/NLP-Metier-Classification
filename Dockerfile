# Image de base : Python léger
FROM python:3.10-slim

# Dossier de travail à l'intérieur du conteneur
WORKDIR /app

# Copier uniquement requirements.txt d'abord (optimisation du cache Docker)
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Pré-télécharger le modèle d'embedding dans l'image
# (évite de le re-télécharger à chaque démarrage du conteneur)
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')"

# Copier tout le reste du projet (code, embeddings, etc.)
COPY . .

# Port utilisé par Streamlit
EXPOSE 8501

# Commande de démarrage
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]