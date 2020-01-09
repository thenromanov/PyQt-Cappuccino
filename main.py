import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.setGeometry(100, 100, 1400, 600)
        self.con = sqlite3.connect('coffee')
        self.cur = self.con.cursor()
        self.tableWidget.setColumnCount(7)
        names = [i[0] for i in self.con.execute(
            '''SELECT * FROM sorts''').description]
        self.tableWidget.setHorizontalHeaderLabels(names)
        data = self.cur.execute('''SELECT * FROM sorts''').fetchall()
        for i, row in enumerate(data):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()

    def makeUpdate(self):
        names = [i[0] for i in self.con.execute(
            '''SELECT * FROM sorts''').description]
        self.tableWidget.setHorizontalHeaderLabels(names)
        data = self.cur.execute('''SELECT * FROM sorts''').fetchall()
        for i, row in enumerate(data):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.update()


class editWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.con = sqlite3.connect('coffee')
        self.cur = self.con.cursor()
        self.open.clicked.connect(self.updateResult)
        self.add.clicked.connect(self.addResult)
        self.save.clicked.connect(self.saveResults)
        self.tableWidget.itemChanged.connect(self.itemChanged)
        self.spinBox.setMinimum(1)
        self.modified = {}
        self.titles = None

    def updateResult(self):
        result = self.cur.execute('''SELECT * FROM sorts WHERE id=?''',
                                  (self.spinBox.text(),)).fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in self.cur.description]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}

    def itemChanged(self, item):
        self.modified[self.titles[item.column()]] = item.text()

    def addResult(self):
        self.cur.execute(
            '''INSERT INTO sorts(sort, roast, type, description, price, volume) VALUES ('name', 1, 1, 'description', 1, 1) ''')
        result = self.cur.execute(
            '''SELECT * FROM sorts WHERE sort = ?''', ('name',)).fetchall()
        self.titles = [description[0] for description in self.cur.description]
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}

    def saveResults(self):
        if self.modified:
            que = "UPDATE sorts SET\n"
            for key in self.modified.keys():
                que += "{}='{}'\n".format(key, self.modified.get(key))
            que += "WHERE id = ?"
            self.cur.execute(que, (self.tableWidget.item(0, 0).text(),))
            self.con.commit()
            win.makeUpdate()


app = QApplication(sys.argv)
win = Window()
win.show()
edit = editWindow()
edit.show()
sys.exit(app.exec_())
