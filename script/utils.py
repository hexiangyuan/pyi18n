from tempfile import TemporaryFile

from xlwt import Workbook


def write_dir_execl(direction, file_path, sheet_name):
    book = Workbook(encoding='utf-8')
    sheet = book.add_sheet(sheet_name)
    col_index = 0
    if direction:
        for key in direction.keys():
            row_index = 0
            print("(" + row_index.__str__() + "," + col_index.__str__() + ")", key)
            print("(" + row_index.__str__() + "," + (col_index + 1).__str__() + ")", direction.get(key))
            sheet.write(row_index, col_index, key)
            sheet.write(row_index, col_index + 1, direction.get(key))
            row_index = row_index + 1
        book.save(file_path)
        book.save(TemporaryFile())
