import json
import pronouncing

with open("./data/failed_corpus_new.json", "r") as failed_words_json_file:
    failed_words_raw = failed_words_json_file.read()

    if len(failed_words_raw) == 0:
        failed_words_json = {
            "words" : {

            }
        }
    else:
        failed_words_json = json.loads(failed_words_raw)["words"]

for word_en, word_data in failed_words_json.items():
    print(pronouncing.phones_for_word(word_en))

