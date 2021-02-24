import sqlite3
import sys

from PyQt5 import uic
from PyQt5.Qt import *
from PyQt5 import QtWidgets


class Coffeemain(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.cur = sqlite3.connect('coffee.sqlite').cursor()
        self.run()
        self.pushButton.clicked.connect(self.search)
        self.pushButton_2.clicked.connect(self.run)

    def run(self):
        self.show_table(self.cur.execute("""SELECT * FROM coffee""").fetchall())

    def search(self):
        try:
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Coffeemain()
    ex.show()
    sys.exit(app.exec())