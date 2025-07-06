from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem
import sys

class Patient:
    def __init__(self, last_name='', first_name='', middle_name='', year='', address='', diagnos='', days=''):
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.year = year
        self.address = address
        self.diagnos = diagnos
        self.days = days

    def to_list(self):
        return [self.last_name, self.first_name, self.middle_name, self.year, self.address, self.diagnos, self.days]

    def equals(self, other):
        return self.to_list() == other.to_list()

class Hospital:
    def __init__(self):
        self.patients = {}
        self.count = 0

    def add(self, data):
        self.patients[self.count] = Patient(*data)
        self.count += 1

    def find_key(self, data):
        target = Patient(*data)
        for key, patient in self.patients.items():
            if patient.equals(target):
                return key
        return -1

    def delete(self, data):
        key = self.find_key(data)
        if key != -1:
            del self.patients[key]
            self.count -= 1

    def edit(self, key, data):
        self.patients[key] = Patient(*data)

    def load(self, filename):
        self.patients = {}
        self.count = 0
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    self.add(line.strip().split("&"))


    def save(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            for item in self.patients.values():
                f.write("&".join(item.to_list()) + "\n")


hospital = Hospital()
hospital.load("hospital.txt")

app = QtWidgets.QApplication([])
win = uic.loadUi("hospital.ui")

win.tableWidget.setColumnCount(7)
win.tableWidget.setHorizontalHeaderLabels(["Фамилия", "Имя", "Отчество", "Год рождения", "Адрес", "Диагноз", "Дней в больнице"])
win.tableWidget.setColumnWidth(0, 119) 
win.tableWidget.setColumnWidth(1, 108) 
win.tableWidget.setColumnWidth(2, 120) 
win.tableWidget.setColumnWidth(3, 150)  
win.tableWidget.setColumnWidth(4, 160) 
win.tableWidget.setColumnWidth(5, 150)  
win.tableWidget.setColumnWidth(6, 200)

def load_table():
    win.tableWidget.setRowCount(len(hospital.patients))
    for row, patient in enumerate(hospital.patients.values()):
        for col, val in enumerate(patient.to_list()):
            win.tableWidget.setItem(row, col, QTableWidgetItem(val))

def add_patient():
    data = [win.lineEdit_4.text(), win.lineEdit_5.text(), win.lineEdit_6.text(),
            win.lineEdit_7.text(), win.lineEdit_8.text(), win.lineEdit_9.text(), win.lineEdit_10.text()]
    hospital.add(data)
    hospital.save("warehouse_data.txt")
    load_table()

def delete_patient():
    data = [win.lineEdit_4.text(), win.lineEdit_5.text(), win.lineEdit_6.text(),
            win.lineEdit_7.text(), win.lineEdit_8.text(), win.lineEdit_9.text(), win.lineEdit_10.text()]
    hospital.delete(data)
    hospital.save("warehouse_data.txt")
    load_table()

def edit_patient():
    row = int(win.lineEdit_2.text()) - 1
    col = int(win.lineEdit_3.text()) - 1
    new_value = win.lineEdit.text()

    if row < 0 or row >= win.tableWidget.rowCount():
        return
    if col < 0 or col >= win.tableWidget.columnCount():
        return

    old_data = [win.tableWidget.item(row, i).text() for i in range(7)]
    key = hospital.find_key(old_data)

    if key != -1:
        win.tableWidget.setItem(row, col, QTableWidgetItem(new_value))
        new_data = [win.tableWidget.item(row, i).text() for i in range(7)]
        hospital.edit(key, new_data)
        hospital.save("warehouse_data.txt")
        load_table()


win.pushButton.clicked.connect(load_table)     
win.pushButton_3.clicked.connect(add_patient)   
win.pushButton_4.clicked.connect(edit_patient)   
win.pushButton_5.clicked.connect(delete_patient) 

win.show()
sys.exit(app.exec())