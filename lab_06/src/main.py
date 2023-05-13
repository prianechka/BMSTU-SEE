import os
import sys
import webbrowser

import numpy as np
from matplotlib import pyplot as plt
from PyQt5 import QtCore, uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog, QHeaderView,
                             QLineEdit, QTableWidgetItem)


def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.getcwd()
    return os.path.join(base_path, relative_path)


QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

params_table = {
    'RELY': [0.75, 0.86, 1.0, 1.15, 1.40],
    'DATA': [0.94, 1.0, 1.08, 1.16],
    'CPLX': [0.70, 0.85, 1.0, 1.15, 1.30],
    'TIME': [1.0, 1.11, 1.50],
    'STOR': [1.0, 1.06, 1.21],
    'VIRT': [0.87, 1.0, 1.15, 1.30],
    'TURN': [0.87, 1.0, 1.07, 1.15],
    'ACAP': [1.46, 1.19, 1.0, 0.86, 0.71],
    'AEXP': [1.29, 1.15, 1.0, 0.91, 0.82],
    'PCAP': [1.42, 1.17, 1.0, 0.86, 0.70],
    'VEXP': [1.21, 1.10, 1.0, 0.90],
    'LEXP': [1.14, 1.07, 1.0, 0.95],
    'MODP': [1.24, 1.10, 1.0, 0.91, 0.82],
    'TOOL': [1.24, 1.10, 1.0, 0.91, 0.82],
    'SCED': [1.23, 1.08, 1.0, 1.04, 1.10],
}

project_modes = {
    'c1': [3.2, 3.0, 2.8],
    'p1': [1.05, 1.12, 1.2],
    'c2': [2.5, 2.5, 2.5],
    'p2': [0.38, 0.35, 0.32]
}


def PM(c1, p1, EAF, SIZE):
    return 3.2 * EAF * (SIZE ** 1.05)


def TM(c2, p2, PM):
    return 2.5 * (PM ** 0.38)


def calc_EAF(params: list):
    return np.prod(params)


