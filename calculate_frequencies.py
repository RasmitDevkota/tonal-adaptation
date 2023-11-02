import json
import atexit
import ipasymbols
from copy import deepcopy
import matplotlib.pyplot as plt

vowels = ipasymbols.phonlist(query={'type': 'vowel'})
diphthongs = ipasymbols.phonlist(query={'type': 'diphthong'})
initials = vowels + diphthongs
# onsets_freq_data   = {'oʊ': 10, 'e': 55, 'ɑ': 26, 'ə': 26, 'eɪ': 16, 'ɪ': 15, 'æ': 45, 'i': 9, 'ɜr': 11, 'aɪ': 12, 'æn': 18, 'ɔ': 5, 'eɪn': 2, 'æk': 3, 'ɑr': 9, 'æʃ': 1, 'eɪs': 1, 'el': 6, 'ɪz': 1, 'ɑk': 1, 'ɑn': 1, 'ɔl': 5, 'ed': 3, 'iv': 1, 'ɑrz': 1, 'æl': 7, 'æm': 1, 'ɑl': 2, 'ɔr': 2, 'en': 2, 'əl': 1, 'eɪmz': 1, 'ju': 2, 'ɪn': 2, 'ɑrm': 1, 'ɜrl': 1, 'ɪl': 1, 'ez': 2, 'aɪvz': 1, 'ɑg': 1, 'ɑs': 1, 'ɔz': 2, 'ɪr': 1, 'oʊl': 2, 'aɪk': 1, 'ɪg': 1, 'ɑt': 1, 'ʌl': 1}
# onsets_freq_data = {'oʊ': 10, 'e': 55, 'ɑ': 26, 'ə': 26, 'eɪ': 17, 'ɪ': 15, 'æ': 45, 'i': 9, 'ɜr': 11, 'aɪ': 12, 'æn': 18, 'ɔ': 5, 'eɪn': 2, 'æk': 3, 'ɑr': 9, 'æʃ': 1, 'eɪs': 1, 'el': 6, 'ɪz': 1, 'ɑk': 1, 'ɑn': 1, 'ɔl': 5, 'ed': 3, 'iv': 1, 'ɑrz': 1, 'æm': 2, 'æl': 7, 'ɑl': 2, 'ɔr': 2, 'en': 2, 'əl': 1, 'eɪmz': 1, 'ju': 2, 'ɪn': 2, 'ɑrm': 1, 'ɜrl': 1, 'ɪl': 1, 'ez': 2, 'aɪvz': 1, 'ɑg': 1, 'ɑs': 1, 'ɔz': 2, 'ɪr': 1, 'oʊl': 2, 'aɪk': 1, 'ɪg': 1, 'ɑt': 1, 'ʌl': 1}
# onsets_freq_data = {'oʊ': 11, 'e': 57, 'ɑ': 27, 'ə': 26, 'eɪ': 18, 'ɪ': 15, 'æ': 45, 'i': 9, 'ɜr': 11, 'aɪ': 12, 'æn': 18, 'ɔ': 5, 'eɪn': 2, 'æk': 3, 'ɑr': 9, 'æʃ': 1, 'eɪs': 1, 'em': 1, 'el': 7, 'ɪz': 1, 'ɑk': 2, 'ɑn': 1, 'ɔl': 5, 'ed': 3, 'iv': 1, 'ɑrz': 1, 'æm': 2, 'æl': 7, 'ɪn': 3, 'ɑl': 2, 'ɔr': 2, 'en': 2, 'əl': 1, 'eɪmz': 1, 'ju': 2, 'ɑrm': 1, 'ɜrl': 1, 'ɪl': 1, 'ez': 2, 'aɪvz': 1, 'ɑg': 1, 'ɑs': 1, 'ɔz': 2, 'ɪr': 1, 'oʊl': 2, 'aɪk': 1, 'ɪg': 1, 'ɑt': 1, 'ʌl': 1}
# onsets_freq_data = {'oʊ': 11, 'e': 54, 'ɑ': 26, 'ə': 26, 'eɪ': 18, 'ɪ': 14, 'æ': 43, 'i': 9, 'ɜr': 10, 'aɪ': 12, 'æn': 17, 'ɔ': 5, 'eɪn': 2, 'æk': 3, 'ɑr': 9, 'æʃ': 1, 'eɪs': 1, 'em': 1, 'el': 7, 'ɪz': 1, 'ɑk': 2, 'ɑn': 1, 'ɔl': 5, 'ed': 3, 'iv': 1, 'ɑrz': 1, 'æm': 2, 'æl': 6, 'ɪn': 3, 'ɑl': 2, 'ɔr': 2, 'en': 2, 'əl': 1, 'eɪmz': 1, 'ju': 2, 'ɑrm': 1, 'ɜrl': 1, 'ɪl': 1, 'ez': 2, 'aɪvz': 1, 'ɑg': 1, 'ɑs': 1, 'ɔz': 2, 'ɪr': 1, 'oʊl': 1, 'aɪk': 1, 'ɪg': 1, 'ɑt': 1, 'ʌl': 1}
# onsets_freq_data = {'oʊ': 9, 'e': 50, 'ɑ': 29, 'ə': 26, 'eɪ': 18, 'ɪ': 14, 'æ': 41, 'i': 9, 'ɜ': 7, 'aɪ': 12, 'æ': 15, 'ɔ': 5, 'eɪ': 2, 'æ': 3, 'ɑr': 8, 'æ': 1, 'eɪ': 1, 'e': 1, 'e': 7, 'ɪ': 1, 'ɑ': 2, 'ɑ': 1, 'e': 3, 'i': 1, 'ɑ': 1, 'æ': 2, 'æ': 5, 'ɪ': 3, 'ɑ': 2, 'ɔ': 2, 'e': 2, 'ə': 1, 'ju': 1, 'ɔ': 4, 'ɑ': 1, 'ɜ': 1, 'ɪ': 1, 'e': 2, 'aɪ': 1, 'ɑ': 1, 'ɑ': 1, 'ɔ': 2, 'ɪ': 1, 'oʊ': 1, 'aɪ': 1}
# onsets_zh_freq_data = {'奥': 38, '艾': 61, '阿': 75, '以': 7, '伊': 24, '亚': 18, '埃': 43, '欧': 5, '安': 26, '爱': 5, '秋': 1, '天': 1, '雅': 1, '猎': 1, '杜': 1, '夏': 1, '象': 1, '恩': 2, '尤': 2, '珠': 1, '靛': 1, '印': 1, '厄': 2, '乌': 2}

