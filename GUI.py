# import xlwt, xlrd
# import sys
# from PyQt5.QtWidgets import QApplication, QWidget
#
# work_book1 = xlrd.open_workbook('./eq_EC.xls.xls', formatting_info=True)
# work_book2 = xlrd.open_workbook('./eq_MPLS.xls', formatting_info=True)
#
# sheet1 = work_book1.sheet_by_index(0)
# sheet2 = work_book2.sheet_by_index(0)
#
# book_for_write = xlwt.Workbook('utf8')  # создаём книгу
# sheet_for_write = book_for_write.add_sheet('EC_MPLS')  # создаём лист в этой книге
#
# vals1 = [sheet1.row_values(rownum) for rownum in range(sheet1.nrows)]
# vals2 = [sheet2.row_values(rownum) for rownum in range(sheet2.nrows)]
#
# # Эл. счетчик Нева 303, 5-100A, 220*380В, МОУ (в упак. 30...
#
# search = 'Эл. счетчик Нева 303, 5-100A, 220*380В, МОУ (в упак. 30...'
#
# for i in range(len(vals1)):
#     if search in vals1[i][0]:
#         print(vals1[i])
#         print(i)
#
# print(vals1[19])

import sys

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget,
                             QPushButton, QAction, QLineEdit, QMessageBox)


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Тест'
        self.left = 200
        self.top = 200
        self.width = 400
        self.height = 140
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.textbox = QLineEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(280, 40)

        self.button = QPushButton('Показать', self)
        self.button.move(20, 80)

        self.button.clicked.connect(self.on_click)
        self.show()

    # @pyqtSlot()
    def on_click(self):
        textboxValue = self.textbox.text()
        QMessageBox.question(self, 'Введено', textboxValue, QMessageBox.Ok, QMessageBox.Ok)
        self.textbox.setText("")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())