import os
import re

from utils import find_line_info_with_index, find_lines_index_with_string, get_dir_year_month

project_path = os.path.realpath(os.path.dirname(__file__))
print("project_path:", project_path)

filename = f'{project_path}/index.md'


count_last_files = 5


def get_last(sorted_data):
    index = 0
    res = []
    for year, months in sorted_data.items():
        for month in months:
            path = f'{year}/{month}'
            days = os.listdir(path)
            days = sorted(days, reverse=True)
            for day in days:
                res.append(f'{path}/{day}')
                index += 1
                if index >= count_last_files:
                    return res

    return res


def modify_with_html(last_info) -> str:
    res = '\n\n'
    for v in last_info:
        # -3: .md
        title = v[:-3]
        file_path = f'{project_path}/{v}'
        details = get_recent_details(file_path)

        one = '<p>\n'
        link = f'<a href="./{v}">...</a>'
        one += f'<span class="date">{title}</span><br />\n'
        one += f'<span class="details">{details}{link}</span>\n'
        one += '</p>\n'
        res += one

    res += '\n\n'
    return res


def get_recent_details(file_path):
    with open(file_path, "r+", encoding='utf-8') as file_handle:
        all_line = file_handle.readlines()
        res = ''
        for index, value in enumerate(all_line):
            if value.startswith('#') or value == '\n':
                continue
            res += value
            res = res.replace('\n', ' ')
            # 将多个空格替换为一个
            res = re.sub(r'\s+', ' ', res)
            if len(res) > 30:
                break

        res = res[:30]

        return res


def update_recent(file_path, rm_begin_line, rm_end_line, recent_info):
    temp_filename = 'temptemp'
    # 打开原始文件以读取模式和一个临时文件以写入模式
    with open(file_path, 'r', encoding='utf-8') as original_file, open(temp_filename, 'w', encoding='utf-8') as temp_file:
        ori_lines = original_file.readlines()
        temp_file.write(''.join(ori_lines[:rm_begin_line]))
        temp_file.write(''.join(recent_info))
        temp_file.write(''.join(ori_lines[rm_end_line:]))

    # 替换原文件为临时文件的内容
    os.replace(temp_filename, file_path)


if __name__ == '__main__':
    get_ym_info = get_dir_year_month(project_path)
    print(get_ym_info)
    # sorted_data = dict(sorted(aa.items(), reverse=True))
    sorted_data = {
        year: sorted(months, reverse=True)
        for year, months in sorted(get_ym_info.items(), reverse=True)
    }
    print("sorted_data", sorted_data)
    last_info = get_last(sorted_data)
    print("last_info", last_info)

    # 找到要删除的部分
    find_last_index = find_lines_index_with_string(filename, '最近更新')
    print("find_last_index", find_last_index)
    find_info = find_line_info_with_index(filename, find_last_index[0])
    print("find_info", find_info)
    count_hashes = find_info.count('#')
    find_index_same_title_lv = find_lines_index_with_string(
        filename, '#'*count_hashes)
    print("find_index_same_title_lv", find_index_same_title_lv)
    index_in_same_title = find_index_same_title_lv.index(find_last_index[0])
    next_index = find_index_same_title_lv[index_in_same_title + 1]
    print("next_index", next_index)
    rm_begin_line, rm_end_line = find_last_index[0], next_index-1

    update_recent(filename, rm_begin_line, rm_end_line,
                  modify_with_html(last_info))
