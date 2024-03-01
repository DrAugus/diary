import math
from datetime import date
import os

from utils import get_dir_year_month

big_month = [1, 3, 5, 7, 8, 10, 12]

month_char = [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
]

url_prefix = "https://draugus.github.io/diary/"

is_windows = os.name == 'nt'
if is_windows:
    print("now is windows")
else:
    print("now not is windows")

# 2022-09 begin index 4
# index from 0, 0 is Sun.
begin_index = 4

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
                # complete_val = "["+val+"]"+"["+str(y)+"/"+str(m)+"/"+val+"]"
                # 表格内不再添加链接
                complete_val = val
                s += complete_val + "|"
        res += s + '\n'
    res += "\n\n\n"
    # print(res)
    return res


def everyday(y, m):
    print("everyday", y, m)
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
        print("month", mm)
        adjust_begin_index(y, m)
        # form
        res += display_form(range_day, begin_index, y, mm)
        for dd in range(1, range_day+1):
            dd = add_prefix(dd)
            y = str(y)
            # link
            res += "[" + y + "/" + mm + "/" + dd + "]: " +\
                url_prefix + y + "/" + mm + "/" + dd + "\n"
        if m:
            break
    # print(res)
    filename=project_path + "/" + y + "/README.md"
    fo = open(filename, "ab+")
    fo.write(res.encode())
    fo.close()
    
    # 前两行是否有年
    with open(filename, 'r') as file:
        lines = file.readlines()
    if lines and (y not in lines[0] and y not in lines[1]):
        # insert title and style
        insert_info = f"# {y}\n\n"
        file_style = f'{project_path}/style.css'
        insert_info += '\n<style>\n'
        with open(file_style, 'r', encoding='utf-8') as file:
            for oneline in file.readlines():
                insert_info += f'{oneline}'
        insert_info += '\n</style>\n'
        insert_line(filename, insert_info)



def add_prefix(a):
    prefix = str(a)
    if int(a) < 10:
        prefix = '0' + str(a)
    return prefix


def adjust_begin_index(y, m):
    global begin_index
    d0 = date(2022, 9, 1)
    d1 = date(y, m, 1)
    dur = d1 - d0
    dur_day = dur.days
    print("dur day:", dur_day)
    dur_day += begin_index
    begin_index = dur_day % 7
    print("new begin: ", begin_index)


def create_today_file(cp=False):
    today = date.today()
    today = str(today).split('-')
    # today = ['2058', '07', '21']
    print("today is", today)

    year, month, day = today[0], today[1], today[2]
    path_today = f'{project_path}/{year}/{month}/{day}.md'

    if os.path.exists(path_today):
        print("add something? Y/N?")
        judge = input()
        judge_arr = [['N', 'n'], ['Y', 'y']]
        if judge in judge_arr[0]:
            print("ok, do nothing")
            return
    
    create_someday_file(year, month, day)

    if cp:
        cp_file(year, month, day)
        return

    option_write_file = "\n" \
        "select one way to write file\n"\
        "   1. use command line to write"\
        "   2. copy a file to current day"
    print(option_write_file)
    while 1:
        judge = input()
        if judge == '1':
            # add something
            write_file(path_today)
            break
        elif judge == '2':
            cp_file(year, month, day)
            break
        else:
            print('error input, check again')


def create_someday_file(year, month, day):
    obj = get_dir_year_month(project_path)
    print("get_dir_year_month", obj)
    years = obj.keys()
    print("path depth1, years:", years)
    if year not in years:
        os.mkdir(project_path + '/' + year)
        os.mkdir(project_path + '/' + year + '/' + month)
        print("mkdir year and month, y m is ", year, month)
        print("create_someday_file: meanwhile add readme and all links about this month")
        everyday(int(year), int(month))
    else:
        months = obj[year]
        print("path depth2, month:", months)
        if month not in months:
            os.mkdir(project_path + '/' + year + '/' + month)
            print("mkdir month, m is ", month)
            print("create_someday_file: meanwhile add readme and all links about this month")
            everyday(int(year), int(month))


def cp_file(year, month, day):
    source = project_path + '/temp'
    fo = open(source, "ab+")
    fo.close()

    des = f'{project_path}/{year}/{month}/{day}.md'
    modify_line(year, month, day)
    print("source: ", source, "\ndes: ", des)
    insert_line(source, f'# {year}/{month}/{day}\n\n')
    cp_file_cmd(source, des)


def cp_file_cmd(source, des):
    if is_windows:
        print("now windows, but using cp command")
        os.system('cp ' + source + ' ' + des)
    else:
        os.system('cp ' + source + ' ' + des)


def write_file(file):
    # ab+
    # 以二进制格式打开一个文件用于追加。
    # 如果该文件已存在，文件指针将会放在文件的结尾。
    # 如果该文件不存在，创建新文件用于读写。
    fo = open(file, "ab+")
    print('please input content, \':q\' to exit')
    while 1:
        file_content = input()
        if file_content != ':q':
            fo.write(('%s\n' % file_content).encode())
        else:
            break
    fo.close()


def modify_month(m, d):
    if not isinstance(m, str):
        m = str(m)
    if len(m) != 2:
        m = '0' + m            
    if not isinstance(d, str):
        d = str(d)
    if len(d) != 2:
        d = '0' + d    
    return m, d


