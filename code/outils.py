import json
import codecs

中文数字 = "〇一二三四五六七八九十"
中转数 = {}
数转中 = {}

for i in range(11):
    中转数[中文数字[i]] = i
    数转中[i] = 中文数字[i]


def read(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        return lines


def keys(dct):
    """return the keys of a dictionary as a list
    """
    return list(dct.keys())


def load_cn_json(path):
    """load Chinese content from a json file
    """
    with codecs.open(path, "r", encoding="utf-8") as f:
        out = json.load(f)
    return out


def dump_cn_json(path, content):
    """dump Chinese content to a json file
    """
    with codecs.open(path, "w", encoding="utf-8") as f:
        json.dump(content, f, indent=4, ensure_ascii=False)


def sort_dict_with(dic, key="grade"):
    pox = {}
    keys = []
    for k, v in dic:
        if v[key] not in pox:
            pox[key] = []
            keys.append(key)
        pox[key].append((k, v))
    
    out = []
    for key in sorted(keys):
        out.extend(pox[key])
    return out
