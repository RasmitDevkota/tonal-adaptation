import json
import regex
import atexit

with open("./data/translations.json", "r") as translations_good_json_file:
    translations_good_json = json.load(translations_good_json_file)
    words_good_json = translations_good_json["words"]

with open("./data/translations_bad.json", "r") as translations_bad_json_file:
    translations_bad_raw = translations_bad_json_file.read()
    if len(translations_bad_raw) == 0:
        translations_bad_json = {
            "words" : {

            }
        }
    else:
        translations_bad_json = json.loads(translations_bad_raw)

    words_bad_json = translations_bad_json["words"]

delete_keys = []

def save_progress():
    for delete_key in delete_keys:
        del translations_good_json["words"][delete_key]

    with open("./data/translations_good.json", "w+") as translations_good_json_file:
        json.dump(translations_good_json, translations_good_json_file, ensure_ascii=False)

    with open("./data/translations_bad.json", "w+") as translations_bad_json_file:
        json.dump(translations_bad_json, translations_bad_json_file, ensure_ascii=False)

atexit.register(save_progress)

for word_en, word_data in words_good_json.items():
    translations = word_data["translations"]

    bad = False
    bad_translation_data = {
        "translations_good": {

        },
        "translations_bad": {
            "untranslated" : {

            },
            "illegal_chars" : {

            },
            "inconsistent" : {

            }
        }
    }

    base_translation = translations["googletrans"]
    for translator, translation in translations.items():
        if translation == "FAILED" or translation == "":
            continue
        elif translation.lower() == word_en.lower():
            bad = True
            bad_translation_data["translations_bad"]["untranslated"][translator] = translation
        elif regex.search("[a-zA-Z ]|[^\u4e00-\u9fff]", translation):
            bad = True
            bad_translation_data["translations_bad"]["illegal_chars"][translator] = translation
        elif translation != base_translation:
            bad = True
            bad_translation_data["translations_bad"]["inconsistent"][translator] = translation
        else:
            bad_translation_data["translations_good"][translator] = translation

    if bad:
        delete_keys.append(word_en)
        translations_bad_json["words"][word_en] = bad_translation_data