with open("./data/output_data.json", "r") as output_data_file:
    try:
        words = json.load(output_data_file)["words"]
    except Exception as e:
        print(e)

onsets_freq_data = { }
onsets_zh_freq_data = { }

for word_en, word_data in words.items():
    onset = word_data["onset_en_ipa"]
    onsets_freq_data[onset] = onsets_freq_data[onset] + 1 if onset in onsets_freq_data else 1

    onset_zh = word_data["word_zh"][0]
    onsets_zh_freq_data[onset_zh] = onsets_zh_freq_data[onset_zh] + 1 if onset_zh in onsets_zh_freq_data else 1

onsets = list(set(onsets_freq_data.keys()))
onset_en_ipa_list = list(onsets_freq_data.keys())

frequency_data_json = {
    "onset_tone_num": {
        "1": { },
        "2": { },
        "3": { },
        "4": { }
    },
    "onset_en_ipa": { },
    "onset_zh": { },
    "onset_en_ipa-onset_zh": { }
}

cond_probs = {}

def save_progress():
    with open("./data/frequency_data.json", "w+") as frequency_data_json_file:
        json.dump(frequency_data_json, frequency_data_json_file, ensure_ascii=False)

atexit.register(save_progress)

def get_data():
    for _, word_data in words.items():
        onset_en_ipa = word_data["onset_en_ipa"]

        frequency_data_json["onset_tone_num"][str(word_data["onset_tone_num"])][onset_en_ipa] = \
            frequency_data_json["onset_tone_num"][str(word_data["onset_tone_num"])].get(onset_en_ipa, 0) \
                + 1

        if onset_en_ipa in frequency_data_json["onset_en_ipa"]:
            frequency_data_json["onset_en_ipa"][onset_en_ipa][word_data["onset_tone_num"]] = \
                frequency_data_json["onset_en_ipa"][onset_en_ipa].get(word_data["onset_tone_num"], 0) \
                    + 1
        else:
            frequency_data_json["onset_en_ipa"][onset_en_ipa] = {
                word_data['onset_tone_num']: 1
            }

        onset_zh = word_data["word_zh"][0]

        if onset_zh in frequency_data_json["onset_zh"]:
            frequency_data_json["onset_zh"][onset_zh][word_data["onset_en_ipa"]] = \
                frequency_data_json["onset_zh"][onset_zh].get(word_data["onset_en_ipa"], 0) \
                    + 1
        else:
            frequency_data_json["onset_zh"][onset_zh] = {
                word_data['onset_en_ipa']: 1
            }

        if onset_en_ipa in frequency_data_json["onset_en_ipa-onset_zh"]:
            frequency_data_json["onset_en_ipa-onset_zh"][onset_en_ipa][onset_zh] = \
                frequency_data_json["onset_en_ipa-onset_zh"][onset_en_ipa].get(onset_zh, 0) \
                    + 1
        else:
            frequency_data_json["onset_en_ipa-onset_zh"][onset_en_ipa] = {
                onset_zh: 1
            }

    # for onset_en_ipa in frequency_data_json["onset_en_ipa"]:
    #     tones = list(frequency_data_json["onset_en_ipa"][onset_en_ipa].keys())
    #     occurrences = list(frequency_data_json["onset_en_ipa"][onset_en_ipa].values())

    #     if sum(occurrences) < 4:
    #         for t in range(len(tones)):
    #             tone = str(tones[t])
    #             frequency_data_json["onset_tone_num"][tone] = frequency_data_json["onset_tone_num"][tone] - frequency_data_json["onset_en_ipa"][onset_en_ipa][tone]

    #         del frequency_data_json["onset_en_ipa"][onset_en_ipa]

    with open("./data/frequency_data.json", "w+") as frequency_data_json_file:
        json.dump(frequency_data_json, frequency_data_json_file, ensure_ascii=False)

    cond_probs = deepcopy(frequency_data_json)

    for tone in ['1','2','3','4']:
        tone_count = sum(frequency_data_json["onset_tone_num"][tone].values())
        for onset in frequency_data_json["onset_tone_num"][tone]:
            cond_probs["onset_tone_num"][tone][onset] = frequency_data_json["onset_tone_num"][tone][onset]/tone_count

    for onset in frequency_data_json["onset_en_ipa"].keys():
        # onset_count = len(frequency_data_json["onset_en_ipa"][onset].keys())
        onset_count = onsets_freq_data[onset]
        for tone in cond_probs["onset_en_ipa"][onset]:
            cond_probs["onset_en_ipa"][onset][tone] = frequency_data_json["onset_en_ipa"][onset][tone]/onset_count

    for onset_zh in frequency_data_json["onset_zh"].keys():
        onset_zh_count = onsets_zh_freq_data[onset_zh]
        for onset_en_ipa in cond_probs["onset_zh"][onset_zh]:
            cond_probs["onset_zh"][onset_zh][onset_en_ipa] = frequency_data_json["onset_zh"][onset_zh][onset_en_ipa]/onset_zh_count

    for onset_en_ipa in frequency_data_json["onset_en_ipa-onset_zh"].keys():
        onset_en_ipa_count = sum(list(frequency_data_json["onset_en_ipa-onset_zh"][onset_en_ipa].values()))
        for onset_zh in cond_probs["onset_en_ipa-onset_zh"][onset_en_ipa]:
            cond_probs["onset_en_ipa-onset_zh"][onset_en_ipa][onset_zh] = frequency_data_json["onset_en_ipa-onset_zh"][onset_en_ipa][onset_zh]/onset_en_ipa_count

    with open("./data/cond_probs_data.json", "w+") as cond_probs_data_json_file:
        json.dump(cond_probs, cond_probs_data_json_file, ensure_ascii=False)

    return [frequency_data_json, cond_probs]

