import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from XLSGUI import Ui_Dialog

equipment = []

# create app
app = QtWidgets.QApplication(sys.argv)

# init
Dialog = QtWidgets.QDialog()
ui = Ui_Dialog()
ui.setupUi(Dialog)
Dialog.show()

# logic
def get_equipment ():
    eq = ui.lineEdit.text()
    equipment.append(eq)


def save_list():
    pass


ui.pushButton.clicked.connect(get_equipment)
ui.pushButton_2.clicked.connect(get_equipment)

# main loop
sys.exit(app.exec_())

