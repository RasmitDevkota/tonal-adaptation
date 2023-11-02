import atexit
import threading
import json
import translators as ts
from googletrans import Translator

lock = threading.Lock()

googletrans = Translator()

translators_pool = [
    'alibaba', 'apertium', 'argos', 'baidu', 'bing', 'caiyun', 'cloudYi',
    'deepl', 'elia', 'google', 'iciba', 'iflytek', 'iflyrec', 'itranslate',
    'judic', 'languageWire', 'lingvanex', 'niutrans', 'mglip', 'mirai',
    'modernMt', 'myMemory', 'papago', 'qqFanyi', 'qqTranSmart', 'reverso',
    'sogou', 'sysTran', 'tilde', 'translateCom', 'translateMe', 'utibet',
    'volcEngine', 'yandex', 'yeekit', 'youdao'
]

translators_selected = [
    "google", "bing",
    "alibaba", "baidu", "caiyun", "iciba", "qqFanyi", "sogou",
    "papago",
    # desired but not working: "sysTran", "baidu", "cloudYi", "niutrans", "youdao", "mirai", "yandex"
    # may be failing on certain words? retry with try/except
]

with open("./data/corpus.csv", "r+") as corpus_file:
    words_en = [line.strip("\n\r") for line in corpus_file.readlines()]

with open("./data/translations.json", "r") as translations_json_file:
    translations_raw = translations_json_file.read()

    if len(translations_raw) == 0:
        translations_json = {
            "words" : {

            }
        }
    else:
        translations_json = json.loads(translations_raw)

    words_json = translations_json["words"]

def save_progress():
    print("Saving progress...")

    with open("./data/translations.json", "w+") as translations_json_file:
        json.dump(translations_json, translations_json_file, ensure_ascii=False)

    print("Saved progress!")

atexit.register(save_progress)

# translate words
def translate(words_en_subset):
    print(f"Thread {threading.current_thread().name} beginning translating")

    for word_en in words_en_subset:
        need_to_save = False

        print(word_en)

        word_json = {}
        if word_en in words_json:
            with lock:
                word_json = words_json[word_en]
        else:
            word_json = {
                "translations" : {

                }
            }

        if "googletrans" not in word_json["translations"]:
            translation_googletrans = googletrans.translate(f"My name is {word_en}", src="en", dest="zh-CN")
            word_json["translations"]["googletrans"] = translation_googletrans.text.replace("我叫", "").replace("我的名字是", "").replace("我的名字叫", "")

            need_to_save = True

        for translator in translators_selected:
            if translator not in word_json["translations"]:
                try:
                    translation = ts.translate_text(f"My name is {word_en}", translator=translator, from_language="en", to_language="zh")
                    word_json["translations"][translator] = translation\
                        .strip()\
                        .replace("我叫", "")\
                        .replace("我的名字是", "")\
                        .replace("我的名字叫", "")
                except:
                    word_json["translations"][translator] = "FAILED"

                need_to_save = True

        if need_to_save:
            with lock:
                words_json[word_en] = word_json
                print(f"Thread {threading.current_thread().name} saving progress...")
                save_progress()
                print(f"Thread {threading.current_thread().name} saved progress!")

    with lock:
        print(f"Thread {threading.current_thread().name} finished translating")

def main():
    workload = 100
    word_count = len(words_en)
    threads = []
    for th in range(min(int(word_count/workload), 100)):
        start_idx = th*workload
        stop_index = min((th + 1) * workload, len(words_en))

        threads.append(threading.Thread(target=translate,
                                        args=[words_en[start_idx:stop_index]],
                                        name=f"translator_{th}"))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

main()
