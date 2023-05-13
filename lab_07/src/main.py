import sys
import math
from functools import reduce
from PyQt5 import uic, QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit, QComboBox, QLabel, QSpinBox, QPushButton

QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True) #enable highdpi scaling
QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

power_params_table = {
    'PREC': [6.2, 4.96, 3.72, 2.48, 1.24, 0.0],
    'FLEX': [5.07, 4.05, 3.04, 2.03, 1.01, 0.0],
    'RESL': [7.07, 5.65, 4.24, 2.83, 1.41, 0.0],
    'TEAM': [5.48, 4.38, 3.29, 2.19, 1.10, 0.0],
    'PMAT': [7.8, 6.24, 4.68, 3.12, 1.56, 0.0]
}

labor_factor_table = {
    'PERS': [1.62, 1.26, 1.00, 0.83, 0.63, 0.50],
    'RCPX': [0.60, 0.83, 1.00, 1.33, 1.91, 2.72],
    'RUSE': [0.95, 1.00, 1.07, 1.15, 1.24],
    'PDIF': [0.87, 1.00, 1.29, 1.81, 2.61],
    'PREX': [1.33, 1.22, 1.00, 0.87, 0.74, 0.62],
    'FCIL': [1.30, 1.10, 1.00, 0.87, 0.73, 0.62],
    'SCED': [1.43, 1.14, 1.00, 1.00, 1.00]
}

params_level_table = {
    'EI': [3, 4, 6],
    'EO': [4, 5, 7],
    'EQ': [3, 4, 6],
    'ILF': [7, 10, 15],
    'EIF': [5, 7, 10]
}

language_fp_table = {
    'ASM': 320,
    'C': 128,
    'Cobol': 106,
    'Fortran': 106,
    'Pascal': 90,
    'CPP': 53,
    'Java': 53,
    'CSharp': 53,
    'Ada': 49,
    'SQL': 125,
    'VCPP': 34,
    'Delphi': 29,
    'Perl': 21,
    'Prolog': 54,
    'JS': 56,
    'VBasic': 32 
}

