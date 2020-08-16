import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QCoreApplication
from XLSGUI import Ui_Dialog
import xlwt, xlrd


# открываем прайс листы
work_book1 = xlrd.open_workbook('./mpls_ec/eq_EC.xls', formatting_info=True)
work_book2 = xlrd.open_workbook('./mpls_ec/eq_MPLS.xls', formatting_info=True)
sheet1 = work_book1.sheet_by_index(0)
sheet2 = work_book2.sheet_by_index(0)
vals1 = [sheet1.row_values(rownum) for rownum in range(sheet1.nrows)]
vals2 = [sheet2.row_values(rownum) for rownum in range(sheet2.nrows)]

# списки для занесения данных
equipment = []
equipment1 = []
equipment2 = []
value = []

# create app
app = QtWidgets.QApplication(sys.argv)

# init
Dialog = QtWidgets.QDialog()
ui = Ui_Dialog()
ui.setupUi(Dialog)
Dialog.show()

# создание эксельки и занесение в нее данных из конечного списка
def create_and_save(equipment2, value):
    book_for_write = xlwt.Workbook('utf8')  # создаём книгу
    sheet_for_write = book_for_write.add_sheet('price')  # создаём лист в этой книге
    sum = 0

    for i in range(len(equipment2)):
        sheet_for_write.write(i, 0, equipment2[i][0])
        if len(equipment2[i][1]) >= 5:
            sheet_for_write.write(i, 1, float(equipment2[i][1].replace(' ', '')) * float(value[i]))
            sum += float(equipment2[i][1].replace(' ', '')) * float(value[i])
        elif len(equipment2[i][1]) < 4:
            sheet_for_write.write(i, 1, float(equipment2[i][1]) * float(value[i]))
            sum += float(equipment2[i][1]) * float(value[i])
        sheet_for_write.write(i, 2, value[i])
        sheet_for_write.write(i, 3, 'шт')
        sheet_for_write.write(i, 4, equipment2[i][1])
        sheet_for_write.write(i, 5, 'за еденицу')
        sheet_for_write.write(i, 6, equipment2[i][2])
        sheet_for_write.write(i, 7, '-')


    sheet_for_write.write(0, 8, 'Итог')
    sheet_for_write.write(0, 9, sum)
    book_for_write.save('account.xls')


# logic
# обработка кнопки "добавить" при нажатии считывает строку и добавляет в список
def get_equipment():
    eq = ui.lineEdit.text()
    eq_2 = ui.lineEdit_2.text()
    equipment.append(eq)
    if eq_2 == '':
        value.append('1')
    else:
        value.append(eq_2)
    ui.lineEdit.clear()
    ui.lineEdit_2.clear()
    return equipment, value


# Вставка ППНИ-37 габарит 2 160А ИЭК
# Таблица под эл./счет. TLR-1F op (в упак - 20 шт)

# Кабель YnDYp-LS (ВВГнг-LS-П) 3х2,5 300/500 V

# обработка кнопки "закончить" начинает поочередный поиск добавленного оборудования в эксельке
def end():
    for i in range(len(equipment)):
        for b in range(len(vals1)):
            if equipment[i] in vals1[b][0]:
                equipment1.append(vals1[b])  # отправная точка, есть элементы

        if len(equipment1) == 0:
            for c in range(len(vals2)):
                if equipment[i] in vals2[c][0]:
                    equipment1.append(vals2[c])
        if len(equipment1) == 0:
            equipment1.append(['not found', '0', 'not found'])

        if len(equipment1) > 1:  # проверяем на количество
            if float(equipment1[0][1]) > float(equipment1[1][1]):
                equipment2.append(equipment1[0])
                equipment1.clear()
            elif float(equipment1[0][1]) < float(equipment1[1][1]):
                equipment2.append(equipment1[1])
                equipment1.clear()
            elif float(equipment1[0][1]) == float(equipment1[1][1]):
                equipment2.append(equipment1[0])
                equipment1.clear()
        elif len(equipment1) < 2:
            equipment2.append(equipment1[0])
            equipment1.clear()
    create_and_save(equipment2, value)


# конектимся с кнопками
ui.pushButton.clicked.connect(get_equipment)
ui.pushButton_2.clicked.connect(end)

sys.exit(app.exec_())

