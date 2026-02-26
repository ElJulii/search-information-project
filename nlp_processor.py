import os
import spacy
from bs4 import BeautifulSoup

# Cargar modelo en inglés
nlp = spacy.load("en_core_web_sm")

PAGES_FOLDER = "pages"
OUTPUT_FOLDER = "output"

# Crear carpeta output si no existe
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

all_tokens = set()
lemma_dict = {}

print("Procesando archivos...")

# Leer todos los archivos HTML
for filename in os.listdir(PAGES_FOLDER):
    filepath = os.path.join(PAGES_FOLDER, filename)

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()

        # Quitar HTML
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(separator=" ")

        # Procesar con spaCy
        doc = nlp(text.lower())

        for token in doc:
            # Filtrar basura
            if (
                token.is_alpha and              # solo letras
                not token.is_stop and           # no stopwords
                not token.is_punct and          # no puntuación
                len(token.text) > 2             # evitar palabras muy cortas
            ):
                word = token.text
                lemma = token.lemma_

                # Agregar token único
                all_tokens.add(word)

                # Agrupar por lemma
                if lemma not in lemma_dict:
                    lemma_dict[lemma] = set()

                lemma_dict[lemma].add(word)

# Guardar tokens.txt
with open(os.path.join(OUTPUT_FOLDER, "tokens.txt"), "w", encoding="utf-8") as f:
    for token in sorted(all_tokens):
        f.write(token + "\n")

# Guardar lemmas.txt
with open(os.path.join(OUTPUT_FOLDER, "lemmas.txt"), "w", encoding="utf-8") as f:
    for lemma in sorted(lemma_dict.keys()):
        tokens_list = " ".join(sorted(lemma_dict[lemma]))
        f.write(f"{lemma} {tokens_list}\n")

print("Proceso terminado.")
print("Archivos generados en carpeta 'output'.")