import os
import json

TOKENS_FOLDER = "output/tokens"
INDEX_FILE = "inverted_index.txt"

inverted_index = {}

print("Construyendo índice invertido...")

for filename in os.listdir(TOKENS_FOLDER):

    doc_id = os.path.splitext(filename)[0]
    filepath = os.path.join(TOKENS_FOLDER, filename)

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            term = line.strip()

            if term not in inverted_index:
                inverted_index[term] = set()

            inverted_index[term].add(doc_id)

# Convertir sets a listas ordenadas
for term in inverted_index:
    inverted_index[term] = sorted(list(inverted_index[term]))

# Guardar como JSON legible
with open(INDEX_FILE, "w", encoding="utf-8") as f:
    json.dump(inverted_index, f, indent=4)

print("Índice creado correctamente.")