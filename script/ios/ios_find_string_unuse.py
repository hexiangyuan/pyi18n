# 查询 iOS 每个翻译词条使用的次数
# 1. 遍历 string 词条文件
# 3. 拿每个词条去 项目里的文件匹配
# 4. 读取每个文件 去除空格和换行符
# 6. 字符串匹配文件使用次数
import os
import re
from tempfile import TemporaryFile

from xlwt import Workbook
import sys

lines = []


class StringsKeyModal:

    def __init__(self, raw, wordK, wordV):
        self.raw = raw
        self.wordK = wordK
        self.wordV = wordV


def read_file_to_list(file_path):
    with open(file_path, "r") as ins:
        return_list = []
        for line in ins:
            stringKV = StringsKeyModal(None, None, None)
            stringKV.raw = line
            if line.strip(" ").startswith(""):
                reResult = re.search(r'\"(.*)\"\s*=\s*\"(.*)\";', line, re.M | re.I)
                if reResult:
                    stringKV.wordK = reResult.group(1)
                    stringKV.wordV = reResult.group(2)
            # else:
            # print("false")
            return_list.append(stringKV)
    return return_list


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


ios_project_dir = "/Users/xyhe/src/code/xt.com/xt-ios/XT/XT"
langs = ["en", "es", "hi", "id", "ja", "ko", "ru", "tr", "zh-Hans", "zh-Hant"]


# langs = [ "zh-Hans"]

def deal_un_use_string(lang):
    strings_list = read_file_to_list(ios_project_dir + "/" + lang + ".lproj/Localizable.strings")
    count_dir = {}

    for item in strings_list:
        if item.wordK:
            count = 0
            for file in find_all_file(ios_project_dir):
                if file.endswith(".swift"):
                    count = count + strings_use_count(file, "\"{}\".locals".format(item.wordK))
            print(item.wordK)
            print(count)
            count_dir[item.wordK] = count

    print("正在把数据写入excel")
    write_dir_execl(count_dir, "./keyUseCounters." + lang + ".xls", lang)
    # 删除未使用的词条
    strings_dir_temp = "Localizable." + lang + ".strings"
    with open(strings_dir_temp, "w") as w:
        for item in strings_list:
            if item.wordK:
                if count_dir[item.wordK] > 0:
                    w.write(item.raw)
            else:
                w.write(item.raw)


def delete_all_un_use_words():
    for lang in langs:
        deal_un_use_string(lang)


def fix_hans_untranslated_words():
    strings_list_en = read_file_to_list(ios_project_dir + "/en.lproj/Localizable.strings")
    strings_list_cn_hans = read_file_to_list(ios_project_dir + "/zh-Hans.lproj/Localizable.strings")
    untranslated_zh_hans_words = []
    for en in strings_list_en:
        has_hans = False
        for hans in strings_list_cn_hans:
            if en.wordK == hans.wordK:
                has_hans = True
                break

        if not has_hans:
            print(en.wordK)
            untranslated_zh_hans_words.append(en.wordK)
    print(untranslated_zh_hans_words.__len__())
    strings_dir_temp = "Localizable.hans_untranslated.strings"
    with open(strings_dir_temp, "w") as w:
        for untranslated_item in untranslated_zh_hans_words:
            if untranslated_item:
                w.write("\"" + untranslated_item + "\" = " + "\"" + untranslated_item + "\";")
                w.write("\r")
    return untranslated_zh_hans_words


args = sys.argv
if args[1] == "-d":
    # 删除无用的词条
    delete_all_un_use_words()
elif args[1] == "-h":
    # 修复未翻译的汉语词条
    fix_hans_untranslated_words()
