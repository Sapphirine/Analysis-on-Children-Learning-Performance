import os
from src.model import model


def clear_temp():
    for i in range(1, 4):
        folder_name = 'result_' + str(i)
        file_list = [f for f in os.listdir("static/temp/" + folder_name + '/') if f.endswith(".png")]
        for f in file_list:
            os.remove("static/temp/" + folder_name + '/' + f)


def create_pic(test_num, names, model_name):
    if not names[model_name]:
        name = '1'
    else:
        name = str(max(names[model_name]) + 1)

    folder_name = 'result_' + model_name[-1]
    if model_name[-1] == '1':
        score = model.predict(test_num, 1, folder_name, name)
    elif model_name[-1] == '2':
        score = model.predict(test_num, 2, folder_name, name)
    elif model_name[-1] == '3':
        score = model.predict(test_num, 3, folder_name, name)
    return name, score
