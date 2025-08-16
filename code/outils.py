import json
import codecs
import matplotlib.pyplot as plt
import numpy as np
from random import shuffle
from collections import deque
from datetime import datetime, timedelta

中文数字 = "〇一二三四五六七八九十"
中文标点 = "，。！？“”‘’；：……、《》（）~——"
中转数 = {}
数转中 = {}

for i in range(11):
    中转数[中文数字[i]] = i
    数转中[i] = 中文数字[i]


def read(path):
    """按行读取路径下的文件
    """
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        return lines


def behead(s, dilim):
    """按分隔符切掉分割出来的第一部分，返回其余部分
    """
    parts = s.split(dilim)
    return dilim.join(parts[1:])


def headtail(s, dilim):
    """按分隔符返回分割出来的第一部分，和其余部分
    """
    parts = s.split(dilim)
    return parts[0], dilim.join(parts[1:])


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
    """"sort a dictionary according to the value of a certain key
    """
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
    while len(rgb_colors) < nchar:
        if min_brightness > 0.98:
            print(f"Error: unable to produce colors of enough brightness. number of colors: {len(rgb_colors)}, number of characters: {nchar}.")
            break
        min_brightness += 0.02
        rgb_colors = generate_rgb_colors(colormap_name, nchar, min_brightness=min_brightness)
    print(f"brightness: {min_brightness}")
    shuffle(rgb_colors)
    i = 0
    for _, key in name_set.items():
        color_set[key] = rgb_colors[i]
        i += 1
    return name_set, color_set


def nice_print(alist, n=5):
    """print a list nicely
    """
    i = 0
    alen = len(alist)
    while i < alen:
        if i+n < alen:
            print(alist[i:i+n])
        else:
            print(alist[i:])
        i += n


def dump_cn_json_compact(path, content, compact_level=2, max_elements=20, indent=4, compact_fields=None, encoding="utf-8"):
    """
    将 JSON 数据以更紧凑的方式写入文件。
    
    参数:
        data: 要写入的 JSON 数据
        path: 输出文件路径
        compact_level: 从哪一层级开始紧凑展示（默认第2层）
        max_elements: 元素数量超过此值时开始紧凑展示（默认5个）
        compact_keys: 指定某些键对应的值始终紧凑展示（默认 None）
    """
    if compact_fields is None:
        compact_fields = []
    
    def custom_dump(obj, current_level=0, compact_level=2, max_elements=20, indent=4, compact_keys=[]):
        """自定义递归处理函数"""
        if isinstance(obj, dict):
            n = len(obj)
            items = []
            for k, v in obj.items():
                key_part = f'"{k}": '
                # print(current_level, k, compact_keys)
                
                # 检查是否需要紧凑展示
                if (current_level >= compact_level and (k in compact_keys or n >= max_elements)) or k in compact_keys:
                    value_part = json.dumps(v, ensure_ascii=False, separators=(',', ':'))
                else:
                    value_part = custom_dump(v, current_level + 1,compact_level=compact_level,max_elements=max_elements,indent=indent, compact_keys=compact_keys)
                
                items.append(key_part + value_part)
            
            space = ' ' * (indent * (current_level - 1))
            if items:
                out = '{\n' + ',\n'.join(
                    f'{space}{" " * indent}{item}' 
                    for item in items
                ) + f'\n{space}' + '}'
            else:
                out = '{}'
            return out
        elif isinstance(obj, list):
            if current_level >= compact_level and len(obj) > max_elements:
                return json.dumps(obj, ensure_ascii=False, separators=(',', ':'))
            else:
                elements = []
                for item in obj:
                    elements.append(custom_dump(item, current_level + 1,compact_level=compact_level,max_elements=max_elements,indent=indent, compact_keys=compact_keys))
                space = ' ' * (indent * (current_level - 1))
                if elements:
                    out = '[\n' + ',\n'.join(
                        f'{space}{" " * indent}{item}' 
                        for item in elements
                    ) + f'\n{space}' + ']'
                else:
                    out = '[]'
                return out
        else:
            return json.dumps(obj, ensure_ascii=False)
    
    print("compact_fields", compact_fields)
    # 将数据转换为紧凑格式字符串
    compact_str = custom_dump(content, compact_level=compact_level, max_elements=max_elements, indent=indent, compact_keys=compact_fields)
    
    # 写入文件
    with codecs.open(path, "w", encoding=encoding) as file:
        file.write(compact_str)


