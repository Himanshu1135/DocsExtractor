with open('name_corpus.txt', 'r') as file:
    corpus_content = file.read()

text = corpus_content.split()



sorted_words = sorted(text)

# filtered_words = [word for word in text if len(word) >= 4]

updated_corpus = '\n'.join(sorted_words)

with open('name_corpus.txt', 'w') as file:
    file.write(updated_corpus)

