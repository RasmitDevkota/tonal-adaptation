import atexit
import json
import translators as ts
from googletrans import Translator

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
    with open("./data/translations.json", "w+") as translations_json_file:
        json.dump(translations_json, translations_json_file, ensure_ascii=False)

atexit.register(save_progress)

# translate words
for word_en in words_en:
    print(word_en)

    word_json = {}
    if word_en in words_json:
        word_json = words_json[word_en]
    else:
        word_json = {
            "translations" : {

            }
        }

    if "googletrans" not in word_json["translations"]:
        translation_googletrans = googletrans.translate(f"My name is {word_en}", src="en", dest="zh-CN")
        word_json["translations"]["googletrans"] = translation_googletrans.text.replace("我叫", "").replace("我的名字是", "").replace("我的名字叫", "")

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

    words_json[word_en] = word_json