def find_json_diff_iter(path_1, path_2, num_show=5):
    """
    以迭代方式查找两个JSON文件的差异，返回易理解的报告
    输入：
    path_1, path_2 (str): 两JSON文件路径
    num_show (int): 差异过多时只展示最先发现的部分差异。num_show表示展示的数量。比如num_show=5表示展示前5个差异。
    输出：
    is_valid (bool): 内容是否一致。True表示内容一致。
    report (str): 描述内容差异问题的报告
    """
    try:
        with open(path_1, 'r', encoding='utf-8') as f1, \
             open(path_2, 'r', encoding='utf-8') as f2:

            data_1 = json.load(f1)
            data_2 = json.load(f2)

            diff_report = []
            stack = deque()
            stack.append( (data_1, data_2, "根节点") )  # (旧值, 新值, 当前路径)

            while stack:
                item_1, item_2, path = stack.pop()

                # 类型检查
                if type(item_1) is not type(item_2):
                    diff_report.append(f"路径 {path}\n  类型不同: 文件1→{type(item_1).__name__} 文件2→{type(item_2).__name__}")
                    continue

                # 字典处理
                if isinstance(item_1, dict):
                    keys_1 = set(item_1.keys())
                    keys_2 = set(item_2.keys())

                    # 报告缺失键
                    for missing_key in keys_1 - keys_2:
                        diff_report.append(f"路径 {path}\n  键 '{missing_key}' 在文件1存在但文件2缺失")

                    # 报告新增键
                    for extra_key in keys_2 - keys_1:
                        diff_report.append(f"路径 {path}\n  键 '{extra_key}' 在文件1不存在但文件2存在")

                    # 比较共有键
                    for common_key in keys_1 & keys_2:
                        new_path = f"{path} → 键 '{common_key}'"
                        stack.append( (
                            item_1[common_key],
                            item_2[common_key],
                            new_path
                        ))

                # 列表处理
                elif isinstance(item_1, list) and not isinstance(item_1, str):
                    if len(item_1) != len(item_2):
                        diff_report.append(
                            f"路径 {path}\n  列表长度不同: 文件1→{len(item_1)} 文件2→{len(item_2)}"
                        )
                        continue

                    for idx, (elem_1, elem_2) in enumerate(zip(item_1, item_2)):
                        new_path = f"{path} → 第{idx+1}项"
                        stack.append( (elem_1, elem_2, new_path) )

                # 基本值比较
                else:
                    if item_1 != item_2:
                        diff_report.append(
                            f"路径 {path}\n  值不同: 文件1→{repr(item_1)} 文件2→{repr(item_2)}"
                        )

            if not diff_report:
                return True, "文件内容完全一致"
    
            # 生成易读报告
            report = "发现差异 (按从外到内的层次排列):\n" + "\n\n".join(
                f"差异 {i+1}:\n{desc}" 
                for i, desc in enumerate(diff_report[:num_show])  # 最多显示前5处差异
            )
            if len(diff_report) > num_show:
                report += f"\n\n(共发现{len(diff_report)}处差异，显示前{num_show}处)"
            return False, report

    except Exception as e:  # pylint: disable=broad-exception-caught
        return False, f"验证过程出错: {str(e)}"


# 使用示例
def compare_json_files(path_1, path_2, report_path=None, num_show=5):
    """
    比较两个JSON文件的内容是否一致。如果内容不一致，给出差异报告。默认给出前五个差异。
    """
    is_valid, report = find_json_diff_iter(path_1, path_2, num_show=num_show)
    if not is_valid:
        print("文件内容不一致，请检查以下差异：")
        print(report)
        if report_path:
            with open(report_path, "w", encoding="utf-8") as f:
                f.write(report)
    else:
        print(report)


