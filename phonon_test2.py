# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\CyKITv2-master\Visual_Exp_20180712\User_API\Saving_Data_API\phonon_test2.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("实验中"))
        MainWindow.resize(1920, 1080)  # 1920, 1017
        MainWindow.showMaximized()
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.centralwidget.setStyleSheet('background-color: rgb(0, 0, 0);')
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(241, 128, 241, 128)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.main_widget = QtGui.QWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_widget.sizePolicy().hasHeightForWidth())
        self.main_widget.setSizePolicy(sizePolicy)
        self.main_widget.setMinimumSize(QtCore.QSize(1438, 761))
        self.main_widget.setObjectName(_fromUtf8("main_widget"))
        self.horizontalLayout.addWidget(self.main_widget)
        MainWindow.setCentralWidget(self.centralwidget)

        # self.label = QtGui.QLabel(self.main_widget)
        # self.label.setStyleSheet(_fromUtf8("font: {}pt \"{}\"\n;" "color:{}".format(36, '宋体', 'white')))
        # self.label.setGeometry(
        #     QtCore.QRect(0.5 * (self.main_widget.width() - 1438), 0.5 * (self.main_widget.height() - 761),
        #                  1438, 761))
        # self.label.setAlignment(QtCore.Qt.AlignCenter)
        #
        # print(self.main_widget.width(), self.main_widget.height())
        # self.label.setText('6666666666666')

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "实验中", None))

class Mywindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Mywindow, self).__init__(parent)
        self.setupUi(self)
        print(self.main_widget.width(), self.main_widget.height())

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    mainapp = Mywindow()
    app.setQuitOnLastWindowClosed(True)
    mainapp.show()
    sys.exit(app.exec_())