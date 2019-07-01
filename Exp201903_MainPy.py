# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\UI_NIMIKit\Experiment_UI\Visual_Exp_20180712\Exp_Test_version0.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from UI import alarm
import time

from UI.NIMIEEG2 import NIMIEEG2_Ui_MainWindow


#   Exp UI
from phonon_func_test import Mywindow



from SavingData2CSV import saving_npdata2csv, saving_subject_information_dict2json


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class NIMIEEG2_Window(QtGui.QMainWindow, NIMIEEG2_Ui_MainWindow):
    def __init__(self, parent=None):
        super(NIMIEEG2_Window, self).__init__(parent)
        self.setupUi(self)

        palette = QtGui.QPalette()
        icon = QtGui.QPixmap('D:\\CyKITv2-master\\Web\\images\\BG_Black.jpg').scaled(self.width(), self.height())
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(icon))  # 添加背景图片
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # self.StartButton.clicked.connect(self.Show_UserUI_Window)   # version 0--2018year

        self.StartButton.clicked.connect(self.Show_UserUI_Window)
        self.pushButton_2.clicked.connect(self.export_information_ButtonOnClicked)

    def Show_UserUI_Window(self):
        if self.information_label0.text() == '信息详情：已提交':

            Avi_filepath_dir = 'D:\\媒体评估\\test\\'
            self.Show_UserUI_Window = Mywindow(Avi_filepath_dir, self.subject_number)
            ####
            self.Show_UserUI_Window.CloseSignal.connect(self.Process_Data)

            self.Show_UserUI_Window.show()
            self.close()
        else:
            self.information_alarm_window = alarm.alarm_window()
            self.information_alarm_window.ui.label.setText('请先提交正确完成的信息！！')
            self.information_alarm_window.show()

    def Process_Data(self):
        import os
        import shutil
        print('Copy Data 2 dir')
        EyeData = "D:\\CyKITv2-master\\UI_201812\\Data\\Eye_Data.txt"
        EyeTimeData = "D:\\CyKITv2-master\\UI_201812\\Data\\EyeData_Timepoints.txt"
        EEG_Data = "D:\\CyKITv2-master\\UI_201812\\Data\\EEG.txt"
        save_eyedata_path = 'Exp_Config_Data/'
        if not os.path.exists(save_eyedata_path):
            os.mkdir(save_eyedata_path)
        saving_eyedata_path = 'Exp_Config_Data/{}/'.format(self.subject_number)
        if not os.path.exists(saving_eyedata_path):
            os.mkdir(saving_eyedata_path)
        eye_raw_data = saving_eyedata_path + "{}_eye_raw_data.txt".format(self.subject_number)
        eye_raw_time_data = saving_eyedata_path + "{}_eye_timepoints.txt".format(self.subject_number)
        eeg_float_raw_data = save_eyedata_path + "{}_EEG.txt".format(self.subject_number)

        shutil.copyfile(EyeData, eye_raw_data)
        shutil.copyfile(EyeTimeData, eye_raw_time_data)
        shutil.copyfile(EEG_Data, eeg_float_raw_data)
        return 0


    def export_information_ButtonOnClicked(self):

        self.subject_number = self.lineEdit_3.text()
        self.subject_age = self.lineEdit_4.text()
        self.subject_gender = self.comboBox.currentText()
        if self.subject_number is not '' and self.subject_age is not '' and (self.subject_gender=='男' or self.subject_gender=='女'):
            try:
                self.is_number = int(self.subject_number)
                self.subject_age = int(self.subject_age)
                subject_informations_dict = dict([('subject_number', self.subject_number), ('subject_age', self.subject_age),
                                                  ('subject_gender', str(self.subject_gender))])
                saving_subject_information_dict2json(subject_informations_dict)
                self.information_label0.setText(_translate("MainWindow", "信息详情：已提交", None))
            except:
                self.information_alarm_window = alarm.alarm_window()
                self.information_alarm_window.show()
        else:
            self.information_alarm_window = alarm.alarm_window()
            self.information_alarm_window.show()


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    ex = NIMIEEG2_Window()
    ex.show()
    app.exec_()