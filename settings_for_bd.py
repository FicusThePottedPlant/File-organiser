import sqlite3
import sys

from PyQt5 import QtGui, QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QMessageBox

import add_extension
import add_type
import second_ui


class AddForm1(QWidget, add_extension.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('ui/plus.png'))
        self.setWindowModality(QtCore.Qt.WindowModality(2))
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)


class AddForm2(QWidget, add_type.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('ui/plus.png'))
        self.setWindowModality(QtCore.Qt.WindowModality(2))
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)


class SecondForm(QWidget, second_ui.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Настройки')
        self.setWindowModality(QtCore.Qt.WindowModality(2))
        self.con = sqlite3.connect('data/files.sqlite')
        self.setWindowIcon(QtGui.QIcon('ui/settings.png'))
        self.cur = self.con.cursor()
        self.data = {}
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_2.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.form1 = AddForm1()
        self.form2 = AddForm2()

        self.load_table1()
        self.load_table2()

        self.pushButton.clicked.connect(self.insert_format)  # Добавить расширение
        self.pushButton_2.clicked.connect(self.edit_format)  # Редактировать расширение
        self.pushButton_3.clicked.connect(self.delete_format)  # Удалить расширение
        self.pushButton_4.clicked.connect(self.insert_type)  # Добавить тип
        self.pushButton_5.clicked.connect(self.edit_type)  # Редактировать тип
        self.pushButton_6.clicked.connect(self.delete_type)  # Удалить тип

        self.tableWidget.horizontalHeader().setSectionsClickable(False)
        self.tableWidget_2.horizontalHeader().setSectionsClickable(False)
        self.tableWidget.cellClicked.connect(self.selection_helper)
        self.tableWidget_2.cellClicked.connect(self.selection_helper)

    def selection_helper(self):
        """a function that automatically select row when user select a cell"""
        self.sender().selectRow(self.sender().currentRow())

    def load_cb_from_form1(self):
        """Loading types from types table of database files.sqlite in combobox of form of adding extension"""
        result = self.cur.execute(
            '''SELECT id, name FROM types''').fetchall()
        self.form1.comboBox.clear()
        for i in result:
            self.form1.comboBox.addItem(i[1])
        self.data = dict((v, k) for k, v in result)

    def load_table1(self):
        """Loading files table from database in TableWidget"""
        self.load_cb_from_form1()
        result = self.cur.execute(
            '''
            SELECT files.id, files.title, types.name FROM files, types
            WHERE files.type = types.id;
            ''').fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.tableWidget.setHorizontalHeaderLabels(['id', 'Расширение', 'Тип'])
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.tableWidget.setColumnWidth(2, 360)
        self.con.commit()

    def load_table2(self):
        """Loading types table from database in TableWidget"""
        self.load_cb_from_form1()
        result = self.cur.execute(
            '''SELECT * FROM types''').fetchall()
        self.tableWidget_2.setRowCount(len(result))
        self.tableWidget_2.setColumnCount(len(result[0]))
        self.tableWidget_2.setHorizontalHeaderLabels(['id', 'Тип'])
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget_2.setItem(i, j, QTableWidgetItem(str(val)))
        self.tableWidget_2.setColumnWidth(1, 485)
        self.con.commit()

    def insert_format(self):
        """Insert new extension in files table of database by add_extension.py GUI"""

        def add():
            if txt := self.form1.lineEdit.text():
                if txt[0] == '.' and txt.count('.') == 1:
                    if txt not in [i[0] for i in self.con.execute(
                            '''SELECT title FROM files''').fetchall()]:
                        count_id = self.cur.execute(
                            '''SELECT id FROM files''').fetchall()[-1][0]

                        self.cur.execute('''INSERT INTO files(id, title, type) VALUES (?, ?, ?)''',
                                         (count_id + 1, txt, self.data[self.form1.comboBox.currentText()]))
                        self.load_table1()
                    else:
                        QMessageBox.information(self, 'Ошибка добавления',
                                                'Файл с таким расширением уже существует', QMessageBox.Ok)
                else:
                    QMessageBox.question(self, 'ВНИМАНИЕ',
                                         'Это не расширение!',
                                         QMessageBox.Ok)
            self.form1.close()
            self.form1.lineEdit.setText('')
            self.form1.pushButton.clicked.disconnect(add)

        self.load_cb_from_form1()
        self.form1.setWindowTitle('Добавить')
        self.form1.show()
        self.form1.pushButton.clicked.connect(add)

    def edit_format(self):
        """edit extension row from files table of database by add_extension.py GUI"""

        def edit():
            try:
                if (txt := self.form1.lineEdit.text()) and txt[0] == '.' and txt.count('.') == 1:
                    if txt == exp.text() or txt not in [i[0] for i in self.con.execute(
                            '''SELECT title FROM files''').fetchall()]:
                        self.cur.execute(
                            '''UPDATE files
                                SET title = ?, type = ?
                                WHERE id = ?''', (txt, self.data[self.form1.comboBox.currentText()], idd.text()))
                        self.load_table1()

                    else:
                        QMessageBox.information(self, 'Ошибка редактирования',
                                                'Файл с таким расширением уже существует', QMessageBox.Ok)
                self.form1.lineEdit.setText('')
                self.form1.close()
                self.form1.pushButton.clicked.disconnect(edit)
            except RuntimeError:
                pass

        if len(data := self.tableWidget.selectedItems()) == 3 and data[0].text().isdigit() and not \
                data[1].text().isdigit():
            idd, exp, typ = data
            self.form1.setWindowTitle('Изменить')
            self.form1.lineEdit.setText(exp.text())
            self.form1.comboBox.setCurrentText(typ.text())
            self.form1.show()
            self.form1.pushButton.clicked.connect(edit)
        else:
            QMessageBox.information(self, 'Не выделена строка',
                                    'Выделите строку для редактирования', QMessageBox.Ok)

    def delete_format(self):
        """delete selected extension row from files table of database"""
        if len(data := self.tableWidget.selectedItems()) == 3 and data[0].text().isdigit() and not \
                data[1].text().isdigit():
            idd, *_ = data
            valid = QMessageBox.question(self, 'Внимание', 'Вы действительно хотите удалить данную строку?',
                                         QMessageBox.Yes,
                                         QMessageBox.No)
            if valid == QMessageBox.Yes:
                self.cur.execute(
                    f'''DELETE from files
                        WHERE id = {int(idd.text())}''')
                self.load_table1()
        else:
            QMessageBox.information(self, 'Не выделена строка',
                                    'Выделите строку для удаления', QMessageBox.Ok)

    def insert_type(self):
        """Insert new type in types table of database by add_type.py GUI"""

        def add():
            if txt := self.form2.lineEdit.text():
                if txt not in [i[0] for i in self.con.execute(
                        '''SELECT name FROM types''').fetchall()]:
                    count_id = self.cur.execute(
                        '''SELECT id FROM types''').fetchall()[-1][0]

                    self.cur.execute('''INSERT INTO types(id, name) VALUES (?, ?)''',
                                     (count_id + 1, txt))
                else:
                    QMessageBox.information(self, 'Ошибка добавления типа',
                                            'Такой тип уже существует', QMessageBox.Ok)
                self.load_table1()
                self.load_table2()

            self.form2.close()
            self.form2.lineEdit.setText('')
            self.form2.pushButton.clicked.disconnect(add)

        self.form2.setWindowTitle('Добавить')
        self.form2.show()
        self.form2.pushButton.clicked.connect(add)

    def edit_type(self):
        """Edit type in types table of database by add_type.py GUI"""

        def edit():
            if txt := self.form2.lineEdit.text():
                if txt == typ.text() or txt not in [i[0] for i in self.con.execute(
                        '''SELECT name FROM types''').fetchall()]:
                    self.cur.execute(
                        '''UPDATE types
                            SET name = ?
                            WHERE id = ?''', (txt, idd.text()))
                    self.form2.lineEdit.setText('')
                    self.form2.close()

                    self.load_table1()
                    self.load_table2()
                else:
                    QMessageBox.information(self, 'Ошибка редактирования типа',
                                            'Такой тип уже существует', QMessageBox.Ok)

            self.form2.pushButton.clicked.disconnect(edit)

        if len(data := self.tableWidget_2.selectedItems()) == 2 and data[0].text().isdigit() and \
                not data[1].text().isdigit():
            idd, typ = data
            self.form2.lineEdit.setText(typ.text())
            self.form2.setWindowTitle('Изменить')
            self.form2.show()
            self.form2.pushButton.clicked.connect(edit)
        else:
            QMessageBox.information(self, 'Не выделены строку',
                                    'Выделите строку для редактирования', QMessageBox.Ok)

    def delete_type(self):
        """Delete type in types table of database"""
        if len(data := self.tableWidget_2.selectedItems()) == 2 and data[0].text().isdigit() and \
                not data[1].text().isdigit():
            idd, *_ = data
            valid = QMessageBox.question(self, 'Внимание', 'Вы действительно хотите удалить данную строку?',
                                         QMessageBox.Yes,
                                         QMessageBox.No)
            if valid == QMessageBox.Yes:
                linked = self.cur.execute(
                    f'''
                    SELECT files.title FROM files WHERE files.type = {idd.text()};
                    ''').fetchall()
                if linked:
                    QMessageBox.information(self, 'Внимание',
                                            'К данному типу привязаны расширения', QMessageBox.Ok)
                else:
                    self.cur.execute(
                        f'''DELETE from types
                            WHERE id = {int(idd.text())}''')
                    self.load_table1()
                    self.load_table2()
        else:
            QMessageBox.information(self, 'Не выделены строку',
                                    'Выделите строку для удаления', QMessageBox.Ok)

    def get_directories(self) -> dict:
        """Returns dict where types of file are keys and values are list of extension"""
        directories = {}
        result = self.cur.execute(
            '''
            SELECT files.title, types.name
             FROM files, types
             WHERE files.type = types.id;
            ''').fetchall()
        for i in result:
            if i[1] in directories.keys():
                directories[i[1]].append(i[0])
            else:
                directories.setdefault(i[1], [i[0]])
        return {k: tuple(v) for k, v in directories.items()}


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)
