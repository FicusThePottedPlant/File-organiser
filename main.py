import sys
import webbrowser

from PyQt5 import QtGui, Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtWidgets import QMessageBox, qApp

from main_window_ui import Ui_MainWindow
from fs_script import OrganiseByFiles
from settings_for_bd import SecondForm


class Main(QMainWindow, Ui_MainWindow):
    """A main window with UX elements.
    fs prefix for file sort function
    (TODO) make a ds(date sort) and ms(mask sort)
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Сортировщик')
        self.action_bars()
        self.setWindowIcon(QtGui.QIcon('ui/logo.png'))
        self.tabWidget.removeTab(1)  # TODO working tabs
        self.tabWidget.removeTab(1)  # now i had deleted them to make a project done
        self.switch = {0: self.listWidget, 1: self.listWidget_2, 2: self.listWidget_3}
        try:
            self.second_form = SecondForm()
            self.data = []
            self.pushButton.clicked.connect(self.fs_settings)
            self.pushButton_2.clicked.connect(self.add)
            self.pushButton_3.clicked.connect(self.delete)
            self.pushButton_4.clicked.connect(self.fs_run)

            self.pushButton_5.clicked.connect(self.add)
            self.pushButton_6.clicked.connect(self.delete)

        except Exception as er:
            print(er.__str__(), '\nВозможно требуется Python >= 3.8.X')

    def action_bars(self):
        def op():
            webbrowser.open_new('t.me/ficusthepottedplant')  # contact me

        def help_():
            print('''Чтобы добавить папку для сортировки нажмите +, 
а для удаления выделите папку и нажмите -.
Когда вы выбрали все папки, нажмите 'Начать сортировку'.
    
Внимание! Все файлы будут перемещены в новые папки, 
поэтому не сортируйте файлы которые зависят от их местоположения.

Вы также можете нажать на кнопку настройки
для редактирования сортировки по вашему усмотрению.''')

        help_action = self.action
        help_action.triggered.connect(help_)
        link_action = self.action_1
        link_action.triggered.connect(op)
        exit_action = self.action_2
        exit_action.triggered.connect(qApp.quit)
        self.action_3.triggered.connect(self.fs_settings)

    def fs_settings(self):
        """open settings"""
        self.second_form.show()

    def fs_run(self):
        """run organising by pressing button"""
        valid = QMessageBox.question(self, 'ВНИМАНИЕ',
                                     'Вы действительно хотите отсортировать папки? Они будут перемещены в новые папки.',
                                     QMessageBox.Ok,
                                     QMessageBox.Cancel)
        if valid == QMessageBox.Ok:
            try:
                for i in range(self.listWidget.count()):
                    OrganiseByFiles(self.listWidget.item(i).text())
                QMessageBox.information(self, 'Готово',
                                        'Все файлы отсортированы по папкам!',
                                        QMessageBox.Ok)
            except Exception as er:
                QMessageBox.information(self, 'Ошибка',
                                        f'Произошла ошибка с сортировкой по файлам,'
                                        f'{er.__str__()}',
                                        QMessageBox.Ok)

    def add(self):
        """add new item in list widget by plus button"""
        filename = QFileDialog.getExistingDirectory()
        if filename and filename not in self.data:
            self.data.append(filename)
            self.switch[self.tabWidget.currentIndex()].addItem(filename)

    def delete(self):
        """delete selected row from list widget by minus button"""
        for item in self.switch[self.tabWidget.currentIndex()].selectedItems():
            self.switch[self.tabWidget.currentIndex()].takeItem(self.switch[self.tabWidget.currentIndex()].row(item))
            self.data.remove(item.text())


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    sys.excepthook = except_hook
    ex.show()
    sys.exit(app.exec_())
