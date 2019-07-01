from phonon_test2 import Ui_MainWindow
from PyQt4 import QtCore, QtGui
from PyQt4 import phonon
import sys
import time
import threading



# import process data functions
from SavingData2CSV import *
from UI.scoringUI import ScoringUi_MainWindow

# EyeTribe Thread
import ctypes
from DefineAllDevicesThread import EyeTribe_InitThread, SerialDataSaving_Thread
# 脑电仪实时数据显示界面
import ClickButton
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#
import os

# chromedriver = 'chromedriver.exe'
# os.environ["webdriver.chrome.driver"] = chromedriver

path = 'D:/CyKit2019/Saving_Data_API/Web/CyKITv2.html'
options = webdriver.ChromeOptions()   # Options()
subject_informations_dict = {}
Testdriver = webdriver.Chrome(chrome_options=options)
# Testdriver = webdriver.Chrome(chromedriver)
Testdriver.get(path)
Testdriver.maximize_window()


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

time_bar = []
video_score_result = {}


class ScoringWindow(QtGui.QMainWindow, ScoringUi_MainWindow):
    finished_scoring_signal = QtCore.pyqtSignal()
    def __init__(self, video_path, parent=None):
        super(ScoringWindow, self).__init__(parent)
        self.video_path = video_path
        self.setupUi(self)

        self.scorewindow_number = 1
        self.score_dict = {}

        self.pushButton_1.clicked.connect(self.ClickButton2Score)
        self.pushButton_2.clicked.connect(self.ClickButton2Score)
        self.pushButton_3.clicked.connect(self.ClickButton2Score)
        self.pushButton_4.clicked.connect(self.ClickButton2Score)
        self.pushButton_5.clicked.connect(self.ClickButton2Score)
        self.pushButton_6.clicked.connect(self.ClickButton2Score)
        self.pushButton_7.clicked.connect(self.ClickButton2Score)
        self.pushButton_8.clicked.connect(self.ClickButton2Score)
        self.pushButton_9.clicked.connect(self.ClickButton2Score)
        self.pushButton_10.clicked.connect(self.ClickButton2Score)

    def ClickButton2Score(self):
        current_button = self.sender()
        if self.scorewindow_number == 1:
            self.score_dict['愉悦度'] = int(current_button.objectName().split('_')[-1])
            print(self.score_dict)
            self.label_title.setText("2.看完这段视频后体验到情绪的强烈程度\n"
                                     "(请认真选择，无法重来)")
            self.label.setText("非常不强烈")
            self.label_2.setText("非常强烈")
        if self.scorewindow_number == 2:
            self.score_dict['唤醒度'] = int(current_button.objectName().split('_')[-1])
            print(self.score_dict)
            self.label_title.setText("3.对这段视频的喜欢程度\n"
                                     "(请认真选择，无法重来)")
            self.label.setText("非常不喜欢")
            self.label_2.setText("非常喜欢")
        if self.scorewindow_number == 3:
            self.score_dict['喜爱度'] = int(current_button.objectName().split('_')[-1])
            print(self.score_dict)
            self.label_title.setText("4.对这段视频熟悉不熟悉\n"
                                     "(请认真选择，无法重来)")
            self.label.setText("非常不熟悉")
            self.label_2.setText("非常熟悉")
        if self.scorewindow_number == 4:
            self.score_dict['熟悉度'] = int(current_button.objectName().split('_')[-1])
            print(self.score_dict)
            self.close()
            video_score_result[self.video_path] = self.score_dict
            self.finished_scoring_signal.emit()

        self.scorewindow_number += 1



