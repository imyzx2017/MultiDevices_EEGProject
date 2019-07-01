# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\UI_NIMIKit\NIMIEEG2.0_Yzx\NIMIEEG2.0.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from cv2 import *
import time
from PIL import Image

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

class NIMIEEG2_Ui_MainWindow(object):
    def LoadVideoButton_Onclick(self):
        self.visual_videofile_name = QtGui.QFileDialog.getOpenFileName()
        print(self.visual_videofile_name)
        if self.visual_videofile_name == None or self.visual_videofile_name=="":
            print('## ERROR!! ##')
        else:
            self.playCapture = VideoCapture()
            self.playCapture.open(self.visual_videofile_name)
            self.video_fps = self.playCapture.get(CAP_PROP_FPS)
            self.timer.set_fps(self.video_fps)
            self.video_frame_counts = self.playCapture.get(CAP_PROP_FRAME_COUNT)
            self.video_duration = self.video_frame_counts / self.video_fps
            self.video_width = self.playCapture.get(CAP_PROP_FRAME_WIDTH)
            self.video_height = self.playCapture.get(CAP_PROP_FRAME_HEIGHT)
            print("Video width, height: %s, %s" %(self.video_width, self.video_height))
            print(self.video_fps, self.video_duration)
            # self.timer.start()
            self.playCapture.release()
            self.swith_video()

    def swith_video(self):
        self.playCapture.open(self.visual_videofile_name)
        self.timer.start()

    def reset(self):
        self.timer.stop()
        self.playCapture.release()
        self.status = 0


    def show_video_images(self):
        if self.playCapture.isOpened():
            success, frame = self.playCapture.read()
            if success:
                height, width = frame.shape[:2]

                if frame.ndim == 3:
                    rgb = cvtColor(frame, COLOR_BGR2RGB)
                elif frame.ndim == 2:
                    rgb = cvtColor(frame, COLOR_GRAY2BGR)

                temp_image = QtGui.QImage(rgb.flatten(), width, height, QtGui.QImage.Format_RGB888)
                temp_pixmap = QtGui.QPixmap.fromImage(temp_image).scaled(self.label_3.width(), self.label_3.height())
                self.label_3.setPixmap(temp_pixmap)
            else:
                print("read failed, no frame data")
                success, frame = self.playCapture.read()
                print(success, frame)
                if not success:
                    print("play finished")  # 判断本地文件播放完毕
                    self.reset()
                #     self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
                return
        else:
            print("open file or capturing device error, init again")
            self.reset()


    def setupUi(self, MainWindow):


        # self.timer = VideoTimer()
        # self.timer.timeSignal.signal[str].connect(self.show_video_images)


        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        # MainWindow.resize(1920, 1020)
        MainWindow.showMaximized()
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        ##########
        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(-1, 0, 1921, 191))
        self.widget.setObjectName(_fromUtf8("widget"))
        palette = QtGui.QPalette()
        background = QtGui.QPixmap('D:\\CyKITv2-master\\Web\\images\\blue-bg.png').scaled(self.widget.width(), self.widget.height())
        palette.setBrush(self.widget.backgroundRole(), QtGui.QBrush(background))  # 添加背景图片
        self.widget.setPalette(palette)
        self.widget.setAutoFillBackground(True)
        ############ set NIMIEEG ICON
        self.label = QtGui.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(40, 20, 321, 141))
        self.label.setObjectName(_fromUtf8("label"))
        self.ICON_NIMIEEG_File_path = 'D:\\CyKITv2-master\\Web\\images\\CyKITv2-bg-off.png'
        self.ICON_NIMIEEG_PNG = QtGui.QPixmap(
            self.ICON_NIMIEEG_File_path)  # .scaled(self.ICON.width(),self.ICON.height())
        self.label.setPixmap(self.ICON_NIMIEEG_PNG)
        #########################
        self.Host_label = QtGui.QLabel(self.widget)
        self.Host_label.setGeometry(QtCore.QRect(420, 20, 61, 31))
        self.Host_label.setStyleSheet(_fromUtf8("font: 17pt \"宋体\"\n;" "color:white"))
        self.Host_label.setObjectName(_fromUtf8("label_2"))
        self.Port_label = QtGui.QLabel(self.widget)
        self.Port_label.setGeometry(QtCore.QRect(420, 60, 61, 31))
        self.Port_label.setStyleSheet(_fromUtf8("font: 17pt \"宋体\"\n;" "color:white"))
        self.Port_label.setObjectName(_fromUtf8("label_3"))
        self.Host_lineEdit = QtGui.QLineEdit(self.widget)
        self.Host_lineEdit.setGeometry(QtCore.QRect(480, 20, 131, 31))
        self.Host_lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.Port_lineEdit = QtGui.QLineEdit(self.widget)
        self.Port_lineEdit.setGeometry(QtCore.QRect(480, 60, 131, 31))
        self.Port_lineEdit.setObjectName(_fromUtf8("lineEdit_2"))
        self.widget_2 = QtGui.QWidget(self.widget)
        self.widget_2.setEnabled(True)
        self.widget_2.setGeometry(QtCore.QRect(720, 10, 1161, 171))
        self.widget_2.setStyleSheet(_fromUtf8("border:2px solid rgb(189, 189, 189);\n"
"border-radius:10px"))
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.StartButton = QtGui.QPushButton(self.widget_2)
        self.StartButton.setGeometry(QtCore.QRect(830, 30, 291, 51))
        self.StartButton.setStyleSheet(_fromUtf8("border:0px;\n"
"\n"
"background-color:rgb(198, 198, 198);\n"
"border-radius:8px;\n"
"font:18pt \"宋体\";"))
        self.StartButton.setObjectName(_fromUtf8("StartButton"))
        self.information_label0 = QtGui.QLabel(self.widget_2)
        self.information_label0.setGeometry(QtCore.QRect(40, 10, 191, 71))
        self.information_label0.setStyleSheet(_fromUtf8("border:0px; font:18px;" "color:white"))
        self.information_label0.setObjectName(_fromUtf8("information_label0"))
        self.EndButton = QtGui.QPushButton(self.widget_2)
        self.EndButton.setGeometry(QtCore.QRect(830, 90, 291, 51))
        self.EndButton.setStyleSheet(_fromUtf8("border:0px;\n"
"\n"
"background-color:rgb(198, 198, 198);\n"
"border-radius:8px;\n"
"font:18pt \"宋体\";"))
        self.EndButton.setObjectName(_fromUtf8("EndButton"))
