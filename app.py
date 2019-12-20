from flask import Flask, Response, request
import logging
from flask import render_template
from src import plt_roc
import json


_names = {'model_1': [], 'model_2': [], 'model_3': []}
_dataset_num = [1]

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

_host = "127.0.0.1"
_port = 5002

app = Flask(__name__)


@app.route('/')
def render():
    plt_roc.clear_temp()
    image_path = 'static\\image\\Nothing.png'
    return render_template('index.html', img=image_path)


@app.route('/choose_dataset/', methods=['POST'])
def choose_dataset():
    num_new = request.get_json()
    if num_new not in (1, 2, 3, 4):
        return Response('Invalid number!', status=400, content_type="application/string")
    _dataset_num[0] = num_new
    rsp_str = str(_dataset_num)
    rsp = Response(rsp_str, status=200, content_type="application/string")
    return rsp


@app.route('/use1/', methods=['POST'])
def use1():
    file_name, score = plt_roc.create_pic(_dataset_num[0], _names, 'model_1')
    _names['model_1'].append(int(file_name))
    score = round(score, 4)
    res_dic = {'file_name': file_name, 'score': score}
    rsp = json.dumps(res_dic)
    rsp = Response(rsp, status=200, content_type="application/json")
    return rsp


@app.route('/use2/', methods=['POST'])
def use2():
    file_name, score = plt_roc.create_pic(_dataset_num[0], _names, 'model_2')
    _names['model_2'].append(int(file_name))
    score = round(score, 4)
    res_dic = {'file_name': file_name, 'score': score}
    rsp = json.dumps(res_dic)
    rsp = Response(rsp, status=200, content_type="application/json")
    return rsp


@app.route('/use3/', methods=['POST'])
def use3():
    file_name, score = plt_roc.create_pic(_dataset_num[0], _names, 'model_3')
    _names['model_3'].append(int(file_name))
    score = round(score, 4)
    res_dic = {'file_name': file_name, 'score': score}
    rsp = json.dumps(res_dic)
    rsp = Response(rsp, status=200, content_type="application/json")
    return rsp


if __name__ == '__main__':
    app.run(host=_host, port=_port)
