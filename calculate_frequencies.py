import json
import atexit
import ipasymbols
from copy import deepcopy
import matplotlib.pyplot as plt

vowels = ipasymbols.phonlist(query={'type': 'vowel'})
diphthongs = ipasymbols.phonlist(query={'type': 'diphthong'})
initials = vowels + diphthongs

onsets_freq_data = {'oʊ': 11, 'e': 53, 'ɑ': 26, 'ə': 26, 'eɪ': 18, 'ɪ': 14, 'æ': 42, 'i': 9, 'ɜr': 9, 'aɪ': 12, 'æn': 16, 'ɔ': 5, 'eɪn': 2, 'æk': 3, 'ɑr': 8, 'æʃ': 1, 'eɪs': 1, 'em': 1, 'el': 7, 'ɪz': 1, 'ɑk': 2, 'ɑn': 1, 'ɔl': 5, 'ed': 3, 'iv': 1, 'ɑrz': 1, 'æm': 2, 'æl': 5, 'ɪn': 3, 'ɑl': 2, 'ɔr': 2, 'en': 2, 'əl': 1, 'eɪmz': 1, 'ju': 1, 'ɑrm': 1, 'ɜrl': 1, 'ɪl': 1, 'ez': 2, 'aɪvz': 1, 'ɑg': 1, 'ɑs': 1, 'ɔz': 2, 'ɪr': 1, 'oʊl': 1, 'aɪk': 1}
# onsets_freq_data = {'oʊ': 9, 'e': 50, 'ɑ': 29, 'ə': 26, 'eɪ': 18, 'ɪ': 14, 'æ': 41, 'i': 9, 'ɜ': 7, 'aɪ': 12, 'æ': 15, 'ɔ': 5, 'eɪ': 2, 'æ': 3, 'ɑr': 8, 'æ': 1, 'eɪ': 1, 'e': 1, 'e': 7, 'ɪ': 1, 'ɑ': 2, 'ɑ': 1, 'e': 3, 'i': 1, 'ɑ': 1, 'æ': 2, 'æ': 5, 'ɪ': 3, 'ɑ': 2, 'ɔ': 2, 'e': 2, 'ə': 1, 'ju': 1, 'ɔ': 4, 'ɑ': 1, 'ɜ': 1, 'ɪ': 1, 'e': 2, 'aɪ': 1, 'ɑ': 1, 'ɑ': 1, 'ɔ': 2, 'ɪ': 1, 'oʊ': 1, 'aɪ': 1}
onsets = list(set(onsets_freq_data.keys()))

with open("./data/output_data.json", "r") as output_data_file:
    try:
        words = json.load(output_data_file)["words"]
    except Exception as e:
        print(e)

frequency_data_json = {
    "onset_tone_num": {
        "1": { },
        "2": { },
        "3": { },
        "4": { }
    },
    "onset_en_ipa": { }
}

cond_probs = {}

def save_progress():
    with open("./data/frequency_data.json", "w+") as frequency_data_json_file:
        json.dump(frequency_data_json, frequency_data_json_file, ensure_ascii=False)

def get_data():
    for _, word_data in words.items():
        frequency_data_json["onset_tone_num"][str(word_data["onset_tone_num"])][word_data["onset_en_ipa"]] = \
            frequency_data_json["onset_tone_num"][str(word_data["onset_tone_num"])].get(word_data["onset_en_ipa"], 0) \
                + 1

        if word_data["onset_en_ipa"] in frequency_data_json["onset_en_ipa"]:
            frequency_data_json["onset_en_ipa"][word_data["onset_en_ipa"]][word_data["onset_tone_num"]] = \
                frequency_data_json["onset_en_ipa"][word_data["onset_en_ipa"]].get(word_data["onset_tone_num"], 0) \
                    + 1
        else:
            frequency_data_json["onset_en_ipa"][word_data["onset_en_ipa"]] = {
                word_data['onset_tone_num']: 1
            }

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

    with open("./data/cond_probs_data.json", "w+") as cond_probs_data_json_file:
        json.dump(cond_probs, cond_probs_data_json_file, ensure_ascii=False)

    return [frequency_data_json, cond_probs]

get_data()

# @TODO - For every word with tones 2 or 3, find the conditional probability:
# P(Tone 2 or Tone 3 | Feature) - Look for probabilities > 0.95

tone_count_2 = 0
tone_count_3 = 0
stresses_2 = 0
stresses_not_2 = 0
stresses_3 = 0
stresses_not_3 = 0
for _, word_data in words.items():
    if word_data["onset_tone_num"] == 2:
        tone_count_2 += 1

        if len(word_data["stresses_en"]) == 2:# and word_data["stresses_en"][0] == 1:
            stresses_2 += 1
    elif word_data["onset_tone_num"] == 3:
        tone_count_3 += 1

        if len(word_data["stresses_en"]) == 3:# and word_data["stresses_en"][0] == 1:
            stresses_3 += 1
    else:
        if len(word_data["stresses_en"]) == 2:# and word_data["stresses_en"][0] == 1:
            stresses_not_2 += 1
            stresses_not_3 += 1

print(f"{stresses_2}/{tone_count_2} (but {stresses_not_2})")
print(f"{stresses_3}/{tone_count_3} (but {stresses_not_3})")


# for o in range(len(onsets)):
#     fig, ax = plt.subplots()
#     plt.xlabel("Tones", fontweight ='bold', fontsize = 14)
#     plt.xticks(np.arange(4))
#     plt.ylabel(onsets[o], fontweight ='bold', fontsize = 14)

#     plt.bar(np.arange(4), ipa_tone_freq_data[o], label = onsets[o])
#     plt.savefig(f"./visuals/ipa_tone_freq_data/P({onsets[o]}|T).png")
#     plt.close()