# 查询 iOS 每个翻译词条使用的次数
# 1. 遍历 string 词条文件
# 3. 拿每个词条去 项目里的文件匹配
# 4. 读取每个文件 去除空格和换行符
# 6. 字符串匹配文件使用次数
import os
import re
from tempfile import TemporaryFile

from xlwt import Workbook


def read_file_to_dir(file_path):
    with open(file_path, "r") as ins:
        return_dir = {}
        for line in ins:
            if line.strip(" ").startswith(""):
                searchObj = re.search(r'\"(.*)\"\s*=\s*\"(.*)\";', line, re.M | re.I)
                if searchObj:
                    return_dir[searchObj.group(1)] = searchObj.group(2)
            # else:
            # print("false")
    return return_dir


def strings_use_count(file_path, strings_key):
    with open(file_path, encoding="utf-8") as file:
        file_content = file.read()
        return file_content.replace('\n', '').replace(' ', '').count(strings_key.replace('\n', '').replace(' ', ''))


def find_all_file(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            fullname = os.path.join(root, f)
            yield fullname


def write_dir_execl(direction, file_path, sheet_name):
    book = Workbook(encoding='utf-8')
    sheet = book.add_sheet(sheet_name)
    row_index = 0
    if direction:
        for dirKey in direction.keys():
            col_index = 0
            print("(" + row_index.__str__() + "," + col_index.__str__() + ")", dirKey)
            print("(" + row_index.__str__() + "," + (col_index + 1).__str__() + ")", direction.get(dirKey))
            sheet.write(row_index, col_index, dirKey)
            sheet.write(row_index, col_index + 1, direction.get(dirKey))
            row_index = row_index + 1
        book.save(file_path)
        book.save(TemporaryFile())


ios_project_dir = "/Users/xyhe/src/code/xt.com/xt-ios/XT/XT/"

strings_dir = read_file_to_dir(ios_project_dir + "/en.lproj/Localizable.strings")
# strings_dir = {"预计盈亏为& USDT": 11}

count_dir = {"key": "使用次数"}

for key in strings_dir.keys():
    count = 0
    for file in find_all_file(ios_project_dir):
        if file.endswith(".swift"):
            count = count + strings_use_count(file, "\"{}\".locals".format(key))
    print(key)
    print(count)
    count_dir[key] = count

print("正在把数据写入excel")
write_dir_execl(count_dir, "./keyUseCount.xls", "ios")