class Mywindow(QtGui.QMainWindow, Ui_MainWindow):
    ShowBaselineEndSignal = QtCore.pyqtSignal(int)
    CloseSignal = QtCore.pyqtSignal(str)
    def __init__(self, Avi_FilePath_Dir, subject_number, parent=None):
        super(Mywindow, self).__init__(parent)
        self.setupUi(self)
        self.subject_number = subject_number

        self.playedvideo_number = 0
        self.label = QtGui.QLabel(self.main_widget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setGeometry(QtCore.QRect(0, 0, self.main_widget.width(), self.main_widget.height()))

        self.LeftMouseClick_OnlyOnce = True

        #### define several signals for sleep and connect to correspond func
        # self.baseline_sleep_thread = HintDurationSleepThread(duration=2*60)
        self.ShowBaselineEndSignal.connect(self.CreateSleepBaselineThread)


        #### step1: 指导语显示
        Hint_Text = '您好，欢迎来参加我们的实验\n\n在接下来的实验中，请注视屏幕中央的“+”，保持静息状态。\n\n' \
                    '任务期间请不要晃动身体和头部。\n\n\n明白上述要求后，请按空格键开始。'
        self.Hint_Text(Hint_Text, img_width=1438, img_height=761, text_color='white', text_style='宋体', text_size='36')

        ####

        #  Open All Devices in Working Thread
        # start_time = time.clock()
        # print("在{}s，开启脑电仪和眼动仪等多台生理数据采集设备".format(start_time))
        # time_bar.append(start_time)




        # 从三种方式中选择，展示基线数据采集的刺激图片
        """
        method1: {'duration': duration_time}  (3s)
        method2: 'ClickMouse'
        method3: {'KeyPress': 'space'}  # default using this method
        """
        # current_method = ['duration': 3]

        # 开始工作线程：
        # 随机生成视频路径输出序列，并传递给实验的工作线程
        self.all_avi_filepath = Avi_FilePath_Dir
        RandomVideoPathSeq = CreateRandomVideofilepathList(self.all_avi_filepath)
        self.work_thread = CorrectDurationMethod_WorkingThread(self, RandomVideoPathSeq, parent=None)
        # connecting  this function to show hint_img
        self.work_thread.finishSignal.connect(self.Choose_Method2ShowCorrectIMG)

        self.work_thread.start()

    def stateChanged(self, newState):

        if newState == phonon.Phonon.ErrorState:
            if self.mediaObject.errorType() == phonon.Phonon.FatalError:
                QtGui.QMessageBox.warning(self, "Fatal Error",
                                          self.mediaObject.errorString())
            else:
                QtGui.QMessageBox.warning(self, "Error",
                                          self.mediaObject.errorString())

        elif newState == phonon.Phonon.PlayingState:
            # self.playAction.setEnabled(False)
            # self.pauseAction.setEnabled(False)
            # self.stopAction.setEnabled(False)
            print("开始播放视频于：{}s".format(time.clock()))
            time_bar.append(time.clock())

        elif newState == phonon.Phonon.StoppedState:
            # self.stopAction.setEnabled(False)
            # self.playAction.setEnabled(False)
            # self.pauseAction.setEnabled(False)

            pass


        elif newState == phonon.Phonon.PausedState:
            # self.pauseAction.setEnabled(False)
            # self.stopAction.setEnabled(False)
            # self.playAction.setEnabled(False)
            print("结束播放视频于：{}s".format(time.clock()))
            time_bar.append(time.clock())

            self.playedvideo_number += 1
            # 删除之前的video widget，并更新新的widget
            for i in reversed(range(self.horizontalLayout.count())):
                self.horizontalLayout.itemAt(i).widget().deleteLater()

            self.main_widget = QtGui.QWidget()
            # print(self.main_widget.width(), self.main_widget.height())

            self.main_widget = QtGui.QWidget(self.centralwidget)
            sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.main_widget.sizePolicy().hasHeightForWidth())
            self.main_widget.setSizePolicy(sizePolicy)
            self.main_widget.setMinimumSize(QtCore.QSize(1438, 761))
            self.main_widget.setObjectName(_fromUtf8("main_widget"))
            self.horizontalLayout.addWidget(self.main_widget)
            self.label = QtGui.QLabel(self.main_widget)

            # self.new_label = QtGui.QLabel(self.main_widget)
            # self.new_label.setText('7777777777777')
            # self.new_label.setGeometry(
            #         QtCore.QRect(0.5 * (self.main_widget.width() - 1438), 0.5 * (self.main_widget.height() - 761),
            #                      1438, 761))
            # self.new_label.setAlignment(QtCore.Qt.AlignCenter)
            # self.new_label.setStyleSheet(_fromUtf8("font: {}pt \"{}\"\n;" "color:{}".format(36, '宋体', 'white')))

            # 展示评分窗体，记录被试对于该视频的情感打分
            self.scorewindow = ScoringWindow(self.file)
            self.scorewindow.show()
            self.scorewindow.finished_scoring_signal.connect(self.PlayVideo_Main)

    def Hint_Text(self, Text, img_width=1438, img_height=761, text_color='white', text_style='宋体', text_size='24'):
        self.label.setText(Text)
        self.label.setGeometry(QtCore.QRect(0.5*(self.main_widget.width() - img_width), 0.5*(self.main_widget.height() - img_height), img_width, img_height))
        self.label.setStyleSheet(_fromUtf8("font: {}pt \"{}\"\n;" "color:{}".format(text_size, text_style, text_color)))
        # print("提示语开始展示时间：{}s".format(time.clock()))

        # 提前开启眼动设备，因为调用dll需要时间解析。

        DLL_PATH = 'D:\\CyKITv2-master\\Visual_Exp_20180712\\User_API\\Saving_Data_API\\EyeDll_Bind2EndKeyPress.dll'
        temp = ctypes.cdll.LoadLibrary
        temp_dll = temp(DLL_PATH)
        self.EyeTribeThread = EyeTribe_InitThread(self.subject_number, temp_dll)
        self.EyeTribeThread.daemon = True
        self.EyeTribeThread.start()
        time_bar.append(time.clock())
        print('开启眼动设备的线程于: {}s'.format(time.clock()))

        ###############

    def BeforePlayVideo_HintText(self, Text, img_width=1438, img_height=761, text_color='white', text_style='宋体', text_size='24'):
        self.label.setText(Text)
        self.label.setGeometry(QtCore.QRect(0.5*(self.main_widget.width() - img_width), 0.5*(self.main_widget.height() - img_height), img_width, img_height))
        self.label.setStyleSheet(_fromUtf8("font: {}pt \"{}\"\n;" "color:{}".format(text_size, text_style, text_color)))
        # print("提示语开始展示时间：{}s".format(time.clock()))
        self.label.setText(Text)
        self.label.setGeometry(
            QtCore.QRect(0.5 * (self.main_widget.width() - img_width), 0.5 * (self.main_widget.height() - img_height),
                         img_width, img_height))
        self.label.setStyleSheet(_fromUtf8("font: {}pt \"{}\"\n;" "color:{}".format(text_size, text_style, text_color)))
    # def mousePressEvent(self, e):
    #     if self.LeftMouseClick_OnlyOnce:
    #         if e.buttons() == QtCore.Qt.LeftButton:
    #             # Play
    #             self.LeftMouseClick_OnlyOnce = False
    #             # self.PlayVideo()
    #     else:
    #         pass

    def CollectBaselineData(self):
        ################
        self.playAction.setEnabled(False)
        # Open All Devices except Eyetibe Here
        # 开启脑电仪
        ClickButton.NIMIKit(0, Testdriver)
        # # 开启皮肤电阻采集设备，默认'COM11' 115200 rate
        # self.pfdz_thread = SerialDataSaving_Thread()
        # self.pfdz_thread.daemon = True
        # self.pfdz_thread.start()

        time_bar.append(time.clock())
        print('开启脑电眼动等多台生理信号接入设备于: {}s'.format(time.clock()))
        # ###############

        self.label.setText('+')
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet(_fromUtf8("font: {}pt ;" "color:{}".format('24', 'white')))

        self.ShowBaselineEndSignal.emit(3)

    def CreateSleepBaselineThread(self, duration):
        # print("开始收集基线数据于: {}s".format(time.clock()))
        time_bar.append(time.clock())

        self.baseline_sleep_thread = HintDurationSleepThread(float(time_bar[-1]), duration=2 * 60)
        self.baseline_sleep_thread.duration = duration
        self.baseline_sleep_thread.start()
        self.baseline_sleep_thread.finished_Signal.connect(self.CollectBaselineData_End_then_PlayVideo)

    def CollectBaselineData_End_then_PlayVideo(self):
        # print("结束收集基线数据于: {}s".format(float(time_bar[-1])))

        Text_BeforePlayVideo = "静息结束！\n\n在接下的实验中，您将观看一些视频\n\n观看过程中请不要晃动身体和头部.\n\n每段视频" \
                               "看完后，请根据要求进行评分\n\n\n明白上述要求后，请按空格键开始。"
        self.BeforePlayVideo_HintText(Text=Text_BeforePlayVideo)

        # block: video_number-->'+'-->video-->result1、2、3


        self.playAction = QtGui.QAction(self.style().standardIcon(QtGui.QStyle.SP_MediaPlay), "Play", self,
                                        shortcut='space', enabled=True, triggered=self.PlayVideo_Main)
        self.addAction(self.playAction)

    def Choose_Method2ShowCorrectIMG(self, method):
        # try:
            self.current_videopath = method['VideoPathSeqList']
            if type(method) is dict and 'duration' in method:
                self.playAction = QtGui.QAction(self.style().standardIcon(QtGui.QStyle.SP_MediaPlay), "Play", self,
                                                shortcut='space', enabled=False, triggered=self.CollectBaselineData)
                self.CollectBaselineData()

                # self.playAction = QtGui.QAction(self.style().standardIcon(QtGui.QStyle.SP_MediaPlay), "Play", self,
                #                                 shortcut="Space", enabled=True, triggered=self.PlayVideo)
                # # self.stopAction = QtGui.QAction(self.style().standardIcon(QtGui.QStyle.SP_MediaStop), "Stop", self,
                # #                                 shortcut="Ctrl+S", enabled=False, triggered=self.mediaObject.stop)
                # # self.pauseAction = QtGui.QAction(self.style().standardIcon(QtGui.QStyle.SP_MediaPause), "Pause", self,
                # #                                  shortcut="Ctrl+A", enabled=False, triggered=self.mediaObject.pause)
                # self.addAction(self.playAction)


            elif type(method) is dict and 'KeyPress' in method:
                self.playAction = QtGui.QAction(self.style().standardIcon(QtGui.QStyle.SP_MediaPlay), "Play", self,
                                                shortcut=method['KeyPress'], enabled=True, triggered=self.CollectBaselineData)
                self.addAction(self.playAction)


            # 开发中
            elif type(method) is dict and 'ClickMouse' in method:
                self.playAction = QtGui.QAction("&new", self)
                self.playAction.setShortcut(QtCore.Qt.Key_Left)
                self.addAction(self.playAction)
                self.connect(self.playAction, QtCore.SIGNAL("triggered()"), self.CollectBaselineData)

        # except:
        #     print("AviVideoPath Setting Error!!")

    def PlayVideo_Main(self):
        # adding Test video
        if not self.playedvideo_number == (len(self.current_videopath)+1):
            if self.playedvideo_number == 0:
                self.file = 'test.avi'
                self.label.setText('练习视频编号: 0')
                time_bar.append(time.clock())  # 视频编码开始时间 marker
                # QtCore.QCoreApplication.processEvents()
                self.show_video_num_thread = HintDurationSleepThread(float(time_bar[-1]), 2)
                self.show_video_num_thread.start()
                self.show_video_num_thread.finished_Signal.connect(self.ShowBaseIMG_BeforePlaying)

            else:
                self.file = self.current_videopath[self.playedvideo_number - 1]
                # 展示视频编号 duration=2s

                # self.update()
                # self.label = QtGui.QLabel(self.main_widget)

                if self.label.text() == '':

                    self.label.setGeometry(
                        QtCore.QRect(0.5 * (self.main_widget.width() - 1438), 0.5 * (self.main_widget.height() - 761),
                                     1438, 761))
                    self.label.setAlignment(QtCore.Qt.AlignCenter)
                    self.label.setStyleSheet(_fromUtf8("font: {}pt \"{}\"\n;" "color:{}".format(36, '宋体', 'white')))
                    # self.label.setText(str(self.file).split('\\')[-1])
                    self.label.setText('视频编号:' + str(self.playedvideo_number))
                    # print(self.label.text())

                self.label.setText('视频编号:' + str(self.playedvideo_number))
                time_bar.append(time.clock())  # 视频编码开始时间 marker
                # QtCore.QCoreApplication.processEvents()
                self.show_video_num_thread = HintDurationSleepThread(float(time_bar[-1]), 2)
                self.show_video_num_thread.start()
                self.show_video_num_thread.finished_Signal.connect(self.ShowBaseIMG_BeforePlaying)

        else:
            self.ShowEndImg()

    def CloseWindow(self):
        print(time_bar)
        print(video_score_result)
        saving_timebar_usingnp(self.subject_number, time_bar)
        saving_score_dict2json(video_score_result, self.subject_number)
        # 关闭各个设备
        # 关闭脑电
        ClickButton.NIMIKit(1, Testdriver)
        # 关闭Serial
        self.pfdz_thread.ser.write(bytes.fromhex('FF C5 03 A4 A1'))
        print("关闭全部电生理信号采集设备于: {}s".format(time.clock()))
        time_bar.append(time.clock())

        root_path = 'Exp_Config_Data/'
        if not os.path.exists(root_path):
            os.mkdir(root_path)
        saving_pfdz_data_path = 'Exp_Config_Data/{}/'.format(self.subject_number)
        if not os.path.exists(saving_pfdz_data_path):
            os.mkdir(saving_pfdz_data_path)
        np.savetxt(saving_pfdz_data_path + '{}_Serial_data.txt'.format(self.subject_number),
                   self.pfdz_thread.serial_data)


        self.close()
        self.CloseSignal.emit(self.subject_number)

    def ShowEndImg(self):
        for i in reversed(range(self.horizontalLayout.count())):
            self.horizontalLayout.itemAt(i).widget().deleteLater()

        self.main_widget = QtGui.QWidget()

        self.main_widget = QtGui.QWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_widget.sizePolicy().hasHeightForWidth())
        self.main_widget.setSizePolicy(sizePolicy)
        self.main_widget.setMinimumSize(QtCore.QSize(1438, 761))
        self.main_widget.setObjectName(_fromUtf8("main_widget"))
        self.horizontalLayout.addWidget(self.main_widget)
        self.label = QtGui.QLabel(self.main_widget)
        self.label.setGeometry(
            QtCore.QRect(0.5 * (self.main_widget.width() - 1438), 0.5 * (self.main_widget.height() - 761),
                         1438, 761))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet(_fromUtf8("font: {}pt \"{}\"\n;" "color:{}".format(36, '宋体', 'white')))
        self.label.setText("实验结束！感谢您的参与！！\n\n按键'End'退出")

        self.endAction = QtGui.QAction(self.style().standardIcon(QtGui.QStyle.SP_MediaPlay), "End", self,
                                        shortcut=QtCore.Qt.Key_End, enabled=True, triggered=self.CloseWindow)
        self.addAction(self.endAction)

    def ShowBaseIMG_BeforePlaying(self):
        # 展示“+”校准刺激图片 duration=5s
        self.label.setText('+')
        time_bar.append(time.clock())  # 基线‘+’展示开始时间 marker


        self.show_video_num_thread_2 = HintDurationSleepThread(float(time_bar[-1]), 5)
        self.show_video_num_thread_2.start()
        self.show_video_num_thread_2.finished_Signal.connect(self.Play_AfterShowing)

    def Play_AfterShowing(self):
        self.mediaObject = phonon.Phonon.MediaObject(self)
        self.videoPlayer = phonon.Phonon.VideoWidget(self)
        self.mediaObject.stateChanged.connect(self.stateChanged)
        self.playAction.setEnabled(False)

        self.videoPlayer.setMinimumSize(QtCore.QSize(1438, 761))
        self.main_widget = self.videoPlayer
        for i in reversed(range(self.horizontalLayout.count())):
            self.horizontalLayout.itemAt(i).widget().deleteLater()
        self.horizontalLayout.addWidget(self.main_widget)

        self.mediaObject.setCurrentSource(phonon.Phonon.MediaSource(self.file))  # 加载当前的源文件
        phonon.Phonon.createPath(self.mediaObject, self.videoPlayer)
        # 初始化视频输出
        self.videoPlayer.setAspectRatio(phonon.Phonon.VideoWidget.AspectRatioAuto)
        self.audioOutput = phonon.Phonon.AudioOutput(phonon.Phonon.VideoCategory, self)
        phonon.Phonon.createPath(self.mediaObject, self.audioOutput)

        # print(self.videoPlayer)
        self.mediaObject.play()


        # 跳转到判断video的changestate函数来响应评分记录窗体


