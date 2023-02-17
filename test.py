def modify_line_find(filename, find_str):
    all_line = ""
    with open(filename, "r+", encoding='utf-8') as file_handle:
        all_line = file_handle.readlines()
        for idx, ll in enumerate(all_line):
            find_index = ll.find(find_str)
            if ll.find(find_str) != -1:
                this_line = all_line[idx]
                print('this_line', this_line)
                prefix = this_line[:find_index]
                print("prefix", prefix)
                suffix = this_line[find_index+len(find_str):]
                print("suffix", suffix)
                all_line[idx] = prefix+'[////]'+suffix
    with open('.output', "w+", encoding='utf-8') as file_handle:
        file_handle.writelines(all_line)


if __name__ == '__main__':
    modify_line_find("temp", '04')
