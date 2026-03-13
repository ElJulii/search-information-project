import os
import math

TFIDF_FOLDER = "tfidf_terms"
INDEX_FILE = "index.txt"


def load_documents():
    documents = {}
    vocabulary = set()

    for filename in os.listdir(TFIDF_FOLDER):

        if not filename.endswith(".txt"):
            continue

        doc_id = filename.replace("token_", "").replace(".txt", "")
        path = os.path.join(TFIDF_FOLDER, filename)

        documents[doc_id] = {}

        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                term, idf, tfidf = line.strip().split()

                tfidf = float(tfidf)

                documents[doc_id][term] = tfidf
                vocabulary.add(term)

    return documents, vocabulary


def load_urls():
    urls = {}

    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split(" ", 1)
            urls[parts[0]] = parts[1]

    return urls


def build_query_vector(query_terms, vocabulary):

    query_vector = {}

    for term in vocabulary:
        query_vector[term] = 0

    for term in query_terms:
        if term in query_vector:
            query_vector[term] += 1

    return query_vector


def cosine_similarity(query_vec, doc_vec):

    dot_product = 0
    query_norm = 0
    doc_norm = 0

    for term in query_vec:

        q = query_vec.get(term, 0)
        d = doc_vec.get(term, 0)

        dot_product += q * d
        query_norm += q ** 2
        doc_norm += d ** 2

    if query_norm == 0 or doc_norm == 0:
        return 0

    return dot_product / (math.sqrt(query_norm) * math.sqrt(doc_norm))


def search(query):

    documents, vocabulary = load_documents()
    urls = load_urls()

    query_terms = query.lower().split()

    query_vector = build_query_vector(query_terms, vocabulary)

    scores = []

    for doc_id, doc_vector in documents.items():

        score = cosine_similarity(query_vector, doc_vector)

        if score > 0:
            scores.append((doc_id, score))

    scores.sort(key=lambda x: x[1], reverse=True)

    print("\nTop search results:\n")

    for doc_id, score in scores[:10]:

        url = urls.get(doc_id, "Unknown URL")

        print(f"Document: {doc_id}")
        print(f"Score: {score}")
        print(f"URL: {url}")
        print()


def main():

    print("Vector Search Engine")
    print("--------------------")

    while True:

        query = input("\nEnter search query (or type 'exit'): ")

        if query.lower() == "exit":
            break

        search(query)


if __name__ == "__main__":
    main()