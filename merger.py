import xlwt, xlrd
import Parser_EC
import parser_MPLS
import os


Parser_EC.parse1()
parser_MPLS.parse2()

work_book1 = xlrd.open_workbook('./eq_EC.xls.xls', formatting_info=True)
work_book2 = xlrd.open_workbook('./eq_MPLS.xls', formatting_info=True)

sheet1 = work_book1.sheet_by_index(0)
sheet2 = work_book2.sheet_by_index(0)

book_for_write = xlwt.Workbook('utf8')  # создаём книгу
sheet_for_write = book_for_write.add_sheet('EC_MPLS')  # создаём лист в этой книге

vals1 = [sheet1.row_values(rownum) for rownum in range(sheet1.nrows)]
vals2 = [sheet2.row_values(rownum) for rownum in range(sheet2.nrows)]


for i in range(len(vals1)):
    sheet_for_write.write(i, 0, vals1[i][0])
    sheet_for_write.write(i, 1, vals1[i][1])
    sheet_for_write.write(i, 2, vals1[i][2])
    sheet_for_write.write(i, 3, '-')


for i in range(len(vals2)):
    sheet_for_write.write(i, 4, vals2[i][0])
    sheet_for_write.write(i, 5, vals2[i][1])
    sheet_for_write.write(i, 6, vals2[i][2])
    sheet_for_write.write(i, 7, '-')


book_for_write.save('EC_MPLS.xls')
# os.remove('./eq_EC.xls.xls')
# os.remove('./eq_MPLS.xls')
