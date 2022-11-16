import math
from datetime import date

big_month = [1, 3, 5, 7, 8, 10, 12]

url_prefix = "https://draugus.github.io/diary/"

# 2022-11 begin index 2
begin_index = 2


def display_form(days, start, y, m):
    # start 0 - 6
    # Sun Mon Tue Wed Thu Fri Sat
    print("|Sun|Mon|Tue|Wed|Thu|Fri|Sat|")
    print("|:---:|:---:|:---:|:---:|:---:|:---:|:---:|")
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
        print(s)
    print("\n\n\n")


def everyday(y, m):
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
        adjust_begin_index(y, m)
        display_form(range_day, begin_index, y, m)
        for dd in range(1, range_day+1):
            dd = add_prefix(dd)
            y = str(y)
            print("[" + y + "/" + mm + "/" + dd + "]: " +
                  url_prefix + y + "/" + mm + "/" + dd)
        if m:
            break


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
    print(dur_day)
    dur_day += begin_index
    begin_index = dur_day % 7
    print("new begin: ", begin_index)


if __name__ == '__main__':
    everyday(2022, 12)
