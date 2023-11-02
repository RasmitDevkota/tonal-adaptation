import math
import ipasymbols

vowels = ipasymbols.phonlist(query={'type': 'vowel'})

def vowel_qualities(onset):
    onset_vowels = ""

    for letter in list(onset):
        if letter in vowels:
            onset_vowels += letter

    vowels_count = len(onset_vowels)

    vowel = onset_vowels[0]
    onset_length = "Y" in onset
    vowel_props = ipasymbols.props(vowel, ["height", "backness"])
    height_binaries = [1 if vowel_props["height"] == level else 0 for level in ["close", "near-close", "close-mid", "mid", "open-mid", "near-open", "open"]]
    backness_binaries = [1 if vowel_props["backness"] == level else 0 for level in ["front", "central", "back"]]

    return [vowels_count, onset_length] + height_binaries + backness_binaries

def map_tone(tone):
    return f"Tone {tone}"
    # if tone == 1:
    #     return "Tone 1/3"
    # elif tone == 2:
    #     return "Tone 2/4"
    # elif tone == 3:
    #     return "Tone 1/3"
    # elif tone == 4:
    #     return "Tone 2/4"
    # else:
    #     return "Tone 0"

backness_weights = [
    3,
    2,
    1
]

def map_vowels(onset):
    backness_avg = 0
    height_avg = 0
    vowel_count = 0

    for letter in list(onset):
        if letter in vowels:
            props = ipasymbols.props(letter, ["height", "backness"])

            height = [
                "close", # 3
                "near-close", # 2
                "close-mid", # 1
                "mid", # 0
                "open-mid", # -1
                "near-open", # -2
                "open" # -3
            ].index(props["height"])

            height_multiplier = 2 * 1 - (height / 6)

            match props["backness"]:
                case "front": backness = backness_weights[0] * height_multiplier
                case "central": backness = backness_weights[1] * height_multiplier
                case "back": backness = backness_weights[2] * height_multiplier

            height = height

            vowel_count += 1

            backness_avg = backness_avg + backness
            height_avg = height_avg + height

    if vowel_count > 0:
        backness_avg = backness_avg / vowel_count
        height_avg = height_avg / vowel_count
        return [backness_avg, height_avg]
    else:
        return [0,0]

stress_nonlinearizations = {
    "recip": lambda stress, average_stress : average_stress/stress if stress > 0 else 0,
    "exp": lambda stress, average_stress : 2^(average_stress/stress) if stress > 0 else 0,
    "log": lambda stress, average_stress : 2^(average_stress/stress) if stress > 0 else 0
}

def nonlinearize_stresses(stresses, method):
    average_stress = sum(stresses)/len(stresses)
    return [stress_nonlinearizations[method](stress, average_stress) for stress in stresses]

tone_mappings = {
    1: [0,0,1],
    2: [1,0,0],
    3: [1,math.sqrt(0.5),0],
    4: [1,math.sqrt(0.5),0.5]
}
