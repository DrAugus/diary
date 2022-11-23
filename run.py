import math
from datetime import date
import os

big_month = [1, 3, 5, 7, 8, 10, 12]

month_char = [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
]

url_prefix = "https://draugus.github.io/diary/"

# 2022-11 begin index 2
begin_index = 2

# 当前文件的上级目录 即本项目目录
project_path = os.path.realpath(os.path.dirname(__file__))
print("project_path:", project_path)

# write file, dairy link
dairy_link_info = ""


def display_form(days, start, y, m):
    res = '\n\n'
    res += '## ' + month_char[int(m) - 1] + '\n\n'
    # start 0 - 6
    # Sun Mon Tue Wed Thu Fri Sat
    res += "|Sun|Mon|Tue|Wed|Thu|Fri|Sat|\n"
    res += "|:---:|:---:|:---:|:---:|:---:|:---:|:---:|\n"
    row = math.ceil((days+start) / 7)
    val = 0
    for i in range(0, row):
        range_s = 0
        if i == 0:
            range_s = start
        s = "|"
        for j in range(0, 7):
            if int(val) >= days:
                s += " |"
                continue
            if i == 0 and j < start:
                s += " |"
            else:
                val = int(val) + 1
                val = add_prefix(val)
                complete_val = "["+val+"]"+"["+str(y)+"/"+str(m)+"/"+val+"]"
                s += complete_val + "|"
        res += s + '\n'
    res += "\n\n\n"
    # print(res)
    return res


def everyday(y, m):
    print(y, m)
    res = ""
    run_year = False
    if y % 4:
        run_year = True
    for mm in range(1, 13):
        if m:
            mm = m
        range_day = 30
        if mm in big_month:
            range_day = 31
        if mm == 2:
            if run_year:
                range_day = 29
            else:
                range_day = 28
        mm = add_prefix(mm)
        print(mm)
        adjust_begin_index(y, m)
        res += display_form(range_day, begin_index, y, mm)
        for dd in range(1, range_day+1):
            dd = add_prefix(dd)
            y = str(y)
            res += "[" + y + "/" + mm + "/" + dd + "]: " +\
                url_prefix + y + "/" + mm + "/" + dd + "\n"
        if m:
            break
    # print(res)
    fo = open(project_path + "/" + y + "/README.md", "ab+")
    fo.write(res.encode())
    fo.close()


def add_prefix(a):
    prefix = str(a)
    if int(a) < 10:
        prefix = '0' + str(a)
    return prefix


def adjust_begin_index(y, m):
    global begin_index
    d0 = date(2022, 11, 1)
    d1 = date(y, m, 1)
    dur = d1 - d0
    dur_day = dur.days
    print("dur day:", dur_day)
    dur_day += begin_index
    begin_index = dur_day % 7
    print("new begin: ", begin_index)


list_file_depth = 2
current_depth = 0
all_file_name = []


def list_all_files(root_dir):
    _files = []
    exclude_path = ['.github', '.vscode', '.gitignore', 'LICENSE', '.git']
    # 列出文件夹下的所有目录和文件
    l1 = os.listdir(root_dir)
    l1 = list(filter(lambda e: e not in exclude_path, l1))
    global current_depth
    current_depth += 1
    # print(l1)
    all_file_name.append(l1)

    if current_depth >= list_file_depth:
        return _files

    for i in range(0, len(l1)):
        path = os.path.join(root_dir, l1[i])
        if os.path.isdir(path):
            _files.extend(list_all_files(path))
        if os.path.isfile(path):
            _files.append(path)

    return _files


def create_today_file():
    today = date.today()
    today = str(today).split('-')
    # today = ['2058', '07', '21']
    print("today is", today)

    l1 = os.listdir(project_path)
    if today[0] not in l1:
        os.mkdir(project_path + '/' + today[0])
        print("mkdir year", today[0])

    path = os.path.join(project_path, today[0])
    l2 = os.listdir(path)
    if today[1] not in l2:
        os.mkdir(path + '/' + today[1])
        print("mkdir month", today[1])
        # meanwhile add readme and
        # all links about this month
        everyday(int(today[0]), int(today[1]))

    path = os.path.join(path, today[1])
    l3 = os.listdir(path)
    day_file = today[2]+".md"
    exist_file = 0
    if day_file in l3:
        exist_file = 1
        print("add something? Y/N?")
        judge = input()
        judge_arr = [['N', 'n'], ['Y', 'y']]
        if judge in judge_arr[0]:
            print("ok, do nothing")
            return

    # no current day file
    # or add something

    # ab+
    # 以二进制格式打开一个文件用于追加。
    # 如果该文件已存在，文件指针将会放在文件的结尾。
    # 如果该文件不存在，创建新文件用于读写。
    fo = open(path+"/"+day_file, "ab+")
    if not exist_file:
        print("new file", day_file)
    print('please input content, \':q\' to exit')
    while 1:
        file_content = input()
        if file_content != ':q':
            fo.write(('%s\n' % file_content).encode())
        else:
            break
    fo.close()


all_feature = '\n=========*****=========\n' \
    'What do you want to do? \n' \
    '   1: create today file or add something in today file\n' \
    '   2: list all files but only depth 2\n' \
    '   3: nothing\n' \
    '=========*****=========\n'

if __name__ == '__main__':
    print(all_feature)
    while 1:
        judge = input()
        if judge == '1':
            create_today_file()
            break
        elif judge == '2':
            list_all_files(project_path)
            # merge
            all_file_name = sum(all_file_name, [])
            all_file_name = list(filter(lambda e: e.isdigit(), all_file_name))
            print(all_file_name)
            break
        elif judge == '3':
            break
        else:
            print('error input, check again')
