"""
    Write Excel File
"""
import openpyxl as xl
from typing import List


def create_excel_file(data, save_path):
    # workbook 생성
    wb = xl.Workbook()

    # first sheet(필수)
    sheet = wb.active
    sheet.title = "API Summary"

    # add sheets
    # wb.create_sheet("addSheet")

    # column header
    headers = ['순번','대메뉴', '중메뉴', '소메뉴', 'API URI', 'methods']
    for idx, name in enumerate(headers):
        sheet.cell(1, idx + 1, name)

    current_row_number = 2
    current_col_number = 2

    # sheet date
    for r_num, row in enumerate(data):
        print(f'rownum : {current_row_number + r_num} ')
        sheet.cell(current_row_number + r_num, current_col_number-1, r_num+1)
        for c_num, col in enumerate(row.split("|")):
            # print(current_row_number + r_num, current_col_number + c_num, col)
            sheet.cell(current_row_number + r_num, current_col_number + c_num, col)

    # set file path
    excel_file = save_path

    # save file
    wb.save(excel_file)
    wb.close()

    print("saved")


if __name__ == '__main__':
    print("excel write start")
