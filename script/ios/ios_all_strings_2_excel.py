import re
from tempfile import TemporaryFile

import xlwt
from xlwt import Workbook

book = Workbook(encoding='utf-8')
sheet = book.add_sheet("all")

'''
把 iOS 所有的翻译都导出成为一个 exel
'''


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


sheet.write(0, 0, "key")
sheet.write(0, 1, "en")
sheet.write(0, 2, "zh-hant")
sheet.write(0, 3, "zh-hans")
sheet.write(0, 4, "es")
sheet.write(0, 5, "hi")
sheet.write(0, 6, "id")
sheet.write(0, 7, "ko")
sheet.write(0, 8, "ru")
sheet.write(0, 9, "tr")

ios_project_dir = "/Users/xyhe/src/code/xt.com/xt-ios/XT/XT"

zh_hans_dir = read_file_to_dir(ios_project_dir+"/zh-Hans.lproj/Localizable.strings")
en_dir = read_file_to_dir(ios_project_dir+"/en.lproj/Localizable.strings")
zh_hant_dir = read_file_to_dir(ios_project_dir+"/zh-Hant.lproj/Localizable.strings")
ko_dir = read_file_to_dir(ios_project_dir+"/ko.lproj/Localizable.strings")
ja_dir = read_file_to_dir(ios_project_dir+"/ja.lproj/Localizable.strings")
es_dir = read_file_to_dir(ios_project_dir+"/es.lproj/Localizable.strings")
hi_dir = read_file_to_dir(ios_project_dir+"/hi.lproj/Localizable.strings")
id_dir = read_file_to_dir(ios_project_dir+"/id.lproj/Localizable.strings")
ru_dir = read_file_to_dir(ios_project_dir+"/ru.lproj/Localizable.strings")
tr_dir = read_file_to_dir(ios_project_dir+"/tr.lproj/Localizable.strings")
col_index = 1
key_set = set()

error_p = xlwt.Pattern()
error_p.pattern = xlwt.Pattern.SOLID_PATTERN
error_p.pattern_fore_colour = 2

error_p_style = xlwt.XFStyle()
error_p_style.pattern = error_p

#  以英文作为标准 判断其他语言是否有翻译
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
    tr_v = tr_dir.get(key)
    # print(col_index.__str__() + " ，1")

    sheet.write(col_index, 0, key)

    if en_value:
        sheet.write(col_index, 1, en_value)
    else:
        sheet.write(col_index, 1, en_value, error_p_style)

    if zh_hant_value:
        sheet.write(col_index, 2, zh_hant_value)
    else:
        sheet.write(col_index, 2, zh_hant_value,error_p_style)

    if zh_hans_value:
        sheet.write(col_index, 3, zh_hans_value)
    else:
        sheet.write(col_index, 3, zh_hans_value, error_p_style)

    if es_value:
        sheet.write(col_index, 4, es_value)
    else:
        sheet.write(col_index, 4, es_value, error_p_style)

    if hi_v:
        sheet.write(col_index, 5, hi_v)
    else:
        sheet.write(col_index, 5, hi_v, error_p_style)

    if id_v:
        sheet.write(col_index, 6, id_v)
    else:
        sheet.write(col_index, 6, id_v, error_p_style)

    if ko_v:
        sheet.write(col_index, 7, ko_v)
    else:
        sheet.write(col_index, 7, ko_v, error_p_style)

    if ru_v:
        sheet.write(col_index, 8, ru_v)
    else:
        sheet.write(col_index, 8, ru_v, error_p_style)

    if tr_v:
        sheet.write(col_index, 9, tr_v)
    else:
        sheet.write(col_index, 9, tr_v, error_p_style)

    col_index = col_index + 1

book.save("iOSAllLang.xls")
#
book.save(TemporaryFile())