def modify_line(y, m, d):
    # print('para', y, m, d)
    if not isinstance(y, str):
        y = str(y)
    filename = project_path+"/" + y + "/README.md"
    m, d = modify_month(m, d)
    # print('modify', y, m, d)
    all_line = ""
    # for month Dec
    next_month = '######'
    m_int = int(m)
    current_month = month_char[m_int-1]
    if m_int < 12:
        # m - 1 is current month
        next_month = month_char[m_int]
    find_str = '|' + d + '|'
    cur_month_line_idx = -1
    next_month_line_idx = 999999

    # 防止没有该文件
    # 检查文件是否存在
    if not os.path.isfile(filename):
        # 文件不存在，创建文件
        with open(filename, 'w') as file:
            # 文件已创建，可以在此处写入内容，如果不需要写入可以什么也不做
            pass
    else:
        # 文件存在，不做任何操作
        print("File already exists.")


    with open(filename, "r+", encoding='utf-8') as file_handle:
        all_line = file_handle.readlines()
        for idx, ll in enumerate(all_line):
            if current_month in ll:
                cur_month_line_idx = idx
                # print("find current month", idx)
            if next_month in ll:
                next_month_line_idx = idx
                # print("find next month", idx)
        
        for idx, ll in enumerate(all_line):
            find_index = ll.find(find_str)

            condition = (int(m) == 12 and idx > cur_month_line_idx) or \
                (int(m) < 12 and
                    idx > cur_month_line_idx and idx < next_month_line_idx)

            if not condition:
                continue
            if ll.find(find_str) != -1:
                this_line = all_line[idx]
                prefix = this_line[:find_index]
                print("prefix", prefix)
                suffix = this_line[find_index+len(find_str):]
                print("suffix", suffix)
                add_link = f'|[{d}][{y}/{m}/{d}]|'
                change_line = prefix+add_link+suffix
                print('this_line', this_line, "change_line", change_line)
                all_line[idx] = change_line
    with open(filename, "w+", encoding='utf-8') as file_handle:
        file_handle.writelines(all_line)


def insert_line(file_path, insert_info):
    temp_filename = 'temptemp'
    # 打开原始文件以读取模式和一个临时文件以写入模式
    with open(file_path, 'r', encoding='utf-8') as original_file, open(temp_filename, 'w', encoding='utf-8') as temp_file:
        # 读取第一行并判断是否存在内容
        first_line = original_file.readline()
        temp_file.write(insert_info)  # 在临时文件中先写入要插入的内容

        # 将原始文件剩余的所有行写入临时文件
        if first_line:
            temp_file.write(first_line)  # 写入原始的第一行（已不是第一行）
        for line in original_file:
            temp_file.write(line)

    # 替换原文件为临时文件的内容
    os.replace(temp_filename, file_path)


all_feature = '\n=========*****=========\n' \
    'What do you want to do? \n' \
    '   1: create today file or add something in today file.\n' \
    '       use command, not commended\n' \
    '   2: list all year/month dirs but only depth 2\n' \
    '   3: copy file to today file \n' \
    '>> 4: commend -> copy file to appoint file \n' \
    '   5: quit and create a file named temp to write \n' \
    '   6: write every day, input y and m \n' \
    '   7: modify line \n' \
    '   0: nothing\n' \
    '=========*****=========\n'

if __name__ == '__main__':
    print(all_feature)
    while 1:
        judge = input()
        if judge == '1':
            create_today_file()
            break
        elif judge == '2':
            obj = get_dir_year_month(project_path)
            print(obj)
            break
        elif judge == '3':
            create_today_file(True)
            break
        elif judge == '4':
            print("please input year month day, as like '2022 01 01' ")
            new_in = input()
            new_in = new_in.split(' ')
            if len(new_in) != 3:
                print('error input, exit')
                break
            year, month, day = new_in[0], new_in[1], new_in[2]
            if len(year) != 4 and len(month) != 2 and len(day) != 2:
                print('error input, exit')
                break                
            create_someday_file(year, month, day)
            cp_file(year, month, day)
            break
        elif judge == '5':
            source = project_path + '/temp'
            fo = open(source, "ab+")
            fo.close()
            break
        elif judge == '6':
            print("everyday, input y, m")
            new_in = input()
            new_in = new_in.split(' ')
            if len(new_in) != 2:
                print("error input")
                break
            y = new_in[0]
            m = new_in[1]
            print("year ", y, "month ", m)
            everyday(int(y), int(m))
            break
        elif judge == '7':
            print("modify line, input y, m")
            new_in = input()
            new_in = new_in.split(' ')
            if len(new_in) != 2:
                print("error input")
                break
            y, m = new_in[0], new_in[1]
            print("your input", y, m)
            cmd = f"cd {project_path}/{y}/{m} && ls | cut -d '.' -f 1"
            obj = os.popen(cmd)
            modify_days = obj.read().split('\n')
            print(modify_days)
            # modify_line('2023', '02','02')
            for dd in modify_days:
                if not len(dd):
                    continue
                modify_line(y, m, dd)
            break
        elif judge == '0':
            break
        else:
            print('error input, check again')
