with open("./corpus.csv", "r+") as corpus_original:
    corpus_original_text = [line for line in corpus_original.readlines()]

    corpus_filtered_text = []
    for word in corpus_original_text:
        if word not in corpus_filtered_text:
            corpus_filtered_text.append(word)

    with open("./corpus.csv", "w+") as corpus_filtered:
        corpus_filtered.writelines(corpus_filtered_text)
