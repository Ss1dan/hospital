from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem, QDialog, QMessageBox
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
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        self.add(line.strip().split("&"))
        except FileNotFoundError:
            pass

    def save(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            for item in self.patients.values():
                f.write("&".join(item.to_list()) + "\n")
    
    def search_by_last_name(self, last_name):
        return {k: v for k, v in self.patients.items() if v.last_name.lower() == last_name.lower()}
    
    def get_sorted_by_last_name(self):
        return dict(sorted(self.patients.items(), key=lambda item: item[1].last_name))

class AddPatientDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("add_patient_dialog.ui", self)
        self.setWindowTitle("Добавить пациента")
        self.buttonBox.accepted.connect(self.validate)
        self.buttonBox.rejected.connect(self.reject)
    
    def validate(self):
        if not all([self.lineEdit_last_name.text(), 
                   self.lineEdit_first_name.text(),
                   self.lineEdit_middle_name.text(),
                   self.lineEdit_year.text(),
                   self.lineEdit_address.text(),
                   self.lineEdit_diagnos.text(),
                   self.lineEdit_days.text()]):
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены!")
            return
        self.accept()
    
    def get_data(self):
        return [
            self.lineEdit_last_name.text(),
            self.lineEdit_first_name.text(),
            self.lineEdit_middle_name.text(),
            self.lineEdit_year.text(),
            self.lineEdit_address.text(),
            self.lineEdit_diagnos.text(),
            self.lineEdit_days.text()
        ]

class EditPatientDialog(QDialog):
    def __init__(self, patient_data, parent=None):
        super().__init__(parent)
        uic.loadUi("edit_patient_dialog.ui", self)
        self.setWindowTitle("Редактировать пациента")
        
        # Заполняем поля текущими значениями
        self.lineEdit_last_name.setText(patient_data[0])
        self.lineEdit_first_name.setText(patient_data[1])
        self.lineEdit_middle_name.setText(patient_data[2])
        self.lineEdit_year.setText(patient_data[3])
        self.lineEdit_address.setText(patient_data[4])
        self.lineEdit_diagnos.setText(patient_data[5])
        self.lineEdit_days.setText(patient_data[6])
        
        self.buttonBox.accepted.connect(self.validate)
        self.buttonBox.rejected.connect(self.reject)
    
    def validate(self):
        if not all([self.lineEdit_last_name.text(), 
                   self.lineEdit_first_name.text(),
                   self.lineEdit_middle_name.text(),
                   self.lineEdit_year.text(),
                   self.lineEdit_address.text(),
                   self.lineEdit_diagnos.text(),
                   self.lineEdit_days.text()]):
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены!")
            return
        self.accept()
    
    def get_data(self):
        return [
            self.lineEdit_last_name.text(),
            self.lineEdit_first_name.text(),
            self.lineEdit_middle_name.text(),
            self.lineEdit_year.text(),
            self.lineEdit_address.text(),
            self.lineEdit_diagnos.text(),
            self.lineEdit_days.text()
        ]

class SearchDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("search_dialog.ui", self)
        self.setWindowTitle("Поиск пациента")
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
    
    def get_last_name(self):
        return self.lineEdit_last_name.text()

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
    dialog = AddPatientDialog(win)
    if dialog.exec_() == QDialog.Accepted:
        data = dialog.get_data()
        hospital.add(data)
        hospital.save("hospital.txt")
        load_table()

def delete_patient():
    selected_row = win.tableWidget.currentRow()
    if selected_row == -1:
        QMessageBox.warning(win, "Ошибка", "Выберите пациента для удаления!")
        return
    
    data = [win.tableWidget.item(selected_row, i).text() for i in range(7)]
    reply = QMessageBox.question(win, "Подтверждение", 
                               "Вы уверены, что хотите удалить этого пациента?",
                               QMessageBox.Yes | QMessageBox.No)
    if reply == QMessageBox.Yes:
        hospital.delete(data)
        hospital.save("hospital.txt")
        load_table()

def edit_patient():
    selected_row = win.tableWidget.currentRow()
    if selected_row == -1:
        QMessageBox.warning(win, "Ошибка", "Выберите пациента для редактирования!")
        return
    
    data = [win.tableWidget.item(selected_row, i).text() for i in range(7)]
    dialog = EditPatientDialog(data, win)
    if dialog.exec_() == QDialog.Accepted:
        new_data = dialog.get_data()
        key = hospital.find_key(data)
        if key != -1:
            hospital.edit(key, new_data)
            hospital.save("hospital.txt")
            load_table()

def search_patient():
    dialog = SearchDialog(win)
    if dialog.exec_() == QDialog.Accepted:
        last_name = dialog.get_last_name()
        if not last_name:
            load_table()
            return
        
        found_patients = hospital.search_by_last_name(last_name)
        win.tableWidget.setRowCount(len(found_patients))
        for row, patient in enumerate(found_patients.values()):
            for col, val in enumerate(patient.to_list()):
                win.tableWidget.setItem(row, col, QTableWidgetItem(val))

def sort_by_last_name():
    hospital.patients = hospital.get_sorted_by_last_name()
    load_table()

win.pushButton.clicked.connect(load_table)
win.pushButton_3.clicked.connect(add_patient)
win.pushButton_4.clicked.connect(edit_patient)
win.pushButton_5.clicked.connect(delete_patient)
win.pushButton_6.clicked.connect(sort_by_last_name)

load_table()
win.show()
sys.exit(app.exec())