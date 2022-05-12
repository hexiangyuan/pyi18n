from tempfile import TemporaryFile
from xlwt import Workbook
import re, sys, os

book = Workbook(encoding='utf-8')
sheet = book.add_sheet("all")

'''
把 iOS 所有的翻译都导出成为一个 exel
'''


def read_file_to_dir(file_path):
    with open(file_path, "r") as ins:
        return_dir = {}
        print(ins.__sizeof__())
        for line in ins:
            if line.strip(" ").startswith(""):
                searchObj = re.search(r'\"(.*)\"\s*=\s*\"(.*)\";', line, re.M | re.I)
                # print("true")
                if searchObj:
                    return_dir[searchObj.group(1)] = searchObj.group(2)
                else:
                    if not line.strip(" ") == " ":
                        print(line)
            # else:
            # print("false")
    return return_dir


sheet.write(0, 0, "key")
sheet.write(0, 1, "zh-hans")
sheet.write(0, 2, "zh-hant")
sheet.write(0, 3, "en")
sheet.write(0, 4, "es")
sheet.write(0, 5, "hi")
sheet.write(0, 6, "id")
sheet.write(0, 7, "ko")
sheet.write(0, 8, "ru")

zh_hans_dir = read_file_to_dir("./ios/zh-Hans.lproj/Localizable.strings")
en_dir = read_file_to_dir("./ios/en.lproj/Localizable.strings")
zh_hant_dir = read_file_to_dir("./ios/zh-Hant.lproj/Localizable.strings")
ko_dir = read_file_to_dir("./ios/ko.lproj/Localizable.strings")
ja_dir = read_file_to_dir("./ios/ja.lproj/Localizable.strings")
es_dir = read_file_to_dir("./ios/es.lproj/Localizable.strings")
hi_dir = read_file_to_dir("./ios/hi.lproj/Localizable.strings")
id_dir = read_file_to_dir("./ios/id.lproj/Localizable.strings")
ru_dir = read_file_to_dir("./ios/ru.lproj/Localizable.strings")
col_index = 1
key_set = set()
for key in zh_hans_dir:
    key_set.add(key)

for key in en_dir:
    key_set.add(key)

for key in key_set:
    zh_hans_value = zh_hans_dir.get(key)
    zh_hant_value = zh_hant_dir.get(key)
    en_value = en_dir.get(key)
    es_value = es_dir.get(key)
    hi_v = hi_dir.get(key)
    id_v = id_dir.get(key)
    ko_v = ko_dir.get(key)
    ru_v = ru_dir.get(key)
    # print(col_index.__str__() + " ，1")
    sheet.write(col_index, 0, key)
    sheet.write(col_index, 1, zh_hans_value)
    sheet.write(col_index, 2, zh_hant_value)
    sheet.write(col_index, 3, en_value)
    sheet.write(col_index, 4, es_value)
    sheet.write(col_index, 5, hi_v)
    sheet.write(col_index, 6, id_v)
    sheet.write(col_index, 7, ko_v)
    sheet.write(col_index, 8, ru_v)
    col_index = col_index + 1

book.save("iOSAllLang.xls")
#
book.save(TemporaryFile())
