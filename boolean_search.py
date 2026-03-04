import json

INDEX_FILE = "inverted_index.txt"

# Cargar índice
with open(INDEX_FILE, "r", encoding="utf-8") as f:
    inverted_index = json.load(f)

all_docs = set()
for docs in inverted_index.values():
    all_docs.update(docs)

def evaluate_query(query):

    tokens = query.replace("(", " ( ").replace(")", " ) ").split()

    def get_postings(term):
        return set(inverted_index.get(term.lower(), []))

    def parse(tokens):

        def parse_expression():
            result = parse_term()
            while tokens and tokens[0] == "OR":
                tokens.pop(0)
                result = result.union(parse_term())
            return result

        def parse_term():
            result = parse_factor()
            while tokens and tokens[0] == "AND":
                tokens.pop(0)
                result = result.intersection(parse_factor())
            return result

        def parse_factor():
            token = tokens.pop(0)

            if token == "NOT":
                return all_docs - parse_factor()

            elif token == "(":
                result = parse_expression()
                tokens.pop(0)  # remove ')'
                return result

            else:
                return get_postings(token)

        return parse_expression()

    return parse(tokens)

while True:
    query = input("Write the boolean query (or 'exit'): ")

    if query.lower() == "exit":
        break

    try:
        result = evaluate_query(query)
        print("Documents found:", sorted(result))
    except Exception as e:
        print("Error in the query:", e)