import ipasymbols

vowels = ipasymbols.phonlist(query={'type': 'vowel'})

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

    backness_avg = backness_avg / vowel_count
    height_avg = height_avg / vowel_count

    return [backness_avg, height_avg]

stress_nonlinearizations = {
    "recip": lambda stress, average_stress : average_stress/stress if stress > 0 else 0,
    "exp": lambda stress, average_stress : 2^(average_stress/stress) if stress > 0 else 0,
    "log": lambda stress, average_stress : 2^(average_stress/stress) if stress > 0 else 0
}

def nonlinearize_stresses(stresses, method):
    average_stress = sum(stresses)/len(stresses)
    return [stress_nonlinearizations[method](stress, average_stress) for stress in stresses]
