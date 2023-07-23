import json
import ipasymbols
from copy import deepcopy
import matplotlib.pyplot as plt

vowels = ipasymbols.phonlist(query={'type': 'vowel'})
diphthongs = ipasymbols.phonlist(query={'type': 'diphthong'})
initials = vowels + diphthongs

# onsets_freq_data = {'oʊ': 9, 'e': 50, 'ɑ': 29, 'ə': 26, 'eɪ': 18, 'ɪ': 14, 'æ': 41, 'i': 9, 'ɜr': 7, 'aɪ': 12, 'æn': 15, 'ɔ': 5, 'eɪn': 2, 'æk': 3, 'ɑr': 8, 'æʃ': 1, 'eɪs': 1, 'em': 1, 'el': 7, 'ɪz': 1, 'ɑk': 2, 'ɑn': 1, 'ed': 3, 'iv': 1, 'ɑrz': 1, 'æm': 2, 'æl': 5, 'ɪn': 3, 'ɑl': 2, 'ɔr': 2, 'en': 2, 'əl': 1, 'ju': 1, 'ɔl': 4, 'ɑrm': 1, 'ɜrl': 1, 'ɪl': 1, 'ez': 2, 'aɪvz': 1, 'ɑg': 1, 'ɑs': 1, 'ɔz': 2, 'ɪr': 1, 'oʊl': 1, 'aɪk': 1}
onsets_freq_data = {'oʊ': 9, 'e': 50, 'ɑ': 29, 'ə': 26, 'eɪ': 18, 'ɪ': 14, 'æ': 41, 'i': 9, 'ɜ': 7, 'aɪ': 12, 'æ': 15, 'ɔ': 5, 'eɪ': 2, 'æ': 3, 'ɑr': 8, 'æ': 1, 'eɪ': 1, 'e': 1, 'e': 7, 'ɪ': 1, 'ɑ': 2, 'ɑ': 1, 'e': 3, 'i': 1, 'ɑ': 1, 'æ': 2, 'æ': 5, 'ɪ': 3, 'ɑ': 2, 'ɔ': 2, 'e': 2, 'ə': 1, 'ju': 1, 'ɔ': 4, 'ɑ': 1, 'ɜ': 1, 'ɪ': 1, 'e': 2, 'aɪ': 1, 'ɑ': 1, 'ɑ': 1, 'ɔ': 2, 'ɪ': 1, 'oʊ': 1, 'aɪ': 1}
onsets = list(set(onsets_freq_data.keys()))

with open("./data/output_data.json", "r") as output_data_file:
    try:
        words = json.load(output_data_file)["words"]
    except Exception as e:
        print(e)

frequencies = {
    "onset_tone_num": {
        "1": { },
        "2": { },
        "3": { },
        "4": { }
    },
    "onset_en_ipa": {
        "a": {

        }
    }
}

def get_data():
    for _, word_data in words.items():
        frequencies["onset_tone_num"][str(word_data["onset_tone_num"])][word_data["onset_en_ipa"]] = \
            frequencies["onset_tone_num"][str(word_data["onset_tone_num"])].get(word_data["onset_en_ipa"], 0) \
                + 1

        if word_data["onset_en_ipa"] in frequencies["onset_en_ipa"]:
            frequencies["onset_en_ipa"][word_data["onset_en_ipa"]][word_data["onset_tone_num"]] = \
                frequencies["onset_en_ipa"][word_data["onset_en_ipa"]].get(word_data["onset_tone_num"], 0) \
                    + 1
        else:
            frequencies["onset_en_ipa"][word_data["onset_en_ipa"]] = {
                f"{word_data['onset_tone_num']}": 1
            }

    cond_probs = deepcopy(frequencies)

    for tone in ['1','2','3','4']:
        tone_count = len(frequencies["onset_tone_num"][tone].keys())
        for onset in frequencies["onset_tone_num"][tone]:
            cond_probs["onset_tone_num"][tone][onset] = frequencies["onset_tone_num"][tone][onset]/tone_count

    for onset in frequencies["onset_en_ipa"].keys():

        onset_count = len(frequencies["onset_en_ipa"][onset].keys())
        for tone in cond_probs["onset_en_ipa"][onset]:
            cond_probs["onset_en_ipa"][onset][tone] = frequencies["onset_en_ipa"][onset][tone]/onset_count

    return [frequencies, cond_probs]

# for o in range(len(onsets)):
#     fig, ax = plt.subplots()
#     plt.xlabel("Tones", fontweight ='bold', fontsize = 14)
#     plt.xticks(np.arange(4))
#     plt.ylabel(onsets[o], fontweight ='bold', fontsize = 14)

#     plt.bar(np.arange(4), ipa_tone_freq_data[o], label = onsets[o])
#     plt.savefig(f"./visuals/ipa_tone_freq_data/P({onsets[o]}|T).png")
#     plt.close()
