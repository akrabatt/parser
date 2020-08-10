import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QCoreApplication
from XLSGUI import Ui_Dialog
import xlwt, xlrd


# открываем прайс листы
work_book1 = xlrd.open_workbook('./eq_EC.xls.xls', formatting_info=True)
work_book2 = xlrd.open_workbook('./eq_MPLS.xls', formatting_info=True)
sheet1 = work_book1.sheet_by_index(0)
sheet2 = work_book2.sheet_by_index(0)
vals1 = [sheet1.row_values(rownum) for rownum in range(sheet1.nrows)]
vals2 = [sheet2.row_values(rownum) for rownum in range(sheet2.nrows)]

# списки для занесения данных
equipment = []
equipment1 = []
equipment2 = []

# create app
app = QtWidgets.QApplication(sys.argv)

# init
Dialog = QtWidgets.QDialog()
ui = Ui_Dialog()
ui.setupUi(Dialog)
Dialog.show()

# создание эксельки и занесение в нее данных из конечного списка
def create_and_save(equipment2):
    book_for_write = xlwt.Workbook('utf8')  # создаём книгу
    sheet_for_write = book_for_write.add_sheet('test')  # создаём лист в этой книге

    for i in range(len(equipment2)):
        sheet_for_write.write(i, 0, equipment2[i][0])
        sheet_for_write.write(i, 1, equipment2[i][1])
        sheet_for_write.write(i, 2, equipment2[i][2])
        sheet_for_write.write(i, 3, '-')

    book_for_write.save('test.xls')


# logic
# обработка кнопки "добавить" при нажатии считывает строку и добавляет в список
def get_equipment():
    eq = ui.lineEdit.text()
    equipment.append(eq)
    # print(equipment)
    ui.lineEdit.clear()
    return equipment


# Вставка ППНИ-37 габарит 2 160А ИЭК
# Таблица под эл./счет. TLR-1F op (в упак - 20 шт)

# Кабель YnDYp-LS (ВВГнг-LS-П) 3х2,5 300/500 V

# обработка кнопки "закончить" начинает поочередный поиск добавленного оборудования в эксельке
def end():
    try:
        for i in range(len(equipment)):
            for b in range(len(vals1)):
                if equipment[i] in vals1[b][0]:
                    equipment1.append(vals1[b])  # отправная точка, есть элементы

            if len(equipment1) > 1:
                if int(equipment1[0][1]) > int(equipment1[1][1]):
                    equipment2.append(equipment1[0])
                    equipment1.clear()
                else:
                    equipment2.append(equipment1[1])
                    equipment1.clear()
            elif len(equipment1) < 2:
                equipment2.append(equipment1[0])
                equipment1.clear()
        print(equipment2)
        # create_and_save(equipment2)
    except:
        for i in range(len(equipment)):
            for b in range(len(vals2)):
                if equipment[i] in vals2[b][0]:
                    equipment1.append(vals2[b])  # отправная точка, есть элементы

            if len(equipment1) > 1:
                if int(equipment1[0][1]) > int(equipment1[1][1]):
                    equipment2.append(equipment1[0])
                    equipment1.clear()
                else:
                    equipment2.append(equipment1[1])
                    equipment1.clear()
            elif len(equipment1) < 2:
                equipment2.append(equipment1[0])
                equipment1.clear()
        print(equipment2)
        # create_and_save(equipment2)
    create_and_save(equipment2)


# конектимся с кнопками
ui.pushButton.clicked.connect(get_equipment)
# ui.pushButton_2.clicked.connect(QCoreApplication.instance().quit)
ui.pushButton_2.clicked.connect(end)

sys.exit(app.exec_())

