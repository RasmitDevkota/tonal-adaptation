import os
import re
import json
import atexit
import requests
import unicodedata
import pronouncing
from dragonmapper import hanzi
from arpa2ipa import arpa_to_ipa
import arpabetandipaconvertor.phoneticarphabet2arpabet as ipa_to_arpa
from syllabifier import syllabifyARPA

APP_ID = os.getenv("APP_ID")
APP_KEY = os.getenv("APP_KEY")

convertor = ipa_to_arpa.PhoneticAlphabet2ARPAbetConvertor()

tones = {
    "": 1,
    "ˊ": 2,
    "ˇ": 3,
    "ˋ": 4,
    "˙": 5
}

table = {
    0x304: ord('1'),
    0x301: ord('2'),
    0x30c: ord('3'),
    0x300: ord('4')
}

with open("./data/translations.json", "r") as translations_good_json_file:
    translations_good_json = json.load(translations_good_json_file)
    words_good_json = translations_good_json["words"]

with open("./data_sources/oxford_dictionaries_api.json", "r") as oxford_dict_json_file:
    oxford_dict_raw = oxford_dict_json_file.read()

    if len(oxford_dict_raw) == 0:
        language = "en-us"
        request_url = f"https://od-api.oxforddictionaries.com/api/v2/entries/{language}/{word_en.lower()}"
        response_object = requests.get(request_url, headers={"app_id": APP_ID, "app_key": APP_KEY})
        oxford_dict_json = json.loads(response_object.content)
    else:
        oxford_dict_json = json.loads(oxford_dict_raw)

with open("./data/output_data.json", "r") as output_data_file:
    output_data_raw = output_data_file.read()

    if len(output_data_raw) == 0:
        output_data_json = {
            "words" : {

            }
        }
    else:
        output_data_json = json.loads(output_data_raw)

with open("./data/failed_corpus.json", "r") as failed_words_json_file:
    failed_words_raw = failed_words_json_file.read()

    if len(failed_words_raw) == 0:
        failed_words_json = {
            "words" : {

            }
        }
    else:
        failed_words_json = json.loads(failed_words_raw)

# def save_progress():
#     with open("./data/output_data.json", "w+") as output_data_json_file:
#         json.dump(output_data_json, output_data_json_file, ensure_ascii=False)

#     with open("./data/failed_corpus.json", "w+") as failed_words_json_file:
#         json.dump(failed_words_json, failed_words_json_file, ensure_ascii=False)

# atexit.register(save_progress)

