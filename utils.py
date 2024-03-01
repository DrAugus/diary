import os

project_path = os.path.realpath(os.path.dirname(__file__))
print("project_path:", project_path)
filename = f'{project_path}/temp'

from enum import Enum
class DateType(Enum):
    INVALID = -1
    YEAR = 1
    MONTH = 2

exclude_path = ['.github', '.vscode', '.gitignore', 'LICENSE', '.git','__pycache__']


def list_all_files(root_dir, current_depth=0):
    _files = []
    # 列出文件夹下的所有目录和文件
    l1 = os.listdir(root_dir)
    l1 = list(filter(lambda e: e not in exclude_path, l1))
    current_depth += 1
    # print(l1)

    for file in l1:
        path = os.path.join(root_dir, file)
        if os.path.isdir(path):
            _files.extend(list_all_files(path, current_depth))
        if os.path.isfile(path):
            _files.append(path)

    return _files


def get_dir_year_month(root_dir, dt:DateType=DateType.INVALID, list_file_depth=2):

    all_file_name = []
    
    def list_all_files(root_dir, current_depth=0):
        _files = []
        # 列出文件夹下的所有目录和文件
        l1 = os.listdir(root_dir)
        l1 = list(filter(lambda e: e not in exclude_path, l1))
        current_depth += 1
        # print(l1)
        all_file_name.append(l1)

        if current_depth >= list_file_depth:
            return _files

        for file in l1:
            path = os.path.join(root_dir, file)
            if os.path.isdir(path):
                # print(">>> ", path)
                _files.extend(list_all_files(path, current_depth))
            if os.path.isfile(path):
                _files.append(path)

        return _files

    list_all_files(root_dir)
    print("all_file_name", all_file_name)
    list_year = all_file_name[0]
    list_month = all_file_name[1:]

    list_year = list(filter(lambda e: e.isdigit(), list_year))
    list_month = [list(filter(lambda e: e.isdigit(), month)) for month in list_month]

    print("list_year", list_year)
    print("list_month", list_month)    

    res = []
    for index, value in enumerate(list_year):
        obj = {
            'year': value,
            'month': list_month[index]
        }
        res.append(obj)
    
    if dt == DateType.YEAR:
       return [item['year'] for item in res]  
    
    if dt == DateType.MONTH:
       return [item['month'] for item in res]      
    
    obj = {}
    for index, value in enumerate(res):    
        obj[value['year']] = value['month']
    
    return obj


def find_lines_index_with_string(file_path, search_string):  
    lines_index = []  
    with open(file_path, 'r') as file:  
        for line_number, line in enumerate(file, start=1):  
            if search_string in line:  
                lines_index.append(line_number)  
    return lines_index  


def find_line_info_with_index(file_path, line_index):
    with open(file_path, 'r') as file:  
        for line_number, line in enumerate(file, start=1):  
            if line_number == line_index:  
                return line
    
