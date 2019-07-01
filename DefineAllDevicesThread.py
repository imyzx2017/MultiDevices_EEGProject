import threading
import pyHook
import pythoncom
import win32api
import serial
import numpy as np
import os

class EyeTribe_InitThread(threading.Thread):
    def __init__(self, subject_number, dll):
        super(EyeTribe_InitThread, self).__init__()
        self.subject_number = subject_number
        self.dll = dll
    def run(self):
        import shutil
        f = open("D:\\CyKITv2-master\\UI_201812\\Data\\eye_raw_data.txt", 'r+')
        f.truncate()
        f1 = open("D:\\CyKITv2-master\\UI_201812\\Data\\Eye_Data.txt", 'r+')
        f1.truncate()
        f.close()
        f1.close()
        data = "D:\\CyKITv2-master\\UI_201812\\Data\\Eye_Data.txt"
        save_eyedata_path = 'Exp_Config_Data/'
        if not os.path.exists(save_eyedata_path):
            os.mkdir(save_eyedata_path)
        saving_eyedata_path = 'Exp_Config_Data/{}/'.format(self.subject_number)
        if not os.path.exists(saving_eyedata_path):
            os.mkdir(saving_eyedata_path)
        eye_raw_data = saving_eyedata_path + "{}_eye_raw_data.txt".format(self.subject_number)
        shutil.copyfile(data, eye_raw_data)

        self.dll.EyeData()
        # from UI_201812.PlotEyeData import smooth_segementation_eyedata
        # from Visual_Exp_20180712.User_API import animation_gif
        # smooth_segementation_eyedata()
        # print('Finished smoothing EyeData!!\n')
        # animation_gif.makegif_for3steps()
        # print('Finished making gif for EyeData!!\n')

        # from UI_201812.PreProcess_EEG_DataFile import save_useful_14channel_Data
        # save_useful_14channel_Data()
        # print('###### Finished EEG_Data Segementation !!#########\n')

        # from UI_201812.PlotEEGData import EEGData_SegmentationAndSave2txt
        # EEG_file_path = 'D:\\CyKITv2-master\\UI_201812\\Data\\EEGData_16label.txt'
        # EEGData_SegmentationAndSave2txt(EEG_file_path)
        # print('######### Finished generating EEG and EyeData Plotting result!!  ############')


        # print(end_time - start_time)  # 误差毫秒级

class ControlSerial_UsingKeyboard_Thread(threading.Thread):

    def __init__(self, subject_number):
        super(ControlSerial_UsingKeyboard_Thread, self).__init__()
        self.ser = serial.Serial(port='COM11', baudrate=115200, timeout=0.3)
        # 开启设备
        d = bytes.fromhex('FF C5 03 A3 A0')
        self.ser.write(d)
        self.showthread = SerialDataSaving_Thread(self.ser)
        self.subject_number = subject_number

    def onKeyboardEvent(self, event):
        # 监听键盘事件
        if event.KeyID == 35:  # 'End' Key
            self.ser.write(bytes.fromhex('FF C5 03 A4 A1'))
            win32api.PostQuitMessage()
            # print(self.showthread.serial_data)
            root_path = 'Exp_Config_Data/'
            if not os.path.exists(root_path):
                os.mkdir(root_path)
            saving_pfdz_data_path = 'Exp_Config_Data/{}/'.format(self.subject_number)
            if not os.path.exists(saving_pfdz_data_path):
                os.mkdir(saving_pfdz_data_path)
            np.savetxt(saving_pfdz_data_path + '{}_Serial_data.txt'.format(self.subject_number), self.showthread.serial_data)
            return 0
        else:
            return 0

    def run(self):
        # 创建一个“钩子”管理对象
        hm = pyHook.HookManager()
        # 监听所有键盘事件
        self.showthread.daemon = True
        self.showthread.start()
        hm.KeyDown = self.onKeyboardEvent
        # 设置键盘“钩子”
        hm.HookKeyboard()

        # # 监听所有鼠标事件
        # hm.MouseAll = onMouseEvent
        # # 设置鼠标“钩子”
        # hm.HookMouse()



        # 进入循环，如不手动关闭，程序将一直处于监听状态
        pythoncom.PumpMessages()

class SerialDataSaving_Thread(threading.Thread):
    def __init__(self):
        super(SerialDataSaving_Thread, self).__init__()
        self.ser = serial.Serial(port='COM11', baudrate=115200)
        self.serial_data = []
    def run(self):
        while True:
            self.serial_data.append(self.ser.read()[0])



# t = ControlSerial_UsingKeyboard_Thread('001')
# t.start()
# # t2.start()
# import ctypes
# DLL_PATH = 'D:\\CyKITv2-master\\Visual_Exp_20180712\\User_API\\Saving_Data_API\\EyeDll_Bind2EndKeyPress.dll'
# temp = ctypes.cdll.LoadLibrary
# temp_dll = temp(DLL_PATH)
# test_thread = EyeTribe_InitThread('007', temp_dll)
# test_thread.start()