class HintDurationSleepThread(QtCore.QThread):
    finished_Signal = QtCore.pyqtSignal()
    def __init__(self, start_time, duration):
        super(HintDurationSleepThread, self).__init__()
        self.start_time = start_time
        self.duration = duration
    def run(self):
        while True:
            if time.clock() - self.start_time >= self.duration:
                time_bar.append(time.clock())
                self.finished_Signal.emit()
                break



class CorrectDurationMethod_WorkingThread(QtCore.QThread):
    finishSignal = QtCore.pyqtSignal(dict)
    def __init__(self, Window, VideoPathSeq, Method={'KeyPress': 'space'}, parent=None):
        super(CorrectDurationMethod_WorkingThread, self).__init__(parent)
        self.Window = Window
        self.VideoPathSeq = VideoPathSeq
        self.Method = Method
        # self.video_list = video_list
    def run(self):
        # 从三种方式中选择，展示基线数据采集的刺激图片
        """
        method1: {'duration': duration_time}  (3s)
        method2: {'ClickMouse': 'Left'}
        method3: {'KeyPress': 'space'}  # default using this method
        """
        if type(self.Method) is dict and 'duration' in self.Method:
            current_method_plus_videopathseq = {'duration': self.Method['duration'], 'VideoPathSeqList': self.VideoPathSeq[0]}

            self.init_step_sleepthread = HintDurationSleepThread(float(current_method_plus_videopathseq['duration']))
            self.init_step_sleepthread.start()
            while True:
                if not self.init_step_sleepthread.is_alive():
                    break

            # self.Window.Choose_Method2ShowCorrectIMG(current_method)   这个如果直接调用，会产生警告，因为在子线程中修改主线程的QPixmap
            self.finishSignal.emit(current_method_plus_videopathseq)

            # Collecting Baseline data duration



        elif type(self.Method) is dict and 'KeyPress' in self.Method:
            current_method_plus_videopathseq = {'KeyPress': self.Method['KeyPress'],
                                                'VideoPathSeqList': self.VideoPathSeq}

            # Open ALL Devices when activate the PlayAction
            self.finishSignal.emit(current_method_plus_videopathseq)

            # Collecting Baseline data duration

            # while True:
            #     if not self.Window.baseline_sleep_thread.is_alive():
            #         break
            # print("结束收集基线数据于: {}s，收集时长为: {}s".format(time.clock(), time.clock() - float(time_bar[-1])))
            # time_bar.append(time.clock())

        # 鼠标点击项待开发
        elif type(self.Method) is dict and 'ClickMouse' in self.Method:
            current_method_plus_videopathseq = {'ClickMouse': self.Method['ClickMouse'],
                                                'VideoPathSeqList': self.VideoPathSeq[0]}

            # Open ALL Devices when activate the PlayAction
            self.finishSignal.emit(current_method_plus_videopathseq)

            # Collecting Baseline data duration



        else:
            assert print('Method Setting Error!!')



if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)

    # Avi_filepath_dir = 'D:\\媒体评估\\AVI_0311\\'
    Avi_filepath_dir = 'D:\\媒体评估\\test\\'
    mainapp = Mywindow(Avi_filepath_dir, '001')
    # mainapp = ScoringWindow('D:\\媒体评估\\AVI_0311\\Neg1.avi')
    app.setQuitOnLastWindowClosed(True)
    mainapp.show()
    sys.exit(app.exec_())


