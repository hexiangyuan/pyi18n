import openpyxl

items = {}


def writeToXml(values):
    f = open("Localizable-ru.strings","w")
    for key, value in values.items():
        print(key, "=====", value)
        if value:
            line = "\n\""+key+"\""+" = "+"\""+value+"\""
            f.write(line)
    f.close()


def readExcel():
    workbook = openpyxl.load_workbook("app-ru.xlsx")
    sheet = workbook["iOS"]
    key = "A2:C" + str(sheet.max_row)
    cell = sheet[key]
    for i in cell:
        items[i[0].value] = i[2].value


readExcel()
writeToXml(items)