class MainWindow(QDialog):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = uic.loadUi(resource_path('ui.ui'), self)

        self.RELY: QComboBox = self.ui.comboBox_1
        self.DATA: QComboBox = self.ui.comboBox_2
        self.CPLX: QComboBox = self.ui.comboBox_3
        self.TIME: QComboBox = self.ui.comboBox_4
        self.STOR: QComboBox = self.ui.comboBox_5
        self.VIRT: QComboBox = self.ui.comboBox_6
        self.TURN: QComboBox = self.ui.comboBox_7
        self.ACAP: QComboBox = self.ui.comboBox_8
        self.AEXP: QComboBox = self.ui.comboBox_9
        self.PCAP: QComboBox = self.ui.comboBox_10
        self.VEXP: QComboBox = self.ui.comboBox_11
        self.LEXP: QComboBox = self.ui.comboBox_12
        self.MODP: QComboBox = self.ui.comboBox_13
        self.TOOL: QComboBox = self.ui.comboBox_14
        self.SCED: QComboBox = self.ui.comboBox_15
        self.SIZE: QLineEdit = self.ui.sizeEdit
        self.project_mode: QComboBox = self.ui.comboBox_16

        self.ui.wbsTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.classicTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def hide(self):
        self.RELY.hidePopup()

    def eaf(self):
        RELY = params_table['RELY'][self.RELY.currentIndex()]
        DATA = params_table['DATA'][self.DATA.currentIndex()]
        CPLX = params_table['CPLX'][self.CPLX.currentIndex()]
        TIME = params_table['TIME'][self.TIME.currentIndex()]
        STOR = params_table['STOR'][self.STOR.currentIndex()]
        VIRT = params_table['VIRT'][self.VIRT.currentIndex()]
        TURN = params_table['TURN'][self.TURN.currentIndex()]
        ACAP = params_table['ACAP'][self.ACAP.currentIndex()]
        AEXP = params_table['AEXP'][self.AEXP.currentIndex()]
        PCAP = params_table['PCAP'][self.PCAP.currentIndex()]
        VEXP = params_table['VEXP'][self.VEXP.currentIndex()]
        LEXP = params_table['LEXP'][self.LEXP.currentIndex()]
        MODP = params_table['MODP'][self.MODP.currentIndex()]
        TOOL = params_table['TOOL'][self.TOOL.currentIndex()]
        SCED = params_table['SCED'][self.SCED.currentIndex()]

        return RELY * DATA * CPLX * TIME * STOR * VIRT * TURN * ACAP * AEXP * PCAP * VEXP * LEXP * MODP * TOOL * SCED

    def PM(self):
        mode = self.project_mode.currentIndex()
        SIZE = float(self.SIZE.text())

        return project_modes['c1'][mode] * self.eaf() * (SIZE ** project_modes['p1'][mode])

    def TM(self):
        mode = self.project_mode.currentIndex()

        return project_modes['c2'][mode] * (self.PM() ** project_modes['p2'][mode])

    @pyqtSlot(name="on_projectButton_clicked")
    def calculate_project(self):
        try:
            float(self.SIZE.text())
        except:
            return

        pm_clean = round(self.PM(), 2)
        tm_clean = round(self.TM(), 2)
        pm = round(pm_clean * 1.08, 2)
        tm = round(tm_clean * 1.36, 2)

        self.ui.pmLabel.setText(f'Трудоемкость: {pm}' + ' Ч/м')
        self.ui.tmLabel.setText(f'Время разработки: {tm}' + ' мес.')

        for i in range(8):
            self.ui.wbsTable.setItem(i, 1,
                                     QTableWidgetItem(
                                         str(round(pm * int(self.ui.wbsTable.item(i, 0).text()) / 100.0, 2))))
        self.ui.wbsTable.setItem(8, 1, QTableWidgetItem(str(pm)))

        self.ui.classicTable.setItem(0, 0, QTableWidgetItem(str(round(pm_clean * 0.08, 2))))
        self.ui.classicTable.setItem(1, 0, QTableWidgetItem(str(round(pm_clean * 0.18, 2))))
        self.ui.classicTable.setItem(2, 0, QTableWidgetItem(str(round(pm_clean * 0.25, 2))))
        self.ui.classicTable.setItem(3, 0, QTableWidgetItem(str(round(pm_clean * 0.26, 2))))
        self.ui.classicTable.setItem(4, 0, QTableWidgetItem(str(round(pm_clean * 0.31, 2))))
        self.ui.classicTable.setItem(5, 0, QTableWidgetItem(str(round(pm_clean, 2))))
        self.ui.classicTable.setItem(6, 0, QTableWidgetItem(str(round(pm, 2))))
        self.ui.classicTable.setItem(0, 1, QTableWidgetItem(str(round(tm_clean * 0.36, 2))))
        self.ui.classicTable.setItem(1, 1, QTableWidgetItem(str(round(tm_clean * 0.36, 2))))
        self.ui.classicTable.setItem(2, 1, QTableWidgetItem(str(round(tm_clean * 0.18, 2))))
        self.ui.classicTable.setItem(3, 1, QTableWidgetItem(str(round(tm_clean * 0.18, 2))))
        self.ui.classicTable.setItem(4, 1, QTableWidgetItem(str(round(tm_clean * 0.28, 2))))
        self.ui.classicTable.setItem(5, 1, QTableWidgetItem(str(round(tm_clean, 2))))
        self.ui.classicTable.setItem(6, 1, QTableWidgetItem(str(round(tm, 2))))

        y = []
        for i in range(5):
            t = round(float(self.ui.classicTable.item(i, 1).text()))
            for _ in range(t):
                y.append(round(round(float(self.ui.classicTable.item(i, 0).text())) / t))

        x = [i + 1 for i in range(len(y))]

        plt.title('Распределение количества работников по месяцам')
        plt.xlabel("Месяц реализации проекта")
        plt.ylabel("Количество работников")
        plt.bar(x, y)
        plt.show()

    @pyqtSlot(name="on_task1Button_clicked")
    def calculate_task1(self):
        EAF = params_table["LEXP"][-1] * params_table['MODP'][-1] * params_table['TOOL'][1]
        Size = 140
        Mode = 1

        PM = project_modes['c1'][Mode] * EAF * (Size ** project_modes['p1'][Mode])
        TM = project_modes['c2'][Mode] * (PM ** project_modes['p2'][Mode])

        pm_clean = round(PM, 2)
        tm_clean = round(TM, 2)
        pm = round(pm_clean * 1.08, 2)
        tm = round(tm_clean * 1.36, 2)

        self.ui.pmLabel.setText(f'Трудоемкость: {pm}' + ' Ч/м')
        self.ui.tmLabel.setText(f'Время разработки: {tm}' + ' мес.')

        for i in range(8):
            self.ui.wbsTable.setItem(i, 1,
                                     QTableWidgetItem(
                                         str(round(pm * int(self.ui.wbsTable.item(i, 0).text()) / 100.0, 2))))
        self.ui.wbsTable.setItem(8, 1, QTableWidgetItem(str(pm)))

        self.ui.classicTable.setItem(0, 0, QTableWidgetItem(str(round(pm_clean * 0.08, 2))))
        self.ui.classicTable.setItem(1, 0, QTableWidgetItem(str(round(pm_clean * 0.18, 2))))
        self.ui.classicTable.setItem(2, 0, QTableWidgetItem(str(round(pm_clean * 0.25, 2))))
        self.ui.classicTable.setItem(3, 0, QTableWidgetItem(str(round(pm_clean * 0.26, 2))))
        self.ui.classicTable.setItem(4, 0, QTableWidgetItem(str(round(pm_clean * 0.31, 2))))
        self.ui.classicTable.setItem(5, 0, QTableWidgetItem(str(round(pm_clean, 2))))
        self.ui.classicTable.setItem(6, 0, QTableWidgetItem(str(round(pm, 2))))
        self.ui.classicTable.setItem(0, 1, QTableWidgetItem(str(round(tm_clean * 0.36, 2))))
        self.ui.classicTable.setItem(1, 1, QTableWidgetItem(str(round(tm_clean * 0.36, 2))))
        self.ui.classicTable.setItem(2, 1, QTableWidgetItem(str(round(tm_clean * 0.18, 2))))
        self.ui.classicTable.setItem(3, 1, QTableWidgetItem(str(round(tm_clean * 0.18, 2))))
        self.ui.classicTable.setItem(4, 1, QTableWidgetItem(str(round(tm_clean * 0.28, 2))))
        self.ui.classicTable.setItem(5, 1, QTableWidgetItem(str(round(tm_clean, 2))))
        self.ui.classicTable.setItem(6, 1, QTableWidgetItem(str(round(tm, 2))))

        y = []
        for i in range(5):
            t = round(float(self.ui.classicTable.item(i, 1).text()))
            for _ in range(t):
                y.append(round(round(float(self.ui.classicTable.item(i, 0).text())) / t))

        x = [i + 1 for i in range(len(y))]

        plt.title('Распределение количества работников по месяцам')
        plt.xlabel("Месяц реализации проекта")
        plt.ylabel("Количество работников")
        plt.bar(x, y)
        plt.show()

    @pyqtSlot(name="on_tzButton_clicked")
    def view_tz(self):
        url = "file:///home/prianechka/Education/BMSTU/EPI/BMSTU-SEE/lab_06/src/TZ.pdf"
        webbrowser.open(url)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == '__main__':
    sys.exit(main())
