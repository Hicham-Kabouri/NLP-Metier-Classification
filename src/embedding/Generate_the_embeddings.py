# Générer les embeddings
embeddings = model.encode(
    reference_corpus_final["Profession"].tolist(),
    batch_size=64,
    normalize_embeddings=True,
    show_progress_bar=True,
    convert_to_numpy=True
)

# Sauvegarder les embeddings
np.save(
    "data/processed/embeddings.npy",
    embeddings
)

# Sauvegarder les métadonnées
reference_corpus_final[
    ["Code", "type", "Profession"]
].to_csv(
    "data/processed/reference_metadata.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nEmbeddings générés avec succès.")
print(f"Nombre d'observations : {embeddings.shape[0]}")
print(f"Dimension des vecteurs : {embeddings.shape[1]}")