#         self.PauseButton = QtGui.QPushButton(self.widget_2)
#         self.PauseButton.setGeometry(QtCore.QRect(980, 30, 141, 51))
#         self.PauseButton.setStyleSheet(_fromUtf8("border:0px;\n"
# "\n"
# "background-color:rgb(198, 198, 198);\n"
# "border-radius:8px;\n"
# "font:18pt \"宋体\";" ))
#         self.PauseButton.setObjectName(_fromUtf8("PauseButton"))
        self.pushButton = QtGui.QPushButton(self.widget)
        self.pushButton.setGeometry(QtCore.QRect(480, 120, 131, 51))
        self.pushButton.setStyleSheet(_fromUtf8("border:0px;\n"
"\n"
"background-color:rgb(198, 198, 198);\n"
"border-radius:8px;\n"
"font:18pt \"宋体\";" ))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        ########### set information_widget background color
        self.information_widget = QtGui.QWidget(self.centralwidget)
        self.information_widget.setGeometry(QtCore.QRect(0, 200, 361, 821))
        self.information_widget.setStyleSheet(_fromUtf8("#information_widget{\nbackground-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0.0170455, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(35, 35, 35, 255));\n}\n"))
        self.information_widget.setObjectName(_fromUtf8("information_widget"))
        ##################
        self.label_4 = QtGui.QLabel(self.information_widget)
        self.label_4.setGeometry(QtCore.QRect(30, 70, 121, 41))
        self.label_4.setStyleSheet(_fromUtf8("font: 75 20pt \"宋体\";""color:white"))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(self.information_widget)
        self.label_5.setGeometry(QtCore.QRect(30, 140, 61, 31))
        self.label_5.setStyleSheet(_fromUtf8("font:15pt \"宋体\";""color:white"))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.lineEdit_3 = QtGui.QLineEdit(self.information_widget)
        self.lineEdit_3.setGeometry(QtCore.QRect(130, 140, 201, 31))
        self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))
        self.lineEdit_4 = QtGui.QLineEdit(self.information_widget)
        self.lineEdit_4.setGeometry(QtCore.QRect(130, 190, 201, 31))
        self.lineEdit_4.setObjectName(_fromUtf8("lineEdit_4"))
        self.comboBox = QtGui.QComboBox(self.information_widget)
        self.comboBox.setGeometry(QtCore.QRect(130, 240, 201, 31))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.setItemText(0, _fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))

        self.pushButton_2 = QtGui.QPushButton(self.information_widget)
        self.pushButton_2.setGeometry(QtCore.QRect(130, 730, 201, 31))
        self.pushButton_2.setStyleSheet(_fromUtf8("font: 75 15pt \"宋体\";""color:black"))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))

        self.label_8 = QtGui.QLabel(self.information_widget)
        self.label_8.setGeometry(QtCore.QRect(30, 300, 121, 41))
        self.label_8.setStyleSheet(_fromUtf8("font: 75 20pt \"宋体\";""color:white"))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.label_9 = QtGui.QLabel(self.information_widget)
        self.label_9.setGeometry(QtCore.QRect(30, 190, 61, 31))
        self.label_9.setStyleSheet(_fromUtf8("font:15pt \"宋体\";""color:white"))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.label_10 = QtGui.QLabel(self.information_widget)
        self.label_10.setGeometry(QtCore.QRect(30, 240, 61, 31))
        self.label_10.setStyleSheet(_fromUtf8("font:15pt \"宋体\";""color:white"))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.lineEdit_5 = QtGui.QLineEdit(self.information_widget)
        self.lineEdit_5.setGeometry(QtCore.QRect(130, 390, 201, 31))
        self.lineEdit_5.setObjectName(_fromUtf8("lineEdit_5"))
        self.label_6 = QtGui.QLabel(self.information_widget)
        self.label_6.setGeometry(QtCore.QRect(30, 390, 91, 31))
        self.label_6.setStyleSheet(_fromUtf8("font:15pt \"宋体\";""color:white"))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_7 = QtGui.QLabel(self.information_widget)
        self.label_7.setGeometry(QtCore.QRect(30, 450, 91, 31))
        self.label_7.setStyleSheet(_fromUtf8("font:15pt \"宋体\";""color:white"))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.label_11 = QtGui.QLabel(self.information_widget)
        self.label_11.setGeometry(QtCore.QRect(30, 510, 91, 31))
        self.label_11.setStyleSheet(_fromUtf8("font:15pt \"宋体\";" "color:white"))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.lineEdit_8 = QtGui.QLineEdit(self.information_widget)
        self.lineEdit_8.setGeometry(QtCore.QRect(130, 570, 201, 31))
        self.lineEdit_8.setObjectName(_fromUtf8("lineEdit_8"))
        self.label_12 = QtGui.QLabel(self.information_widget)
        self.label_12.setGeometry(QtCore.QRect(30, 570, 91, 31))
        self.label_12.setStyleSheet(_fromUtf8("font:15pt \"宋体\";""color:white"))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.lineEdit_9 = QtGui.QLineEdit(self.information_widget)
        self.lineEdit_9.setGeometry(QtCore.QRect(130, 630, 201, 31))
        self.lineEdit_9.setObjectName(_fromUtf8("lineEdit_9"))
        self.label_13 = QtGui.QLabel(self.information_widget)
        self.label_13.setGeometry(QtCore.QRect(30, 630, 91, 31))
        self.label_13.setStyleSheet(_fromUtf8("font:15pt \"宋体\";""color:white"))
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.toolButton = QtGui.QToolButton(self.information_widget)
        self.toolButton.setGeometry(QtCore.QRect(130, 450, 201, 31))
        self.toolButton.setObjectName(_fromUtf8("toolButton"))
        self.comboBox_3 = QtGui.QComboBox(self.information_widget)
        self.comboBox_3.setGeometry(QtCore.QRect(130, 510, 201, 31))
        self.comboBox_3.setObjectName(_fromUtf8("comboBox_3"))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.comboBox_3.setItemText(0, _fromUtf8(""))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.comboBox_4 = QtGui.QComboBox(self.information_widget)
        self.comboBox_4.setGeometry(QtCore.QRect(130, 570, 201, 31))
        self.comboBox_4.setObjectName(_fromUtf8("comboBox_4"))
        self.comboBox_4.addItem(_fromUtf8(""))
        self.comboBox_4.setItemText(0, _fromUtf8(""))
        self.comboBox_4.addItem(_fromUtf8(""))
        self.comboBox_4.addItem(_fromUtf8(""))
        ##############
        self.ShowData_widget = QtGui.QWidget(self.centralwidget)
        self.ShowData_widget.setGeometry(QtCore.QRect(360, 190, 1561, 831))
        self.ShowData_widget.setObjectName(_fromUtf8("ShowData_widget"))
        palette = QtGui.QPalette()
        icon = QtGui.QPixmap('D:\\CyKITv2-master\\Web\\images\\BG_Black.png').scaled(self.ShowData_widget.width(), self.ShowData_widget.height())
        palette.setBrush(self.ShowData_widget.backgroundRole(), QtGui.QBrush(icon))  # 添加背景图片
        self.ShowData_widget.setPalette(palette)
        self.ShowData_widget.setAutoFillBackground(True)
        #############
        self.EEGData_widget = QtGui.QWidget(self.ShowData_widget)
        self.EEGData_widget.setGeometry(QtCore.QRect(10, 10, 780, 406))
        self.EEGData_widget.setStyleSheet(_fromUtf8("border:3px solid white;\n"
"border-radius:5px;\n" "background-image: url(D:/UI_NIMIKit/NIMIEEG2.0_Yzx/graph.png)"))
        self.EEGData_widget.setObjectName(_fromUtf8("EEGData_widget"))
        ####################
        self.label_2 = QtGui.QLabel(self.EEGData_widget)
        self.label_2.setGeometry(QtCore.QRect(-90, -20, 850, 450))
        self.label_2.setStyleSheet(_fromUtf8("border:0px;\n"
                                              "font: 75 20px;\n"
                                              "color:rgb(255, 255, 255);\n"
                                              "background:transparent;"))
        self.label_2.setObjectName(_fromUtf8("label_2"))


        self.label_14 = QtGui.QLabel(self.EEGData_widget)
        self.label_14.setGeometry(QtCore.QRect(10, 10, 71, 31))
        self.label_14.setStyleSheet(_fromUtf8("border:0px;\n"
"font: 75 20px;\n"
"color:rgb(255, 255, 255);\n"
"background:transparent;"))
        self.label_14.setObjectName(_fromUtf8("label_14"))

        self.EyeData_widget = QtGui.QWidget(self.ShowData_widget)
        self.EyeData_widget.setGeometry(QtCore.QRect(10, 420, 780, 406))
        self.EyeData_widget.setStyleSheet(_fromUtf8("border:3px solid white;\n"
"border-radius:5px;\n" "background-image: url(D:/UI_NIMIKit/NIMIEEG2.0_Yzx/graph.png)"))
        self.EyeData_widget.setObjectName(_fromUtf8("EyeData_widget"))

        self.label_3 = QtGui.QLabel(self.EyeData_widget)
        self.label_3.setGeometry(QtCore.QRect(70, 0, 850, 450))
        self.label_3.setStyleSheet(_fromUtf8("border:0px;\n"
                                             "font: 75 20px;\n"
                                             "color:rgb(255, 255, 255);\n"
                                             "background:transparent;"))
        self.label_3.setObjectName(_fromUtf8("label_3"))

        self.label_15 = QtGui.QLabel(self.EyeData_widget)
        self.label_15.setGeometry(QtCore.QRect(10, 10, 71, 31))
        self.label_15.setStyleSheet(_fromUtf8("border:0px;\n"
"font: 75 20px;\n"
"color:rgb(255, 255, 255);\n"
"background:transparent;"))
        self.label_15.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.label_15.setObjectName(_fromUtf8("label_15"))

        self.ECG_widget = QtGui.QWidget(self.ShowData_widget)
        self.ECG_widget.setGeometry(QtCore.QRect(800, 10, 751, 198))
        self.ECG_widget.setStyleSheet(_fromUtf8("border:3px solid white;\n"
                                                    "border-radius:5px;\n" "background-image: url(D:/UI_NIMIKit/NIMIEEG2.0_Yzx/graph.png)"))
        self.ECG_widget.setObjectName(_fromUtf8("ECG_widget"))

        self.label_ECG = QtGui.QLabel(self.ECG_widget)
        self.label_ECG.setGeometry(QtCore.QRect(0, 0, 750, 180))  # deafult 0,0,800,198
        self.label_ECG.setStyleSheet(_fromUtf8("border:0px;\n"
                                               "font: 75 20px;\n"
                                               "color:rgb(255, 255, 255);\n"
                                               "background:transparent;"))
        self.label_ECG.setObjectName(_fromUtf8("label_ECG"))

        self.label_16 = QtGui.QLabel(self.ECG_widget)
        self.label_16.setGeometry(QtCore.QRect(10, 10, 71, 31))
        self.label_16.setStyleSheet(_fromUtf8("border:0px;\n"
"font: 75 20px;\n"
"color:rgb(255, 255, 255);\n"
"background:transparent;"))
        self.label_16.setObjectName(_fromUtf8("label_16"))

        self.EMG_widget = QtGui.QWidget(self.ShowData_widget)
        self.EMG_widget.setGeometry(QtCore.QRect(800, 220, 751, 191))
        self.EMG_widget.setStyleSheet(_fromUtf8("border:3px solid white;\n"
                                                    "border-radius:5px;\n" "background-image: url(D:/UI_NIMIKit/NIMIEEG2.0_Yzx/graph.png)"))
        self.EMG_widget.setObjectName(_fromUtf8("EMG_widget"))
        self.label_17 = QtGui.QLabel(self.EMG_widget)
        self.label_17.setGeometry(QtCore.QRect(10, 10, 71, 31))
        self.label_17.setStyleSheet(_fromUtf8("border:0px;\n"
"font: 75 20px;\n"
"color:rgb(255, 255, 255);\n"
"background:transparent;"))
        self.label_17.setObjectName(_fromUtf8("label_17"))

        self.GSR_widget = QtGui.QWidget(self.ShowData_widget)
        self.GSR_widget.setGeometry(QtCore.QRect(800, 420, 751, 198))
        self.GSR_widget.setStyleSheet(_fromUtf8("border:3px solid white;\n"
                                                    "border-radius:5px;\n" "background-image: url(D:/UI_NIMIKit/NIMIEEG2.0_Yzx/graph.png)"))
        self.GSR_widget.setObjectName(_fromUtf8("GSR_widget"))

        self.label_GSR = QtGui.QLabel(self.GSR_widget)
        self.label_GSR.setGeometry(QtCore.QRect(0, 0, 750, 180))
        self.label_GSR.setStyleSheet(_fromUtf8("border:0px;\n"
                                               "font: 75 20px;\n"
                                               "color:rgb(255, 255, 255);\n"
                                               "background:transparent;"))
        self.label_GSR.setObjectName(_fromUtf8("label_GSR"))

        self.label_18 = QtGui.QLabel(self.GSR_widget)
        self.label_18.setGeometry(QtCore.QRect(10, 10, 71, 31))
        self.label_18.setStyleSheet(_fromUtf8("border:0px;\n"
"font: 75 20px;\n"
"color:rgb(255, 255, 255);\n"
"background:transparent;"))
        self.label_18.setObjectName(_fromUtf8("label_18"))

        self.RSP_widget = QtGui.QWidget(self.ShowData_widget)
        self.RSP_widget.setGeometry(QtCore.QRect(800, 630, 751, 191))
        self.RSP_widget.setStyleSheet(_fromUtf8("border:3px solid white;\n"
                                                    "border-radius:5px;\n" "background-image: url(D:/UI_NIMIKit/NIMIEEG2.0_Yzx/graph.png)"))
        self.RSP_widget.setObjectName(_fromUtf8("RSP_widget"))
        self.label_19 = QtGui.QLabel(self.RSP_widget)
        self.label_19.setGeometry(QtCore.QRect(10, 10, 71, 31))
        self.label_19.setStyleSheet(_fromUtf8("border:0px;\n"
"font: 75 20px;\n"
"color:rgb(255, 255, 255);\n"
"background:transparent;"))
        self.label_19.setObjectName(_fromUtf8("label_19"))


        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


        self.pushButton.clicked.connect(self.LoadVideoButton_Onclick)


    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        # self.label.setText(_translate("MainWindow", "ICON", None))
        self.Host_label.setText(_translate("MainWindow", "主机", None))
        self.Port_label.setText(_translate("MainWindow", "端口", None))
        self.Host_lineEdit.setText(_translate("MainWindow", "127.0.0.1", None))
        self.Port_lineEdit.setText(_translate("MainWindow", "55555", None))
        self.StartButton.setText(_translate("MainWindow", "测试开始", None))
        self.information_label0.setText(_translate("MainWindow", "信息详情：待提交", None))
        self.EndButton.setText(_translate("MainWindow", "测试结束/生成报告", None))
        # self.PauseButton.setText(_translate("MainWindow", "测试暂停", None))
        self.pushButton.setText(_translate("MainWindow", "建立通讯", None))
        self.label_4.setText(_translate("MainWindow", "被试信息", None))
        self.label_5.setText(_translate("MainWindow", "编号", None))
        self.comboBox.setItemText(1, _translate("MainWindow", "男", None))
        self.comboBox.setItemText(2, _translate("MainWindow", "女", None))
        self.comboBox_3.setItemText(0, _translate("MainWindow", "视觉刺激", None))
        self.comboBox_4.setItemText(0, _translate("MainWindow", "多模态数据分析", None))
        self.label_8.setText(_translate("MainWindow", "实验设置", None))
        self.label_9.setText(_translate("MainWindow", "年龄", None))
        self.label_10.setText(_translate("MainWindow", "性别", None))
        self.label_6.setText(_translate("MainWindow", "实验题目", None))
        self.label_7.setText(_translate("MainWindow", "样本路径", None))
        self.label_11.setText(_translate("MainWindow", "测试模式", None))
        self.label_12.setText(_translate("MainWindow", "评估模式", None))
        self.label_13.setText(_translate("MainWindow", "时间戳", None))
        self.pushButton_2.setText(_translate("MainWindow", "提交被试信息", None))
        self.toolButton.setText(_translate("MainWindow", "...", None))
        self.label_14.setText(_translate("MainWindow", "EEG", None))
        self.label_15.setText(_translate("MainWindow", "Eye", None))
        self.label_16.setText(_translate("MainWindow", "ECG", None))
        self.label_17.setText(_translate("MainWindow", "EMG", None))
        self.label_18.setText(_translate("MainWindow", "GSR", None))
        self.label_19.setText(_translate("MainWindow", "RSP", None))

