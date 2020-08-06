import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QCoreApplication
from XLSGUI import Ui_Dialog
import xlwt, xlrd

work_book1 = xlrd.open_workbook('./eq_EC.xls.xls', formatting_info=True)
sheet1 = work_book1.sheet_by_index(0)
vals1 = [sheet1.row_values(rownum) for rownum in range(sheet1.nrows)]

equipment = []
equipment1 = []
value = []
value1 = []


def create_and_save():
    book_for_write = xlwt.Workbook('utf8')  # создаём книгу
    sheet_for_write = book_for_write.add_sheet('test')  # создаём лист в этой книге
    book_for_write.save('test.xls')


# create app
app = QtWidgets.QApplication(sys.argv)

# init
Dialog = QtWidgets.QDialog()
ui = Ui_Dialog()
ui.setupUi(Dialog)
Dialog.show()

# logic
def get_equipment():
    eq = ui.lineEdit.text()
    equipment.append(eq)
    # print(equipment)
    ui.lineEdit.clear()
    return equipment


def end():
    # print(equipment)
    # create_and_save()

    for i in range(len(equipment)):
        for b in range(len(vals1)):
            if equipment[i] in vals1[b][0]:
                print(vals1[b][1])


ui.pushButton.clicked.connect(get_equipment)
# ui.pushButton_2.clicked.connect(QCoreApplication.instance().quit)
ui.pushButton_2.clicked.connect(end)
print(vals1[180])
sys.exit(app.exec_())