# get_data()

# @TODO - For every word with tones 2 or 3, find the conditional probability:
# P(Tone 2 or Tone 3 | Feature) - Look for probabilities > 0.95

# tone_count_1 = 0
# initial_stresses = 0

# tone_count_2 = 0
# tone_count_3 = 0
# stresses_2 = 0
# stresses_not_2 = 0
# stresses_3 = 0
# stresses_not_3 = 0

# tone_count_4 = 0

# for _, word_data in words.items():
    # if word_data["onset_tone_num"] == 2:
    #     tone_count_2 += 1

    #     if len(word_data["stresses_en"]) == 2:# and word_data["stresses_en"][0] == 1:
    #         stresses_2 += 1
    # elif word_data["onset_tone_num"] == 3:
    #     tone_count_3 += 1

    #     if len(word_data["stresses_en"]) == 3:# and word_data["stresses_en"][0] == 1:
    #         stresses_3 += 1
    # else:

    #     if len(word_data["stresses_en"]) == 2:# and word_data["stresses_en"][0] == 1:
    #         stresses_not_2 += 1
    #         stresses_not_3 += 1

    # if word_data["stresses_en"][0] == 1:
    #     initial_stresses += 1
    #     if word_data["onset_tone_num"] == 1:
    #         tone_count_1 += 1
    #     elif word_data["onset_tone_num"] == 2:
    #         tone_count_2 += 1
    #     elif word_data["onset_tone_num"] == 3:
    #         tone_count_3 += 1
    #     elif word_data["onset_tone_num"] == 4:
    #         tone_count_4 += 1

# print(tone_count_1, tone_count_2, tone_count_3, tone_count_4)
# print(f"{tone_count_1}/{initial_stresses}")
# print(f"{stresses_2}/{tone_count_2} (but {stresses_not_2})")
# print(f"{stresses_3}/{tone_count_3} (but {stresses_not_3})")

# for o in range(len(onsets)):
#     fig, ax = plt.subplots()
#     plt.xlabel("Tones", fontweight ='bold', fontsize = 14)
#     plt.xticks(np.arange(4))
#     plt.ylabel(onsets[o], fontweight ='bold', fontsize = 14)

#     plt.bar(np.arange(4), ipa_tone_freq_data[o], label = onsets[o])
#     plt.savefig(f"./visuals/ipa_tone_freq_data/P({onsets[o]}|T).png")
#     plt.close()