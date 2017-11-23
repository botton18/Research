import xlrd

workbook = xlrd.open_workbook("testinfo.xlsx")

worksheet = workbook.sheet_by_name("Sheet1")


print(format(worksheet.cell(0,1).value))
