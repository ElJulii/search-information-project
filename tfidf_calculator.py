import os
import math
from collections import Counter

TOKENS_FOLDER = "output/tokens"
LEMMAS_FOLDER = "output/lemmas"

TFIDF_TERMS_FOLDER = "tfidf_terms"
TFIDF_LEMMAS_FOLDER = "tfidf_lemmas"

os.makedirs(TFIDF_TERMS_FOLDER, exist_ok=True)
os.makedirs(TFIDF_LEMMAS_FOLDER, exist_ok=True)


def load_documents(folder):
    documents = {}
    
    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)
        
        with open(path, "r", encoding="utf-8") as f:
            terms = [line.strip() for line in f if line.strip()]
            
        documents[filename] = terms
    
    return documents


def compute_document_frequency(documents):

    df = {}

    for terms in documents.values():
        unique_terms = set(terms)

        for term in unique_terms:
            df[term] = df.get(term, 0) + 1

    return df


def compute_idf(df, total_docs):

    idf = {}

    for term, freq in df.items():
        idf[term] = math.log(total_docs / freq)

    return idf


def compute_tf(terms):

    total_terms = len(terms)
    counts = Counter(terms)

    tf = {}

    for term, count in counts.items():
        tf[term] = count / total_terms

    return tf


def compute_tfidf(documents, idf, output_folder):

    for doc_name, terms in documents.items():

        tf = compute_tf(terms)

        output_path = os.path.join(output_folder, doc_name)

        with open(output_path, "w", encoding="utf-8") as f:

            for term, tf_value in tf.items():

                term_idf = idf.get(term, 0)
                tfidf = tf_value * term_idf

                f.write(f"{term} {term_idf} {tfidf}\n")

        print(f"TF-IDF file generated for document: {doc_name}")


def main():

    print("Loading token documents...")
    token_docs = load_documents(TOKENS_FOLDER)

    print("Loading lemma documents...")
    lemma_docs = load_documents(LEMMAS_FOLDER)

    total_docs = len(token_docs)

    print(f"Total documents: {total_docs}")

    print("Computing document frequency for terms...")
    df_terms = compute_document_frequency(token_docs)

    print("Computing document frequency for lemmas...")
    df_lemmas = compute_document_frequency(lemma_docs)

    print("Computing IDF values...")
    idf_terms = compute_idf(df_terms, total_docs)
    idf_lemmas = compute_idf(df_lemmas, total_docs)

    print("Computing TF-IDF for terms...")
    compute_tfidf(token_docs, idf_terms, TFIDF_TERMS_FOLDER)

    print("Computing TF-IDF for lemmas...")
    compute_tfidf(lemma_docs, idf_lemmas, TFIDF_LEMMAS_FOLDER)

    print("TF-IDF computation completed successfully.")


if __name__ == "__main__":
    main()