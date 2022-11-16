import math


big_month = [1, 3, 5, 7, 8, 10, 12]

url_prefix = "https://draugus.github.io/diary/"


def display_form(days, start, y, m):
    # start 0 - 6
    # Sun Mon Tue Wed Thu Fri Sat
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
        display_form(range_day, 2, y, m)
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


if __name__ == '__main__':
    everyday(2022, 11)
