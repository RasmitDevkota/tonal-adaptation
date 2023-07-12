import re
import unicodedata
import pronouncing
from dragonmapper import hanzi
from arpa2ipa import arpa_to_ipa
from googletrans import Translator
from syllabifier import syllabifyARPA

translator = Translator()

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

stress_nonlinearizations = {
    "recip": lambda stress, average_stress : average_stress/stress if stress > 0 else 0,
    "exp": lambda stress, average_stress : 2^(average_stress/stress) if stress > 0 else 0,
    "log": lambda stress, average_stress : 2^(average_stress/stress) if stress > 0 else 0
}

def nonlinearize(stresses, method):
    average_stress = sum(stresses)/len(stresses)
    return [stress_nonlinearizations[method](stress, average_stress) for stress in stresses]

corpus_file = open("./corpus_sample.csv", "r+")
failed_words_file = open("./failed_corpus.csv", "a+")

# data file format:
data_file = open("./data.csv", "a+")

words_en = [line.strip("\n\r") for line in corpus_file.readlines()] # words in english

data = [] # english onset (vowel)-mandarin tone pairs

# batch translate
# translations = translator.translate(words_en, src="en", dest="zh-CN")

# loop translate
for word_en in words_en:
    # translation
    ## @TODO - confirm translations using other sources/methods, consider discarding inconsistencies
    translation = translator.translate(word_en, src="en", dest="zh-CN")

    # english arpa
    word_en_arpa = pronouncing.phones_for_word(translation.origin)

    if len(word_en_arpa) == 0:
        print(f"Failed word - {word_en} (phones_for_word)")
        failed_words_file.write(f"{word_en} (phones_for_word)\n")
        continue

    if len(word_en_arpa) > 1 and (word_en_arpa[0].split(" ")[0] != word_en_arpa[1].split(" ")[0]):
        print(f"Potentially-failed word: {word_en} with arpa {word_en_arpa} contains onset variation, defaulting to first")
        failed_words_file.write(f"{word_en} (phones_for_word onset variation)\n")

    # english syllabification
    syllables_en_arpa = ""
    try:
        syllables_en_arpa = syllabifyARPA(word_en_arpa[0])
    except Exception as e:
        print(f"Failed word - {word_en} (syllabifyARPA)")
        failed_words_file.write(f"{word_en} (syllabifyARPA)\n")
        continue

    syllables_en_ipa = " ".join(arpa_to_ipa(syllable).replace(" ", "") for syllable in syllables_en_arpa)
    onset_en_ipa = arpa_to_ipa(syllables_en_arpa[0]).replace(" ", "")

    # english stress
    stresses_en = [phone[-1] for phone in word_en_arpa[0] if phone[-1] in "0123456789"]

    if len(syllables_en_arpa) != len(stresses_en):
        print(f"Failed word - {word_en} (stresses_en)")
        failed_words_file.write(f"{word_en} (stresses_en)\n")
        continue

    # mandarin pinyin
    pinyin_non_unicode = hanzi.to_pinyin(" ".join(list(translation.text)))
    pinyin_unicode = unicodedata.normalize('NFD', pinyin_non_unicode).translate(table)
    word_zh_pinyin = pinyin_unicode.split(" ")
    onset_zh_pinyin = word_zh_pinyin[0]

    # mandarin ipa
    syllables_zh_ipa = hanzi.to_ipa(" ".join(list(translation.text)))
    onset_zh_ipa = syllables_zh_ipa.split(" ")[0]

    # mandarin tones
    onset_tone_num = 1

    onset_tone = hanzi.to_zhuyin(translation.text).split(" ")[0][-1]
    if onset_tone == "ˊ":
        onset_tone_num = 2
    elif onset_tone == "ˇ":
        onset_tone_num = 3
    elif onset_tone == "ˋ":
        onset_tone_num = 4
    elif onset_tone == "˙":
        onset_tone_num = 5

    # variables
    datum = [
        word_en,
        translation.text,
        word_en_arpa[0], # can be reproduced easily with datum[3]
        ";".join(syllables_en_arpa), # can be reproduced easily with datum[2]
        syllables_en_ipa, # can be reproduced easily with datum[2] and datum[3]
        onset_en_ipa, # can be reproduced easily with datum[2] and datum[3] and datum[4]
        "".join(stresses_en),
        pinyin_non_unicode,
        ";".join(word_zh_pinyin),
        onset_zh_pinyin,
        syllables_zh_ipa,
        onset_zh_pinyin,
        str(onset_tone_num)
    ]

    print(datum)
    continue

    data_file.write(",".join(datum) + "\n")

corpus_file.close()
failed_words_file.close()
data_file.close()
