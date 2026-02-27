import os
import spacy
from bs4 import BeautifulSoup

nlp = spacy.load("en_core_web_sm")

PAGES_FOLDER = "pages"
OUTPUT_FOLDER = "output"
TOKENS_FOLDER = os.path.join(OUTPUT_FOLDER, "tokens")
LEMMAS_FOLDER = os.path.join(OUTPUT_FOLDER, "lemmas")

# Crear carpetas si no existen
os.makedirs(TOKENS_FOLDER, exist_ok=True)
os.makedirs(LEMMAS_FOLDER, exist_ok=True)

print("Procesando archivos individualmente...")

# Procesar cada archivo de pages
for filename in os.listdir(PAGES_FOLDER):

    page_path = os.path.join(PAGES_FOLDER, filename)

    # Leer HTML
    with open(page_path, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()

    # Quitar etiquetas HTML
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator=" ")

    doc = nlp(text.lower())

    tokens_set = set()
    lemma_dict = {}

    for token in doc:
        if (
            token.is_alpha and
            not token.is_stop and
            not token.is_punct and
            len(token.text) > 2
        ):
            word = token.text
            lemma = token.lemma_

            tokens_set.add(word)

            if lemma not in lemma_dict:
                lemma_dict[lemma] = set()

            lemma_dict[lemma].add(word)

    # Nombre base sin extensión
    base_name = os.path.splitext(filename)[0]

    # Guardar tokens del archivo
    tokens_output_path = os.path.join(TOKENS_FOLDER, f"token_{base_name}.txt")
    with open(tokens_output_path, "w", encoding="utf-8") as f:
        for token in sorted(tokens_set):
            f.write(token + "\n")

    # Guardar lemmas del archivo
    lemmas_output_path = os.path.join(LEMMAS_FOLDER, f"lemma_{base_name}.txt")
    with open(lemmas_output_path, "w", encoding="utf-8") as f:
        for lemma in sorted(lemma_dict.keys()):
            tokens_line = " ".join(sorted(lemma_dict[lemma]))
            f.write(f"{lemma} {tokens_line}\n")

    print(f"Procesado: {filename}")

print("Proceso terminado.")