for word_en, word_data in words_good_json.items():
    translations = word_data["translations"]
    translation = translations["googletrans"]

    output_datum = {}

    try:
        output_datum = output_data_json["words"][word_en]
    except:
        output_datum = {
            "word_en" : word_en,
            "word_zh": translation,
            "word_en_arpa": None,
            "syllables_en_arpa": None,
            "syllables_en_ipa": None,
            "onset_en_ipa": None, # ***
            "stresses_en": None, # ***
            "word_zh_pinyin": None,
            "onset_zh_pinyin": None, # ***
            "syllables_zh_ipa": None,
            "onset_zh_ipa": None, # ***
            "onset_tone_num": None, # ***
        }

    # english arpa
    word_en_arpa = output_datum["word_en_arpa"]
    if not word_en_arpa:
        # cmu
        word_en_arpa = pronouncing.phones_for_word(word_en)

        if len(word_en_arpa) == 0:
            # oxford
            try:
                lexical_entry = oxford_dict_json[word_en]["results"][0]["lexicalEntries"][0]
                if lexical_entry["lexicalCategory"]["id"] == "noun":
                    phonetic_spelling = lexical_entry["entries"][0]["pronunciations"][0]["phoneticSpelling"]
                    ipa_spelling = re.sub(r"[\u0300-\u0302]|[\u0304-\u036f]|ˈ|ˌ", "", unicodedata.normalize("NFD", phonetic_spelling))
                    word_en_arpa = [convertor.convert(ipa_spelling)]
                    continue
                else:
                    failed_words_json["words"][word_en] = "phones_for_word"
                    continue
            except Exception as e:
                failed_words_json["words"][word_en] = "phones_for_word"
                continue

        if len(word_en_arpa) > 1 and (word_en_arpa[0].split(" ")[0] != word_en_arpa[1].split(" ")[0]):
            failed_words_json["words"][word_en] = f"onset_arpa_variation: {word_en_arpa}"

        output_datum["word_en_arpa"] = word_en_arpa[0].split(" ")

    # english syllabification
    syllables_en_arpa = output_datum["syllables_en_arpa"]
    if not syllables_en_arpa:
        try:
            syllables_en_arpa = syllabifyARPA(word_en_arpa[0])

            output_datum["syllables_en_arpa"] = syllables_en_arpa
        except Exception as e:
            failed_words_json["words"][word_en] = f"syllabifyARPA: {word_en_arpa[0]}"
            print(word_en, e)
            continue

    syllables_en_ipa = output_datum["syllables_en_ipa"]
    if not syllables_en_ipa:
        syllables_en_ipa = [arpa_to_ipa(syllable).replace(" ", "") for syllable in syllables_en_arpa]

        output_datum["syllables_en_ipa"] = syllables_en_ipa

    onset_en_ipa = output_datum["onset_en_ipa"]
    if not onset_en_ipa:
        # @TODO - Is individual syllable conversion (without full word context) reliable? Desirable?
        onset_en_ipa = arpa_to_ipa(syllables_en_arpa[0]).replace(" ", "")

        output_datum["onset_en_ipa"] = onset_en_ipa

    # english stress
    stresses_en = output_datum["stresses_en"]
    if not stresses_en:
        stresses_en = [int(phone[-1]) for phone in word_en_arpa[0] if phone[-1] in "0123456789"]

        output_datum["stresses_en"] = stresses_en

        if len(syllables_en_arpa) != len(stresses_en):
            failed_words_json["words"][word_en] = f"stresses_en: {len(syllables_en_arpa)} != {len(stresses_en)}"
            continue

    # mandarin pinyin
    word_zh_pinyin = output_datum["word_zh_pinyin"]
    onset_zh_pinyin = output_datum["onset_zh_pinyin"]
    if not word_zh_pinyin or not onset_zh_pinyin:
        pinyin_non_unicode = hanzi.to_pinyin(" ".join(list(translation)))
        pinyin_unicode = unicodedata.normalize('NFD', pinyin_non_unicode).translate(table)
        word_zh_pinyin = pinyin_unicode.split(" ")
        onset_zh_pinyin = word_zh_pinyin[0]

        output_datum["word_zh_pinyin"] = word_zh_pinyin
        output_datum["onset_zh_pinyin"] = onset_zh_pinyin

    # mandarin ipa
    syllables_zh_ipa = output_datum["syllables_zh_ipa"]
    onset_zh_ipa = output_datum["onset_zh_ipa"]
    if not syllables_zh_ipa or not onset_zh_ipa:
        try:
            syllables_zh_ipa = hanzi.to_ipa(" ".join(list(translation)))
            onset_zh_ipa = syllables_zh_ipa.split(" ")[0]

            output_datum["syllables_zh_ipa"] = syllables_zh_ipa.split(" ")
            output_datum["onset_zh_ipa"] = onset_zh_ipa
        except:
            failed_words_json["words"][word_en] = f"invalid_syllable: {translation}"
            continue

    # mandarin tones
    onset_tone_num = output_datum["onset_tone_num"]
    if not onset_tone_num:
        onset_tone_num = 1

        onset_tone = hanzi.to_zhuyin(translation).split(" ")[0][-1]
        if onset_tone == "ˊ":
            onset_tone_num = 2
        elif onset_tone == "ˇ":
            onset_tone_num = 3
        elif onset_tone == "ˋ":
            onset_tone_num = 4
        elif onset_tone == "˙":
            onset_tone_num = 5

        output_datum["onset_tone_num"] = onset_tone_num

    output_data_json["words"][word_en] = output_datum

