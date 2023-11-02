import numpy as np
import pandas as pd
from dragonmapper import hanzi
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report, matthews_corrcoef

def print_metrics(X_test, y_test, y_pred, X_labels, y_labels, clf=None, clf_list=None, print_probas=False, print_sandhi_effects=False):
    y_comparisons = list(zip(X_test, y_test, y_pred))

    y_counts = { }
    for y_label in y_labels:
        y_counts[y_label] = 0

    y_corrects = { }
    for y_label in y_labels:
        y_corrects[y_label] = 0

    if print_probas:
        tone_2_probas = []
        tone_3_probas = []

    if clf:
        decision_paths = clf.decision_path(X_test)
        leaves = clf.apply(X_test)
    elif clf_list:
        for c in range(len(clf_list)):
            clf_item = clf_list[c]

            print(f"DecisionTreeClassifier #{c}:")
            decision_paths = clf_item.decision_path(X_test)
            leaves = clf_item.apply(X_test)

    for y in range(len(y_comparisons)):
        y_comparison = y_comparisons[y]

        if print_sandhi_effects:
            pinyin_with_sandhi = hanzi.to_pinyin(y_comparison).lower()
            pinyin_without_sandhi = ''.join(hanzi.to_pinyin(syllable_zh) for syllable_zh in y_comparison).lower()
            if pinyin_with_sandhi != pinyin_without_sandhi:
                print(f"{y_comparison}: {pinyin_with_sandhi} w/ sandhi, {pinyin_without_sandhi} w/o sandhi gives: {y_comparison[1]} vs. {y_comparison[2]}")

        tone = str(y_comparison[1])
        y_counts[tone] = y_counts[tone] + 1

        if clf and print_probas:
            proba = clf.predict_proba([y_comparison[0]])[0]
            tone_2_probas.append(proba[1])
            tone_3_probas.append(proba[2])

        # print(y_comparison)
        if y_comparison[1] == y_comparison[2]:
            y_corrects[tone] = y_corrects[tone] + 1
        else:
            if clf:
                print(y_comparison)
                if "2" in y_comparison[1] or "3" in y_comparison[1]:
                    print(f"{leaves[y]} incorrectly predicted tone {tone} (guessed tone {y_comparison[2]} w/ decision path {decision_paths.indices[decision_paths.indptr[y]:decision_paths.indptr[y+1]]})")

    if print_probas:
        tone_2_probas = pd.Series(tone_2_probas)
        tone_3_probas = pd.Series(tone_3_probas)
        sig_tests_2 = pd.Series([(point - tone_2_probas.mean())/tone_2_probas.std() for point in tone_2_probas])
        sig_tests_3 = pd.Series([(point - tone_3_probas.mean())/tone_3_probas.std() for point in tone_3_probas])

        ts = 0
        for test_stat_2, test_stat_3 in zip(sig_tests_2, sig_tests_3):
            if test_stat_2 >= 3 or test_stat_2 <= -3:
                print(f"test_stat_2 ({test_stat_2}) significant for ({y_comparisons[ts]})")

            if test_stat_3 >= 3 or test_stat_3 <= -3:
                print(f"test_stat_3 ({test_stat_3}) significant for ({y_comparisons[ts]})")

            ts += 1

    print(y_counts, y_corrects)

    for y_label, count in y_counts.items():
        if count != 0:
            print(f"{y_label} accuracy: {y_corrects[y_label]}/{y_counts[y_label]} ({y_corrects[y_label]/y_counts[y_label] * 100}%)")

    print(confusion_matrix(y_test, y_pred))

    print(matthews_corrcoef(y_test, y_pred))

    if clf:
        print("\n".join([f"Feature {feature_pair[0]} w/ importance {feature_pair[1]}" for feature_pair in list(zip(X_labels, clf.feature_importances_))]))
    elif clf_list:
        total = [0] * len(clf_list[0].feature_importances_)

        for c in range(len(clf_list)):
            clf_item = clf_list[c]
            total = [total[i] + clf_item.feature_importances_[i] for i in range(len(total))]

            print(f"DecisionTreeClassifier #{c}:")
            for feature_pair in list(zip(X_labels, clf_item.feature_importances_)):
                if feature_pair[1] > 0:
                    print(f"Feature {feature_pair[0]} w/ importance {feature_pair[1]}")

        print(total)

    print(classification_report(y_test, y_pred))
