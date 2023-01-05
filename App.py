import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 781, 541))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        self.lineEdit_search = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_search.setGeometry(QtCore.QRect(10, 560, 371, 41))
        self.lineEdit_search.setObjectName("lineEdit_search")
        self.pushButton_add = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_add.setGeometry(QtCore.QRect(390, 560, 141, 41))
        self.pushButton_add.setObjectName("pushButton_add")
        self.pushButton_modify = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_modify.setGeometry(QtCore.QRect(550, 560, 141, 41))
        self.pushButton_modify.setObjectName("pushButton_modify")
        self.pushButton_delete = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_delete.setGeometry(QtCore.QRect(710, 560, 81, 41))
        self.pushButton_delete.setObjectName("pushButton_delete")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.menuFile.addAction(self.actionQuit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Student Management"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "ID"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Name"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "GPA"))
        self.lineEdit_search.setPlaceholderText(_translate("MainWindow", "Search for a student..."))
        self.pushButton_add.setText(_translate("MainWindow", "Add"))
        self.pushButton_modify.setText(_translate("MainWindow", "Modify"))
        self.pushButton_delete.setText(_translate("MainWindow", "Delete"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionQuit.setShortcut(_translate("MainWindow", "Ctrl+Q"))

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Create connection to the database
        self.conn = sqlite3.connect("students.db")
        self.cursor = self.conn.cursor()

        # Create the table if it doesn't exist
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY, name TEXT, gpa REAL)")
        self.conn.commit()

        # Populate the table with data
        self.populate_table()

        # Connect the search line edit to the search function
        self.lineEdit_search.textChanged.connect(self.search)

        # Connect the Add button to the add function
        self.pushButton_add.clicked.connect(self.add)

        # Connect the Modify button to the modify function
        self.pushButton_modify.clicked.connect(self.modify)

        # Connect the Delete button to the delete function
        self.pushButton_delete.clicked.connect(self.delete)

        # Connect the Quit action to the
# closeEvent function to close the program
        self.actionQuit.triggered.connect(self.closeEvent)

    def populate_table(self):
        # Clear the table
        self.tableWidget.setRowCount(0)

        # Get the data from the database
        self.cursor.execute("SELECT * FROM students")
        rows = self.cursor.fetchall()

        # Add the data to the table
        for row in rows:
            row_index = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_index)
            self.tableWidget.setItem(row_index, 0, QtWidgets.QTableWidgetItem(str(row[0])))
            self.tableWidget.setItem(row_index, 1, QtWidgets.QTableWidgetItem(row[1]))
            self.tableWidget.setItem(row_index, 2, QtWidgets.QTableWidgetItem(str(row[2])))

    def search(self, text):
        # Clear the table
        self.tableWidget.setRowCount(0)

        # Get the data from the database
        self.cursor.execute("SELECT * FROM students WHERE name LIKE ?", ("%"+text+"%",))
        rows = self.cursor.fetchall()

        # Add the data to the table
        for row in rows:
            row_index = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_index)
            self.tableWidget.setItem(row_index, 0, QtWidgets.QTableWidgetItem(str(row[0])))
            self.tableWidget.setItem(row_index, 1, QtWidgets.QTableWidgetItem(row[1]))
            self.tableWidget.setItem(row_index, 2, QtWidgets.QTableWidgetItem(str(row[2])))

    def add(self):
        # Open the Add Student dialog
        self.add_dialog = QtWidgets.QDialog()
        self.add_ui = Ui_DialogAdd()
        self.add_ui.setupUi(self.add_dialog)
        self.add_dialog.show()

        # Connect the OK button to the add function
        self.add_ui.pushButton_ok.clicked.connect(self.add_student)

    def add_student(self):
        # Get the data from the dialog
        name = self.add_ui.lineEdit_name.text()
        gpa = self.add_ui.lineEdit_gpa.text()

        # Add the data to the database
        self.cursor.execute("INSERT INTO students (name, gpa) VALUES (?, ?)", (name, gpa))
        self.conn.commit()

        # Close the dialog
        self.add_dialog.close()

        # Update the table
        self.populate_table()

    def modify(self):
        # Get the selected row
        selected_row = self.tableWidget.currentRow()

        if selected_row == -1:
            # No row is selected
            QtWidgets.QMessageBox.warning(
self, "Error", "No student is selected")
            return

        # Get the student ID from the table
        student_id = self.tableWidget.item(selected_row, 0).text()

        # Open the Modify Student dialog
        self.modify_dialog = QtWidgets.QDialog()
        self.modify_ui = Ui_DialogModify()
        self.modify_ui.setupUi(self.modify_dialog)
        self.modify_dialog.show()

        # Get the student data from the database
        self.cursor.execute("SELECT * FROM students WHERE id=?", (student_id,))
        student = self.cursor.fetchone()

        # Set the line edit text
        self.modify_ui.lineEdit_name.setText(student[1])
        self.modify_ui.lineEdit_gpa.setText(str(student[2]))

        # Connect the OK button to the modify function
        self.modify_ui.pushButton_ok.clicked.connect(self.modify_student)

    def modify_student(self):
        # Get the student ID from the table
        selected_row = self.tableWidget.currentRow()
        student_id = self.tableWidget.item(selected_row, 0).text()

        # Get the data from the dialog
        name = self.modify_ui.lineEdit_name.text()
        gpa = self.modify_ui.lineEdit_gpa.text()

        # Update the database
        self.cursor.execute("UPDATE students SET name=?, gpa=? WHERE id=?", (name, gpa, student_id))
        self.conn.commit()

        # Close the dialog
        self.modify_dialog.close()

        # Update the table
        self.populate_table()

    def delete(self):
        # Get the selected row
        selected_row = self.tableWidget.currentRow()

        if selected_row == -1:
            # No row is selected
            QtWidgets.QMessageBox.warning(self, "Error", "No student is selected")
            return

        # Get the student ID from the table
        student_id = self.tableWidget.item(selected_row, 0).text()

        # Delete the student from the database
        self.cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
        self.conn.commit()

        # Update the table
        self.populate_table()

    def closeEvent(self, event):
        # Close the database connection
        self.conn.close()

        # Close the program
        event.accept()

class Ui_DialogAdd(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 40, 57, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(30, 90, 57, 16))
        self.label_2.setObjectName("label_2")
        self.lineEdit_name = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_name.setGeometry(QtCore.QRect(30, 60, 341, 22))
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.lineEdit_gpa = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_gpa.setGeometry(QtCore.QRect(30, 110, 341, 22))
        self.lineEdit_gpa.setObjectName("lineEdit_gpa")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        # Add the OK button to a variable
        self.pushButton_ok = self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Add Student"))
        self.label.setText(_translate("Dialog", "Name:"))
        self.label_2.setText(_translate("Dialog", "GPA:"))

class Ui_DialogModify(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 40, 57, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(30, 90, 57, 16))
self.label_2.setObjectName("label_2")
        self.lineEdit_name = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_name.setGeometry(QtCore.QRect(30, 60, 341, 22))
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.lineEdit_gpa = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_gpa.setGeometry(QtCore.QRect(30, 110, 341, 22))
        self.lineEdit_gpa.setObjectName("lineEdit_gpa")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        # Add the OK button to a variable
        self.pushButton_ok = self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Modify Student"))
        self.label.setText(_translate("Dialog", "Name:"))
        self.label_2.setText(_translate("Dialog", "GPA:"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


