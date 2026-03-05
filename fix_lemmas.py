import os

INPUT_FOLDER = "tfidf_lemmas"

for filename in os.listdir(INPUT_FOLDER):

    if not filename.endswith(".txt"):
        continue

    file_path = os.path.join(INPUT_FOLDER, filename)

    new_lines = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:

            parts = line.strip().split()

            if len(parts) == 4:
                lemma = parts[0]
                idf = parts[2]
                tfidf = parts[3]

                new_lines.append(f"{lemma} {idf} {tfidf}\n")

            elif len(parts) == 3:
                new_lines.append(line)

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

print("Lemma files corrected successfully.")