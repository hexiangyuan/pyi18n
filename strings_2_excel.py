from tempfile import TemporaryFile
from xlwt import Workbook
import re, sys, os

book = Workbook(encoding='utf-8')
sheet = book.add_sheet("iOS")


def read_file(file_path):
    with open(file_path, "r") as ins:
        row_index = 0
        for line in ins:
            if line.strip(" ").startswith(""):
                col_index = 0
                searchObj = re.search(r'\"(.*)\"\s*=\s*\"(.*)\";', line, re.M | re.I)
                if searchObj:
                    print("(" + row_index.__str__() + "," + col_index.__str__() + ")", searchObj.group(1))
                    print("(" + row_index.__str__() + "," + (col_index+1).__str__() + ")", searchObj.group(2))
                    print(searchObj.group(2))
                    sheet.write(row_index, col_index, searchObj.group(1))
                    sheet.write(row_index, col_index + 1, searchObj.group(2))
                    row_index = row_index + 1

            pass


read_file("./ios/en.lproj/Localizable.strings")
book.save("iOS.xls")

book.save(TemporaryFile())
