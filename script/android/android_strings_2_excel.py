# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import xml.sax

import openpyxl


def write_excel_xlsx(path, sheet_name, value):
    index = len(value)
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = sheet_name
    for i in range(0, index):
        for j in range(0, len(value[i])):
            sheet.cell(row=i + 1, column=j + 1, value=str(value[i][j]))
    workbook.save(path)


class StringHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.key = ""
        self.value = ""
        self.tag = ""
        self.dic = {}

    # 元素开始调用
    def startElement(self, tag, attributes):
        self.tag = tag
        if tag == "string":
            self.key = attributes["name"]

    # 元素结束调用
    def endElement(self, tag):
        if tag == "string":
            self.dic[self.key] = self.value

    # 读取字符时调用
    def characters(self, content):
        if self.tag == "string":
            self.value = content


class StringsParser:
    def __init__(self, str):
        # 创建一个 XMLReader
        parser = xml.sax.make_parser()
        # 关闭命名空间
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)

        # 重写 ContextHandler
        Handler = StringHandler()
        parser.setContentHandler(Handler)
        parser.parse(str)
        self.dic = Handler.dic


# 这个是 android 对比2个 string 资源文件分别 生成一个 excel
if __name__ == '__main__':

    parser1 = StringsParser("stringsen.xml")
    parser2 = StringsParser("stringses.xml")
    value = [["key", "english", "es"]]

    for key in parser1.dic:
        if key not in parser2.dic.keys():
            value.append([key, parser1.dic[key], ""])
            print("key=", key, "value=")

    write_excel_xlsx("../../xml.xlsx", '西班牙', value)