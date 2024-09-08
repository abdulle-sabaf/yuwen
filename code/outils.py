import json
import codecs
import matplotlib.pyplot as plt
import numpy as np
from random import shuffle


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


def keys(dico):
    """return the keys of a dictionary as a list
    """
    return list(dico.keys())


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
    for k, v in dic.items():
        if v[key] not in pox:
            pox[v[key]] = []
            keys.append(v[key])
        pox[v[key]].append((k, v))

    out = []
    for key in sorted(keys):
        out.extend(pox[key])
    return out



def generate_rgb_colors(colormap_name, k, min_brightness=0.3):
    # Get the colormap from matplotlib
    cmap = plt.get_cmap(colormap_name)
    
    # Generate `k` evenly spaced values from 0 to 1
    norm = plt.Normalize(vmin=0, vmax=k-1)
    scalar_map = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    indices = np.arange(k)
    colors = scalar_map.to_rgba(indices)
    
    # Convert RGBA colors to RGB integers between 0 and 255
    rgb_colors = []
    for color in colors:
        brightness = 0.2126 * color[0] + 0.7152 * color[1] + 0.0722 * color[2]  # Luminance formula
        if brightness < min_brightness:
            rgb_colors.append((int(color[0] * 255), int(color[1] * 255), int(color[2] * 255)))
    
    # If not enough colors are below the brightness threshold, reduce the threshold
    while len(rgb_colors) < k and min_brightness < 1:
        min_brightness += 0.05
        for color in colors:
            brightness = 0.2126 * color[0] + 0.7152 * color[1] + 0.0722 * color[2]
            if brightness < min_brightness and (int(color[0] * 255), int(color[1] * 255), int(color[2] * 255)) not in rgb_colors:
                rgb_colors.append((int(color[0] * 255), int(color[1] * 255), int(color[2] * 255)))
        rgb_colors = rgb_colors[:k]  # Ensure only `k` colors are returned
    
    return rgb_colors


def set_char_colors(content, script_key, colormap_name="tab10", min_brightness=0.5):
    """Set the colors for the characters in a script.
    Inputs:
    content (list of str): the content of the script. With each line the speech of one character at a time beginning with \\item[***]. 
    script_key (str): the key of the script so as to generate color keys. The color keys start with the script key.
    colormap_name (str): name of the colormap to use. 
    min_brightness (float): minimal brightness requirement so that the colors don't get too light. smaller min means stricter (darker) colors.
    Output:
    name_set: set of character names with color key. dict: name --> key 
    color_set: set of colors by key. dict: key --> color
    """
    name_set = {}
    color_set = {}
    i = 0
    for line in content:
        if line.startswith("\\item["):
            name = line.split(']')[0][6:]
            if name not in name_set:
                name_key = script_key + "-" + str(i)
                name_set[name] = name_key
                # color_set[name_key] = 
                i += 1

    nchar = len(name_set)
    rgb_colors = generate_rgb_colors(colormap_name, nchar, min_brightness=min_brightness)
    shuffle(rgb_colors)
    i = 0
    for _, key in name_set.items():
        color_set[key] = rgb_colors[i]
        i += 1
    return name_set, color_set


def nice_print(alist, n=5):
    i = 0
    alen = len(alist)
    while i < alen:
        if i+n < alen:
            print(alist[i:i+n])
        else:
            print(alist[i:])
        i += n
