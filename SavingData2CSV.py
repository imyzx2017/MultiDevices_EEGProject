import csv
import numpy as np
import json
import pandas
import os

def pandas_showcsv_adding_eeglabel2header(csv_path):
    electric_label_list = ['AF3','F7','F3','FC5','T7','P7','O1','O2','P8','T8','FC6','F4','F8','AF4']
    data_metric = pandas.read_csv(csv_path, header=None, names=electric_label_list)
    return data_metric

def saving_npdata2csv(data_metric, data_classname, subject_number):
    root_path = 'data_csvfiles/'
    if not os.path.exists(root_path):
        os.mkdir(root_path)
    saving_csv_path = 'data_csvfiles/{}/'.format(subject_number)
    if not os.path.exists(saving_csv_path):
        os.mkdir(saving_csv_path)
    np.savetxt(saving_csv_path + str(data_classname) + '.csv', data_metric, delimiter=',')

def saving_subject_information_dict2json(diction):
    root_path = 'Exp_Config_Data/'
    if not os.path.exists(root_path):
        os.mkdir(root_path)
    saving_config_json_path = 'Exp_Config_Data/{}/'.format(str(diction['subject_number']))
    if not os.path.exists(saving_config_json_path):
        os.mkdir(saving_config_json_path)
    with open(saving_config_json_path + '{}_subject_information.json'.format(str(diction['subject_number'])), "w") as f:
        json.dump(diction, f)

def saving_score_dict2json(score_dict, subject_number):
    root_path = 'Exp_Config_Data/'
    if not os.path.exists(root_path):
        os.mkdir(root_path)
    saving_score_json_path = 'Exp_Config_Data/{}/'.format(subject_number)
    if not os.path.exists(saving_score_json_path):
        os.mkdir(saving_score_json_path)
    with open(saving_score_json_path + '{}_score_result.json'.format(subject_number), "w") as f:
        json.dump(score_dict, f)

def saving_timebar_usingnp(subject_number, time_bar):
    root_path = 'Exp_Config_Data/'
    if not os.path.exists(root_path):
        os.mkdir(root_path)
    saving_timebar_path = 'Exp_Config_Data/{}/'.format(subject_number)
    if not os.path.exists(saving_timebar_path):
        os.mkdir(saving_timebar_path)

    np.savetxt(saving_timebar_path + '{}_time_bar.txt'.format(subject_number), time_bar)

def readjson(json_file_path):
    up_root_path = os.path.abspath(os.path.dirname(os.getcwd()))
    with open(up_root_path + '\\' + json_file_path, 'r') as load_json_f:
        load_dict = json.load(load_json_f)
        print(load_dict)

def CreateRandomVideofilepathList(all_video_inonedir_path):
    file_path_list = []
    for current_avi_file in os.listdir(all_video_inonedir_path):
        file_path_list.append(all_video_inonedir_path + current_avi_file)
    np.random.shuffle(file_path_list)
    return file_path_list


# Test Code:

# avi_video_path = 'D:\\媒体评估\\AVI_0311\\'
# CreateRandomVideofilepathList(avi_video_path)


# data_path = 'EEGData_16label.txt'
# metric = np.loadtxt(data_path)
# saving_npdata2csv(metric, 'EEG', 'huang')


# json_filepath = 'Exp_Config_Data/1/subject_information.json'
# readjson(json_filepath)


