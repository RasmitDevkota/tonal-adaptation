from itertools import permutations

frequencies = [
    183,
    3,
    8,
    103
]
total = sum(frequencies)

probs = [frequency/total for frequency in frequencies]

data = [1] * frequencies[0] \
    + [2] * frequencies[1] \
    + [3] * frequencies[2] \
    + [4] * frequencies[3]

data_permutations = permutations(data)

accuracies = []
for permutation in data_permutations:
    guesses = [1] * frequencies[0] \
            + [2] * frequencies[1] \
            + [3] * frequencies[2] \
            + [4] * frequencies[3]

    corrects = sum(guesses[i] == permutation[i] for i in range(total))

    accuracies.append(corrects/total)

print(max(accuracies), min(accuracies), max(accuracies)/total)

# with open("./data_sources/raw.githubusercontent.com_fivethirtyeight_data_master_most-common-name_surnames.csv", "r") as f:
#     names = [name.title() for name in f.readlines()]
#     print(names)

# with open("./data_sources/raw.githubusercontent.com_fivethirtyeight_data_master_most-common-name_surnames.csv", "w") as f:
#     f.writelines(names)

# import os
# import json

# with open("./data/output_data.json", "r") as output_data_file:
#     output_data_raw = output_data_file.read()
#     output_data_json = json.loads(output_data_raw)

# with open("./data/frequency_data.json", "r") as frequency_data_file:
#     frequency_data_raw = frequency_data_file.read()
#     frequency_data_json = json.loads(frequency_data_raw)

# with open("./data/cond_probs_data.json", "r") as cond_probs_data_file:
#     cond_probs_data_raw = cond_probs_data_file.read()
#     cond_probs_data_json = json.loads(cond_probs_data_raw)

# tone_1 = []
# tone_4 = []

# for word_en, word_data in output_data_json["words"].items():
#     if word_data["onset_tone_num"] == 1:
#         tone_1.append(f"\n    - {word_en}, {word_data['word_zh']}")
#     if word_data["onset_tone_num"] == 4:
#         tone_4.append(f"\n    - {word_en}, {word_data['word_zh']}")

# print("Tone 1:", "".join(tone_1))
# print("Tone 4:", "".join(tone_4))

# t1 = frequency_data_json["onset_tone_num"]["1"]
# for onset in t1:
#     p_t1_given_onset = cond_probs_data_json["onset_en_ipa"][onset]["1"]
#     print(f"Onset {onset} has {round(p_t1_given_onset*100, 2)}% probability of having tone 1")

# t4 = frequency_data_json["onset_tone_num"]["4"]
# for onset in t4:
#     p_t4_given_onset = cond_probs_data_json["onset_en_ipa"][onset]["4"]
#     print(f"Onset {onset} has {round(p_t4_given_onset*100, 2)}% probability of having tone 4")