def sectime(seconds, ouf="str"):
    """
    将从2000年1月1日0时0分0秒到指定秒数的时间转换为年月日时分秒或中文样式字符串。

    参数:
        seconds (int): 从2000年1月1日0时0分0秒到目标时间的秒数。
        output_format (str): 输出格式，"int"表示返回6个整数，"str"表示返回中文样式字符串。默认为"int"。

    返回:
        如果output_format为"int"，返回一个元组，包含年、月、日、时、分、秒；
        如果output_format为"str"，返回一个中文样式的时间字符串，如"2014年3月19日17时52分48秒"。
    """
    # 定义基准时间：2000年1月1日0时0分0秒
    base_time = datetime(2000, 1, 1, 0, 0, 0)

    # 计算目标时间
    target_time = base_time + timedelta(seconds=seconds)

    # 提取年、月、日、时、分、秒
    year = target_time.year
    month = target_time.month
    day = target_time.day
    hour = target_time.hour
    minute = target_time.minute
    second = target_time.second

    if ouf == "int":
        return (year, month, day, hour, minute, second)
    elif ouf == "str":
        return f"{year}年{month}月{day}日{hour}时{minute}分{second}秒"
    elif ouf == "short":
        return f"{year % 100}年{month}月{day}日{hour}时{minute}分{second}秒"
    else:
        raise ValueError("output_format参数无效，必须为'int'或'str'")


def numsec(year=None, month=1, day=1, hour=0, minute=0, second=0):
    """
    将年月日时分秒格式的时刻转换为从2000年1月1日0时0分0秒到该时刻秒数。
    如果不输入年份，则默认转换当前时刻。
    """
    if year is None:
        now = datetime.now()
        year, month, day, hour, minute, second = now.year, now.month, now.day, now.hour, now.minute, now.second
    # 定义基准时间：2000年1月1日0时0分0秒
    base_time = datetime(2000, 1, 1, 0, 0, 0)

    # 创建输入时间的datetime对象
    input_time = datetime(year, month, day, hour, minute, second)

    # 计算时间差
    time_difference = input_time - base_time

    # 计算总秒数（包括秒和微秒部分）
    total_seconds = time_difference.total_seconds()

    # 转换为整数
    return int(total_seconds)


def old_functions():
    """end"""
    pass

# def custom_dump(obj, indent=2, compact_keys=None, current_level=0, compact_len=20, forced_keys=False):
#     if compact_keys is None:
#         compact_keys = set()

#     if isinstance(obj, dict):
#         n = len(obj)
#         items = []
#         for k, v in obj.items():
#             key_part = f'"{k}": '

#             # 关键修改点：对指定键进行紧凑处理
#             if k in compact_keys or n >= compact_len or forced_keys:
#                 value_part = json.dumps(v, ensure_ascii=False, separators=(',', ':'))
#             else:
#                 value_part = custom_dump(v, indent, compact_keys, current_level + 1)

#             items.append(key_part + value_part)

#         space = ' ' * (indent * current_level)
#         if len(items):
#             out = '{\n' + ',\n'.join(
#                 f'{space}{" " * indent}{item}' 
#                 for item in items
#             ) + f'\n{space}' + '}'
#         else:
#             out = r"{}"
#         return out
    
#     elif isinstance(obj, list):
#         # 列表处理保持原有逻辑
#         if len(obj) >= compact_len:
#             items = [custom_dump(item, indent, compact_keys, current_level + 1) for item in obj]
#         else:
#             items = [custom_dump(item, indent, compact_keys, current_level + 1) for item in obj]
        
#         space = ' ' * (indent * current_level)
#         if len(items):
#             out = '[\n' + ',\n'.join(f'{space}{" " * indent}{item}' for item in items) + f'\n{space}]'
#         else:
#             out = r"{}"
#         return out
    
#     else:
#         return json.dumps(obj, ensure_ascii=False)


# def dump_cn_json_compact(path, content, compact_fields={'shizi', 'xiezi', 'ci'}):
#     with codecs.open(path, "w", encoding="utf-8") as f:
#         # compact_fields = {'shizi', 'xiezi', 'ci'}  # 需要紧凑处理的字段
#         json_str = custom_dump(content, indent=4, compact_keys=compact_fields)
#         f.write(json_str)