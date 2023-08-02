import json
import collections

with open("./data/translations.json", "r") as translations_json_file:
    translations_json = json.load(translations_json_file)["words"]

with open("./data/output_data.json", "r") as output_data_file:
    output_data_json = json.load(output_data_file)["words"]

word_en_arpa_list = ["|".join(word_data["word_en_arpa"]) for word_data in output_data_json.values()]
word_en_arpa_redundancies = {

}

for word_en, word_data in output_data_json.items():
    word_en_arpa = "|".join(word_data["word_en_arpa"])

    if word_en_arpa in word_en_arpa_redundancies.keys():
        first_occurrence = word_en_arpa_redundancies[word_en_arpa][0]
        exact_match = True

        for feature in word_data.keys():
            if feature != "word_en" and word_data[feature] != output_data_json[first_occurrence][feature]:
                print(word_en, first_occurrence, feature, word_data[feature], output_data_json[first_occurrence][feature])
                exact_match = False
                break

        if exact_match:
            word_en_arpa_redundancies[word_en_arpa] += [word_en]
        else:
            print(word_en)
    elif word_en_arpa_list.count(word_en_arpa) > 1:
        word_en_arpa_redundancies[word_en_arpa] = [word_en]

with open("./data/redundancies.json", "w+") as redundancies_json_file:
    json.dump({
        "word_en_arpa": word_en_arpa_redundancies
    }, redundancies_json_file, ensure_ascii=False)
