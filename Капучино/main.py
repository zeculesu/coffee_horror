import sqlite3
import sys

from PyQt5 import uic
from PyQt5.Qt import *
from PyQt5 import QtWidgets
from PyQt5 import QtCore


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 227)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(270, 170, 101, 31))
        self.pushButton.setObjectName("pushButton")
        self.formLayoutWidget = QtWidgets.QWidget(Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(20, 10, 361, 141))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.label_4 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.label_5 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.lineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_2)
        self.lineEdit_5 = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.lineEdit_5)
        self.spinBox = QtWidgets.QSpinBox(self.formLayoutWidget)
        self.spinBox.setObjectName("spinBox")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.spinBox)
        self.comboBox = QtWidgets.QComboBox(self.formLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.comboBox)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "Сохранить"))
        self.label.setText(_translate("Dialog", "Название сорта"))
        self.label_2.setText(_translate("Dialog", "Степень обжарки"))
        self.label_3.setText(_translate("Dialog", "Тип"))
        self.label_4.setText(_translate("Dialog", "Цена"))
        self.label_5.setText(_translate("Dialog", "Объём"))
        self.comboBox.setItemText(0, _translate("Dialog", "зёрна"))
        self.comboBox.setItemText(1, _translate("Dialog", "молотый"))


class Coffeemain(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.cur = sqlite3.connect('coffee.sqlite').cursor()
        self.dialo = None
        self.run()
        self.pushButton.clicked.connect(self.search)
        self.pushButton_2.clicked.connect(self.run)
        self.add_button.clicked.connect(lambda x: self.dialog('add'))
        self.edit_button.clicked.connect(lambda x: self.dialog('change'))

    def dialog(self, action):
        self.dialo = AddEditCoffeeForm(self.run, action, self.tableWidget)

    def run(self):
        self.statusbar.showMessage('')
        self.show_table(self.cur.execute("""SELECT * FROM coffee""").fetchall())

    def search(self):
        try:
            self.statusbar.showMessage('')
            text = self.lineEdit.text()
            result = self.cur.execute("""SELECT * FROM coffee WHERE title = (?)""", (text,)).fetchall()
            if not result:
                raise ValueError
            self.show_table(result)
        except ValueError:
            self.statusbar.showMessage('Такого у нас нет')

    def show_table(self, result):
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Название сорта", "Степень обжарки", "Тип", "Цена", 'Объём'])
        self.tableWidget.setRowCount(len(result))
        for i in range(len(result)):
            for j in range(6):
                it = QtWidgets.QTableWidgetItem(str(result[i][j]))
                self.tableWidget.setItem(i, j, it)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(2)


class AddEditCoffeeForm(Coffeemain, Ui_Dialog):
    def __init__(self, callback, action, tableWidget):
        super().__init__()
        self.setupUi(self)
        self.callback = callback
        self.cur = sqlite3.connect('coffee.sqlite').cursor()
        try:
            self.show()
            if action == 'add':
                self.pushButton.clicked.connect(self.add_coffee)
            elif action == 'change':
                self.id = 0
                self.show_info(tableWidget)
                # self.pushButton.clicked.connect(self.change_coffee)
        except Exception as e:
            print(e)

    def show_info(self, tableWidget):
        try:
            self.pushButton.setText('Отредактировать')
            self.id = tableWidget.item(tableWidget.selectedItems()[0].row(), 0).text()
            id, title, degree_roasting, type_cofee, cost, package_size = self.cur.execute(
                """SELECT * FROM coffee WHERE id = (?)""", (self.id,)).fetchone()
            self.lineEdit.setText(str(title))
            self.lineEdit_2.setText(str(degree_roasting))
            self.comboBox.setCurrentText(type_cofee)
            self.spinBox.setValue(int(cost))
            self.lineEdit_5.setText(str(package_size))
        except IndexError:
            self.hide()

    def close(self):
        self.hide()
        self.callback()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Coffeemain()
    ex.show()
    sys.exit(app.exec())