class NIMIEEG2_MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(NIMIEEG2_MainWindow, self).__init__(parent)
        self.ui = NIMIEEG2_Ui_MainWindow()
        self.ui.setupUi(self)

        palette = QtGui.QPalette()
        icon = QtGui.QPixmap('D:\\CyKITv2-master\\Web\\images\\BG_Black.jpg').scaled(self.width(), self.height())
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(icon))  # 添加背景图片
        self.setPalette(palette)
        self.setAutoFillBackground(True)


class Communicate(QtCore.QObject):
    signal = QtCore.pyqtSignal(str)

class VideoTimer(QtCore.QThread):

    def __init__(self, frequent=20):
        QtCore.QThread.__init__(self)
        self.stopped = False
        self.frequent = frequent
        self.timeSignal = Communicate()
        self.mutex = QtCore.QMutex()

    def run(self):
        with QtCore.QMutexLocker(self.mutex):
            self.stopped = False
        while True:
            if self.stopped:
                return
            self.timeSignal.signal.emit("1")
            time.sleep(1 / self.frequent)

    def stop(self):
        with QtCore.QMutexLocker(self.mutex):
            self.stopped = True

    def is_stopped(self):
        with QtCore.QMutexLocker(self.mutex):
            return self.stopped

    def set_fps(self, fps):
        self.frequent = fps


if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    myapp = NIMIEEG2_MainWindow()
    myapp.show()
    app.exec_()