experience_level = [4, 7, 13, 25, 50]

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = uic.loadUi("7.ui", self)

        # super().__init__()
        # self.setupUi(self)
        self.tab1 = self.ui.tabWidget.widget(2)
        self.tab2 = self.ui.tabWidget.widget(0)
        self.tab3 = self.ui.tabWidget.widget(3)
        self.tab4 = self.ui.tabWidget.widget(1)

        self.EILowQty: QSpinBox = self.tab1.findChild(QLineEdit, 'EILowEdit')
        self.EOLowQty: QSpinBox = self.tab1.findChild(QLineEdit, 'EOLowEdit')
        self.EQLowQty: QSpinBox = self.tab1.findChild(QLineEdit, 'EQLowEdit')
        self.ILFLowQty: QSpinBox = self.tab1.findChild(QLineEdit, 'ILFLowEdit')
        self.EIFLowQty: QSpinBox = self.tab1.findChild(QLineEdit, 'EIFLowEdit')

        self.EIMidQty: QSpinBox = self.tab1.findChild(QLineEdit, 'EIMidEdit')
        self.EOMidQty: QSpinBox = self.tab1.findChild(QLineEdit, 'EOMidEdit')
        self.EQMidQty: QSpinBox = self.tab1.findChild(QLineEdit, 'EQMidEdit')
        self.ILFMidQty: QSpinBox = self.tab1.findChild(QLineEdit, 'ILFMidEdit')
        self.EIFMidQty: QSpinBox = self.tab1.findChild(QLineEdit, 'EIFMidEdit')

        self.EIHighQty: QSpinBox = self.tab1.findChild(QLineEdit, 'EIHighEdit')
        self.EOHighQty: QSpinBox = self.tab1.findChild(QLineEdit, 'EOHighEdit')
        self.EQHighQty: QSpinBox = self.tab1.findChild(QLineEdit, 'EQHighEdit')
        self.ILFHighQty: QSpinBox = self.tab1.findChild(QLineEdit, 'ILFHighEdit')
        self.EIFHighQty: QSpinBox = self.tab1.findChild(QLineEdit, 'EIFHighEdit')

        self.EIRes: QLabel = self.tab1.findChild(QLabel, 'EILabel')
        self.EORes: QLabel = self.tab1.findChild(QLabel, 'EOLabel')
        self.EQRes: QLabel = self.tab1.findChild(QLabel, 'EQLabel')
        self.ILFRes: QLabel = self.tab1.findChild(QLabel, 'ILFLabel')
        self.EIFRes: QLabel = self.tab1.findChild(QLabel, 'EIFLabel')
        self.TFPRes: QLabel = self.tab1.findChild(QLabel, 'ResLabel')

        self.sysParams = []
        for i in range(1, 15):
            self.sysParams.append(self.tab1.findChild(QSpinBox, 'spinBox_' + str(i)))

        self.ASMPercent: QLineEdit = self.tab1.findChild(QLineEdit, 'ASMEdit')
        self.CPercent: QLineEdit = self.tab1.findChild(QLineEdit, 'CEdit')
        self.CobolPercent: QLineEdit = self.tab1.findChild(QLineEdit, 'CobolEdit')
        self.FortranPercent: QLineEdit = self.tab1.findChild(QLineEdit, 'FortranEdit')
        self.PascalPercent: QLineEdit = self.tab1.findChild(QLineEdit, 'PascalEdit')
        self.CPPPercent: QLineEdit = self.tab1.findChild(QLineEdit, 'CPPEdit')
        self.JavaPercent: QLineEdit = self.tab1.findChild(QLineEdit, 'JavaEdit')
        self.CSharpPercent: QLineEdit = self.tab1.findChild(QLineEdit, 'CSharpEdit')
        self.AdaPercent: QLineEdit = self.tab1.findChild(QLineEdit, 'AdaEdit')
        self.SQLPercent: QLineEdit = self.tab1.findChild(QLineEdit, 'SQLEdit')
        self.VCPPPercent: QLineEdit = self.tab1.findChild(QLineEdit, 'VCPPEdit')
        self.DelphiPercent: QLineEdit = self.tab1.findChild(QLineEdit, 'DelphiEdit')
        self.PerlPercent: QLineEdit = self.tab1.findChild(QLineEdit, 'PerlEdit')
        self.PrologPercent: QLineEdit = self.tab1.findChild(QLineEdit, 'PrologEdit')
        self.JSPercent: QLineEdit = self.tab1.findChild(QLineEdit, 'JSEdit')
        self.VBasicPercent: QLineEdit = self.tab1.findChild(QLineEdit, 'BasicEdit')

        self.FPRes: QLabel = self.tab1.findChild(QLabel, 'FPLabel')
        self.LOCRes: QLabel = self.tab1.findChild(QLabel, 'LOCLabel')

        self.PREC: QComboBox = self.tab2.findChild(QComboBox, 'powComboBox_1')
        self.FLEX: QComboBox = self.tab2.findChild(QComboBox, 'powComboBox_2')
        self.RESL: QComboBox = self.tab2.findChild(QComboBox, 'powComboBox_3')
        self.TEAM: QComboBox = self.tab2.findChild(QComboBox, 'powComboBox_4')
        self.PMAT: QComboBox = self.tab2.findChild(QComboBox, 'powComboBox_5')

        self.Power: QLabel = self.tab2.findChild(QLabel, 'PLabel')

        self.arch = [
            self.tab3.findChild(QComboBox, 'archComboBox_8'),
            self.tab3.findChild(QComboBox, 'archComboBox_9'),
            self.tab3.findChild(QComboBox, 'archComboBox_10'),
            self.tab3.findChild(QComboBox, 'archComboBox_11'),
            self.tab3.findChild(QComboBox, 'archComboBox_12'),
            self.tab3.findChild(QComboBox, 'archComboBox_13'),
            self.tab3.findChild(QComboBox, 'archComboBox_14'),
        ]

        self.archLab: QLabel = self.tab3.findChild(QLabel, 'archLabLabel')
        self.archTime: QLabel = self.tab3.findChild(QLabel, 'archTimeLabel')
        self.archBudget: QLabel = self.tab3.findChild(QLabel, 'archBudgetLabel')

        self.screenQty = [
            self.tab4.findChild(QLineEdit, 'screenSimpleEdit'),
            self.tab4.findChild(QLineEdit, 'screenMediumEdit'),
            self.tab4.findChild(QLineEdit, 'screenDifficultEdit'),
        ]

        self.reportQty = [
            self.tab4.findChild(QLineEdit, 'reportSimpleEdit'),
            self.tab4.findChild(QLineEdit, 'reportMediumEdit'),
            self.tab4.findChild(QLineEdit, 'reportDifficultEdit'),
        ]

        self.gen3Qty: QLineEdit = self.tab4.findChild(QLineEdit, 'gen3Edit')
        self.RUSE: QLineEdit = self.tab4.findChild(QLineEdit, 'RUSEEdit')
        self.EXP: QComboBox = self.tab4.findChild(QComboBox, 'expComboBox')

        self.compLab: QLabel = self.tab4.findChild(QLabel, 'compLabLabel')
        self.compTime: QLabel = self.tab4.findChild(QLabel, 'compTimeLabel')
        self.compBudget: QLabel = self.tab4.findChild(QLabel, 'compBudgetLabel')
        self.avgSalary: QLineEdit = self.tab4.findChild(QLineEdit, 'avgSalaryEdit')
        self.avgSalary2: QLineEdit = self.tab3.findChild(QLineEdit, 'avgSalaryEdit_2')

        btn: QPushButton = self.tab3.findChild(QPushButton, 'archCalculateButton_2')
        btn.clicked.connect(self.calculate_arch)

        self.LOC = 0
        self.p = 0

    def get_sys_params(self):
        return list(map(lambda sb: sb.value(), self.sysParams))

    def get_lang_percentages(self):
        return {
            'ASM': float(self.ASMEdit.value()),
            'C': float(self.CEdit.value()),
            'Cobol': float(self.CobolEdit.value()),
            'Fortran': float(self.FortranEdit.value()),
            'Pascal': float(self.PascalEdit.value()),
            'CPP': float(self.CPPEdit.value()),
            'Java': float(self.JavaEdit.value()),
            'CSharp': float(self.CSharpEdit.value()),
            'Ada': float(self.AdaEdit.value()),
            'SQL': float(self.SQLEdit.value()),
            'VCPP': float(self.VCPPEdit.value()),
            'Delphi': float(self.DelphiEdit.value()),
            'Perl': float(self.PerlEdit.value()),
            'Prolog': float(self.PrologEdit.value()),
            'JS': float(self.JSEdit.value()),
            'VBasic': float(self.BasicEdit.value())
        }

    def get_fp_qty(self):
        return {
            'EILow': int(self.EILowEdit.value()),
            'EOLow': int(self.EOLowEdit.value()),
            'EQLow': int(self.EQLowEdit.value()),
            'ILFLow': int(self.ILFLowEdit.value()),
            'EIFLow': int(self.EIFLowEdit.value()),
            'EIMid': int(self.EIMidEdit.value()),
            'EOMid': int(self.EOMidEdit.value()),
            'EQMid': int(self.EQMidEdit.value()),
            'ILFMid': int(self.ILFMidEdit.value()),
            'EIFMid': int(self.EIFMidEdit.value()),
            'EIHigh': int(self.EIHighEdit.value()),
            'EOHigh': int(self.EOHighEdit.value()),
            'EQHigh': int(self.EQHighEdit.value()),
            'ILFHigh': int(self.ILFHighEdit.value()),
            'EIFHigh': int(self.EIFHighEdit.value()),
        }

    def set_fp_results(self, EI, EO, EQ, ILF, EIF, RES):
        self.EIRes.setText(str(EI))
        self.EORes.setText(str(EO))
        self.EQRes.setText(str(EQ))
        self.ILFRes.setText(str(ILF))
        self.EIFRes.setText(str(EIF))
        self.TFPRes.setText(str(RES))

    def set_calculate_fp_results(self, NormFP, FP, LOC):
        self.FPRes.setText(str(NormFP))
        self.LOCRes.setText(str(LOC))

    def get_power_params(self):
        return {
            'PREC': self.PREC.currentIndex(),
            'FLEX': self.FLEX.currentIndex(),
            'RESL': self.RESL.currentIndex(),
            'TEAM': self.TEAM.currentIndex(),
            'PMAT': self.PMAT.currentIndex(),
        }

    def set_power_result(self, P):
        self.Power.setText(str(P))

    def get_arch_params(self):
        return list(map(lambda sb: sb.currentIndex(), self.arch))

    def get_avg_salary(self):
        return float(self.avgSalary.text())

    def get_avg_salary2(self):
        return float(self.avgSalary2.text())

    def set_arch_results(self, labor, time, budget):
        self.archLab.setText(str(labor))
        self.archTime.setText(str(time))
        self.archBudget.setText(str(budget))

    def get_screen_qty(self):
        return list(map(lambda le: float(le.text()), self.screenQty))

    def get_report_qty(self):
        return list(map(lambda le: float(le.text()), self.reportQty))

    def get_3gen_qty(self):
        return float(self.gen3Qty.text())

    def get_ruse_percent(self):
        return float(self.RUSE.text())

    def get_experience_level(self):
        return self.EXP.currentIndex()

    def set_comp_results(self, labor, time, budget):
        self.compLab.setText(str(labor))
        self.compTime.setText(str(time))
        self.compBudget.setText(str(budget))

    @pyqtSlot(name='on_varButton_clicked')
    def set_func_var_params(self):
        self.ASMEdit.setValue(0)
        self.CEdit.setValue(0)
        self.CobolEdit.setValue(0)
        self.FortranEdit.setValue(0)
        self.PascalEdit.setValue(0)
        self.CPPEdit.setValue(0)
        self.JavaEdit.setValue(25)
        self.CSharpEdit.setValue(60)
        self.AdaEdit.setValue(0)
        self.SQLEdit.setValue(15)
        self.VCPPEdit.setValue(0)
        self.DelphiEdit.setValue(0)
        self.PerlEdit.setValue(0)
        self.PrologEdit.setValue(0)
        self.JSEdit.setValue(0)
        self.BasicEdit.setValue(0)

        self.spinBox_1.setValue(5)
        self.spinBox_2.setValue(5)
        self.spinBox_3.setValue(3)
        self.spinBox_4.setValue(2)
        self.spinBox_5.setValue(3)
        self.spinBox_6.setValue(4)
        self.spinBox_7.setValue(1)
        self.spinBox_8.setValue(4)
        self.spinBox_9.setValue(4)
        self.spinBox_10.setValue(0)
        self.spinBox_11.setValue(1)
        self.spinBox_12.setValue(2)
        self.spinBox_13.setValue(2)
        self.spinBox_14.setValue(2)

        self.EILowEdit.setValue(4)
        self.EOLowEdit.setValue(2)
        self.EQLowEdit.setValue(1)
        self.ILFLowEdit.setValue(3)
        self.EIFLowEdit.setValue(1)
        self.EIMidEdit.setValue(0)
        self.EOMidEdit.setValue(0)
        self.EQMidEdit.setValue(0)
        self.ILFMidEdit.setValue(0)
        self.EIFMidEdit.setValue(0)
        self.EIHighEdit.setValue(0)
        self.EOHighEdit.setValue(0)
        self.EQHighEdit.setValue(0)
        self.ILFHighEdit.setValue(0)
        self.EIFHighEdit.setValue(0)

    @pyqtSlot(name='on_compCalculateButton_2_clicked')
    def set(self):
        self.avgSalaryEdit.setText("100000")
        self.screenSimpleEdit.setText("11")
        self.screenMediumEdit.setText("5")
        self.screenDifficultEdit.setText("0")
        self.reportSimpleEdit.setText("0")
        self.reportMediumEdit.setText("2")
        self.reportDifficultEdit.setText("0")
        self.gen3Edit.setText("3")
        self.RUSEEdit.setText("0")
        self.expComboBox.setCurrentIndex(1)

    @pyqtSlot(name='on_var1Button_clicked')
    def set_func_1var_params(self):
        self.powComboBox_1.setCurrentIndex(1)
        self.powComboBox_2.setCurrentIndex(3)
        self.powComboBox_3.setCurrentIndex(1)
        self.powComboBox_4.setCurrentIndex(2)
        self.powComboBox_5.setCurrentIndex(0)

    @pyqtSlot(name='on_archCalculateButton_3_clicked')
    def fix_result(self):
        self.archComboBox_8.setCurrentIndex(2)
        self.archComboBox_9.setCurrentIndex(4)
        self.archComboBox_10.setCurrentIndex(0)
        self.archComboBox_11.setCurrentIndex(2)
        self.archComboBox_12.setCurrentIndex(1)
        self.archComboBox_13.setCurrentIndex(3)
        self.archComboBox_14.setCurrentIndex(3)


    @pyqtSlot(name='on_calculateButton_clicked')
    def calculate_fp(self):
        self.LOC = 0
        fp_qty = self.get_fp_qty()
        sys_params = self.get_sys_params()
        languages = self.get_lang_percentages()

        EIResult = int(fp_qty['EILow']) * params_level_table['EI'][0] + int(fp_qty['EIMid']) * params_level_table['EI'][1] + int(fp_qty['EIHigh']) * params_level_table['EI'][2]
        EOResult = int(fp_qty['EOLow']) * params_level_table['EO'][0] + int(fp_qty['EOMid']) * params_level_table['EO'][1] + int(fp_qty['EOHigh']) * params_level_table['EO'][2]
        EQResult = int(fp_qty['EQLow']) * params_level_table['EQ'][0] + int(fp_qty['EQMid']) * params_level_table['EQ'][1] + int(fp_qty['EQHigh']) * params_level_table['EQ'][2]
        ILFResult = int(fp_qty['ILFLow']) * params_level_table['ILF'][0] + int(fp_qty['ILFMid']) * params_level_table['ILF'][1] + int(fp_qty['ILFHigh']) * params_level_table['ILF'][2]
        EIFResult = int(fp_qty['EIFLow']) * params_level_table['EIF'][0] + int(fp_qty['EIFMid']) * params_level_table['EIF'][1] + int(fp_qty['EIFHigh']) * params_level_table['EIF'][2]
        FP = EIResult + EOResult + EQResult + ILFResult + EIFResult

        coeff = 0.65 + 0.01 * sum(sys_params)
        normFP = FP * coeff

        for lang in ['ASM', 'C', 'Cobol', 'Fortran', 'Pascal', 'CPP', 'Java', 'CSharp', 'Ada', 'SQL', 'VCPP', 'Delphi',
            'Perl', 'Prolog', 'JS', 'VBasic']:
            self.LOC += normFP * (float(languages[lang]) / 100.0) * language_fp_table[lang]

        self.set_fp_results(EIResult, EOResult, EQResult, ILFResult, EIFResult, FP)
        self.set_calculate_fp_results(round(normFP, 3), FP, int(self.LOC))

    @pyqtSlot(name='on_pCalculateButton_clicked')
    def calculate_p(self):
        power_params = self.get_power_params()

        PREC = power_params_table['PREC'][power_params['PREC']]
        FLEX = power_params_table['FLEX'][power_params['FLEX']]
        RESL = power_params_table['RESL'][power_params['RESL']]
        TEAM = power_params_table['TEAM'][power_params['TEAM']]
        PMAT = power_params_table['PMAT'][power_params['PMAT']]

        result = PREC + FLEX + RESL + TEAM + PMAT
        self.p = result / 100 + 1.01
        
        self.set_power_result(self.p)

    @pyqtSlot(name='on_archCalculateButton_2_clicked')
    def calculate_arch(self):
        avg_salary = self.get_avg_salary2()
        arch_params = self.get_arch_params()
        arch_params_values = []
        
        arch_params_values.append(labor_factor_table['PERS'][arch_params[0]])
        arch_params_values.append(labor_factor_table['RCPX'][arch_params[1]])
        arch_params_values.append(labor_factor_table['RUSE'][arch_params[2]])
        arch_params_values.append(labor_factor_table['PDIF'][arch_params[3]])
        arch_params_values.append(labor_factor_table['PREX'][arch_params[4]])
        arch_params_values.append(labor_factor_table['FCIL'][arch_params[5]])
        arch_params_values.append(labor_factor_table['SCED'][arch_params[6]])

        labor = round(reduce(lambda x, y: x * y, arch_params_values) * 2.45 * math.pow(self.LOC / 1000.0, self.p), 2)
        time = round(3 * math.pow(labor, 0.33 + 0.2 * (self.p - 1.01)), 2)
        budget = round(avg_salary * labor, 2)

        self.set_arch_results(labor, time, budget)
        
    @pyqtSlot(name='on_compCalculateButton_clicked')
    def calculate_comp(self):
        avg_salary = self.get_avg_salary()
        ruse = self.get_ruse_percent()
        exp = experience_level[self.get_experience_level()]
        
        easy_forms = self.get_screen_qty()[0]
        medium_forms = self.get_screen_qty()[1]
        hard_forms = self.get_screen_qty()[2]

        easy_report = self.get_report_qty()[0]
        medium_report = self.get_report_qty()[1]
        hard_report = self.get_report_qty()[2]

        modules = self.get_3gen_qty()

        points = easy_forms + medium_forms * 2 + hard_forms * 3 + easy_report * 2 + medium_report * 5 + hard_report * 8 + modules * 10
        labor = round((points * (100 - ruse) / 100) / exp, 2)
        time = round(3 * math.pow(labor, 0.33 + 0.2 * (self.p - 1.01)), 2)
        budget = round(avg_salary * labor, 2)

        self.set_comp_results(labor, time, budget)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == '__main__':
    sys.exit(main())